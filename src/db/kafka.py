from typing import Optional

from kafka import KafkaProducer

from src.core.config import settings

NUM_SYMBOLS_IN_EMAIL = 7


class CustomKafkaProducer:
    def __init__(self, address):
        self.producer = KafkaProducer(
            bootstrap_servers=address,
            value_serializer=lambda x: x
        )

    def send(self, topic, value, key):
        self.producer.send(
            topic,
            value=value.encode(),
            key=key.encode()
        )

    def close(self):
        self.producer.close()


def get_kafka_producer() -> KafkaProducer:
    return CustomKafkaProducer([f'{settings.kafka_host}:{settings.kafka_port}'])
