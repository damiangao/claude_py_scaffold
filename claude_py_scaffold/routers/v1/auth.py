from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from claude_py_scaffold.database import get_db
from claude_py_scaffold.exceptions import BadRequestException, UnauthorizedException
from claude_py_scaffold.models.user import User
from claude_py_scaffold.schemas import Token, UserCreate, UserResponse
from claude_py_scaffold.security import hash_password, verify_password
from claude_py_scaffold.token import create_access_token

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """用户注册"""
    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalar_one_or_none():
        raise BadRequestException("用户名已存在", error_code="USERNAME_EXISTS")

    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise BadRequestException("邮箱已被注册", error_code="EMAIL_EXISTS")

    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> dict:
    """用户登录"""
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedException("用户名或密码错误")

    if not user.is_active:
        raise UnauthorizedException("用户已被禁用")

    if not verify_password(form_data.password, user.password_hash):
        raise UnauthorizedException("用户名或密码错误")

    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=30),
    )

    return {"access_token": access_token, "token_type": "bearer"}
