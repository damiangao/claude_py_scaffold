# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Claude Py Scaffold - 专为 Claude Code 开发的 FastAPI Python 脚手架项目。

## 常用命令

```bash
# 安装依赖
uv sync          # 生产依赖
uv sync --dev    # 开发依赖

# 运行
uv run uvicorn claude_py_scaffold.main:app --reload

# 测试
uv run pytest
uv run pytest tests/test_users.py::test_create_user

# 代码检查
uv run ruff check .
uv run ruff format .

# 数据库迁移
uv run alembic revision --autogenerate -m "消息"
uv run alembic upgrade head
uv run alembic downgrade -1

# 发布
uv build
uv publish
```

## 代码架构

```
claude_py_scaffold/
├── claude_py_scaffold/        # 主包
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理 (pydantic-settings)
│   ├── database.py          # 数据库连接 (SQLAlchemy)
│   ├── logging.py           # 日志配置
│   ├── middleware.py        # CORS 中间件
│   ├── exceptions.py        # 自定义异常
│   ├── handlers.py          # 异常处理器
│   ├── deps.py              # 依赖注入
│   ├── security.py          # 密码加密
│   ├── token.py             # JWT 令牌
│   ├── schemas.py           # Pydantic 数据模型
│   ├── utils/               # 工具函数
│   │   └── pagination.py    # 分页工具
│   ├── models/              # SQLAlchemy 模型
│   │   ├── base.py          # 模型基类
│   │   └── user.py          # 用户模型
│   └── routers/
│       └── v1/              # API v1
│           ├── auth.py      # 认证路由
│           └── users.py     # 用户路由
├── tests/
│   └── test_users.py        # 单元测试
├── alembic/                 # 数据库迁移
│   ├── env.py
│   └── versions/
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env.example
├── Dockerfile
└── README.md
```

## 模块说明

### 配置管理 (config.py)
- 使用 `pydantic-settings` 读取环境变量
- `get_settings()` 返回单例配置

### 数据库 (database.py)
- 异步 SQLAlchemy 引擎
- `get_db()` 依赖注入获取会话

### 日志 (logging.py)
- 彩色控制台输出
- `setup_logging()` 初始化日志
- `get_logger(name)` 获取日志器

### 异常处理 (exceptions.py, handlers.py)
- `AppException` 基类
- `NotFoundException`, `DuplicateException` 等子类
- `register_exception_handlers()` 注册处理器

### 中间件 (middleware.py)
- CORS 跨域支持
- 开发环境默认允许 localhost:3000/8080

### 分页 (utils/pagination.py)
- `PaginationParams` - 分页参数（page, page_size）
- `paginate()` - 通用分页查询函数
- `PaginatedResponse` - 分页响应格式

### 数据库迁移 (alembic/)
- Alembic 配置在 `alembic.ini`
- 迁移脚本在 `alembic/versions/`
- 使用 `uv run alembic revision --autogenerate -m "消息"` 生成迁移

## 代码规范

- 类型注解：使用 Python 类型注解
- Pydantic 模型：放在 `schemas.py` 中
- 路由组织：按功能模块放在 `routers/` 目录下
- 导入顺序：标准库 → 第三方库 → 本地模块
- 模型组织：每个模型独立文件，统一在 `models/__init__.py` 导出
- 分页接口：使用 `PaginationParams` 和 `paginate()`

## 测试规范

- 测试文件放在 `tests/` 目录
- 使用 `httpx.AsyncClient` 进行接口测试
- 每个测试前重置数据库状态（使用 fixture）
- 测试函数以 `test_` 开头
