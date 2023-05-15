from abc import ABC, abstractmethod


class AbstractQueueStorage(ABC):
    @abstractmethod
    async def put_event_to_db(self, *args):
        pass

    @abstractmethod
    async def get_event_from_db(self, *args):
        pass
