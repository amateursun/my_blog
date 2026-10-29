# src/core/entities/comment.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comment:
    id: int | None = None
    content: str = ""
    post_id: int = 0
    author_id: int = 0
    is_deleted: bool = False
    created_at: datetime | None = None

    def can_be_deleted_by(self, user_id: int, post_author_id: int) -> bool:
        """评论作者或文章作者均可删除"""
        return self.author_id == user_id or post_author_id == user_id