from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from claude_py_scaffold.database import get_db
from claude_py_scaffold.exceptions import UnauthorizedException
from claude_py_scaffold.models.user import User
from claude_py_scaffold.token import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """获取当前登录用户"""
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedException("无效的令牌")

    user_id: str = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("无效的令牌")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise UnauthorizedException("用户不存在")

    if not user.is_active:
        raise UnauthorizedException("用户已被禁用")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
