import random
import string
import uuid
from datetime import datetime
from urllib.request import Request

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from kafka import KafkaProducer
from redis.client import Redis
from src.db.kafka import get_kafka_producer
from src.db.redis import get_redis

router = APIRouter()


class UserTimestamp(BaseModel):
    movie_id: uuid.UUID
    timestamp: datetime


NUM_SYMBOLS_IN_EMAIL = 10

def create_kafka_test_data():
    # Итерируем timestamp просмотра
    timestamp = 0
    while True:
        timestamp += 1
        # Создаем случайный ключ (в конце запятая обязательна!)
        email = ''.join(random.choices(
            string.ascii_uppercase, k=NUM_SYMBOLS_IN_EMAIL)
        ) + '@mail.com'
        film_id = str(uuid.uuid4())
        key = email + film_id + ','
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_generated_content = f'{email}, {film_id}, "{current_time}", {timestamp}'
        yield user_generated_content, key


@router.get(
    '/{email_movie_id}',
    summary='Получение timestamp',
    description='На каком timestamp остановился пользователь, при просмотре фильма',
    response_description='Временная метка'
)
async def content(
        email_movie_id: str,
        redis: Redis = Depends(get_redis),
):
    timestamp = redis.get_timestamp(email_movie_id)
    return {'timestamp': timestamp}


@router.post(
    '',
    summary='Получение timestamps для определенного количества фильмов',
    description='На каком timestamp остановился пользователь, при просмотре фильма',
    response_description='Временная метка для фильмов',
)
async def content(
        movies_id: str,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),

):
    for user_generated_content, email_movie_id in create_kafka_test_data():
    # Отправляем данные в кафку
        kafka_producer.send('user_film_timestamp', user_generated_content, email_movie_id)
        return {'email_movie_id': email_movie_id}
