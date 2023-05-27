import os
from logging import config as logging_config

from pydantic import BaseSettings

from .logger import LOGGING


class Settings(BaseSettings):
    ugc_api_port: int = 8000
    debug_level: str = 'DEBUG'
    project_name: str = 'ugc_service'
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_db: int = 1
    token_secret_key: str = 'very_secret_key'
    kafka_host: str = '127.0.0.1'
    kafka_port: int = 9092
    mongo_host: str = '127.0.0.1'
    mongo_port: int = 27117
    mongo_database: str = 'UserGeneratedContent'
    mongo_collection: str = 'UsersContent'
    clickhouse_host = '127.0.0.1'  # clickhouse-node1
    kafka_connector: str = 'http://127.0.0.1:8083/connectors' # kafka-connect



settings = Settings()

# Уровень логирования
LOGGING['root']['level'] = settings.debug_level

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
