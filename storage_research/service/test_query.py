CLICK_QUERIES = {
    'Список всех фильмов @юзера':
        """
        SELECT DISTINCT (movie_id)
        FROM research.views
        WHERE user_email = %(user_email)s
        """,
    'Все фильмы @юзера (+ лучший тайминг)':
        """
        SELECT movie_id, max(timestamp)
        FROM research.views
        WHERE user_email = %(user_email)s
        GROUP BY movie_id
        """,
    'Самый долгий просмотра @фильма @юзером':
        """
        SELECT max(timestamp)
        FROM research.views
        WHERE movie_id = %(movie_id)s AND user_email = %(user_email)s
        """,
    'Список юзеров смотревших @фильм':
        """
        SELECT DISTINCT user_email 
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
    'Список всех юзеров': 'SELECT DISTINCT user_email from research.views',
    'Сколько раз каждый юзер запускал просмотр':
        """
        SELECT user_email, count(movie_id)
        FROM research.views
        GROUP by user_email
        """
}

VERTICA_QUERIES_2 = {
    'Сколько всего записей': 'SELECT count(*) FROM views',
    'Средний тайминг просмотра каждого фильма':
        """
        SELECT movie_id, avg(timestamp)
        FROM views
        GROUP BY movie_id
        """,
    'Список всех юзеров': 'SELECT DISTINCT user_email from views',
    'Сколько раз каждый юзер запускал просмотр':
        """
        SELECT user_email, count(movie_id)
        FROM views
        GROUP by user_email
        """
}
VERTICA_QUERIES_1 = {
    'Список всех фильмов @юзера':
        """
        SELECT DISTINCT (movie_id)
        FROM views
        WHERE user_email = :user_email
        """,
    'Все фильмы @юзера (+ лучший тайминг)':
        """
        SELECT movie_id, max(timestamp)
        FROM views
        WHERE user_email = :user_email
        GROUP BY movie_id
        """,
    'Самый долгий просмотра @фильма @юзером':
        """
        SELECT max(timestamp)
        FROM views
        WHERE movie_id = :movie_id AND user_email = :user_email
        """,
    'Список юзеров смотревших @фильм':
        """
        SELECT DISTINCT user_email
        FROM views 
        WHERE movie_id = :movie_id
        """,
}
