from fastapi import APIRouter, Depends, HTTPException
from elasticsearch import AsyncElasticsearch
from es.models.search import SearchRequest, SearchResponse, SearchHit
from es.deps.search import get_es

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_docs(
    req: SearchRequest,
    es: AsyncElasticsearch = Depends(get_es),
):
    try:
        result = await es.search(
            index="cmp-search-item-index-001",
            query={"match": {"searchText": req.query}},
        )

        hits = result["hits"]["hits"]
        return SearchResponse(
            total=result["hits"]["total"]["value"],
            results=[SearchHit(id=hit["_id"], source=hit["_source"]) for hit in hits],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
