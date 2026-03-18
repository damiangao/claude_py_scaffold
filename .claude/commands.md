# Claude Code 常用命令

## 开发流程

### 创建新功能
```
1. 创建模型 (如需): models/<name>.py
2. 创建 Schema: schemas.py
3. 创建路由：routers/v1/<name>.py
4. 注册路由：routers/v1/__init__.py
5. 创建测试：tests/test_<name>.py
6. 生成迁移：uv run alembic revision --autogenerate -m "xxx"
7. 运行迁移：uv run alembic upgrade head
```

### 数据库操作
```bash
# 生成迁移
uv run alembic revision --autogenerate -m "描述"

# 应用迁移
uv run alembic upgrade head

# 回滚
uv run alembic downgrade -1

# 查看当前版本
uv run alembic current
```

### 测试
```bash
# 运行所有测试
uv run pytest -v

# 运行单个测试
uv run pytest tests/test_users.py::test_create_user -v

# 运行带标记的测试
uv run pytest -m asyncio -v
```

### 代码质量
```bash
# 检查并修复
uv run ruff check . --fix

# 格式化
uv run ruff format .

# 运行 pre-commit
uv run pre-commit run --all-files
```

## 文件创建规范

### 新建 Model
位置：`models/<name>.py`
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class <Name>(Base):
    __tablename__ = "<name>s"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 新建 Schema
位置：`schemas.py`
```python
class <Name>Create(BaseModel):
    """创建请求"""
    field: str = Field(..., description="描述")

class <Name>Response(BaseModel):
    """响应"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    field: str
```

### 新建 Router
位置：`routers/v1/<name>.py`
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from claude_py_scaffold.database import get_db

router = APIRouter(prefix="/<name>", tags=["模块名"])

@router.get("/")
async def list_items(db: AsyncSession = Depends(get_db)):
    pass
```

### 新建测试
位置：`tests/test_<name>.py`
```python
import pytest

@pytest.mark.asyncio
async def test_xxx(client):
    response = await client.post("/api/v1/auth/register", json={...})
    assert response.status_code == 201
```
