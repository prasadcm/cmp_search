from elasticsearch import AsyncElasticsearch
from es.models.previously_searched_item import (
    PreviouslySearchedItemResponse,
    PreviouslySearchedItemHit,
)
from es.config.settings import settings
import logging

logger = logging.getLogger(__name__)


async def search_documents(
    es: AsyncElasticsearch, email: str, phone_number: str
) -> PreviouslySearchedItemResponse:
    should_filters = []

    # Include non-empty email
    if email and email.strip():
        should_filters.append({"term": {"email": email.strip()}})

    # Include non-empty phone number
    if phone_number and phone_number.strip():
        should_filters.append({"term": {"phone_number": phone_number.strip()}})

    # If neither email nor phone number is provided, return empty result
    if not should_filters:
        return PreviouslySearchedItemResponse(total=0, results=[])

    query = {
        "function_score": {
            "query": {
                "constant_score": {
                    "filter": {
                        "bool": {
                            "should": should_filters,
                            "minimum_should_match": 1,
                        }
                    }
                }
            },
            "functions": [
                {
                    "field_value_factor": {
                        "field": "search_count",
                        "factor": 3,
                        "missing": 1,
                    }
                },
                {"exp": {"updated_at": {"origin": "now", "scale": "7d", "decay": 0.5}}},
            ],
            "score_mode": "multiply",
            "boost_mode": "multiply",
        }
    }
    source = ["search_text", "type", "icon_url", "slug", "product_id", "category_id"]
    result = await es.search(
        index=settings.previously_searched_index_name,
        query=query,
        size=10,
        source_includes=source,
    )

    hits = result["hits"]["hits"]
    return PreviouslySearchedItemResponse(
        total=result["hits"]["total"]["value"],
        results=[PreviouslySearchedItemHit(**hit["_source"]) for hit in hits],
    )
