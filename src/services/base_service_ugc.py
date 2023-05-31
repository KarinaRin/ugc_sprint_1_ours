from ..db.base import AbstractDocStorage


class BaseServiceUGC:
    def __init__(
            self,
            doc_db_storage: AbstractDocStorage
    ):
        self.db_storage = doc_db_storage

    async def insert_one_object(self, document: dict):
        await self.db_storage.put_object_to_db(document)
        return document

    async def get_aggregation(self, pipeline):
        return await self.db_storage.collection.aggregate(
            pipeline
        ).to_list(length=None)

    async def find_one_document(self, query: dict):
        document = await self.db_storage.get_one_object_from_db(query)
        return document

    async def update_one_document(self, present_data, new_data):
        await self.db_storage.update_object_in_db(
            present_data, new_data
        )

    async def insert_one_document(self, document):
        await self.db_storage.put_object_to_db(document)
