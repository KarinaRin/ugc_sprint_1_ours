import os
import sqlite3

import pandas as pd

cwd = os.getcwd()

CON = sqlite3.connect(cwd + '/example.db')

from airflow import DAG
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def extract_data(url, tmp_file, **context) -> pd.DataFrame:
    """ Extract CSV
    """

    pd.read_csv(url).to_csv(tmp_file)  # Изменение to_csv


def transform_data(group, agreg, tmp_file, tmp_agg_file,
                   **context) -> pd.DataFrame:
    """ Group by data
    """
    data = pd.read_csv(tmp_file)  # Изменение read_csv
    data.groupby(group).agg(agreg).reset_index().to_csv(
        tmp_agg_file)  # Изменение to_csv


def load_data(tmp_file, table_name, conn=CON, **context) -> None:
    """ Load to DB
    """
    data = pd.read_csv(tmp_file)  # Изменение read_csv
    data["insert_time"] = pd.to_datetime("now")
    data.to_sql(table_name, conn, if_exists='replace', index=False)


with DAG(dag_id='dag',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily',
         start_date=days_ago(1)
         ) as dag:
    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/dm-novikov/stepik_airflow_course/main/data/data.csv',
            'tmp_file': '/tmp/file.csv'},
        dag=dag
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        dag=dag,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'tmp_agg_file': '/tmp/file_agg.csv',
            'group': ['A', 'B', 'C'],
            'agreg': {"D": sum}}
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        dag=dag,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'table_name': 'table',
            'conn': CON
        }
    )

    email_op = EmailOperator(
        task_id='send_email',
        to="stepikairflowcourse@yandex.ru",
        subject="Test Email Please Ignore",
        html_content=None,
        files=['/tmp/file.csv']
    )

    extract_data >> transform_data >> [load_data, email_op]
