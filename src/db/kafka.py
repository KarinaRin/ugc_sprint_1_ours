# import random
# import string
# import uuid
# from datetime import datetime
# from time import sleep
# from typing import Optional
#
# from kafka import KafkaProducer
#
# from src.core.config import settings
#
# NUM_SYMBOLS_IN_EMAIL = 7
#
# kafka: Optional[KafkaProducer] = KafkaProducer(
#     bootstrap_servers=f'{settings.kafka_host}:{settings.kafka_port}'
# )
#
#
# class CustomKafkaProducer:
#     def __init__(self, address):
#         self.producer = KafkaProducer(
#             bootstrap_servers=address,
#             value_serializer=lambda x: x
#         )
#
#     def send(self, topic, value, key):
#         self.producer.send(
#             topic,
#             value=value.encode(),
#             key=key.encode()
#         )
#
#     def close(self):
#         self.producer.close()
#
#
# def create_kafka_test_data():
#     # Итерируем timestamp просмотра
#     timestamp = 0
#     while True:
#         timestamp += 1
#         # Создаем случайный ключ (в конце запятая обязательна!)
#         email = ''.join(random.choices(
#             string.ascii_uppercase, k=NUM_SYMBOLS_IN_EMAIL)
#         ) + '@mail.com'
#         film_id = str(uuid.uuid4())
#         key = email + film_id + ','
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         user_generated_content = f'{email}, {film_id}, "{current_time}", {timestamp}'
#         yield user_generated_content, key
#
#
# def push(kafka_producer, redis):
#     for user_generated_content, key in create_kafka_test_data():
#         # Отправляем данные в кафку
#         kafka_producer.send('user_film_timestamp', user_generated_content, key)
#
#         print(
#             f'{"-" * 100} \n produced: \n\t key:  {key} \n\t message: {user_generated_content}'
#         )
#
#         sleep(3)
#
#         # Забираем из редиса
#         message = redis._get_message(key)
#         return_timestamp = redis.get_timestamp(key)
#
#         print(
#             f'redis: \n\t key:  {key} \n\t message: {message}, timestamp: {return_timestamp}'
#         )
#
