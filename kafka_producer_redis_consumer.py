""" Code for data creation and feeding into kafka """
from kafka import KafkaProducer
from redis import Redis

from time import sleep
import random
import string
from datetime import datetime
import uuid

NUM_SYMBOLS_IN_EMAIL = 7

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: x
)


def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def push():
    id = 0
    timestamp = 1683964363
    while True:
        # Итерируем айди записи и timestamp просмотра
        id += 1
        timestamp += 1

        # Создаем случайный ключ (в конце запятая обязательна!)
        email = ''.join(random.choices(
            string.ascii_uppercase, k=NUM_SYMBOLS_IN_EMAIL)
        ) + '@mail.com'
        film_id = str(uuid.uuid4())
        key = email + film_id + ','

        # Создаем пользовательские данные
        user_generated_content = f'{email}, {film_id}, "{get_current_time()}", {timestamp}'


        #Отправляем данные в кафку
        producer.send(
            'user_film_timestamp',
            value=user_generated_content.encode(),
            key=key.encode()
        )

        print('-' * 100)
        print(
            f'produced: \n\t key:  {key} \n\t message: {user_generated_content}'
        )

        sleep(3)
        redis = Redis(host=f'127.0.0.1', port=6379, db=1)
        message = redis.get(key)

        print(
            f'redis: \n\t key:  {key} \n\t message: {message}'
        )

try:
    push()
except KeyboardInterrupt:
    producer.close()
    print("exit")

