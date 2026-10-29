# src/data/repositories/comment_repository.py
from typing import Optional
from sqlalchemy.orm import Session

from src.core.entities.comment import Comment
from src.core.interfaces.repositories import CommentRepositoryProtocol
from src.data.orm.comment import CommentORM


class SqlalchemyCommentRep(CommentRepositoryProtocol):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        orm = self.db.query(CommentORM).filter(
            CommentORM.id == comment_id, CommentORM.is_deleted == False
        ).first()
        return self._to_entity(orm) if orm else None

    def list_by_post(self, post_id: int, skip: int, limit: int) -> list[Comment]:
        orms = self.db.query(CommentORM).filter(
            CommentORM.post_id == post_id, CommentORM.is_deleted == False
        ).order_by(CommentORM.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(o) for o in orms]

    def create(self, comment: Comment) -> Comment:
        orm = CommentORM(
            content=comment.content,
            post_id=comment.post_id,
            author_id=comment.author_id,
        )
        self.db.add(orm)
        self.db.flush()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def soft_delete(self, comment_id: int) -> None:
        orm = self.db.query(CommentORM).filter(CommentORM.id == comment_id).first()
        if orm:
            orm.is_deleted = True
            self.db.flush()

    @staticmethod
    def _to_entity(orm: CommentORM) -> Comment:
        return Comment(
            id=orm.id,
            content=orm.content,
            post_id=orm.post_id,
            author_id=orm.author_id,
            is_deleted=orm.is_deleted,
            created_at=orm.created_at,
        )