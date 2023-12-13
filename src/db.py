from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users.models import UP
from sqlalchemy import DateTime, Enum, Integer, String, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import db_settings

DATABASE_URL = db_settings.url


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    surname: Mapped[str] = mapped_column(String(length=255), nullable=True)
    phone: Mapped[str] = mapped_column(String(length=20), nullable=True)
    tg_chat_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    role: Mapped[str] = mapped_column(
        Enum("admin", "master", "client", name="user_role"),
        nullable=False, default="client",
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=True,
    )
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(),
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("(now() at time zone 'utc')"),
    )


class CustomUserDatabase(SQLAlchemyUserDatabase[UP, str]):

    async def get_by_email(self, username: str) -> User | None:
        statement = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(statement)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomUserDatabase(session, User)
