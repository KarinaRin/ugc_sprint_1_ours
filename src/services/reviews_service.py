import time
from datetime import date
from functools import lru_cache

from fastapi import Depends

from .base_service_ugc import BaseServiceUGC
from ..api.v1.pipelines.reviews_pipeline import (
    pipeline_exist_review, pipeline_list_reviews, pipeline_count_review
)
from ..db.base import AbstractDocStorage
from ..db.mongo import get_db_storage


class ReviewsService(BaseServiceUGC):
    async def change_review_or_create(self, film_id, user_email, text):
        pipeline = pipeline_exist_review(film_id, user_email)
        present_data = await super().find_one_document(pipeline)
        if present_data:
            new_data = {
                '$set': {
                    'review.text': text,
                    'review.created':
                        int(time.mktime(date.today().timetuple()))
                }}
            await super().update_one_document(present_data, new_data)
        else:
            await self.create_document(film_id, user_email, text)
        return await super().find_one_document(pipeline)

    async def create_document(self, film_id, user_email, text):
        document = {
            "email": user_email,
            "film_id": film_id,
            'likes': None,
            "review": {
                'text': text,
                'created': int(time.mktime(date.today().timetuple())),
                'likes': [],
                'dislikes': []
            },
            'bookmark': False
        }
        await super().insert_one_document(document)

    async def get_reviews_from_user(self, user_email):
        query = pipeline_list_reviews(
            field_name="email", field_value=user_email
        )
        result = await super().find_list_documents(query)
        if not result:
            return None
        return result

    async def get_reviews_to_film(self, film_id):
        query = pipeline_list_reviews("film_id", film_id)
        result = await super().find_list_documents(query)
        if not result:
            return None
        return result

    async def post_like_dislike(
            self, film_id, author_email, user_email, type_
    ):
        pipeline = pipeline_exist_review(film_id, author_email)
        present_data = await super().find_one_document(pipeline)
        if not present_data:
            return None

        if type_ == 'like':
            await self.like_dislike(
                film_id, author_email, user_email, 'likes', present_data
            )
        else:
            await self.like_dislike(
                film_id, author_email, user_email, 'dislikes', present_data
            )
        return await super().find_one_document(pipeline)

    # TODO: надо починить
    async def like_dislike(
            self, film_id, author_email, user_email, type_field, present_data
    ):
        update = {}
        field = f'review.' + type_field
        print('9999999999999', field)
        pipeline = pipeline_exist_review(film_id, user_email)
        present_data = await super().find_one_document(pipeline)
        print(present_data)
        if present_data:
            # Если email присутствует в массиве, удаляем его
            update['$pull'] = {field: user_email}
        else:
            # Если email отсутствует в массиве, добавляем его
            update['$addToSet'] = {field: user_email}
        await super().update_one_document(present_data, update)


@lru_cache()
def get_reviews_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> ReviewsService:
    return ReviewsService(doc_db_storage)
