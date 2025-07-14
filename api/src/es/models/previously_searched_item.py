from pydantic import BaseModel, Field
from typing import List


class PreviouslySearchedItemHit(BaseModel):
    iconUrl: str = Field(alias="icon_url")
    searchText: str = Field(alias="search_text")
    type: str = Field(alias="type")
    slug: str = Field(alias="slug")
    productId: str = Field(alias="product_id")
    categoryId: str = Field(alias="category_id")


class PreviouslySearchedItemResponse(BaseModel):
    total: int
    results: List[PreviouslySearchedItemHit]
