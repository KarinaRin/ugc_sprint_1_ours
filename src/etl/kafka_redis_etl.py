import asyncio
import aiohttp
import logging

from src.core.config import settings

payload = {
    "name": "RedisSinkConnector1",
    "config": {
        "connector.class": "com.github.jcustenborder.kafka.connect.redis.RedisSinkConnector",
        "tasks.max": "1",
        "topics": "user_film_timestamp",
        "redis.hosts": "big_data_redis:6379",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter"
    }
}


async def create_connector():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(settings.kafka_connector, json=payload) as response:
                    logging.info(response.status)
                    logging.info(await response.text())
                    break
        except:
            await asyncio.sleep(1)
            logging.info('waiting kafka-connect')

    async with aiohttp.ClientSession() as session:
        async with session.post(settings.kafka_connector, json=payload) as response:
            logging.info(response.status)
            logging.info(await response.text())


if __name__ == '__main__':
    asyncio.run(create_connector())
