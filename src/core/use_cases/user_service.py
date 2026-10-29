# src/core/use_cases/user_service.py
from src.core.entities.user import User
from src.core.exceptions import (
    UsernameExistsError, EmailExistsError, AuthenticationError,
    InvalidTokenError, UserNotFoundError, AccountDisabledError,)
from src.core.interfaces.repositories import UserRepositoryProtocol
from src.core.interfaces.services import HashServiceProtocol, TokenServiceProtocol

# ---------- 用户服务 ----------
class UserService:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        hasher: HashServiceProtocol,
        token_service: TokenServiceProtocol,
    ):
        self.repo = repo
        self.hasher = hasher
        self.token_service = token_service

    # ---------- 注册 ----------
    def register_user(self, username: str, email: str, password: str) -> User:
        if self.repo.get_by_username(username):
            raise UsernameExistsError(username)
        if self.repo.get_by_email(email):
            raise EmailExistsError(email)

        user = User(
            username=username,
            email=email,
            hash_password=self.hasher.hash_password(password),
        )
        return self.repo.create(user)

    # ---------- 登录 ----------
    def login_user(self, username: str, password: str) -> dict:
        user = self.repo.get_by_username(username)
        if not user or not self.hasher.verify_password(password, user.hash_password):
            raise AuthenticationError("用户名或密码错误")
        if not user.is_active:
            raise AccountDisabledError()
        return self.token_service.create_access_token({"sub": str(user.id)})

    # ---------- Token 解析 ----------
    def get_current_user(self, token: str) -> User:
        payload = self.token_service.decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError()
        user = self.repo.get_by_id(int(user_id))
        if user is None:
            raise UserNotFoundError(int(user_id))
        return user

    def get_current_active_user(self, token: str) -> User:
        user = self.get_current_user(token)
        if not user.is_active:
            raise AccountDisabledError()
        return user


