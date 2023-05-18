from typing import Optional

from redis.asyncio import Redis

from src.core.config import settings


class CustomRedis:
    def __init__(self, host, port, db):
        self.redis = Redis(host=host, port=port, db=db)

    async def _get_message(self, key):
        message = await self.redis.get(key)
        return message.decode()

    async def get_timestamp(self, key):
        message = await self._get_message(key)
        return message.split(',')[3]


def get_redis() -> Redis:
    return CustomRedis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
