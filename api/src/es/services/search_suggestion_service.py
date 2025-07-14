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
                                "operator": "or",
                                "minimum_should_match": 1,
                            }
                        }
                    ]
                }
            },
            "functions": [
                # Search count boosting
                {
                    "field_value_factor": {
                        "field": "search_count",
                        "factor": 0.1,
                        "missing": 0,
                        "modifier": "log1p",
                    }
                },
                # Popularity boosting
                {
                    "field_value_factor": {
                        "field": "popularity",
                        "factor": 0.1,
                        "missing": 0,
                        "modifier": "log1p",
                    }
                },
                # Recency boosting (applies to all types)
                {"exp": {"updated_at": {"origin": "now", "scale": "7d", "decay": 0.5}}},
                # Product-specific boosting (only for Product type)
                {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"type": "Product"}},
                                {"term": {"is_bestseller": True}},
                            ]
                        }
                    },
                    "weight": 1.5,
                },
                {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"type": "Product"}},
                                {"term": {"new_arrival": True}},
                            ]
                        }
                    },
                    "weight": 1.4,
                },
                {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"type": "Product"}},
                                {"term": {"is_featured": True}},
                            ]
                        }
                    },
                    "weight": 1.3,
                },
                # Discount boosting (only for Product type with discount > 0)
                {
                    "filter": {
                        "bool": {
                            "must": [
                                {"term": {"type": "Product"}},
                                {"range": {"discount": {"gt": 0}}},
                            ]
                        }
                    },
                    "field_value_factor": {
                        "field": "discount",
                        "factor": 0.1,
                        "missing": 0,
                        "modifier": "log1p",
                    },
                },
            ],
            "score_mode": "sum",
            "boost_mode": "multiply",
        }
    }

    # Perform the search
    result = await es.search(
        index=settings.search_suggestion_index_name,
        query=query,
        size=10,
        source_includes=[
            "name",
            "type",
            "icon_url",
            "slug",
            "product_id",
            "category_id",
            "tags",
            "is_bestseller",
            "new_arrival",
            "is_featured",
            "discount",
        ],
    )

    hits = result["hits"]["hits"]
    return SearchSuggestionResponse(
        total=result["hits"]["total"]["value"],
        results=[SearchSuggestionHit(**hit["_source"]) for hit in hits],
    )


async def search_documents_with_script_boost(
    es: AsyncElasticsearch, queryString: str
) -> SearchSuggestionResponse:
    """
    Alternative search function using script_score for more complex product-specific boosting.
    This approach allows for more sophisticated boosting logic.
    """

    # If query is empty, return empty result
    if not queryString or not queryString.strip():
        return SearchSuggestionResponse(total=0, results=[])

    # Complex product-specific boosting script
    product_boost_script = {
        "source": """
            double boost = 1.0;
            
            // Only apply product-specific boosting for Product type
            if (doc['type.keyword'].value == 'Product') {
                // Bestseller boost
                if (doc['is_bestseller'].value == true) {
                    boost *= 1.5;
                }
                
                // New arrival boost
                if (doc['new_arrival'].value == true) {
                    boost *= 1.4;
                }
                
                // Featured product boost
                if (doc['is_featured'].value == true) {
                    boost *= 1.3;
                }
                
                // Discount boost (logarithmic)
                if (doc['discount'].size() > 0 && doc['discount'].value > 0) {
                    double discount = doc['discount'].value;
                    boost *= (1.0 + Math.log(discount + 1) * 0.1);
                }
                
                // Stock availability boost
                if (doc['in_stock'].value == true) {
                    boost *= 1.1;
                }
            }
            
            return boost;
        """
    }

    query = {
        "function_score": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": queryString,
                                "fields": ["name^2", "tags^3"],
                                "operator": "or",
                                "minimum_should_match": 1,
                            }
                        }
                    ]
                }
            },
            "functions": [
                # Search count boosting
                {
                    "field_value_factor": {
                        "field": "search_count",
                        "factor": 0.1,
                        "missing": 0,
                        "modifier": "log1p",
                    }
                },
                # Popularity boosting
                {
                    "field_value_factor": {
                        "field": "popularity",
                        "factor": 0.1,
                        "missing": 0,
                        "modifier": "log1p",
                    }
                },
                # Product-specific boosting using script
                {"script_score": {"script": product_boost_script}},
                # Recency boosting (applies to all types)
                {"exp": {"updated_at": {"origin": "now", "scale": "7d", "decay": 0.5}}},
            ],
            "score_mode": "multiply",
            "boost_mode": "multiply",
        }
    }

    # Perform the search
    result = await es.search(
        index=settings.search_suggestion_index_name,
        query=query,
        size=10,
        source_includes=[
            "name",
            "type",
            "icon_url",
            "slug",
            "product_id",
            "category_id",
            "tags",
            "is_bestseller",
            "new_arrival",
            "is_featured",
            "discount",
            "in_stock",
        ],
    )

    hits = result["hits"]["hits"]
    return SearchSuggestionResponse(
        total=result["hits"]["total"]["value"],
        results=[SearchSuggestionHit(**hit["_source"]) for hit in hits],
    )
