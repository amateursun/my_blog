# FastAPI 依赖函数(函数显式调用); 其他方式: 依赖容器container(高级用法)

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.bootstrap.config import settings
from src.bootstrap.database import get_db
from src.data.repositories.user_repository import SqlalchemyUserRep
from src.data.repositories.post_repository import SqlalchemyPostRep
from src.data.repositories.tag_repository import SqlalchemyTagRep
from src.data.repositories.comment_repository import SqlalchemyCommentRep
from src.bootstrap.security import HashPasswordRep, AuthServiceRep
from src.core.use_cases.user_service import UserService
from src.core.use_cases.post_service import PostService
from src.core.use_cases.tag_service import TagService
from src.core.use_cases.comment_service import CommentService
from src.core.entities.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")
 
def get_user_repo(db: Session = Depends(get_db)) -> SqlalchemyUserRep:
    return SqlalchemyUserRep(db)
 
def get_hasher() -> HashPasswordRep:
    return HashPasswordRep()
 
def get_token_service() -> AuthServiceRep:
    return AuthServiceRep(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

def get_user_service(
    repo: SqlalchemyUserRep = Depends(get_user_repo),
    hasher: HashPasswordRep = Depends(get_hasher),
    token_service: AuthServiceRep = Depends(get_token_service),) -> UserService:
    return UserService(repo=repo, hasher=hasher, token_service=token_service)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),) -> User:
    return service.get_current_user(token)

async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),) -> User:
    return service.get_current_active_user(token)

def get_post_repo(db: Session = Depends(get_db)) -> SqlalchemyPostRep:
    return SqlalchemyPostRep(db)

def get_post_service(
    post_repo: SqlalchemyPostRep = Depends(get_post_repo),
    user_repo: SqlalchemyUserRep = Depends(get_user_repo),
) -> PostService:
    return PostService(post_repo=post_repo, user_repo=user_repo)

def get_tag_repo(db: Session = Depends(get_db)) -> SqlalchemyTagRep:
    return SqlalchemyTagRep(db)


def get_comment_repo(db: Session = Depends(get_db)) -> SqlalchemyCommentRep:
    return SqlalchemyCommentRep(db)


def get_tag_service(repo: SqlalchemyTagRep = Depends(get_tag_repo)) -> TagService:
    return TagService(repo=repo)


def get_comment_service(
    comment_repo: SqlalchemyCommentRep = Depends(get_comment_repo),
    post_repo: SqlalchemyPostRep = Depends(get_post_repo),
) -> CommentService:
    return CommentService(comment_repo=comment_repo, post_repo=post_repo)

# ----------------------------------------------------
# utils
#-----------------------------------------------------
import re
def slugify(text: str) -> str:
    """将标题转为 URL 友好的 slug"""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")
    return slug or "untitled"

