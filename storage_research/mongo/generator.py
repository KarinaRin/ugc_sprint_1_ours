
import time
from random import randint, choice, sample
from uuid import uuid4

from faker import Faker
from pymongo import MongoClient
from tqdm import tqdm

from src.core.config import settings

fake = Faker(locale="ru_RU")
fake.seed_instance(0)

USERS_COUNT = 100_000
MOVIES_COUNT = 2_000

CLEAN_DOC = {
    "film_id": '',
    "email": '',
    "likes": None,
    "review": {},
    "bookmark": False
}


def generate_doc():
    """"Генератор одной рецензии на фильм"""
    # client = AsyncIOMotorClient(
    #         settings.mongo_host, settings.mongo_port
    #     )
    # codec_options = pymongo.codec_options.CodecOptions(uuid_representation=bson.binary.STANDARD)
    client = MongoClient(
        settings.mongo_host, settings.mongo_port, connect=True,
        # codec_options=codec_options
    )
    mongo_db = client[settings.mongo_database]
    collection = mongo_db[settings.mongo_collection]
    collection.delete_many({})
    user_ids = list(set([fake.ascii_email() for _ in range(USERS_COUNT)]))
    film_ids = [str(uuid4()) for _ in range(MOVIES_COUNT)]
    for user in tqdm(user_ids):
        liking_films = set(sample(film_ids, randint(0, 10)))
        bookmarking_films = set(sample(film_ids, randint(0, 10)))
        bookmarking_films = bookmarking_films.difference(liking_films)
        gross = liking_films.union(bookmarking_films)
        like_bookmark_films = set(sample(film_ids, randint(0, 10)))
        like_bookmark_films = like_bookmark_films.difference(gross)
        gross = gross.union(like_bookmark_films)
        reviewing_films = set(sample(film_ids, randint(0, 20)))
        reviewing_films = reviewing_films.difference(gross)
        # list_docs = []
        for film in liking_films:
            doc = CLEAN_DOC.copy()
            doc['film_id'] = film
            doc['email'] = user
            doc['likes'] = choice([10, 0])
            # list_docs.append(doc)
            collection.insert_one(doc)
        for film in bookmarking_films:
            doc = CLEAN_DOC.copy()
            doc['film_id'] = film
            doc['email'] = user
            doc['bookmark'] = True
            # list_docs.append(doc)
            collection.insert_one(doc)
        for film in like_bookmark_films:
            doc = CLEAN_DOC.copy()
            doc['film_id'] = film
            doc['email'] = user
            doc['likes'] = choice([10, 0])
            doc['bookmark'] = True
            # list_docs.append(doc)
            collection.insert_one(doc)
        if randint(1, 100) >= 95:
            for film in reviewing_films:
                created = fake.date_between(start_date='-5y')
                doc = {
                    "film_id": film,
                    "email": user,
                    "likes": choice([10, 0]),
                    "review": {
                        "text": fake.text(max_nb_chars=randint(100, 1000)),
                        "created": time.mktime(created.timetuple()),
                        "likes": list(
                            set([choice(user_ids) for _ in
                                 range(randint(1, 40))])),
                        "dislikes": list(
                            set([choice(user_ids) for _ in
                                 range(randint(1, 40))]))
                    },
                    "bookmark": choice([True, False])
                }
                # list_docs.append(doc)
                collection.insert_one(doc)
        # if len(list_docs) > 0:
        #     collection.insert_many(list_docs)


if __name__ == '__main__':
    generate_doc()
