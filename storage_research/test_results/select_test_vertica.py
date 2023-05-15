"""Измерение скорости вставки данных в заполненное хранилище"""
from random import choice

import vertica_python

from storage_research.vertica import CONN_INFO
from utility_vert import users_ids, movies_ids, time_execute

SELECT_WITHOUT_VALUE = {
    'Сколько всего записей': 'SELECT count(*) FROM views',
    'Средний тайминг просмотра каждого фильма':
        """
        SELECT movie_id, avg(timestamp)
        FROM views
        GROUP BY movie_id
        """,
    'Список всех фильмов по разу': 'SELECT DISTINCT user_id from views',
    'Количество фильмов, запущенных хоть ра на просмотр каждым юзером':
        """
        SELECT user_id, count(movie_id)
        FROM views
        GROUP by user_id
        """
}
SELECT_QUERIES = {
    'Список всех фильмов @юзера':
        """
        SELECT DISTINCT (movie_id)
        FROM views
        WHERE user_id = :user_id
        """,
    'Все фильмы @юзера (+ лучший тайминг)':
        """
        SELECT movie_id, max(timestamp)
        FROM views
        WHERE user_id = :user_id
        GROUP BY movie_id
        """,
    'Самый долгий просмотра @фильма @юзером':
        """
        SELECT max(timestamp)
        FROM views
        WHERE movie_id = :movie_id AND user_id = :user_id
        """,
    'Список юзеров смотревших @фильм':
        """
        SELECT DISTINCT (user_id) 
        FROM views 
        WHERE movie_id = :movie_id
        """,

}

if __name__ == "__main__":
    with vertica_python.connect(**CONN_INFO) as connection:
        cursor = connection.cursor()

        values = {
            "user_id": choice(users_ids(cursor)),
            "movie_id": choice(movies_ids(cursor))
        }
        with open("select_test.csv", "r") as file:
            text = file.readlines()
            for i, query in enumerate(SELECT_QUERIES, start=1):
                results = []
                for _ in range(10):
                    exec_time = time_execute(
                        cursor, SELECT_QUERIES[query], values
                    )
                    results.append(exec_time)
                avg = sum(results) / 10
                row_list = text[i].rstrip().split(sep=',')
                text[i] = row_list[0] + f',{avg:0.4f},' + row_list[-1] + '\n'
            for i, query in enumerate(SELECT_WITHOUT_VALUE,
                                      start=(len(SELECT_QUERIES) + 1)):
                results = []
                for _ in range(10):
                    exec_time = time_execute(
                        cursor, SELECT_WITHOUT_VALUE[query], values=None
                    )
                    results.append(exec_time)
                avg = sum(results) / 10
                row_list = text[i].rstrip().split(sep=',')
                text[i] = row_list[0] + f',{avg:0.4f},' + row_list[-1] + '\n'
        with open("select_test.csv", "w") as file:
            file.writelines(text)
