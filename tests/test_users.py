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
    response = await client.post("/api/v1/auth/register", json=user_data)
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
    create_response = await client.post("/api/v1/auth/register", json=user_data)
    user_id = create_response.json()["id"]

    # 获取用户
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    """测试获取不存在的用户"""
    response = await client.get("/api/v1/users/999")
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
    await client.post("/api/v1/auth/register", json=user_data)

    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 409
    assert "用户名已存在" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_duplicate_email(client):
    """测试邮箱重复"""
    await client.post("/api/v1/auth/register", json={
        "username": "user1",
        "email": "test@example.com",
        "password": "password123",
    })

    response = await client.post("/api/v1/auth/register", json={
        "username": "user2",
        "email": "test@example.com",
        "password": "password123",
    })
    assert response.status_code == 409
    assert "邮箱已被注册" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_list_users(client):
    """测试用户列表（分页）"""
    # 创建多个用户
    await client.post("/users/", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123",
    })
    await client.post("/users/", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123",
    })

    # 获取用户列表（分页）
    response = await client.get("/users/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()

    # 检查分页结构
    assert "items" in data
    assert "page_info" in data
    assert data["page_info"]["total"] == 2
    assert data["page_info"]["page"] == 1
    assert data["page_info"]["page_size"] == 10

    # 检查用户数据
    items = data["items"]
    assert len(items) == 2
    assert items[0]["username"] == "user1"


@pytest.mark.asyncio
async def test_list_users_pagination(client):
    """测试分页功能"""
    # 创建 5 个用户
    for i in range(5):
        await client.post("/users/", json={
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password": "password123",
        })

    # 第一页
    response = await client.get("/users/?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["page_info"]["total"] == 5
    assert data["page_info"]["total_pages"] == 3
    assert data["page_info"]["has_next"] is True
    assert data["page_info"]["has_prev"] is False

    # 第二页
    response = await client.get("/users/?page=2&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["page_info"]["page"] == 2
    assert data["page_info"]["has_next"] is True
    assert data["page_info"]["has_prev"] is True

    # 第三页（最后一页）
    response = await client.get("/users/?page=3&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["page_info"]["has_next"] is False
    assert data["page_info"]["has_prev"] is True
