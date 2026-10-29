# src/data/orm/post.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.orm.base import Base
from src.data.orm.base import TimestampMixin, SoftDeleteMixin
from src.data.orm.associations import post_tag


if TYPE_CHECKING:
    from src.data.orm.user import UserORM
    from src.data.orm.tag import TagORM

class PostORM(Base, TimestampMixin, SoftDeleteMixin):
    """文章表"""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)          # 主键
    title: Mapped[str] = mapped_column(String(100), nullable=False)                 # 标题
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)  # URL 标识(原缺失,必须加)
    content: Mapped[str] = mapped_column(Text, nullable=False)                      # 正文
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)              # 是否发布
    # Post(多)持有 author_id外键, User(一)通过 relationship 反向访问
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False) # 作者外键

    author: Mapped["UserORM"] = relationship("UserORM", back_populates="posts")     # 多对一
    # 多对多关系不需要在 relationship 上加 cascade="all, delete-orphan",因为,中间表已经通过 ondelete="CASCADE" 处理了级联
    tags: Mapped[list["TagORM"]] = relationship(                                     # 多对多
        "TagORM",                                     # 指向另一端的主表ORM
        secondary=post_tag,                           # 中间表
        back_populates="posts",                       # back_populates 只指向另一端的主表模型属性
        lazy="selectin",)                             # 决定何时、如何从数据库加载关联对象

    def __repr__(self) -> str:
        return f"<PostORM(id={self.id}, title='{self.title}')>"