from pydantic import BaseModel
from typing import List


class SearchHit(BaseModel):
    id: str
    source: dict


class SearchResponse(BaseModel):
    total: int
    results: List[SearchHit]
