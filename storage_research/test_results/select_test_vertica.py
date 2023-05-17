"""Измерение скорости чтения данных из Vertica посредством sql-запросов"""
import os
from random import choice

import vertica_python

from service.common import REPEAT_COUNT
from storage_research.vertica import CONN_INFO
from service.test_query import VERTICA_QUERIES_1, VERTICA_QUERIES_2
from service.utility_vert import users_ids, movies_ids, time_execute


def select_query_result(query, values=None):
    results = []
    for _ in range(REPEAT_COUNT):
        exec_time = time_execute(
            cursor, query, values
        )
        results.append(exec_time)
    avg = sum(results) / REPEAT_COUNT
    return avg


def write_file():
    with open("select_test.csv", "w") as file:
        file.write('Vertica, Описание запроса\n')
        for query in VERTICA_QUERIES_1:
            data = select_query_result(VERTICA_QUERIES_1[query], values)
            file.write(f'{data:0.4f}, {query}\n')
        for query in VERTICA_QUERIES_2:
            data = select_query_result(VERTICA_QUERIES_2[query])
            file.write(f'{data:0.4f}, {query}\n')


def select_time_rate():
    """
    Функция
    - создаст файл, если его нет
    - перезапишет файл, если количество запросов в файле поменялось
      по сравнению с предыдущим выполнением
    - обновит данные скорости чтения по Vertica, если они были, или
    - добавит колонку vertica с результатами, если данных не было
    """
    _file = "select_test.csv"
    if not os.path.exists(_file) or os.path.getsize(_file) == 0:
        write_file()
    else:
        with open(_file, "r") as file:
            text = file.readlines()
            if len(text) != (
                    len(VERTICA_QUERIES_1) + len(VERTICA_QUERIES_2) + 1
            ):
                write_file()
                return
            if 'Clickhouse' in text[0]:
                text[0] = 'Clickhouse,Vertica, Описание запроса\n'
            else:
                text[0] = 'Vertica, Описание запроса\n'

            for i, query in enumerate(VERTICA_QUERIES_1, start=1):
                avg = select_query_result(VERTICA_QUERIES_1[query], values)
                row_list = text[i].rstrip().split(sep=',')
                if 'Clickhouse' in text[0]:
                    text[i] = f'{row_list[0]},{avg:0.4f}, {query}\n'
                else:
                    text[i] = f'{avg:0.4f}, {query}\n'
            for i, query in enumerate(VERTICA_QUERIES_2,
                                      start=(len(VERTICA_QUERIES_1) + 1)):
                avg = select_query_result(VERTICA_QUERIES_2[query])
                row_list = text[i].rstrip().split(sep=',')
                if 'Clickhouse' in text[0]:
                    text[i] = f'{row_list[0]},{avg:0.4f}, {query}\n'
                else:
                    text[i] = f'{avg:0.4f}, {query}\n'
        with open(_file, "w") as file:
            file.writelines(text)


if __name__ == "__main__":
    with vertica_python.connect(**CONN_INFO) as connection:
        cursor = connection.cursor()

        values = {
            "user_id": choice(users_ids(cursor)),
            "movie_id": choice(movies_ids(cursor))
        }
        select_time_rate()
