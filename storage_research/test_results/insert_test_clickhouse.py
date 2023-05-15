"""Измерение скорости вставки данных в заполненное хранилище"""
from random import randint, choice

from common import CHUNKS
from select_test_clickhouse import users_ids, movies_ids
from utility_click import time_execute
from storage_research.clickhouse import INSERT_QUERY


def insert_time_rate():
    with open("insert_test.csv", "w") as file:
        file.write('chunk,clickhouse_old,vertica')
        for chunk in CHUNKS:
            results = []
            for _ in range(10):  # 10 - число повторов для расчета средней
                values = [(
                    choice(users_ids),
                    choice(movies_ids),
                    randint(10_000, 30_000),
                ) for _ in range(chunk)]
                exec_time = time_execute(INSERT_QUERY, values)
                results.append(exec_time)
            avg = sum(results) / 10

            file.write(f'{chunk},{avg:0.4f},\n')


if __name__ == "__main__":
    insert_time_rate()
