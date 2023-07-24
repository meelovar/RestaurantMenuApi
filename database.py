from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    Session,
)

from config import (
    PG_DB,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
)

DATABASE_URL_ASYNC = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

async_engine = create_async_engine(DATABASE_URL_ASYNC)


async def get_async_session() -> Session:
    async_session = async_sessionmaker(async_engine)

    async with async_session() as session:
        yield session
