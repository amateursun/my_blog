# src/data/repositories/user_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.core.entities.user import User
from src.core.interfaces.repositories import UserRepositoryProtocol
from src.core.exceptions import EmailExistsError, UsernameExistsError
from src.data.orm.user import UserORM


class SqlalchemyUserRep(UserRepositoryProtocol):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        orm = self.db.query(UserORM).filter(
            UserORM.id == user_id, UserORM.is_deleted == False
        ).first()
        return self._to_entity(orm) if orm else None

    def get_by_email(self, email: str) -> Optional[User]:
        orm = self.db.query(UserORM).filter(
            UserORM.email == email, UserORM.is_deleted == False
        ).first()
        return self._to_entity(orm) if orm else None

    def get_by_username(self, username: str) -> Optional[User]:
        orm = self.db.query(UserORM).filter(
            UserORM.username == username, UserORM.is_deleted == False
        ).first()
        return self._to_entity(orm) if orm else None

    def create(self, user: User) -> User:
        orm = UserORM(
            username=user.username,
            email=user.email,
            hash_password=user.hash_password,
            is_active=user.is_active,
        )
        self.db.add(orm)
        try:
            self.db.flush()
        except IntegrityError as e:
            self.db.rollback()
            msg = str(e.orig).lower()
            if "email" in msg:
                raise EmailExistsError(user.email) from e
            if "username" in msg:
                raise UsernameExistsError(user.username) from e
            raise
        self.db.refresh(orm)
        return self._to_entity(orm)

    def update(self, user: User) -> User:
        orm = self.db.query(UserORM).filter(UserORM.id == user.id).first()
        if not orm:
            raise ValueError(f"User {user.id} not found")
        orm.username = user.username
        orm.email = user.email
        orm.hash_password = user.hash_password
        orm.is_active = user.is_active
        self.db.flush()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def soft_delete(self, user_id: int) -> None:
        orm = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if orm:
            orm.is_deleted = True
            self.db.flush()

    @staticmethod
    def _to_entity(orm: UserORM) -> User:
        return User(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            hash_password=orm.hash_password,
            is_active=orm.is_active,
            is_deleted=orm.is_deleted,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )