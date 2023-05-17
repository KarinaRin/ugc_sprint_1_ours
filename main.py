import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.etl.kafka_clickhouse_etl import create_kafka_clickhouse_etl
from src.api.v1 import view
from src.core.config import settings


app = FastAPI(
    title=settings.project_name,
    description="Информация о пользовательском контенте",
    version="1.0.0",
    docs_url='/ugc_service/api/openapi',
    openapi_url='/ugc_service/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(
    view.router, prefix='/api/v1/view', tags=['View'])

@app.on_event('startup')
async def startup():
    create_kafka_clickhouse_etl()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
