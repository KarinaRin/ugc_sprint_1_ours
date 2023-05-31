import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.v1.pipelines.bookmarks_pipeline import BookmarksPipline
from src.models.bookmark import BookmarkResponse, BookmarkResponseAll
from src.services.bookmarks_service import get_bookmark_service
from src.services.service import Service
from src.utils.auth_check import check_permission

router = APIRouter()
bearer_token = HTTPBearer()


@router.post(
    '/{film_id}',
    response_model=BookmarkResponse,
    summary='Добавление фильма в закладки',
    description='Добавление фильма в закладки',
    response_description='Фильм добавлен в закладки'
)
@check_permission(required_role=['admin', 'subscriber'])
async def add_bookmark(
        film_id: uuid.UUID,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        bookmark_service: Service = Depends(get_bookmark_service),
):
    result = await bookmark_service.update_bookmark(film_id=str(film_id),
                                                    user_email=request['email'],
                                                    bookmark_status=True)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='document not found'
        )
    return BookmarkResponse(**result)


@router.delete(
    '/{film_id}',
    response_model=BookmarkResponse,
    summary='Удаление фильма из закладок',
    description='Удаление фильма из закладок',
    response_description='Фильм удален из закладок'
)
@check_permission(required_role=['admin', 'subscriber'])
async def delete_bookmark(
        film_id: uuid.UUID,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        bookmark_service: Service = Depends(get_bookmark_service),
):
    result = await bookmark_service.update_bookmark(film_id=film_id,
                                                    user_email=request['email'],
                                                    bookmark_status=False)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='document not found'
        )
    return BookmarkResponse(**result)


@router.get(
    '',
    response_model=list[BookmarkResponseAll],
    summary='Все закладки пользователя',
    description='Получение всех закладок пользователя по фильмам',
    response_description='Список фильмов'
)
@check_permission(required_role=['admin', 'subscriber'])
async def get_user_bookmarks(
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        bookmark_service: Service = Depends(get_bookmark_service),
):
    pipeline = BookmarksPipline().all_user_bookmarks(request['email'])
    result = await bookmark_service.get_all_bookmarks(pipeline)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='document not found'
        )
    return [BookmarkResponseAll(**item) for item in result]
