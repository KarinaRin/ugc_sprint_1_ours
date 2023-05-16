import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import view
from src.core.config import settings
from src.db.kafka import CustomKafkaProducer, kafka
from src.db.redis import CustomRedis, redis

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


# @app.on_event('startup')
# async def startup():
#     kafka.kafka = CustomKafkaProducer(
#         address=[f'{settings.kafka_host}:{settings.kafka_port}']
#     )
#     redis.redis = CustomRedis(
#         host=settings.redis_host, port=settings.redis_port, db=1
#     )
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     await kafka.kafka.close()
#     await redis.redis.close()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
