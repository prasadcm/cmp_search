from fastapi import APIRouter, Depends, HTTPException
from es.models.search import SearchRequest, SearchResponse
from es.deps.elasticsearch_dep import get_es
from es.services.search_service import search_documents
from elasticsearch import AsyncElasticsearch

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_docs(
    req: SearchRequest,
    es: AsyncElasticsearch = Depends(get_es),
):
    try:
        return await search_documents(es, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
