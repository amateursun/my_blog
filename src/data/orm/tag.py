# src/data/orm/tag.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.orm.base import Base
from src.data.orm.associations import post_tag
from src.data.orm.post import PostORM

if TYPE_CHECKING:
    from src.data.orm.post import PostORM

class TagORM(Base):
    """标签表"""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)          # 主键
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)  # 标签名

    posts: Mapped[list["PostORM"]] = relationship(                                   # 反向多对多
        "PostORM", secondary=post_tag, back_populates="tags", lazy="selectin")

    def __repr__(self):  # 魔术方法: ORM 实体类的 __repr__ 方法,调试、日志、REPL,面向开发; __str__ 方法是面向用户,print() 输出。目标是“可读、友好”
        return f"<UserORM(id={self.id}, username='{self.username}')>"