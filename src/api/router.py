from fastapi import APIRouter

from src.schemas.users import UserCreate, UserRead, UserUpdate
from src.users import auth_backend, fastapi_users

api_router = APIRouter()

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'],
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
api_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)
api_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth'],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
