
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError

from src.bootstrap.config import settings
from src.bootstrap.database import engine
from src.data.orm import Base  # main.py 导入包时,模型已经被“构建并注册”了,但这个构建动作是间接由 __init__.py 触发的
from src.bootstrap.logging import setup_logging
from src.presentation.middleware.request_id import RequestIDMiddleware
from src.presentation.middleware.access_log import AccessLogMiddleware
from src.presentation.routers import auth, users, posts, tags, comments
from src.core.exceptions import (
    NotFoundError, ConflictError, AuthError, PermissionDeniedError,
    BusinessRuleError, InfrastructureError, DomainError,
)

# 日志必须先初始化
setup_logging()
logger = logging.getLogger(__name__)

# 开发环境自动建表(生产用 Alembic): 同步
if settings.DEBUG:
    Base.metadata.create_all(bind=engine)

''' 异步
async with engine.begin() as conn:  # 从异步引擎借一个连接,并开启事务。async with 保证用完自动归还连接
    await conn.run_sync(Base.metadata.create_all)  # run_sync() 把同步方法 create_all 放到线程池中执行,避免阻塞事件循环。await 等待它执行完毕
'''

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# ============================================================
# 中间件注册（后注册先执行）
# ============================================================
app.add_middleware(CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(AccessLogMiddleware)

# ============================================================
# 全局异常处理器
# ============================================================
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})

@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": exc.message})

@app.exception_handler(AuthError)
async def auth_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.exception_handler(PermissionDeniedError)
async def permission_handler(request: Request, exc: PermissionDeniedError):
    return JSONResponse(status_code=403, content={"detail": exc.message})

@app.exception_handler(BusinessRuleError)
async def business_rule_handler(request: Request, exc: BusinessRuleError):
    return JSONResponse(status_code=400, content={"detail": exc.message})

@app.exception_handler(InfrastructureError)
async def infra_handler(request: Request, exc: InfrastructureError):
    logger.error(f"基础设施异常: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": "参数校验失败", "errors": exc.errors()})

@app.exception_handler(DomainError)
async def domain_fallback(request: Request, exc: DomainError):
    return JSONResponse(status_code=400, content={"detail": exc.message})

# ============================================================
# 路由注册
# ============================================================
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(posts.router, prefix=settings.API_PREFIX)
app.include_router(tags.router, prefix=settings.API_PREFIX)
app.include_router(comments.router, prefix=settings.API_PREFIX)

@app.get("/health", tags=["系统"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)




