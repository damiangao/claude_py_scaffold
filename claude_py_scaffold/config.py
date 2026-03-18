from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    # 应用
    app_name: str = "FastAPI Practice"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "testing", "production"] = "development"

    # 服务器
    host: str = "0.0.0.0"
    port: int = 8000

    # 数据库
    database_url: str = "sqlite+aiosqlite:///./app.db"

    # 日志
    log_level: str = "INFO"

    # JWT 配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
