# ----------------------------------------------------------1.3---/bootstrap/logging.py
# 1.31 src/bootstrap/logging/filters.py
import logging
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestIDFilter(logging.Filter):
    """为每条日志注入当前请求的 request_id"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get() or "-"
        return True

# 1.32 src/bootstrap/logging/formatters.py
import json
import logging
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    """生产环境结构化日志"""
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)

class DevFormatter(logging.Formatter):
    """开发环境可读日志"""
    COLORS = {
        "DEBUG": "\033[36m", "INFO": "\033[32m", "WARNING": "\033[33m",
        "ERROR": "\033[31m", "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        return (
            f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')} | "
            f"{color}{record.levelname}{self.RESET} | "
            f"{record.name}:{record.funcName}:{record.lineno} | "
            f"[{getattr(record, 'request_id', '-')}] {record.getMessage()}"
        )

# 1.33 src/bootstrap/logging/config.py
import logging
import logging.config
import sys
from pathlib import Path

from src.bootstrap.config import settings

def setup_logging() -> None:
    """初始化全局日志配置，必须在应用启动前调用"""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    formatter = "dev" if settings.DEBUG else "json"

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"dev": {"()": DevFormatter}, "json": {"()": JSONFormatter}},
        "filters": {"request_id": {"()": RequestIDFilter}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": formatter,
                "filters": ["request_id"],
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_dir / "app.log",
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 10,
                "encoding": "utf-8",
                "formatter": formatter,
                "filters": ["request_id"],
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_dir / "error.log",
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 10,
                "encoding": "utf-8",
                "formatter": formatter,
                "level": "ERROR",
                "filters": ["request_id"],
            },
        },
        "root": {"level": log_level, "handlers": ["console", "file", "error_file"]},
        "loggers": {
            "uvicorn": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "uvicorn.access": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "uvicorn.error": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "sqlalchemy.engine": {"level": "WARNING" if not settings.DEBUG else "INFO",
                                  "handlers": ["console"], "propagate": False},
            "httpx": {"level": "WARNING"},
            "httpbootstrap": {"level": "WARNING"},
        },
    }

    logging.config.dictConfig(config)
    logging.getLogger(__name__).info("日志系统初始化完成",extra={"request_id": "-"},)
