# ------------------------------------------------1.1--/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """全局配置:从 .env 文件和环境变量中读取"""
    # ----应用----
    APP_NAME: str = "Blog API"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    # ----数据库----
    DATABASE_URL: str = "sqlite:///./user_blog.db"
    # ----JWT----
    SECRET_KEY: str = "change-me-in-production-please-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # ----CORS----
    CORS_ALLOW_ORIGIN: list[str] = ["http://localhost:3000"]
    # ----日志----
    LOG_DIR: str = "logs"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",                    # 指定环境变量文件
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",)

settings = Settings()