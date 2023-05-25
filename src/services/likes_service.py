from datetime import datetime
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

    async def change_like_or_create(self, query, like):
        print('22222222222', query)
        present_data = await super().find_one_document(query)
        print('111111111111', present_data)
        if present_data:
            new_data = {'$set': {"likes": like}}
            await super().update_one_document(present_data, new_data)
        else:
            document = {
                "doc_id": "00110-45-678",
                "user_id": "001110-13-518",
                "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                'likes': like,
                "review": {
                    "review_id": "20221-32221-0515",
                    "text": "this was bad!",
                    'date': datetime.utcnow(),
                    'author': 'test@test.com',
                    'likes': ['test3@test.com', 'test4@test.com'],
                    'dislikes': ['test0@test.com', 'test5@test.com']
                },
                'bookmark': True
            }
            await super().insert_one_document(document)

@lru_cache()
def get_likes_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> LikesService:
    return LikesService(doc_db_storage)
