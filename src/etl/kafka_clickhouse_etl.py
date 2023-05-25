from clickhouse_driver import Client


def create_kafka_clickhouse_etl():
    client = Client(host='localhost')
    create_kafka_engine = """
    CREATE TABLE IF NOT EXISTS user_film_timestamp_queue (
        email String,
        film_id String,
        time DateTime,
        timestamp Int32
    )
    ENGINE = Kafka
    SETTINGS kafka_broker_list = 'localhost:9092',
           kafka_topic_list = 'user_film_timestamp',
           kafka_group_name = 'user_film_timestamp_clickhouse',
           kafka_format = 'CSV',
           kafka_max_block_size = 1048576;
    """
    client.execute(create_kafka_engine)

    create_materialized_view = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS user_film_timestamp_queue_mv TO default.user_film_timestamp AS
        SELECT email, film_id, time, timestamp
        FROM user_film_timestamp_queue;
    """
    client.execute(create_materialized_view)

# TODO: fix

# from clickhouse_driver import Client
#
#
# def create_kafka_clickhouse_etl():
#     client = Client(host='clickhouse-node1')
#     create_kafka_engine = """
#     CREATE TABLE IF NOT EXISTS user_film_timestamp_queue (
#         email String,
#         film_id String,
#         time DateTime,
#         timestamp Int32
#     )
#     ENGINE = Kafka
#     SETTINGS kafka_broker_list = 'broker:29092',
#            kafka_topic_list = 'user_film_timestamp',
#            kafka_group_name = 'user_film_timestamp_clickhouse',
#            kafka_format = 'CSV',
#            kafka_max_block_size = 1048576;
#     """
#     client.execute(create_kafka_engine)
#
#     create_materialized_view = """
#         CREATE MATERIALIZED VIEW IF NOT EXISTS user_film_timestamp_queue_mv TO default.user_film_timestamp AS
#         SELECT email, film_id, time, timestamp
#         FROM user_film_timestamp_queue;
#     """
#     client.execute(create_materialized_view)
