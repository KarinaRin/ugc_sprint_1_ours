from clickhouse_driver import Client

client = Client(host='localhost')

create_kafka_engine = """
CREATE TABLE IF NOT EXISTS readings_queue (
    email String,
    film_id String,
    time DateTime,
    timestamp Int32
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'broker:29092',
       kafka_topic_list = 'readings',
       kafka_group_name = 'readings_consumer_group1',
       kafka_format = 'CSV',
       kafka_max_block_size = 1048576;
"""
client.execute(create_kafka_engine)

create_materialized_view = """
    CREATE MATERIALIZED VIEW readings_queue_mv TO default.readings AS
    SELECT email, film_id, time, timestamp
    FROM readings_queue;
"""
client.execute(create_materialized_view)

