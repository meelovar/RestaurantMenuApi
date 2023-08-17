import json
from typing import Any

import redis.asyncio as redis
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.database import get_redis_session


class RedisCache:
    def __init__(self, session: redis.Redis = Depends(get_redis_session)):
        self.__session = session
        self.__ttl = 700

    async def get(self, key: str) -> Any | None:
        data = await self.__session.get(key)
        result = json.loads(data) if data else None

        return result

    async def set(self, key: str, value: Any) -> None:
        data = json.dumps(jsonable_encoder(value))

        await self.__session.setex(key, self.__ttl, data)

    async def delete(self, *patterns: str) -> None:
        for pattern in patterns:
            async for key in self.__session.scan_iter(pattern):
                await self.__session.delete(key)
