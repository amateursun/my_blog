# src/presentation/routers/users.py
from fastapi import APIRouter, Depends

from src.presentation.schemas.user import UserOut
from src.core.entities.user import User
from src.bootstrap.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

