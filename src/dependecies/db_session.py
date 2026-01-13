from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import Database


database = Database()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with database.get_async_session() as session:
        yield session
