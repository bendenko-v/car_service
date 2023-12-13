import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from src.config import settings
from src.db import CustomUserDatabase, User, get_user_db

SECRET = settings.SECRET_KEY


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")  # noqa: T201

    async def on_after_forgot_password(
            self, user: User, token: str, request: Request | None = None,
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")  # noqa: T201

    async def on_after_request_verify(
            self, user: User, token: str, request: Request | None = None,
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")  # noqa: T201


async def get_user_manager(user_db: CustomUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)