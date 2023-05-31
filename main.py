import logging

import logstash
import uvicorn as uvicorn
import sentry_sdk

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.etl.kafka_clickhouse_etl import create_kafka_clickhouse_etl
from src.api.v1 import view, likes, bookmark
from src.core.config import settings
from src.etl.kafka_redis_etl import create_connector

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.project_name,
    description="Информация о пользовательском контенте",
    version="1.0.0",
    docs_url='/ugc_service/api/openapi',
    openapi_url='/ugc_service/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)
# logstash
app.logger.addHandler(logstash.LogstashHandler('localhost', 5044, version=1))

app.include_router(
    view.router, prefix='/api/v1/view', tags=['View'])
app.include_router(
    likes.router, prefix='/api/v1/likes', tags=['Likes'])
app.include_router(
    bookmark.router, prefix='/api/v1/bookmarks', tags=['Bookmarks'])


@app.on_event('startup')
async def startup():
    await create_kafka_clickhouse_etl()
    await create_connector()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001
    )
