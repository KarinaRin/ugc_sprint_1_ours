from functools import lru_cache

from fastapi import Depends

from ..db.base import AbstractDocStorage
from ..db.mongo import get_db_storage
from .base_service_ugc import BaseServiceUGC


class LikesService(BaseServiceUGC):
    async def get_aggregation_likes_dislikes(self, pipeline):
        result = await super().get_aggregation(pipeline)

        if not result:
            return

        response = {
            'film_id': result[0]['_id']['film_id'],
            'likes': 0,
            'dislikes': 0
        }
        for item in result:
            if item['_id']['likes'] == 10:
                response['likes'] = item['count']
            elif item['_id']['likes'] == 0:
                response['dislikes'] = item['count']
        return response

    async def get_aggregation_average_rating(self, pipeline):
        result = await super().get_aggregation(pipeline)
        if not result:
            return
        return {
            'film_id': result[0]['_id']['film_id'],
            'average_movie_rating': result[0]['average_movie_rating']
        }

    async def change_like_or_create(self, query, user_content):
        present_data = await super().find_one_document(query)
        if present_data:
            new_data = {'$set': {"likes": user_content.like}}
            await super().update_one_document(present_data, new_data)
        else:
            document = {
                "email": user_content.email,
                "film_id": str(user_content.film_id),
                'likes': user_content.like,
                "review": {},
                'bookmark': False
            }
            await super().insert_one_document(document)
        return await super().find_one_document(query)


@lru_cache()
def get_likes_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> LikesService:
    return LikesService(doc_db_storage)
