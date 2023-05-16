from random import randint, choice
from uuid import uuid4

USERS_COUNT = 1_000_000
MOVIES_COUNT = 10_000
INIT_RECORDS_ALL = 10_000_000
INIT_RECORDS_CHUNK = 10_000

user_ids = [str(uuid4()) for _ in range(USERS_COUNT)]
movie_ids = [str(uuid4()) for _ in range(MOVIES_COUNT)]

CHUNKS = [100, 200, 500, 700, 1000, 1500, 2000, 3000, 4000, 5000, 6000,
          8000, 10000]


def gen_views(num: int) -> (
        list[tuple[str, str, int], None, None]
):
    return [(choice(user_ids),
             choice(movie_ids),
             randint(10_000, 30_000)) for _ in range(num)]
