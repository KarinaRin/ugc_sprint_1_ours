"""Измерение скорости вставки данных в заполненное хранилище"""
from random import choice

from utility_click import list_ids, time_execute

users_ids = list_ids('user_id')
movies_ids = list_ids('movie_id')

SELECT_QUERIES = {
    'Список всех фильмов @юзера':
        """
        SELECT DISTINCT (movie_id)
        FROM research.views
        WHERE user_id = %(user_id)s
        """,
    'Все фильмы @юзера (+ лучший тайминг)':
        """
        SELECT movie_id, max(timestamp)
        FROM research.views
        WHERE user_id = %(user_id)s
        GROUP BY movie_id
        """,
    'Самый долгий просмотра @фильма @юзером':
        """
        SELECT max(timestamp)
        FROM research.views
        WHERE movie_id = %(movie_id)s AND user_id = %(user_id)s
        """,
    'Список юзеров смотревших @фильм':
        """
        SELECT DISTINCT (user_id) 
        FROM research.views 
        WHERE movie_id = %(movie_id)s
        """,
    'Сколько всего записей': 'SELECT count() FROM research.views',
    'Средний тайминг просмотра каждого фильма':
        """
        SELECT movie_id, avg(timestamp)
        FROM research.views
        GROUP BY movie_id
        """,
    'Список всех фильмов по разу': 'SELECT DISTINCT user_id from research.views',
    'Количество фильмов запущенных хоть раз на просмотр каждым юзером':
        """
        SELECT user_id, count(movie_id)
        FROM research.views
        GROUP by user_id
        """
}


if __name__ == "__main__":

    values = {"user_id": choice(users_ids), "movie_id": choice(movies_ids)}
    with open("select_test.csv", "w") as file:
        file.write('Clickhouse, Vertica, Описание запроса\n')
        for query in SELECT_QUERIES:
            results = []
            for _ in range(10):
                exec_time = time_execute(SELECT_QUERIES[query], values)
                results.append(exec_time)
            avg = sum(results)/10
            file.write(f'{avg:0.4f},,{query}\n')
