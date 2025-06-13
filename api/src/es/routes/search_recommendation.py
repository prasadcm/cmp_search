from es.models.search_recommendation import SearchRecommendationResponse
from fastapi import APIRouter, Depends, HTTPException
from es.deps.elasticsearch_dep import get_es
from es.services.search_recommendation_service import search_documents
from elasticsearch import AsyncElasticsearch

router = APIRouter()


@router.get("", response_model=SearchRecommendationResponse)
async def search_docs(
    es: AsyncElasticsearch = Depends(get_es),
):
    try:
        return await search_documents(es)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
