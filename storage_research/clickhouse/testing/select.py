"""Измерение скорости вставки данных в заполненное хранилище"""
from random import choice

from testing.utility_code import list_ids, time_execute

users_ids = list_ids('user_id')
movies_ids = list_ids('movie_id')

SELECT_QUERIES = {
    'Сколько всего записей': 'SELECT count() FROM research.views',
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
    'Список юзеров, смотревших @фильм':
        """
        SELECT DISTINCT (user_id) 
        FROM research.views 
        WHERE movie_id = %(movie_id)s
        """,
    'Средний тайминг просмотра каждого фильма':
        """
        SELECT movie_id, avg(timestamp)
        FROM research.views
        GROUP BY movie_id
        """,
}


if __name__ == "__main__":

    values = {"user_id": choice(users_ids), "movie_id": choice(movies_ids)}
    with open("select.txt", "w") as file:
        for query in SELECT_QUERIES:
            results = []
            for _ in range(10):
                exec_time = time_execute(SELECT_QUERIES[query], values)
                results.append(exec_time)
            avg = sum(results)/10
            file.write(f'Среднее время: {avg:0.4f}, Запрос: {query}\n')
        file.write(
            '\nСимвол @ в описании запроса соответствует слову "конкретный"'
        )
