from elasticsearch import AsyncElasticsearch
from es.models.search import SearchRequest, SearchResponse, SearchHit
from es.config.settings import settings


async def search_documents(
    es: AsyncElasticsearch, req: SearchRequest
) -> SearchResponse:
    should_filters = []

    # Include non-empty email
    if req.email and req.email.strip():
        should_filters.append({"term": {"email": req.email.strip()}})

    # Include non-empty phone number
    if req.phone_number and req.phone_number.strip():
        should_filters.append({"term": {"phoneNumber": req.phone_number.strip()}})

    # If neither email nor phone number is provided, return empty result
    if not should_filters:
        return SearchResponse(total=0, results=[])

    query = {
        "bool": {
            "filter": [{"bool": {"should": should_filters, "minimum_should_match": 1}}],
            "should": [
                {"rank_feature": {"field": "searchCount", "boost": 3}},
                {"rank_feature": {"field": "productRank", "boost": 2}},
                {
                    "function_score": {
                        "functions": [
                            {
                                "exp": {
                                    "updatedDate": {
                                        "origin": "now",
                                        "scale": "7d",
                                        "decay": 0.5,
                                    }
                                }
                            }
                        ],
                        "score_mode": "multiply",
                        "boost_mode": "multiply",
                    }
                },
            ],
            "minimum_should_match": 1,
        }
    }

    result = await es.search(index=settings.search_index_name, query=query, size=10)

    hits = result["hits"]["hits"]
    return SearchResponse(
        total=result["hits"]["total"]["value"],
        results=[SearchHit(id=hit["_id"], source=hit["_source"]) for hit in hits],
    )
