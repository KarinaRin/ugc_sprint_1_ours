import uuid
from datetime import datetime
from urllib.request import Request

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter()

bearer_token = HTTPBearer()


class UserTimestamp(BaseModel):
    movie_id: uuid.UUID
    timestamp: datetime


@router.post(
    '',
    summary='Сбор информации о просмотрах',
    description='Сбор информации о просмотре фильма,'
                'принимает id фильма и timestamp на котором завершился просмотр',
    response_description='Статус код',
)
async def view(
        user_content: UserTimestamp,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
):
    token = request.credentials
    '''
    какие то действия с токеном и кафкой
    '''
    return user_content.dict()


@router.get(
    '/{movie_id}',
    summary='Получение timestamp',
    description='На каком timestamp остановился пользователь, при просмотре фильма',
    response_description='Временная метка',
)
async def content(
        movies_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
):
    token = request.credentials
    '''
    какие то действия с токеном и кафкой
    '''
    return {'movie_id': movies_id}


@router.post(
    '/movies',
    summary='Получение timestamps для определенного количества фильмов',
    description='На каком timestamp остановился пользователь, при просмотре фильма',
    response_description='Временная метка для фильмов',
)
async def content(
        movies_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
):
    token = request.credentials
    '''
    какие то действия с токеном и кафкой
    '''
    return {'movie_id': movies_id}
