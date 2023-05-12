"""Измерение скорости вставки данных в заполненное хранилище"""
from random import randint, choice

from initial.data_generator import INSERT_QUERY
from testing.select import users_ids, movies_ids
from testing.utility_code import time_execute

CHUNKS = [10, 100, 500, 1000, 5000]


def insert_time_rate():
    with open("insert.txt", "w") as file:
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
            avg = sum(results)/10
            file.write(
                f'Среднее время: {avg:0.4f}, Количество строк: {chunk}\n'
            )


if __name__ == "__main__":
    insert_time_rate()
