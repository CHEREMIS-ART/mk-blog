from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    title: str
    text: str
    category_id: int


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    category_id: Optional[int] = None


class ArticleOut(BaseModel):
    id: int
    title: str
    text: str
    category_id: int
    image_url: Optional[str] = None
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedArticles(BaseModel):
    items: list[ArticleOut]
    page_number: int
    page_size: int
    total: int
    total_pages: int
