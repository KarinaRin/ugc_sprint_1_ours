"""Измерение скорости чтения данных из Clickhouse посредством sql-запросов"""
import os
from random import choice

from service.common import REPEAT_COUNT
from service.test_query import CLICK_QUERIES
from service.utility_click import list_ids, time_execute


def select_query_result(query):
    results = []
    for _ in range(REPEAT_COUNT):
        exec_time = time_execute(CLICK_QUERIES[query], values)
        results.append(exec_time)
    avg = sum(results) / REPEAT_COUNT
    return avg


def write_file():
    with open("select_test.csv", "w") as file:
        file.write('Clickhouse, Описание запроса\n')
        for query in CLICK_QUERIES:
            data = select_query_result(query)
            file.write(f'{data:0.4f},{query}\n')


def select_time_rate():
    """
    Функция
    - создаст файл, если его нет
    - перезапишет файл, если количество запросов в файле поменялось
      по сравнению с предыдущим выполнением
    - обновит данные скорости чтения по Clickhouse, если они были, или
    - добавит колонку Clickhouse с результатами, если данных не было
    """
    _file = "select_test.csv"
    if not os.path.exists(_file) or os.path.getsize(_file) == 0:
        write_file()
    else:
        with open(_file, "r") as file:
            text = file.readlines()
            if len(text) != (len(CLICK_QUERIES) + 1):
                write_file()
                return
            if 'Vertica' in text[0]:
                text[0] = 'Clickhouse,Vertica, Описание запроса\n'
            else:
                text[0] = 'Clickhouse, Описание запроса\n'

            for i, query in enumerate(CLICK_QUERIES, start=1):
                data = select_query_result(query)
                row_list = text[i].rstrip().split(sep=',')
                if 'Vertica' in text[0]:
                    text[i] = (
                            f'{data:0.4f},{row_list[0]}, {query}\n'
                    )
                else:
                    text[i] = f'{data:0.4f}, {query}\n'
        with open(_file, "w") as file:
            file.writelines(text)


if __name__ == "__main__":
    users_ids = list_ids('user_email')
    movies_ids = list_ids('movie_id')
    values = {"user_email": choice(users_ids), "movie_id": choice(movies_ids)}
    select_time_rate()


