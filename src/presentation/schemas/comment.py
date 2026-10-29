# src/presentation/schemas/comment.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)