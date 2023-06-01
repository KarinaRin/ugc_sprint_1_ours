from abc import ABC, abstractmethod


class AbstractDocStorage(ABC):
    @abstractmethod
    async def get_aggregation(self, pipeline):
        pass

    @abstractmethod
    async def get_one_object_from_db(self, *args):
        pass

    @abstractmethod
    async def get_objects_from_db(self, *args):
        pass

    @abstractmethod
    async def put_object_to_db(self, *args):
        pass

    @abstractmethod
    async def delete_object_from_db(self, *args):
        pass

    @abstractmethod
    async def update_object_in_db(self, *args):
        pass

    @abstractmethod
    async def count_filtered_objects_in_db(self, *args):
        pass
