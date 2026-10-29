# src/core/entities/post.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Post:
    id: int | None = None
    title: str = ""
    slug: str = ""
    content: str = ""
    is_published: bool = False
    is_deleted: bool = False
    author_id: int = 0
    tags: list[str] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def can_be_edited_by(self, user_id: int) -> bool:
        """业务规则：只有作者本人可以编辑"""
        return self.author_id == user_id


