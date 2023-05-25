from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from ..core.config import settings
from .base import AbstractDocStorage


class MongoDB(AbstractDocStorage):
    def __init__(self):
        self.mongo_client = AsyncIOMotorClient(
            settings.mongo_host, settings.mongo_port
        )
        self.mongo_db = self.mongo_client[settings.mongo_database]
        self.collection = self.mongo_db[settings.mongo_collection]

    async def get_aggregation(self, pipeline):
        await self.collection.aggregate(pipeline).to_list(length=None)

    async def get_one_object_from_db(
            self, index, doc_id: str, model: BaseModel
    ):
        pass

    async def get_objects_from_db(
            self, index, body: dict, model: BaseModel
    ):
        pass

    async def put_object_to_db(
            self, document: dict
    ):
        await self.collection.insert_one(document)

    async def delete_object_from_db(
            self, index, body: dict, model: BaseModel
    ):
        pass

    async def upgrade_object_in_db(
            self, index, body: dict, model: BaseModel
    ):
        pass


async def get_db_storage():
    return MongoDB()
