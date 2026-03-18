from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    """用户创建请求"""

    username: str = Field(..., description="用户名", min_length=3, max_length=20)
    email: str = Field(..., description="邮箱")
    password: str = Field(..., description="密码", min_length=6)


class UserResponse(BaseModel):
    """用户响应"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    is_active: bool


class UserLogin(BaseModel):
    """用户登录请求"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class Token(BaseModel):
    """令牌响应"""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """令牌载荷"""

    sub: str | None = None
    exp: datetime | None = None
