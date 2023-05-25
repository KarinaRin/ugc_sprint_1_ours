from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.likes_service import get_likes_service
from src.services.service import Service, get_ugc_service
from src.utils.auth_check import check_permission

router = APIRouter()
bearer_token = HTTPBearer()

#155-15-515
@router.get(
    '/likes-dislikes-statistics',
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
    pipeline = [
        # Matchn the documents possible
        {"$match": {"film_id": film_id, "likes": {"$ne": None}}},

        # # Group the documents and "count" via $sum on the values
        {"$group": {
            "_id": {
                "film_id": "$film_id",
                "likes": "$likes"
            },
            'count': {"$sum": 1},
        }}
    ]

    return await like_service.get_aggregation(pipeline)


@router.get(
    '/average-rating',
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
    pipeline = [
        # Matchn the documents possible
        {"$match": {"film_id": film_id}},

        # # Group the documents and "count" via $sum on the values
        {"$group": {
            "_id": {
                "film_id": "$film_id",
            },
            'average_movie_rating': {"$avg": "$likes"}
        }}
    ]

    return await like_service.get_aggregation(pipeline)