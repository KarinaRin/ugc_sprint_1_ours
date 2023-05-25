from functools import lru_cache

from fastapi import Depends

from ..db.base import AbstractDocStorage
from ..db.mongo import get_db_storage
from .base_service_ugc import BaseServiceUGC


class LikesService(BaseServiceUGC):
    async def get_aggregation_likes_dislikes(self, pipeline):
        result = await super().get_aggregation(pipeline)

        response = None
        if result:
            response = {
                'film_id': result[0]['_id']['film_id'],
                'likes': 0,
                'dislikes': 0
            }
            for item in result:
                if item['_id']['likes'] == 10:
                    response['likes'] = item['count']
                else:
                    response['dislikes'] = item['count']
        return response

    async def get_aggregation_average_rating(self, pipeline):
        result = await super().get_aggregation(pipeline)
        response = None
        if result:
            response = {
                'film_id': result[0]['_id']['film_id'],
                'average_movie_rating': result[0]['average_movie_rating']
            }
        return response


@lru_cache()
def get_likes_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> LikesService:
    return LikesService(doc_db_storage)
