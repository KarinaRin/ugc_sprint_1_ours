from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.v1.pipelines.likes_pipeline import LikesPipline
from src.models.likes import (FilmAverageRatingResponse,
                              FilmLikesDislikesResponse)
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
    response_description='Количество лайков и дизлайков'
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
    summary='Получение лайков и дизлайков',
    description='Вывод количество лайков и дизлайков',
    response_description='Количество лайков и дизлайков'
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