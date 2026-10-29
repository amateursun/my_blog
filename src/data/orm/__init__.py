# src/data/orm/__init__.py

'''
__init__.py 是 ORM 包的“总入口”:它把散落在各个文件中的 Base 和所有 ORM 模型聚合到包顶层,对外提供简洁的导入接口,
同时确保所有模型在包被导入时自动注册到 Base.metadata
main.py 只需 from src.data.orm import Base 一行,就能保证 Base.metadata 包含所有表,create_all() 和 Alembic 迁移才能正常工作
'''

from src.data.orm.base import Base
from src.data.orm.user import UserORM
from src.data.orm.post import PostORM
from src.data.orm.user_profile import UserProfileORM
from src.data.orm.tag import TagORM

__all__ = ["Base", "UserORM", "PostORM", "UserProfileORM", "TagORM"]

