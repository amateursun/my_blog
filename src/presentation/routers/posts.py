# src/presentation/routers/posts.py
from fastapi import APIRouter, Depends, Query

from src.presentation.schemas.post import PostCreate, PostUpdate, PostOut, PostListOut
from src.core.use_cases.post_service import PostService
from src.core.entities.user import User
from src.bootstrap.dependencies import get_post_service, get_current_active_user

router = APIRouter(prefix="/posts", tags=["文章"])


@router.post("/", response_model=PostOut, status_code=201)
def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_active_user),
    service: PostService = Depends(get_post_service),
):
    return service.create_post(current_user.id, data.title, data.content, data.is_published)


@router.get("/", response_model=list[PostListOut])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    keyword: str | None = None,
    service: PostService = Depends(get_post_service),
):
    return service.list_posts(skip, limit, published_only=True, keyword=keyword)


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, service: PostService = Depends(get_post_service)):
    return service.get_post(slug)


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: User = Depends(get_current_active_user),
    service: PostService = Depends(get_post_service),
):
    return service.update_post(
        post_id, current_user, data.title, data.content, data.is_published
    )


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    service: PostService = Depends(get_post_service),
):
    service.delete_post(post_id, current_user)

