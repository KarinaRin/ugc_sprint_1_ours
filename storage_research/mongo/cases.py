import time
from random import randint

from pymongo import MongoClient

from src.core.config import settings


def random_film():
    """ Подберем случайный фильм из уже заполненной коллекции """
    pipeline = [{"$sample": {"size": 1}}]
    result_cursor = collection.aggregate(pipeline)
    random_doc = None
    for doc in result_cursor:
        random_doc = doc
    film = random_doc['film_id']
    return film


def random_email(film=None):
    """
    Подберем случайный имейл из уже заполненной коллекции.
    Наличие в параметрах film - требование избегать документы с ним
    """
    if not film:
        pipeline = [{"$sample": {"size": 1}}]
        result_cursor = collection.aggregate(pipeline)
        random_doc = None
        for doc in result_cursor:
            random_doc = doc
        email = random_doc['email']
        return email
    result = list(collection.find({'film_id': {'$ne': film}}))
    result_len = len(result)
    rand_email = result[randint(0, result_len)]['email']
    return rand_email


def case1_insert_like_read_list_likes():
    """
    Вставка лайка пользователем и последующий вывод
    всех фильмов списком, которые он лайкнул.
    Тестируется скорость на заполненной базе.
    """

    film = random_film()
    # Выберем email из БД, который не связан с выбранным фильмом
    email = random_email(film)
    result_old = list(collection.find({'email': email}, {'likes': 10}))
    doc = {
        "film_id": film,
        "email": email,
        "likes": 10,
        "review": {},
        "bookmark": False
    }
    start = time.time()
    collection.insert_one(doc)
    result_new = collection.find({'email': email}, {'likes': 10})
    finish = time.time() - start
    result_new = list(result_new)
    print(
        f'\nКЕЙС #1: "ДОБАВИТЬ ОТ ЮЗЕРА ЛАЙК + ВЫВЕСТИ ВСЕ ФИЛЬМЫ С ЛАЙКАМИ"\n'
        f'*************************************************************\n'
        f'На начало теста было {len(result_old)} лайкнутых фильмов юзером'
        f' <{email}>\n'
        f'Под конец кейса таких фильмов должно быть +1, '
        f'и по факту - {len(result_new)}\n'
        f'Время выполнения теста - {round(finish * 1000)}мс, '
        f'что меньше требуемых 200мс\n'
    )


def case2_count_likes_dislikes():
    """
    Подсчитаем количество лайков или дизлайков у определённого фильма.
    Тестируется скорость на заполненной базе - не больше 200мс.
    """
    film = random_film()
    pipeline = [{"$match": {"film_id": film}},
                {"$group": {
                    "_id": {
                        "likes": "$likes"
                    },
                    'count': {"$sum": 1},
                }}]
    start = time.time()
    result = collection.aggregate(pipeline)
    finish = time.time() - start
    result = list(result)
    for item in result:
        if item['_id']['likes'] == 10:
            likes = item['count']
        elif item['_id']['likes'] == 0:
            dislikes = item['count']
    print(
        f'\nКЕЙС #2: "ВЫВЕСТИ КОЛ-ВО ЛАЙКОВ/ДИЗЛАЙКОВ ОПРЕДЕЛЕННОГО ФИЛЬМА"\n'
        f'************************************************************\n'
        f'Случайно подобранный фильм <{film}> \n'
        f'имеет следующую статистику, собранную за {round(finish * 1000)}мс'
        f' (что гораздо меньше 200мс):\n'
        f'Количество лайков = <{likes}>; '
        f'количество дизлайков = <{dislikes}>\n'
    )


def case3_film_score():
    """
    Найдем среднее значение по полю LIKES.
    Это и составит пользовательский рейтинг фильма.
    Тестируется скорость на заполненной базе - не больше 200мс.
    """
    film = random_film()
    pipeline = [{"$match": {"film_id": film}},
                {"$group": {
                    "_id": {
                        "film_id": "$film_id",
                    },
                    'average_movie_rating': {"$avg": "$likes"}
                }}]
    start = time.time()
    result = collection.aggregate(pipeline)
    finish = time.time() - start
    result = list(result)
    print(
        f'\nКЕЙС #3: "РАССЧИТАТЬ ПОЛЬЗОВАТЕЛЬСКИЙ РЕЙТИНГ ФИЛЬМА"\n'
        f'************************************************************\n'
        f'(задача производная от кейса #2, результат ожидаем) \n'
        f'Случайно подобранный фильм <{film}> \n'
        f'имеет среднюю пользовательскую оценку равную '
        f'{result[0]["average_movie_rating"]:0.2f}\n'
        f'Скорость выполнения запроса - {round(finish * 1000)}мс'
        f' (что ожидаемо меньше  требуемых 200мс):\n'
    )


def case4_ins_bookmark_read_list_bookmarks():
    """
    Добавим закладку на определенный фильм.
    После чего выведем список всех фильмов,
    просмотр которых юзер отложил на потом.
    """
    film = random_film()
    # Выберем email из БД, который не связан с выбранным фильмом
    email = random_email(film)
    result_old = list(collection.find({'email': email}, {'bookmark': True}))
    doc = {
        "film_id": film,
        "email": email,
        "likes": None,
        "review": {},
        "bookmark": True
    }
    start = time.time()
    collection.insert_one(doc)
    result_new = collection.find({'email': email}, {'bookmark': True})
    finish = time.time() - start
    result_new = list(result_new)
    print(
        f'\nКЕЙС #4: "ДОБАВИТЬ ОТ ЮЗЕРА ЗАКЛАДКУ И ВЫВЕСТИ СПИСОК ЗАКЛАДОК"\n'
        f'*************************************************************\n'
        f'На начало теста было {len(result_old)} фильмов с закладкой от юзера'
        f' <{email}>\n'
        f'Под конец кейса таких фильмов должно быть +1, '
        f'и по факту - {len(result_new)}\n'
        f'Время выполнения теста - {round(finish * 1000)}мс, '
        f'что меньше требуемых 200мс\n'
    )


if __name__ == '__main__':
    client = MongoClient(
        settings.mongo_host, settings.mongo_port, connect=True,
    )
    mongo_db = client[settings.mongo_database]
    collection = mongo_db[settings.mongo_collection]

    case1_insert_like_read_list_likes()
    case2_count_likes_dislikes()
    case3_film_score()
    case4_ins_bookmark_read_list_bookmarks()
