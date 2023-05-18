from fastapi import Depends
from kafka import KafkaProducer
from redis.client import Redis

from src.db.kafka import get_kafka_producer
from src.db.redis import get_redis
from src.utils.utils import get_email_film_id, get_current_datetime


class Service:
    def __init__(self, redis: Redis, kafka_producer: KafkaProducer):
        self.redis = redis
        self.kafka_producer = kafka_producer

    async def get_timestamp(self, email: str, film_id: str) -> dict:
        email_film_id = get_email_film_id(email, film_id)
        timestamp = await self.redis.get_timestamp(email_film_id)
        return {'timestamp': timestamp}

    async def add_timestamp(self, email: str, user_content) -> dict:
        key = get_email_film_id(email, user_content.film_id)
        user_generated_content = f"{email}, {user_content.film_id}, {get_current_datetime()}, {user_content.timestamp}"
        await self.kafka_producer.send('user_film_timestamp', user_generated_content, key)
        return {'email': email,
                'film_id': user_content.film_id,
                'user_timestamp': user_content.timestamp}


def get_ugc_service(
        redis: Redis = Depends(get_redis),
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> Service:
    return Service(redis, kafka_producer)

