from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.v1.pipelines.likes_pipeline import LikesPipline
from src.models.likes import (FilmAverageRatingResponse,
                              FilmLikesDislikesResponse,
                              LikeChangeModel)
from src.services.likes_service import get_likes_service
from src.services.service import Service
from src.utils.auth_check import check_permission

router = APIRouter()
bearer_token = HTTPBearer()


@router.get(
    '/likes-dislikes-statistics',
    response_model=FilmLikesDislikesResponse,
    summary='Получение лайков и дизлайков',
    description='Вывод количество лайков и дизлайков',
    response_description='ID фильма и количество лайков и дизлайков'
)
@check_permission(required_role=['admin', 'subscriber'])
async def likes_dislikes_statistics(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        like_service: Service = Depends(get_likes_service),
):
    pipeline = LikesPipline().likes_dislikes_pipeline(film_id)
    result = await like_service.get_aggregation_likes_dislikes(pipeline)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='document not found'
        )
    return FilmLikesDislikesResponse(**result)


@router.get(
    '/average-rating',
    response_model=FilmAverageRatingResponse,
    summary='Получение среднего значения рейтинга',
    description='Вывод среднего значения рейтинга',
    response_description='ID фильма и среднее значение рейтинга'
)
@check_permission(required_role=['admin', 'subscriber'])
async def get_average_rating(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        like_service: Service = Depends(get_likes_service),
):
    pipeline = LikesPipline().average_rating_pipeline(film_id)
    result = await like_service.get_aggregation_average_rating(pipeline)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='document not found'
        )
    return FilmAverageRatingResponse(**result)


@router.post(
    '/change-like',
    summary='',
    description='',
    response_description=''
)
@check_permission(required_role=['admin', 'subscriber'])
async def change_like(
        user_content: LikeChangeModel,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        like_service: Service = Depends(get_likes_service),
):
    query = {"film_id": user_content.film_id,
             "email": request['email']}

    user_info = {}
    user_info['email'] = request['email']
    user_info['film_id'] = user_content.film_id
    user_info['like'] = user_content.like

    result = await like_service.change_like_or_create(
        query,
        user_info
    )
    del result['_id']
    print('aaaaaaaaaaaaaaaaaaaaaaa', result)
    return result
