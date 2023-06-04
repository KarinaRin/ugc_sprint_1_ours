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


async def like_dislike(doc, user_email, type_field):
    update = {}
    field = f'review.' + type_field
    if user_email in doc['review'][type_field]:
        update['$pull'] = {field: user_email}
    else:
        update['$addToSet'] = {field: user_email}
    return update


class ReviewsService(BaseServiceUGC):
    async def change_review_or_create(self, film_id, user_email, text):
        query = {'film_id': film_id, 'email': user_email}
        present_data = await super().find_one_document(query)
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
        return await super().find_one_document(query)

    async def create_document(self, film_id, user_email, text):
        document = {
            'email': user_email,
            'film_id': film_id,
            'likes': None,
            'review': {
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
            field_name='email', field_value=user_email
        )
        result = await super().find_list_documents(query)
        if not result:
            return None
        return result

    async def get_reviews_to_film(self, film_id):
        query = pipeline_list_reviews('film_id', film_id)
        result = await super().find_list_documents(query)
        if not result:
            return None
        return result

    async def post_like_dislike(
            self, film_id, author_email, user_email, type_
    ):
        pipeline = pipeline_exist_review(film_id, author_email)
        doc = await super().find_one_document(pipeline)
        if not doc:
            return None

        if type_ == 'like':
            update = await like_dislike(doc, user_email, 'likes')
        else:
            update = await like_dislike(doc, user_email, 'dislikes')
        await super().update_one_document(doc, update)

        return await super().find_one_document(pipeline)


@lru_cache()
def get_reviews_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> ReviewsService:
    return ReviewsService(doc_db_storage)
