# src/core/use_cases/comment_service.py
from src.core.entities.comment import Comment
from src.core.entities.user import User
from src.core.exceptions import (
    PostNotFoundError, NotFoundError, PermissionDeniedError,
)
from src.core.interfaces.repositories import (
    CommentRepositoryProtocol, PostRepositoryProtocol,
)


class CommentService:
    def __init__(self, comment_repo: CommentRepositoryProtocol,
                 post_repo: PostRepositoryProtocol):
        self.comment_repo = comment_repo
        self.post_repo = post_repo

    def create_comment(self, post_id: int, author_id: int, content: str) -> Comment:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)
        if not content.strip():
            raise ValueError("评论内容不能为空")

        comment = Comment(content=content, post_id=post_id, author_id=author_id)
        return self.comment_repo.create(comment)

    def list_comments(self, post_id: int, skip: int, limit: int) -> list[Comment]:
        return self.comment_repo.list_by_post(post_id, skip, limit)

    def delete_comment(self, comment_id: int, current_user: User) -> None:
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("评论", comment_id)

        post = self.post_repo.get_by_id(comment.post_id)
        post_author_id = post.author_id if post else -1

        if not comment.can_be_deleted_by(current_user.id, post_author_id):
            raise PermissionDeniedError("无权限删除此评论")
        self.comment_repo.soft_delete(comment_id)