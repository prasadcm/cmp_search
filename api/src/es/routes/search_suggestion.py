from es.models.search_suggestion import SearchSuggestionResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from es.deps.elasticsearch_dep import get_es
from es.services.search_suggestion_service import search_documents
from elasticsearch import AsyncElasticsearch

router = APIRouter()


@router.get("", response_model=SearchSuggestionResponse)
async def search_docs(
    query: str = Query(None, description="Search query"),
    es: AsyncElasticsearch = Depends(get_es),
):
    try:
        return await search_documents(es, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
