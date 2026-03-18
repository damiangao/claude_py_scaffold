# Claude Py Scaffold

专为 Claude Code 开发的 FastAPI Python 脚手架项目，包含完整的基础设施。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 环境要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## 快速开始

### 1. 安装依赖

```bash
uv sync --dev
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

### 3. 启动服务器

```bash
uv run uvicorn claude_py_scaffold.main:app --reload
```

访问：
- 主页：http://127.0.0.1:8000/
- API 文档：http://127.0.0.1:8000/docs
- API v1：http://127.0.0.1:8000/api/v1

### 4. 运行测试

```bash
uv run pytest -v
```

## 命令参考

### 开发

```bash
# 同步依赖
uv sync          # 生产依赖
uv sync --dev    # 开发依赖

# 运行服务器
uv run uvicorn claude_py_scaffold.main:app --reload

# 代码检查
uv run ruff check .
uv run ruff format .

# 运行测试
uv run pytest
uv run pytest -v

# 数据库迁移
uv run alembic revision --autogenerate -m "消息"
uv run alembic upgrade head
uv run alembic downgrade -1
```

### Pre-commit

```bash
# 安装 pre-commit hooks
pip install pre-commit  # 或 uv pip install pre-commit
pre-commit install
```

### 发布

```bash
# 构建包
uv build

# 发布到 PyPI
uv publish
```

### Docker

```bash
# 使用 docker-compose
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down

# 传统方式
docker build -t claude-py-scaffold .
docker run -p 8000:8000 claude-py-scaffold
```

## API 接口

### 认证

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 | ❌ |
| POST | `/api/v1/auth/login` | 用户登录 | ❌ |

### 用户管理

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/users/me` | 获取当前用户 | ✅ |
| GET | `/api/v1/users/` | 用户列表（分页） | ❌ |
| GET | `/api/v1/users/{id}` | 用户详情 | ❌ |

### 其他

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 根路径 |
| GET | `/health` | 健康检查（含数据库状态） |
| GET | `/docs` | Swagger API 文档 |
| GET | `/redoc` | ReDoc API 文档 |

### 使用示例

```bash
# 1. 注册
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"123456"}'

# 2. 登录获取 token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456"

# 3. 访问受保护资源
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <token>"

# 4. 健康检查
curl http://localhost:8000/health

# 5. 用户列表（分页）
curl "http://localhost:8000/api/v1/users/?page=1&page_size=10"
```

## 项目结构

```
claude_py_scaffold/
├── claude_py_scaffold/        # 主包
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── logging.py           # 日志配置
│   ├── middleware.py        # CORS 中间件
│   ├── exceptions.py        # 自定义异常
│   ├── handlers.py          # 异常处理器
│   ├── deps.py              # 依赖注入
│   ├── security.py          # 密码加密
│   ├── token.py             # JWT 令牌
│   ├── schemas.py           # Pydantic 模型
│   ├── utils/               # 工具函数
│   │   ├── __init__.py
│   │   └── pagination.py    # 分页工具
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── base.py          # 模型基类
│   │   └── user.py          # 用户模型
│   └── routers/
│       ├── __init__.py
│       └── v1/              # API v1
│           ├── __init__.py
│           ├── auth.py      # 认证路由
│           └── users.py     # 用户路由
├── tests/
│   └── test_users.py        # 单元测试
├── alembic/                 # 数据库迁移
│   ├── __init__.py
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini              # Alembic 配置
├── scripts/
│   └── docker-build.sh      # Docker 脚本
├── .github/workflows/
│   ├── docker-build.yml     # Docker CI/CD
│   ├── test.yml             # 测试工作流
│   └── lint.yml             # 代码检查工作流
├── .pre-commit-config.yaml  # Pre-commit 配置
├── docker-compose.yml       # Docker Compose
├── pyproject.toml
├── uv.lock
├── .env.example
├── Dockerfile
├── .gitignore
├── CHANGELOG.md
├── README.md
├── CLAUDE.md
└── LICENSE
```

## 核心模块

### 配置管理
- `pydantic-settings` 读取环境变量
- 支持多环境配置

### 数据库
- SQLAlchemy 异步模式
- 自动创建表
- 会话管理依赖注入

### 认证/授权
- JWT 令牌
- OAuth2 Password Flow
- bcrypt 密码加密

### 数据库迁移
- Alembic 数据库版本管理
- 支持自动迁移生成
- 支持回滚操作

### 分页
- 通用分页工具
- 分页响应格式统一

### 中间件
- CORS 跨域支持（开发环境默认允许 localhost:3000/8080）

### 日志
- 彩色控制台输出
- 可配置日志级别

### 错误处理
- 统一异常格式
- 全局异常处理器

### CI/CD
- GitHub Actions (test.yml, lint.yml, docker-build.yml)
- 支持多 Python 版本测试 (3.10, 3.11, 3.12)

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `APP_NAME` | 应用名称 | FastAPI Practice |
| `DEBUG` | 调试模式 | false |
| `ENVIRONMENT` | 环境 | development |
| `DATABASE_URL` | 数据库连接 | SQLite |
| `LOG_LEVEL` | 日志级别 | INFO |
| `SECRET_KEY` | JWT 密钥 | (生产环境务必修改) |
| `ALGORITHM` | JWT 算法 | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 令牌过期时间 | 30 |

详见 `.env.example`。

## 代码质量

```bash
# 检查代码
uv run ruff check .

# 格式化代码
uv run ruff format .

# 运行测试
uv run pytest -v
```

## Changelog

详见 [CHANGELOG.md](CHANGELOG.md)

## License

MIT License - 详见 [LICENSE](LICENSE)
