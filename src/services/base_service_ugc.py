from ..db.base import AbstractDocStorage


class BaseServiceUGC:
    def __init__(
            self,
            doc_db_storage: AbstractDocStorage
    ):
        self.db_storage = doc_db_storage

    async def insert_one_object(self, document: dict):
        await self.doc_db_storage.put_object_to_db(document)
        return document

    async def get_aggregation(self, pipeline):
        return await self.db_storage.collection.aggregate(
            pipeline
        ).to_list(length=None)
