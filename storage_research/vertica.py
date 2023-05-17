from uuid import uuid4

import vertica_python
from tqdm import tqdm

from service.common import (
    gen_views, INIT_RECORDS_CHUNK, INIT_RECORDS_ALL,
    USERS_COUNT, MOVIES_COUNT
)

CONN_INFO = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'VMart',
    'autocommit': True,
    # 'use_prepared_statements': True,
}

QUERY = """
INSERT INTO views (user_id, movie_id, timestamp) VALUES (%s,%s, %s)
"""

user_ids = [str(uuid4()) for _ in range(USERS_COUNT)]
movie_ids = [str(uuid4()) for _ in range(MOVIES_COUNT)]


def init_db(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS views (
        user_id VARCHAR(36) NOT NULL,
        movie_id VARCHAR(36) NOT NULL,
        timestamp INTEGER NOT NULL
        )
        ORDER BY user_id, movie_id;
        """
    )


def write_to_bd(cursor,
                chunk: int = INIT_RECORDS_CHUNK,
                total_size: int = INIT_RECORDS_ALL):
    for _ in tqdm(range(1, total_size, chunk), desc='Загрузка в Vertica'):
        values = gen_views(chunk)
        cursor.executemany(QUERY, values, use_prepared_statements=False)


if __name__ == '__main__':
    with vertica_python.connect(**CONN_INFO) as connection:
        cursor = connection.cursor()
        init_db(cursor)
        write_to_bd(cursor)
