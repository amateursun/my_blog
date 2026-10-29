# src/presentation/middleware/access_log.py
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("access")

# 为每个 HTTP 请求记录一条访问日志(Access Log),包含请求方法、路径、响应状态码和处理耗时
class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        cost_ms = (time.perf_counter() - start) * 1000
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({cost_ms:.2f}ms)")
        return response

