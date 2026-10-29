# -----------------------------------------------2.1--/core/entities/user.py
# src/core/entities/user.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int | None = None
    username: str = ""
    email: str = ""
    password: str = ""
    hash_password: str = ""
    is_active: bool = True
    is_deleted: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def is_valid_for_login(self) -> bool:
        """业务规则：能否登录"""
        return self.is_active and not self.is_deleted

