# src/core/use_cases/tag_service.py
from src.core.entities.tag import Tag
from src.core.interfaces.repositories import TagRepositoryProtocol


class TagService:
    def __init__(self, repo: TagRepositoryProtocol):
        self.repo = repo

    def list_tags(self) -> list[Tag]:
        return self.repo.list_all()

    def get_or_create(self, name: str) -> Tag:
        name = name.strip()
        if not name:
            raise ValueError("标签名不能为空")
        return self.repo.get_or_create(name)