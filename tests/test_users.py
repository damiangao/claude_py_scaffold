import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from claude_py_scaffold.database import get_db
from claude_py_scaffold.main import app
from claude_py_scaffold.models.base import Base

# 内存数据库 URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_session():
    """创建内存数据库会话"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client(db_session):
    """创建测试客户端"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_user(client):
    """测试创建用户"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user(client):
    """测试获取用户"""
    # 先创建用户
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }
    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # 获取用户
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    """测试获取不存在的用户"""
    response = await client.get("/users/999")
    assert response.status_code == 404
    assert "用户不存在" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_duplicate_username(client):
    """测试用户名重复"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }
    await client.post("/users/", json=user_data)

    response = await client.post("/users/", json=user_data)
    assert response.status_code == 409
    assert "用户名已存在" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_duplicate_email(client):
    """测试邮箱重复"""
    await client.post("/users/", json={
        "username": "user1",
        "email": "test@example.com",
        "password": "password123",
    })

    response = await client.post("/users/", json={
        "username": "user2",
        "email": "test@example.com",
        "password": "password123",
    })
    assert response.status_code == 409
    assert "邮箱已被注册" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_list_users(client):
    """测试用户列表"""
    await client.post("/users/", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
    })

    response = await client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "user1"
