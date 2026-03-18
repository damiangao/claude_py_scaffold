# Commands and Templates

## Development Workflow

### Create New Feature
1. Create model: `models/<name>.py`
2. Create Schema: `schemas.py`
3. Create router: `routers/v1/<name>.py`
4. Register router: `routers/v1/__init__.py`
5. Create tests: `tests/test_<name>.py`
6. Generate migration: `uv run alembic revision --autogenerate -m "xxx"`
7. Apply migration: `uv run alembic upgrade head`

## Quick Reference

### Database
```bash
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
uv run alembic downgrade -1
uv run alembic current
```

### Testing
```bash
uv run pytest -v
uv run pytest tests/test_users.py::test_create_user -v
```

### Code Quality
```bash
uv run ruff check . --fix
uv run ruff format .
uv run pre-commit run --all-files
```

## Code Templates

### Model
```python
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base

class <Name>(Base):
    __tablename__ = "<name>s"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Schema
```python
class <Name>Create(BaseModel):
    field: str = Field(..., description="description")

class <Name>Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    field: str
```

### Router
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from claude_py_scaffold.database import get_db

router = APIRouter(prefix="/<name>", tags=["Module Name"])

@router.get("/")
async def list_items(db: AsyncSession = Depends(get_db)):
    pass
```

### Test
```python
import pytest

@pytest.mark.asyncio
async def test_xxx(client):
    response = await client.post("/api/v1/auth/register", json={...})
    assert response.status_code == 201
```
