# src/data/repositories/post_repository.py
from typing import Optional
from sqlalchemy.orm import Session

from src.core.entities.post import Post
from src.core.interfaces.repositories import PostRepositoryProtocol
from src.data.orm.post import PostORM


class SqlalchemyPostRep(PostRepositoryProtocol):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Optional[Post]:
        orm = self.db.query(PostORM).filter(
            PostORM.id == post_id, PostORM.is_deleted == False
        ).first()
        return self._to_entity(orm) if orm else None

    def get_by_slug(self, slug: str) -> Optional[Post]:
        orm = self.db.query(PostORM).filter(
            PostORM.slug == slug, PostORM.is_deleted == False
        ).first()
        return self._to_entity(orm) if orm else None

    def list_posts(self, skip: int, limit: int, published_only: bool,
                   author_id: int | None = None,
                   keyword: str | None = None) -> list[Post]:
        q = self.db.query(PostORM).filter(PostORM.is_deleted == False)
        if published_only:
            q = q.filter(PostORM.is_published == True)
        if author_id:
            q = q.filter(PostORM.author_id == author_id)
        if keyword:
            like = f"%{keyword}%"
            q = q.filter((PostORM.title.like(like)) | (PostORM.content.like(like)))
        orms = q.order_by(PostORM.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(o) for o in orms]

    def create(self, post: Post) -> Post:
        orm = PostORM(
            title=post.title,
            slug=post.slug,
            content=post.content,
            is_published=post.is_published,
            author_id=post.author_id,
        )
        self.db.add(orm)
        self.db.flush()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def update(self, post: Post) -> Post:
        orm = self.db.query(PostORM).filter(PostORM.id == post.id).first()
        if not orm:
            raise ValueError(f"Post {post.id} not found")
        orm.title = post.title
        orm.slug = post.slug
        orm.content = post.content
        orm.is_published = post.is_published
        self.db.flush()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def soft_delete(self, post_id: int) -> None:
        orm = self.db.query(PostORM).filter(PostORM.id == post_id).first()
        if orm:
            orm.is_deleted = True
            self.db.flush()

    @staticmethod
    def _to_entity(orm: PostORM) -> Post:
        return Post(
            id=orm.id,
            title=orm.title,
            slug=orm.slug,
            content=orm.content,
            is_published=orm.is_published,
            is_deleted=orm.is_deleted,
            author_id=orm.author_id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

