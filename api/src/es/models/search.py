from pydantic import BaseModel
from typing import List, Optional


class SearchRequest(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None


class SearchHit(BaseModel):
    id: str
    source: dict


class SearchResponse(BaseModel):
    total: int
    results: List[SearchHit]
