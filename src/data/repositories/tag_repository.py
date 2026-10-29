# src/data/repositories/tag_repository.py
from typing import Optional
from sqlalchemy.orm import Session

from src.core.entities.tag import Tag
from src.core.interfaces.repositories import TagRepositoryProtocol
from src.data.orm.tag import TagORM


class SqlalchemyTagRep(TagRepositoryProtocol):
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Tag]:
        orm = self.db.query(TagORM).filter(TagORM.name == name).first()
        return Tag(id=orm.id, name=orm.name) if orm else None

    def list_all(self) -> list[Tag]:
        return [Tag(id=o.id, name=o.name) for o in self.db.query(TagORM).all()]

    def get_or_create(self, name: str) -> Tag:
        orm = self.db.query(TagORM).filter(TagORM.name == name).first()
        if not orm:
            orm = TagORM(name=name)
            self.db.add(orm)
            self.db.flush()
        return Tag(id=orm.id, name=orm.name)