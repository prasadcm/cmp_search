from elasticsearch import AsyncElasticsearch
from es.models.search_recommendation import (
    SearchRecommendationHit,
    SearchRecommendationResponse,
)
from es.config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def search_documents(es: AsyncElasticsearch) -> SearchRecommendationResponse:

    query = {
        "function_score": {
            "query": {
                "bool": {
                    "must": {"match_all": {}},
                    "should": [
                        {"rank_feature": {"field": "search_count", "boost": 2}},
                        {"rank_feature": {"field": "popularity", "boost": 3}},
                    ],
                    "minimum_should_match": 1,
                }
            },
            "functions": [
                {"exp": {"updated_at": {"origin": "now", "scale": "7d", "decay": 0.5}}}
            ],
            "score_mode": "multiply",
            "boost_mode": "multiply",
        }
    }

    # Perform the search
    result = await es.search(
        index=settings.search_suggestion_index_name, query=query, size=10
    )

    hits = result["hits"]["hits"]
    return SearchRecommendationResponse(
        total=result["hits"]["total"]["value"],
        results=[SearchRecommendationHit(**hit["_source"]) for hit in hits],
    )
