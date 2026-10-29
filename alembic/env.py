# alembic/env.py ( 生产级 env.py（同步 + 多数据库支持）)
import os
import re
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. 导入所有模型的 Base（确保 metadata 完整）
from src.data.orm.base import Base
from src.data.orm import *

config = context.config

# 2. 动态读取数据库 URL（优先环境变量，其次 ini）
#    生产环境通过环境变量注入，不把密码写进文件
def get_url(name: str = "DATABASE_URL") -> str:
    url = os.getenv(name) or config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError(f"数据库 URL 未配置：环境变量 {name} 或 alembic.ini")
    return url

# 3. 支持多数据库：alembic.ini 中配置 databases = main,analytics
def get_engines():
    """返回 {引擎名: URL} 的字典，用于多库迁移"""
    db_names = config.get_main_option("databases", "main")
    names = [n.strip() for n in re.split(r",", db_names) if n.strip()]
    engines = {}
    for name in names:
        env_key = f"{name.upper()}_DATABASE_URL"
        engines[name] = get_url(env_key)
    return engines


def run_migrations_offline() -> None:
    """离线模式：生成 SQL 脚本，不连接数据库，供 DBA 审核"""
    for name, url in get_engines().items():
        print(f"-- 生成 {name} 的迁移 SQL --")
        context.configure(
            url=url,
            target_metadata=Base.metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,          # 检测列类型变更
            compare_server_default=True,  # 检测默认值变更
        )
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    """在线模式：直接连接数据库执行迁移"""
    engines_dict = get_engines()
    
    # 每个数据库独立执行
    for name, url in engines_dict.items():
        # 生产环境迁移使用同步引擎（psycopg2 / psycopg）
        # 注意：URL 需使用同步驱动，如 postgresql+psycopg2://
        connectable = engine_from_config(
            {"sqlalchemy.url": url},
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,  # 迁移用完即断，不保留连接
            connect_args={"charset": "utf8mb4"},   # 👈 新增：直接传给 PyMySQL
        )
        
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=Base.metadata,
                compare_type=True,
                compare_server_default=True,
            )
            with context.begin_transaction():
                context.run_migrations()
        
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()