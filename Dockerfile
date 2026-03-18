FROM python:3.11-slim

WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 复制项目文件
COPY pyproject.toml ./
COPY claude_py_scaffold/ ./claude_py_scaffold/
COPY tests/ ./tests/

# 安装依赖
RUN uv sync --frozen

# 运行服务器
CMD ["uv", "run", "uvicorn", "claude_py_scaffold.main:app", "--host", "0.0.0.0", "--port", "8000"]
