from redis.asyncio import Redis

from src.core.config import settings


class CustomRedis:
    def __init__(self, host: str, port: int, db: int):
        self.redis = Redis(host=host, port=port, db=db)

    async def _get_message(self, key: str) -> str:
        message = await self.redis.get(key)
        return message.decode()

    async def get_timestamp(self, key: str) -> str:
        message = await self._get_message(key)
        return message.split(',')[3]


def get_redis() -> CustomRedis:
    return CustomRedis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db
    )
