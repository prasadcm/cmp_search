from pydantic import BaseModel, Field
from typing import List


class SearchSuggestionHit(BaseModel):
    iconUrl: str = Field(alias="icon_url")
    name: str = Field(alias="name")
    type: str = Field(alias="type")
    slug: str = Field(alias="slug")
    productId: str = Field(alias="product_id")
    categoryId: str = Field(alias="category_id")


class SearchSuggestionResponse(BaseModel):
    total: int
    results: List[SearchSuggestionHit]
