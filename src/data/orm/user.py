# src/data/orm/user.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.orm.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:  # 使用 TYPE_CHECKING 延迟导入,这样运行时不会真正执行 import,但 IDE 能识别类型
    from src.data.orm.user_profile import UserProfileORM
    from src.data.orm.post import PostORM

class UserORM(Base, TimestampMixin, SoftDeleteMixin):
    """用户表"""
    __tablename__ = "users"                           # 表名

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)          # 主键
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)  # 用户名
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)    # 邮箱
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)       # 哈希密码(字段名统一)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)                  # 是否激活

    # 一对一:User ↔ UserProfile                       # "UserProfileORM | None" 类型注解加上双引号变成字符串,告诉 SQLAlchemy 延迟解析
    profile: Mapped["UserProfileORM | None"] = relationship(  # 可为 None,否则会报类型错
        "UserProfileORM",
        back_populates="user",                        # 反向引用,真正的职责是把两端的关系“绑定”成同一段关系的两个方向,使它们在内存中自动同步
        uselist=False,                                # 一对一关键, ORM 层的语义声明,unique=True 是外键是数据库层的约束,两者缺一不可
        cascade="all, delete-orphan",)                # 级联删除

    # 一对多:User → Post
    posts: Mapped[list["PostORM"]] = relationship(
        "PostORM",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin",)                             # 避免 N+1

    def __repr__(self) -> str:
        return f"<UserORM(id={self.id}, username='{self.username}')>"


