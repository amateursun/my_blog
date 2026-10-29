# src/data/orm/comment.py
from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.orm.base import Base
from src.data.orm.base import TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from src.data.orm.user import UserORM

class UserProfileORM(Base, TimestampMixin, SoftDeleteMixin):
    """用户资料表"""
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)          # 主键
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False) # 外键 + 唯一
    personal_profile: Mapped[str | None] = mapped_column(Text, nullable=True)        # 个人简介

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="profile")     # 反向

    def __repr__(self) -> str:
        return f"<UserProfileORM(user_id={self.user_id}, personal_profile='{self.personal_profile}')>"
