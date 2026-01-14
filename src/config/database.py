# app/config/database.py
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.config import DatabaseSettings


class Database:
    def __init__(self) -> None:
        self._db_settings = DatabaseSettings()

        self.engine: AsyncEngine = create_async_engine(
            url=self._db_settings.connection_url,
            echo=self._db_settings.echo,
            pool_size=self._db_settings.pool_size,
            pool_pre_ping=self._db_settings.pool_pre_ping,
            pool_recycle=self._db_settings.pool_recycle,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_async_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            yield session

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[AsyncConnection]:
        async with self.engine.connect() as conn:
            yield conn
