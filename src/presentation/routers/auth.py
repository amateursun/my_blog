# src/presentation/routers/auth.py
from fastapi import APIRouter, Depends

from src.presentation.schemas.user import UserRegister, UserLogin, UserOut
from src.core.use_cases.user_service import UserService
from src.bootstrap.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserRegister, service: UserService = Depends(get_user_service)):
    return service.register_user(data.username, data.email, data.password)


@router.post("/login")
def login(data: UserLogin, service: UserService = Depends(get_user_service)):
    return service.login_user(data.username, data.password)

