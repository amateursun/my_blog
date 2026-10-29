# -----------------------------------------------1.4--/core/exceptions.py
from typing import Any

class DomainError(Exception):
    """业务层异常基类"""
    def __init__(self, message: str, code: int | None = None):
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(DomainError):
    """资源未找到异常 404 """
    def __init__(self, source: str, identifier: Any):
        self.source = source
        self.identifier = identifier
        super().__init__(f"{source} 不存在: {identifier}")
class UserNotFoundError(NotFoundError):
    """用户未找到异常"""
    def __init__(self, username: str):
        super().__init__("用户", username)
class PostNotFoundError(NotFoundError):
    """帖子未找到异常"""
    def __init__(self, post_id: int):
        super().__init__("帖子", post_id)

class ConflictError(DomainError):
    """资源冲突异常 409 """
    pass
class EmailExistsError(ConflictError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"邮箱 {email} 已被注册")
class UsernameExistsError(ConflictError):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"用户名 {username} 已被注册")

class AuthError(DomainError):
    """认证与授权异常 401/403 """
    pass
class AuthenticationError(AuthError):
    def __init__(self, message: str = "用户名或密码错误"):
        super().__init__(message)
class InvalidTokenError(AuthError):
    def __init__(self):
        super().__init__("无效的访问令牌")
class TokenExpiredError(AuthError):
    def __init__(self):
        super().__init__("访问令牌已过期")
class AccountDisabledError(AuthError):
    def __init__(self):
        super().__init__("账号已被禁用，请联系管理员")
class PermissionDeniedError(DomainError):
    def __init__(self, message: str = "无权限执行此操作"):
        super().__init__(message)

class BusinessRuleError(DomainError):
    '''业务规则违反错误 400 '''
    pass
class InvalidOperationError(BusinessRuleError):
    def __init__(self, message: str):
        super().__init__(message)

class InfrastructureError(DomainError):
    '''基础设施错误 500 '''
    pass