from motor.motor_asyncio import AsyncIOMotorClient

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
        return await self.collection.aggregate(pipeline).to_list(length=None)

    async def get_one_object_from_db(self, query):
        return await self.collection.find_one(query)

    async def get_objects_from_db(self, query):
        documentes_gen = self.collection.find(query)
        documentes = []
        async for doc in documentes_gen:
            documentes.append(doc)
        return documentes

    async def put_object_to_db(self, document: dict):
        await self.collection.insert_one(document)

    async def delete_object_from_db(self):
        pass

    async def update_object_in_db(self, present_data, new_data):
        await self.collection.update_one(present_data, new_data)

    async def count_filtered_objects_in_db(self, query):
        await self.collection.count_documents(query)


async def get_db_storage():
    return MongoDB()
