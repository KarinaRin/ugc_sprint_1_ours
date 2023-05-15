from src.db.base import AbstractQueueStorage


class KafkaProducer(AbstractQueueStorage):
    pass


async def get_db_storage() -> KafkaProducer:
    return KafkaProducer()
