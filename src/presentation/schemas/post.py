# src/presentation/schemas/post.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    is_published: bool = False


class PostUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1)
    is_published: bool | None = None


class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    is_published: bool
    author_id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class PostListOut(BaseModel):
    id: int
    title: str
    slug: str
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

