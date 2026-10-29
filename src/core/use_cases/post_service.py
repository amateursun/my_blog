# src/core/use_cases/post_service.py
from src.core.entities.post import Post
from src.core.entities.user import User
from src.core.exceptions import (PostNotFoundError, PermissionDeniedError, InvalidOperationError,)
from src.core.interfaces.repositories import (PostRepositoryProtocol, UserRepositoryProtocol,)
from src.bootstrap.dependencies import slugify


class PostService:
    def __init__(self, post_repo: PostRepositoryProtocol,
                 user_repo: UserRepositoryProtocol):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def create_post(self, author_id: int, title: str, content: str,
                    is_published: bool = False) -> Post:
        if not self.user_repo.get_by_id(author_id):
            raise InvalidOperationError("作者不存在")
        if not title.strip():
            raise InvalidOperationError("标题不能为空")

        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while self.post_repo.get_by_slug(slug):
            counter += 1
            slug = f"{base_slug}-{counter}"

        post = Post(
            title=title, slug=slug, content=content,
            is_published=is_published, author_id=author_id,
        )
        return self.post_repo.create(post)

    def get_post(self, slug: str) -> Post:
        post = self.post_repo.get_by_slug(slug)
        if not post:
            raise PostNotFoundError(slug)
        return post

    def list_posts(self, skip: int, limit: int, published_only: bool = True,
                   author_id: int | None = None,
                   keyword: str | None = None) -> list[Post]:
        return self.post_repo.list_posts(skip, limit, published_only, author_id, keyword)

    def update_post(self, post_id: int, current_user: User,
                    title: str | None = None, content: str | None = None,
                    is_published: bool | None = None) -> Post:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)
        if not post.can_be_edited_by(current_user.id):
            raise PermissionDeniedError("无权限修改此文章")

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if is_published is not None:
            post.is_published = is_published
        return self.post_repo.update(post)

    def delete_post(self, post_id: int, current_user: User) -> None:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)
        if not post.can_be_edited_by(current_user.id):
            raise PermissionDeniedError("无权限删除此文章")
        self.post_repo.soft_delete(post_id)

