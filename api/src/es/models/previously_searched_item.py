from pydantic import BaseModel
from typing import List


class PreviouslySearchedItemHit(BaseModel):
    productIcon: str
    productUrl: str
    searchText: str
    searchCount: int


class PreviouslySearchedItemResponse(BaseModel):
    total: int
    results: List[PreviouslySearchedItemHit]
