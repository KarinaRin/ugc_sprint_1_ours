import csv
import logging
from random import randint, choice
from typing import Generator
from uuid import uuid4

from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from tqdm import tqdm

logger = logging.getLogger(__name__)

client = Client(host='localhost')

USERS_COUNT = 1_000_000
MOVIES_COUNT = 10_000
INSERT_QUERY = (
    'INSERT INTO research.views (user_id, movie_id, timestamp) VALUES'
)

user_ids = [str(uuid4()) for _ in range(USERS_COUNT)]
movie_ids = [str(uuid4()) for _ in range(MOVIES_COUNT)]


def gen_views(num: int) -> (
        Generator[tuple[str, str, int], None, None]
):
    return ((choice(user_ids),
             choice(movie_ids),
             randint(10_000, 30_000)) for _ in range(num))


def write_to_file(chunk: int = 10_000, total_size: int = 10_000_000):
    with open('data.csv', mode='w') as file:
        writer = csv.writer(file)
        headers = ['user_id', 'movie_id', 'timestamp']
        writer.writerow(headers)

        for _ in tqdm(range(1, total_size, chunk),
                      desc='Загрузка в Clickhouse'):
            writer.writerows(gen_views(chunk))


def write_to_bd(chunk: int = 10_000, total_size: int = 10_000_000):
    for _ in tqdm(range(1, total_size, chunk), desc='Загрузка в Clickhouse'):
        try:
            client.execute(INSERT_QUERY, gen_views(chunk))
        except Error as error:
            logger.error(f'Ошибка загрузки данных: {error}')


if __name__ == "__main__":
    write_to_bd()
