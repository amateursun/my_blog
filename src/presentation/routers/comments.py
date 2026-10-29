# src/presentation/routers/comments.py
from fastapi import APIRouter, Depends, Query

from src.presentation.schemas.comment import CommentCreate, CommentOut
from src.core.use_cases.comment_service import CommentService
from src.core.entities.user import User
from src.bootstrap.dependencies import get_comment_service, get_current_active_user

router = APIRouter(tags=["评论"])


@router.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=201)
def create_comment(
    post_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    service: CommentService = Depends(get_comment_service),
):
    return service.create_comment(post_id, current_user.id, data.content)


@router.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def list_comments(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: CommentService = Depends(get_comment_service),
):
    return service.list_comments(post_id, skip, limit)


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    service: CommentService = Depends(get_comment_service),
):
    service.delete_comment(comment_id, current_user)