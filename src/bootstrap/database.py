# ------------------------------------------------1.2--/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import sessionmaker
from bootstrap.config import settings

engine = create_engine(  # 创建数据库引擎
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,)

AsyncSessionLocal = sessionmaker(  # 创建异步会话
    engine,
    expire_on_commit=False,
    autoflush=False,)

async def get_db():  # 获取数据库会话db
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception:
                db.rollback()
                raise
        finally:
            await db.close()