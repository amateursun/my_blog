# src/bootstrap/security.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext

from src.core.exceptions import TokenExpiredError, InvalidTokenError
from src.core.interfaces.services import HashServiceProtocol, TokenServiceProtocol


class HashPasswordRep(HashServiceProtocol):
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self._pwd_context.verify(plain, hashed)


class AuthServiceRep(TokenServiceProtocol):
    def __init__(self, secret_key: str, algorithm: str, expires_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_minutes = expires_minutes

    def create_access_token(self, data: dict) -> dict:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expires_minutes)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return {"access_token": token, "token_type": "bearer"}

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except JWTError:
            raise InvalidTokenError()