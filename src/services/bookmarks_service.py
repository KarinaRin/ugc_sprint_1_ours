from functools import lru_cache

from fastapi import Depends

from ..db.base import AbstractDocStorage
from ..db.mongo import get_db_storage
from .base_service_ugc import BaseServiceUGC


class BookmarksService(BaseServiceUGC):
    async def update_bookmark(self, film_id: str, user_email: str, bookmark_status: bool):
        query = {'film_id': str(film_id),
                 'email': user_email}
        present_data = await super().find_one_document(query)
        if present_data:
            new_data = {'$set': {"bookmark": bookmark_status}}
            await super().update_one_document(present_data, new_data)
        else:
            await self.create_document(film_id, user_email, bookmark_status)
        return await super().find_one_document(query)

    async def create_document(self, film_id, user_email, bookmark_status):
        document = {
            "email": user_email,
            "film_id": str(film_id),
            'likes': None,
            "review": {},
            'bookmark': bookmark_status
        }
        await super().insert_one_document(document)

    async def get_all_bookmarks(self, pipeline):
        result = await super().get_aggregation(pipeline)
        if not result:
            return None

        return [item['_id'] for item in result]


@lru_cache()
def get_bookmark_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> BookmarksService:
    return BookmarksService(doc_db_storage)
