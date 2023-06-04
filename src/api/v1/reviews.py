import uuid
from enum import Enum
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.models.reviews import ReviewResponse
from src.services.reviews_service import get_reviews_service
from src.services.service import Service
from src.utils.auth_check import check_permission

router = APIRouter()
bearer_token = HTTPBearer()


@router.post(
    '/{film_id}',
    response_model=ReviewResponse,
    summary='Добавление или обновление рецензии к фильму',
    description='Добавление или обновление рецензии к фильму',
    response_description='Рецензия успешно добавлена'
)
@check_permission(required_role=['admin', 'subscriber'])
async def add_review(
        film_id: uuid.UUID,
        text: str = Body(),
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        review_service: Service = Depends(get_reviews_service),
):
    result = await review_service.change_review_or_create(
        film_id=str(film_id), user_email=request['email'], text=text
    )
    return ReviewResponse(**result)


@router.get(
    '/{film_id}/reviews',
    response_model=list[ReviewResponse],
    summary='Список рецензий на фильм',
    description='Список рецензий на открытый фильм',
    response_description='Список рецензий'
)
# @check_permission(required_role=['admin', 'subscriber'])
async def get_film_reviews(
        film_id: uuid.UUID,
        # request: HTTPAuthorizationCredentials = Depends(bearer_token),
        review_service: Service = Depends(get_reviews_service),
):
    result = await review_service.get_reviews_to_film(str(film_id))
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='У фильма нет рецензий'
        )
    return [ReviewResponse(**item) for item in result]


@router.get(
    '/',
    response_model=list[ReviewResponse],
    summary='Список рецензий от пользователя',
    description='Список рецензий от пользователя',
    response_description='Список рецензий'
)
@check_permission(required_role=['admin', 'subscriber'])
async def get_reviews(
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        review_service: Service = Depends(get_reviews_service),
):
    result = await review_service.get_reviews_from_user(request['email'])
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='нет рецензий')
    return [ReviewResponse(**item) for item in result]


class Choice(str, Enum):
    like = "like"
    dislike = "dislike"


@router.post(
    '/{film_id}/like_or',
    response_model=ReviewResponse,
    summary='Ваша оценка рецензии',
    description='Ваша оценка рецензии, посредством лайка-дизлайка',
    response_description='Отредактированный документ'
)
@check_permission(required_role=['admin', 'subscriber'])
async def get_reviews(
        film_id: uuid.UUID,
        type_: Choice,
        author_email: Optional[str] = Body(),
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        review_service: Service = Depends(get_reviews_service),
):
    if author_email == request['email']:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя ставить оценку самому себе'
        )
    result = await review_service.post_like_dislike(
        str(film_id), author_email, request['email'], type_)
    return ReviewResponse(**result)
