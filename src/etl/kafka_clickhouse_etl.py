from asynch import connect
from asynch.cursors import DictCursor
import asyncio


async def create_kafka_clickhouse_etl():
    conn = await connect(
        host="clickhouse-node1",
        port=9000,
    )
    async with conn.cursor(cursor=DictCursor) as cursor:
        await cursor.execute('create database if not exists test')
        create_kafka_engine = """
        CREATE TABLE IF NOT EXISTS user_film_timestamp_queue (
            email String,
            film_id String,
            time DateTime,
            timestamp Int32
        )
        ENGINE = Kafka
        SETTINGS kafka_broker_list = 'broker:29092',
               kafka_topic_list = 'user_film_timestamp',
               kafka_group_name = 'user_film_timestamp_clickhouse',
               kafka_format = 'CSV',
               kafka_max_block_size = 1048576;
        """
        await cursor.execute(create_kafka_engine)

        create_materialized_view = """
            CREATE MATERIALIZED VIEW IF NOT EXISTS user_film_timestamp_queue_mv TO default.user_film_timestamp AS
            SELECT email, film_id, time, timestamp
            FROM user_film_timestamp_queue;
        """
        await cursor.execute(create_materialized_view)


if __name__ == '__main__':
    asyncio.run(create_kafka_clickhouse_etl())
