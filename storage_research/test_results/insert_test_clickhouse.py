"""Измерение скорости вставки данных в заполненное хранилище"""
import os
from random import randint, choice

from service.common import CHUNKS, REPEAT_COUNT
from service.utility_click import time_execute, list_ids
from storage_research.clickhouse import INSERT_QUERY


def count_chunk_result(chunk):
    results = []
    for _ in range(REPEAT_COUNT):
        values = [(
            choice(users_ids),
            choice(movies_ids),
            randint(10_000, 30_000),
        ) for _ in range(chunk)]
        exec_time = time_execute(INSERT_QUERY, values)
        results.append(exec_time)
    avg = sum(results) / REPEAT_COUNT
    return avg


def write_file():
    with open("insert_test.csv", "w") as file:
        file.write('Chunk,Clickhouse\n')
        for chunk in CHUNKS:
            data = count_chunk_result(chunk)
            file.write(f'{chunk},{data:0.4f}\n')


def insert_time_rate():
    """
    Функция
    - создаст файл, если его нет
    - перезапишет файл, если количество CHUNK в файле
      отличается от константы CHUNKS из файла common.py
    - обновит данные по Clickhouse, если они были, или
    - добавит колонку Clickhouse с результатами, если данных не было
    """
    _file = "insert_test.csv"
    if not os.path.exists(_file) or os.path.getsize(_file) == 0:
        write_file()
    else:
        with open(_file, "r") as file:
            text = file.readlines()
            if len(text) != (len(CHUNKS) + 1):
                write_file()
                return
            if 'Vertica' in text[0]:
                text[0] = 'Chunk,Clickhouse,Vertica\n'
            else:
                text[0] = 'Chunk,Clickhouse\n'

            for i, chunk in enumerate(CHUNKS, start=1):
                data = count_chunk_result(chunk)
                row_list = text[i].rstrip().split(sep=',')
                if 'Vertica' in text[0]:
                    text[i] = f'{row_list[0]},{data:0.4f},{row_list[-1]}\n'
                else:
                    text[i] = f'{row_list[0]},{data:0.4f}\n'
        with open(_file, "w") as file:
            file.writelines(text)


if __name__ == "__main__":
    users_ids = list_ids('user_id')
    movies_ids = list_ids('movie_id')
    insert_time_rate()
