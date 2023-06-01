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
    async def change_review_or_create(self, film_id, user_id, text):
        pipeline = pipeline_exist_review(film_id, user_id)
        present_data = await super().find_one_document(pipeline)
        if present_data:  # если есть рецензия
            new_data = {
                '$set': {
                    'review.text': text,
                    'review.created':
                        int(time.mktime(date.today().timetuple()))
                }}
            await super().update_one_document(present_data, new_data)
        else:
            document = {
                "email": user_id,
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
        return await super().find_one_document(pipeline)

    async def get_reviews_from_user(self, user_id):
        query = pipeline_list_reviews(field_name="email", field_value=user_id)
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

    async def post_like_dislike(self, film_id, author_id, user_id, type):
        pipeline = pipeline_exist_review(film_id, author_id)
        present_data = await super().find_one_document(pipeline)
        if not present_data:
            return None
        update = {}
        if type == 'like':
            query = pipeline_count_review(
                film_id, author_id, 'likes', user_id
            )
            is_present = await super().count_objects(query)
            if is_present > 0:
                # Если email присутствует в массиве, удаляем его
                update['$pull'] = {'review.likes': user_id}
            else:
                # Если email отсутствует в массиве, добавляем его
                update['$addToSet'] = {'review.likes': user_id}
            await super().update_one_document(present_data, update)
        else:
            query = pipeline_count_review(
                film_id, author_id, 'dislikes', user_id
            )
            is_present = await super().count_objects(query)
            if is_present > 0:
                # Если email присутствует в массиве, удаляем его
                update['$pull'] = {'review.dislikes': user_id}
            else:
                # Если email отсутствует в массиве, добавляем его
                update['$addToSet'] = {'review.dislikes': user_id}
            await super().update_one_document(present_data, update)
        return await super().find_one_document(pipeline)


@lru_cache()
def get_reviews_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> ReviewsService:
    return ReviewsService(doc_db_storage)
