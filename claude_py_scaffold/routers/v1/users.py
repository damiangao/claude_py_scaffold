from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from claude_py_scaffold.database import get_db
from claude_py_scaffold.deps import CurrentUser
from claude_py_scaffold.exceptions import NotFoundException
from claude_py_scaffold.models.user import User
from claude_py_scaffold.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser) -> User:
    """获取当前用户信息"""
    return current_user


@router.get("/", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)) -> List[User]:
    """获取用户列表"""
    result = await db.execute(select(User))
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> User:
    """获取单个用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("用户不存在")

    return user
