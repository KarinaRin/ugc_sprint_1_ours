from clickhouse_driver import Client
from tqdm import tqdm

from service.common import gen_views, INIT_RECORDS_CHUNK, INIT_RECORDS_ALL

INSERT_QUERY = (
    'INSERT INTO research.views (user_id, movie_id, timestamp) VALUES'
)


def init_db(client):
    client.execute('CREATE DATABASE IF NOT EXISTS research')
    client.execute('DROP TABLE IF EXISTS research.views')
    client.execute(
        '''
        CREATE TABLE IF NOT EXISTS research.views (
            user_id UUID,
            movie_id UUID,
            timestamp UInt32
        ) ENGINE = MergeTree()
        ORDER BY (user_id, movie_id);
        '''
    )


def write_to_bd(client,
                chunk: int = INIT_RECORDS_CHUNK,
                total_size: int = INIT_RECORDS_ALL):
    for _ in tqdm(range(1, total_size, chunk), desc='Загрузка в Clickhouse'):
        client.execute(INSERT_QUERY, gen_views(chunk))


if __name__ == '__main__':
    client = Client(host='localhost')
    init_db(client)
    write_to_bd(client)
