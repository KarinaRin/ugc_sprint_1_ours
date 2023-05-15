"""Измерение скорости вставки данных в заполненное хранилище"""
from random import randint, choice

import vertica_python

from common import CHUNKS
from storage_research.vertica import CONN_INFO
from test_results.utility_vert import users_ids, movies_ids, time_execute
from vertica import QUERY


def insert_time_rate(cursor):
    u_ids = users_ids(cursor)
    m_ids = movies_ids(cursor)
    with open("insert_test.csv", "r") as file:
        text = file.readlines()
        for i, chunk in enumerate(CHUNKS, start=1):
            results = []
            for _ in range(10):  # 10 - число повторов для расчета средней
                values = [(
                    choice(u_ids),
                    choice(m_ids),
                    randint(10_000, 30_000),
                ) for _ in range(chunk)]
                exec_time = time_execute(cursor, QUERY, values, insert=True)
                results.append(exec_time)
            avg = sum(results) / 10
            text[i] = text[i].rstrip() + f"{avg:0.4f}\n"

    with open("insert_test.csv", "w") as file:
        file.writelines(text)


if __name__ == "__main__":
    with vertica_python.connect(**CONN_INFO) as connection:
        cursor = connection.cursor()
        insert_time_rate(cursor)
