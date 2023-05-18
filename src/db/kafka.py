from aiokafka import AIOKafkaProducer

from src.core.config import settings

NUM_SYMBOLS_IN_EMAIL = 7


class CustomKafkaProducer:
    def __init__(self, address):
        self.address = address

    async def send(self, topic, value, key):
        # have to define here, otherwise RuntimeError('There is no current event loop in thread %r.'
        # https://github.com/aio-libs/aiokafka/issues/689#issuecomment-739567831
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.address,
            value_serializer=lambda x: x
        )
        await self.producer.start()
        await self.producer.send_and_wait(
            topic,
            value=value.encode(),
            key=key.encode()
        )

    async def close(self):
        await self.producer.close()


def get_kafka_producer() -> AIOKafkaProducer:
    return CustomKafkaProducer([f'{settings.kafka_host}:{settings.kafka_port}'])
