# from typing import Optional
#
# from redis.client import Redis
#
# from src.core.config import settings
#
# redis: Optional[Redis] = Redis(
#     host=f'{settings.redis_host}',
#     port=settings.redis_port
# )
#
#
# class CustomRedis:
#     def __init__(self, host, port, db):
#         self.redis = Redis(host=host, port=port, db=db)
#
#     def _get_message(self, key):
#         return self.redis.get(key).decode()
#
#     def get_timestamp(self, key):
#         return self._get_message(key).split(',')[3]
