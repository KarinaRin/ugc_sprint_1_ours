import uuid

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from src.services.service import Service, get_ugc_service
from src.utils.auth_check import check_permission

router = APIRouter()
bearer_token = HTTPBearer()


class UserTimestamp(BaseModel):
    film_id: uuid.UUID
    timestamp: int


@router.get(
    '/{film_id}',
    summary='Получение timestamp',
    description='На каком timestamp остановился пользователь, смотря фильм',
    response_description='Временная метка'
)
@check_permission(required_role=['admin', 'subscriber'])
async def content(
        film_id: uuid.UUID,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        ugc_service: Service = Depends(get_ugc_service),
) -> dict:
    try:
        return await ugc_service.get_timestamp(request['email'], str(film_id))
    except Exception:
        return {'error': f'No available data for user with email '
                         f'{request["email"]} with film id = {str(film_id)}'
                }


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
        ugc_service: Service = Depends(get_ugc_service),
) -> dict:
    return await ugc_service.add_timestamp(request['email'], user_content)
