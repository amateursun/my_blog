# src/data/orm/associations.py
from sqlalchemy import Table, Column, ForeignKey

from src.data.orm.base import Base

post_tag = Table(                                     # 多对多中间表:文章 ↔ 标签
    "post_tag",                                       # 表名
    Base.metadata,                                    # 挂到 Base 元数据
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),  # 文章外键
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),)    # 标签外键
