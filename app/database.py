from typing import AsyncIterator

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import (
    PG_DB,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
    REDIS_HOST,
    REDIS_PORT,
)

DATABASE_URL_ASYNC = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

async_engine = create_async_engine(DATABASE_URL_ASYNC)


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(async_engine)

    async with async_session() as session:
        yield session


async def get_redis_session() -> AsyncIterator[redis.Redis]:
    async with redis.from_url(REDIS_URL) as session:
        yield session
