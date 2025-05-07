
import redis.asyncio as redis

from typing import Any
from ..configs.settings import settings


class RedisCache:
    def __init__(self):
        self.redis = None

    async def initialize(self):
        if self.redis is None:
            self.redis = redis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                password=settings.REDIS_PASSWORD,
                encoding="utf-8",
                decode_responses=True
            )

        return self

    async def close(self):
        if self.redis is not None:
            await self.redis.close()

    async def ping(self):
        if self.redis is None:
            await self.initialize()
        return await self.redis.ping()

    async def get(self, key: str):
        if self.redis is None:
            await self.initialize()
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, expire: int = 60):
        if self.redis is None:
            await self.initialize()
        await self.redis.setex(key, expire, value)

    async def delete(self, key: str):
        if self.redis is None:
            await self.initialize()
        await self.redis.delete(key)
