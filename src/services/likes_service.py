from functools import lru_cache

from fastapi import Depends

from ..db.base import AbstractDocStorage
from .base_service_ugc import BaseServiceUGC
from ..db.mongo import get_db_storage


class LikesService(BaseServiceUGC):
    pass


@lru_cache()
def get_likes_service(
        doc_db_storage: AbstractDocStorage = Depends(get_db_storage),
) -> LikesService:
    return LikesService(doc_db_storage)
