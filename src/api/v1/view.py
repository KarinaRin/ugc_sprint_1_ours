import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from kafka import KafkaProducer
from redis.client import Redis
from src.db.kafka import get_kafka_producer
from src.db.redis import get_redis
from src.utils.auth_check import check_permission
from src.utils.utils import get_current_datetime, get_email_film_id

router = APIRouter()
bearer_token = HTTPBearer()


class UserTimestamp(BaseModel):
    film_id: uuid.UUID
    timestamp: int


@router.get(
    '/{film_id}',
    summary='Получение timestamp',
    description='На каком timestamp остановился пользователь, при просмотре фильма',
    response_description='Временная метка'
)
@check_permission(required_role=['admin', 'subscriber'])
async def content(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        redis: Redis = Depends(get_redis),
):
    email_film_id = get_email_film_id(request['email'], film_id)
    try:
        timestamp = redis.get_timestamp(email_film_id)
        return {'timestamp': timestamp}
    except Exception:
        return {'error': 'No available data for user with film id'}

@router.post(
    '',
    summary='Получение timestamps для определенного количества фильмов',
    description='На каком timestamp остановился пользователь, при просмотре фильма',
    response_description='Временная метка для фильмов',
)
@check_permission(required_role=['admin', 'subscriber'])
async def view(
        user_content: UserTimestamp,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
):
    key = get_email_film_id(request['email'], user_content.film_id)
    user_generated_content = f"{request['email']}, {user_content.film_id}, {get_current_datetime()}, {user_content.timestamp}"
    kafka_producer.send('user_film_timestamp', user_generated_content, key)
    return {
        'email': request['email'],
        'film_id': user_content.film_id,
        'user_timestamp': user_content.timestamp
    }
