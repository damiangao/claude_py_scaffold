from contextlib import asynccontextmanager
from time import time

from fastapi import FastAPI, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from claude_py_scaffold.config import get_settings
from claude_py_scaffold.database import engine
from claude_py_scaffold.handlers import register_exception_handlers
from claude_py_scaffold.logging import get_logger, setup_logging
from claude_py_scaffold.middleware import setup_cors
from claude_py_scaffold.models.base import Base
from claude_py_scaffold.routers.v1 import auth as auth_v1
from claude_py_scaffold.routers.v1 import users as users_v1

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    # 启动
    setup_logging(settings)
    logger.info(f"启动应用：{settings.app_name} v{settings.app_version}")
    logger.info(f"环境：{settings.environment}")

    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("数据库表已创建")

    yield

    # 关闭
    logger.info("应用关闭")
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI 练习项目",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 注册异常处理器
register_exception_handlers(app)

# 配置 CORS
setup_cors(app)

# 注册 v1 路由
app.include_router(auth_v1.router, prefix="/api/v1")
app.include_router(users_v1.router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to FastAPI Practice",
        "version": settings.app_version,
        "docs": "/docs",
        "api": "/api/v1",
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """健康检查"""
    health_info = {
        "status": "ok",
        "timestamp": int(time()),
        "version": settings.app_version,
    }

    # 检查数据库连接
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        health_info["database"] = "connected"
    except SQLAlchemyError as e:
        health_info["database"] = "disconnected"
        health_info["database_error"] = str(e)

    return health_info
