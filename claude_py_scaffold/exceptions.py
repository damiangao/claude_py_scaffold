from typing import Any


class AppException(Exception):
    """应用异常基类"""

    def __init__(
        self,
        message: str = "操作失败",
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        data: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.data = data
        super().__init__(self.message)


class NotFoundException(AppException):
    """资源不存在"""

    def __init__(self, message: str = "资源不存在", error_code: str = "NOT_FOUND"):
        super().__init__(message=message, status_code=404, error_code=error_code)


class BadRequestException(AppException):
    """请求错误"""

    def __init__(self, message: str = "请求错误", error_code: str = "BAD_REQUEST"):
        super().__init__(message=message, status_code=400, error_code=error_code)


class UnauthorizedException(AppException):
    """未授权"""

    def __init__(self, message: str = "未授权", error_code: str = "UNAUTHORIZED"):
        super().__init__(message=message, status_code=401, error_code=error_code)


class ForbiddenException(AppException):
    """禁止访问"""

    def __init__(self, message: str = "禁止访问", error_code: str = "FORBIDDEN"):
        super().__init__(message=message, status_code=403, error_code=error_code)


class DuplicateException(AppException):
    """重复资源"""

    def __init__(self, message: str = "资源已存在", error_code: str = "DUPLICATE"):
        super().__init__(message=message, status_code=409, error_code=error_code)


class ValidationException(AppException):
    """验证错误"""

    def __init__(
        self,
        message: str = "验证失败",
        error_code: str = "VALIDATION_ERROR",
        details: Any = None,
    ):
        super().__init__(
            message=message, status_code=422, error_code=error_code, data=details
        )
