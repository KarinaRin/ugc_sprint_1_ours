import csv
import logging
from datetime import datetime, timedelta
import random

import pymongo
from airflow import DAG, macros
from airflow.operators.python import PythonOperator
from clickhouse_driver import Client


def on_failure_callback(**context):
    print(f"Task {context['task_instance_key_str']} failed.")


def upload_mongo(**context):
    """Таска, для загрузки случайных данных в mongodb."""

    client = pymongo.MongoClient('router01', 27017)
    db = client.UserGeneratedContent
    collection = db.UsersContent

    mylist = [
        {
            "email": f"test{i}@test.com",
            "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            'likes': random.choice([0, 10]),
            'date': datetime.utcnow(),
            "review": {
                "review_id": "205-325-056",
                "text": random.choice(["rewiew 1!", "rewiew 2!"]),
                'date': datetime.utcnow(),
                'likes': ['test2@test.com', 'test1@test.com'],
                'dislikes': ['test3@test.com', 'test4@test.com']
            },
            'bookmark': random.choice([True, False])
        } for i in range(20)
    ]
    collection.insert_many(mylist)


def read_mongo(**context):
    """Таска, для выгрузки данных из mongodb и запись их в csv."""

    client = pymongo.MongoClient('router01', 27017)
    db = client.UserGeneratedContent
    collection = db.UsersContent

    documents = collection.find()

    start_time = context['prev_execution_date_success']
    end_time = datetime.utcnow()
    logging.info(f'11111111111 {start_time}, {end_time}')
    end_time = '2023-06-03 21:06'
    start_time = '2023-06-03 00:56'


    data = collection.find({
        'date': {'$lte': datetime.strptime(end_time, '%Y-%m-%d %H:%M'),
                 '$gt': datetime.strptime(start_time, '%Y-%m-%d %H:%M'),
                 }
    })

    # w - если таска упадет, то перетираем для идемпотентности файл
    with open('/tmp/mongo_data.csv', 'w') as f:
        for one_document in documents:
            try:
                logging.info(one_document)
                # write a row to the csv file
                string_to_write = (
                    f'{one_document["email"]},'
                    f'{one_document["film_id"]},'
                    f'{one_document["likes"]},'
                    f'{one_document["date"]},'
                    f'{one_document["review"]["text"]},'
                    f'{one_document["review"]["date"]},'
                    f'{one_document["bookmark"]} '
                    f'\r\n')
                f.writelines(string_to_write)
            except:
                logging.info('skip')


def read_in_chunks(file_object):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    reader = csv.reader(file_object, delimiter=",")
    for data in reader:
        logging.info(f'data {data}')
        yield data


def load_clickhouse(**context):
    client = Client('clickhouse-node1')
    with open('/tmp/mongo_data.csv', 'r') as f:
        data_chunk = []
        for data in read_in_chunks(f):
            data_chunk.append(data)

            if len(data_chunk) > 3:
                data_chunk_prepared = list(map(lambda x: [
                    x[0],  # email
                    x[1],  # film_id
                    int(x[2]),  # likes
                    datetime.strptime(x[3].strip().split('.')[0],  # date
                                      '%Y-%m-%d %H:%M:%S'),
                    x[4],  # review_text
                    datetime.strptime(x[5].strip().split('.')[0],
                                      # review_date
                                      '%Y-%m-%d %H:%M:%S'),
                    int(x[6].strip() == 'True'),  # bookmark
                ], data_chunk))
                data_chunk = []
                logging.info(f'data_chunk_prepared {data_chunk_prepared}')
                client.execute(
                    'INSERT INTO ugc (email, film_id, likes, date, review, review_date, bookmark) VALUES',
                    data_chunk_prepared
                )


with DAG(
        dag_id="mongo-client-etl",
        schedule_interval=None,
        start_date=datetime(2022, 10, 28),
        catchup=False,
        tags=["etl"],
        default_args={
            "owner": "Owner",
            "retries": 2,
            "retry_delay": timedelta(minutes=5),
            'on_failure_callback': on_failure_callback
        }
) as dag:
    t1 = PythonOperator(
        task_id='upload-mongodb',
        python_callable=upload_mongo,
        op_kwargs={},
        dag=dag
    )

    t2 = PythonOperator(
        task_id='read-mongodb',
        python_callable=read_mongo,
        op_kwargs={},
        dag=dag
    )

    t3 = PythonOperator(
        task_id='load-clickhouse',
        python_callable=load_clickhouse,
        op_kwargs={},
        dag=dag
    )

    t1 >> t2 >> t3
