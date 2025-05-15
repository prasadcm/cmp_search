from pydantic import BaseModel
from typing import List, Optional


class SearchRequest(BaseModel):
    query: str


class SearchHit(BaseModel):
    id: str
    source: dict


class SearchResponse(BaseModel):
    total: int
    results: List[SearchHit]
