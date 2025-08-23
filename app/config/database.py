from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import pyodbc
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


if TYPE_CHECKING:
    from src.settings import DatabaseSettings


class Database:
    def init(self, db_settings: "DatabaseSettings") -> None:
        pyodbc.pooling = False
        self._db_settings = db_settings
        self.engine: AsyncEngine = create_async_engine(
            url=db_settings.connection_url,
            echo=db_settings.echo,
            pool_size=db_settings.pool_size,
            pool_pre_ping=db_settings.pool_pre_ping,
            pool_recycle=db_settings.pool_recycle,
        )

    async def get_connection(self) -> AsyncConnection:
        async with self.engine.connect() as conn:
            return conn

    @asynccontextmanager
    async def get_async_session(self):
        async with AsyncSession(self.engine) as session:
            yield session