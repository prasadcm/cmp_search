from elasticsearch import AsyncElasticsearch
from es.models.search_suggestion import (
    SearchSuggestionHit,
    SearchSuggestionResponse,
)
from es.config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def search_documents(
    es: AsyncElasticsearch, queryString: str
) -> SearchSuggestionResponse:

    # If query is empty, return empty result
    if not queryString or not queryString.strip():
        return SearchSuggestionResponse(total=0, results=[])

    query = {
        "function_score": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": queryString,
                                "fields": ["name^2", "tags^3"],
                                "operator": "and",
                            }
                        }
                    ],
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
    return SearchSuggestionResponse(
        total=result["hits"]["total"]["value"],
        results=[SearchSuggestionHit(**hit["_source"]) for hit in hits],
    )
