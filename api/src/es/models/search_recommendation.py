from pydantic import BaseModel, Field
from typing import List


class SearchRecommendationHit(BaseModel):
    iconUrl: str = Field(alias="icon_url")
    name: str = Field(alias="name")
    searchCount: int = Field(alias="search_count")
    type: str = Field(alias="type")
    slug: str = Field(alias="slug")
    productId: str = Field(alias="product_id")
    categoryId: str = Field(alias="category_id")


class SearchRecommendationResponse(BaseModel):
    total: int
    results: List[SearchRecommendationHit]
