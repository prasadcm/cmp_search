from elasticsearch import AsyncElasticsearch
from es.models.search import SearchRequest, SearchResponse, SearchHit
from es.config.settings import settings


async def search_documents(
    es: AsyncElasticsearch, req: SearchRequest
) -> SearchResponse:
    result = await es.search(
        index=settings.search_index_name,
        query={"match": {settings.search_match_key: req.query}},
    )
    hits = result["hits"]["hits"]
    return SearchResponse(
        total=result["hits"]["total"]["value"],
        results=[SearchHit(id=hit["_id"], source=hit["_source"]) for hit in hits],
    )
