"""Измерение скорости вставки данных в заполненное хранилище"""
import os
from random import randint, choice

import vertica_python

from service.common import CHUNKS, REPEAT_COUNT
from storage_research.vertica import CONN_INFO
from service.utility_vert import users_ids, movies_ids, time_execute
from vertica import QUERY


def count_chunk_result(chunk):
    results = []
    for _ in range(REPEAT_COUNT):
        values = [(
            choice(u_ids),
            choice(m_ids),
            randint(10_000, 30_000),
        ) for _ in range(chunk)]
        exec_time = time_execute(cursor, QUERY, values, insert=True)
        results.append(exec_time)
    avg = sum(results) / REPEAT_COUNT
    return avg


def write_file():
    with open("insert_test.csv", "w") as file:
        file.write('Chunk,Vertica\n')
        for chunk in CHUNKS:
            data = count_chunk_result(chunk)
            file.write(f'{chunk},{data:0.4f}\n')


def insert_time_rate():
    """
    Функция
    - создаст файл, если его нет
    - перезапишет файл, если количество CHUNK в файле
      отличается от константы CHUNKS из файла common.py
    - обновит данные по Vertica, если они есть, или
    - добавит колонку Vertica с результатами, если данных не было
    """
    _file = "insert_test.csv"
    if not os.path.exists(_file):
        write_file()
    else:
        with open(_file, "r") as file:
            text = file.readlines()
            if len(text) != (len(CHUNKS) + 1):
                write_file()
                return
            if 'Clickhouse' in text[0]:
                text[0] = 'Chunk,Clickhouse,Vertica\n'
            else:
                text[0] = 'Chunk,Vertica\n'

            for i, chunk in enumerate(CHUNKS, start=1):
                data = count_chunk_result(chunk)
                row_list = text[i].rstrip().split(sep=',')
                if 'Clickhouse' in text[0]:
                    text[i] = (
                            f'{row_list[0]},{row_list[1]},{data:0.4f}\n'
                    )
                else:
                    text[i] = row_list[0] + f',{data:0.4f}\n'
        with open(_file, "w") as file:
            file.writelines(text)


if __name__ == "__main__":
    with vertica_python.connect(**CONN_INFO) as connection:
        cursor = connection.cursor()
        u_ids = users_ids(cursor)
        m_ids = movies_ids(cursor)
        insert_time_rate()
