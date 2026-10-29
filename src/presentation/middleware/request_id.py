# src/presentation/middleware/request_id.py
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.bootstrap.logging import request_id_var

# 为每个请求分配(或复用)一个唯一 ID,存入 ContextVar 供整个请求链路使用,写入响应头供客户端追踪,最后恢复 ContextVar 防止污染下一次请求
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_var.set(request_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            request_id_var.reset(token)

