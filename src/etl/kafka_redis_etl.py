import asyncio
import aiohttp

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
                async with session.post('http://kafka-connect:8083/connectors', json=payload) as response:
                    print(response.status)
                    print(await response.text())
                    break
        except:
            await asyncio.sleep(1)
            print('waiting kafka-connect')


    async with aiohttp.ClientSession() as session:
        async with session.post('http://kafka-connect:8083/connectors', json=payload) as response:
            print(response.status)
            print(await response.text())


if __name__ == '__main__':
    asyncio.run(create_connector())
