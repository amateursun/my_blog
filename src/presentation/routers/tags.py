# src/presentation/routers/tags.py
from fastapi import APIRouter, Depends

from src.presentation.schemas.tag import TagOut, TagCreate
from src.core.use_cases.tag_service import TagService
from src.bootstrap.dependencies import get_tag_service

router = APIRouter(prefix="/tags", tags=["标签"])


@router.get("/", response_model=list[TagOut])
def list_tags(service: TagService = Depends(get_tag_service)):
    return service.list_tags()


@router.post("/", response_model=TagOut, status_code=201)
def create_tag(data: TagCreate, service: TagService = Depends(get_tag_service)):
    return service.get_or_create(data.name)