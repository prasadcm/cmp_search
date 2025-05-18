from fastapi import APIRouter, Depends, HTTPException, Query
from es.models.search import SearchResponse
from es.deps.elasticsearch_dep import get_es
from es.services.search_service import search_documents
from elasticsearch import AsyncElasticsearch

router = APIRouter()


@router.get("", response_model=SearchResponse)
async def search_docs(
    email: str = Query(None, description="User email"),
    phone_number: str = Query(None, description="User phone number"),
    es: AsyncElasticsearch = Depends(get_es),
):
    try:
        return await search_documents(es, email=email, phone_number=phone_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
