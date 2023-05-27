"""
При инициализации были загружены:
1. 100 000 резенций (на каждый фильм в среднем по 10 рецензий) с лайками
2. 10 000 000 лайков/дизлайков к фильмам (по 10 в среднем от 1 юзера)
3. 5 000 000 закладок (по 5 фильмов в закладках на каждого юзера)
"""

import time
from random import randint, choice
from typing import Callable
from uuid import uuid4

from faker import Faker
from pymongo import MongoClient
from tqdm import tqdm

from mongo_vs_postgres.common import MOVIES_COUNT, USERS_COUNT, MONGO_HOST, \
    MONGO_PORT, MONGO_DB

fake = Faker(locale="ru_RU")
fake.seed_instance(0)

user_ids = [fake.ascii_email() for _ in range(USERS_COUNT)]
film_ids = [str(uuid4()) for _ in range(MOVIES_COUNT)]


def generate_review_doc():
    """"Генератор одной рецензии на фильм"""
    created = fake.date_between(start_date='-5y')
    modify = fake.date_between(start_date=created)
    review = {
        "review_id": str(uuid4()),
        "film_id": choice(film_ids),
        "author": choice(user_ids),
        "author_name": fake.first_name() + " " + fake.last_name(),
        "text_review": fake.text(max_nb_chars=randint(100, 1000)),
        "created": time.mktime(created.timetuple()),
        "modify": time.mktime(modify.timetuple()),
        "author_score": round(randint(10, 100) / 10, 1),
        "likes": list(
            set([choice(user_ids) for _ in range(randint(1, 20))])),
        "dislikes": list(
            set([choice(user_ids) for _ in range(randint(1, 20))]))
    }
    return review


def generate_like_doc():
    """Генератор одного лайка или дизлайка"""
    return {
        "user_id": choice(user_ids),
        "film_id": choice(film_ids),
        "type": choice([10, 0]),
        "date": fake.date_time_between(start_date='-5y'),
    }


def generate_bookmark_doc():
    """Генератор закладки на фильм"""
    d = fake.date_between(start_date='-5y')
    return {
        "user_id": choice(user_ids),
        "film_id": choice(film_ids),
        "date": time.mktime(d.timetuple()),
    }


# def generator_list_docs(func: Callable, chunk: int):
#     """Генератор пакета данных"""
#     return [func() for _ in range(chunk)]


def load_collection():
    """ Вставка документов в коллекции """
    coll_set = [
        ('bookmarks', 5_000_000, generate_bookmark_doc),
        ('reviews', 100_000, generate_review_doc),
        ('likes', 10_000_000, generate_like_doc),
    ]
    chunk = 5000

    client = MongoClient(MONGO_HOST, MONGO_PORT, connect=True)
    db = client[MONGO_DB]

    for name, count_docs, generate_func in coll_set:
        collection = db.get_collection(name)
        collection.delete_many({})
        for _ in tqdm(
                range(1, count_docs, chunk),
                desc=f'"{name.upper()}": загрузка {count_docs} партиями по {chunk} документов'
        ):
            collection.insert_many([generate_func() for _ in range(chunk)])


if __name__ == '__main__':
    load_collection()
