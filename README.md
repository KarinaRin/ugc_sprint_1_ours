# Запуск

1. Запускаем все контейнеры 
```bash
./run.sh
```
2. Заходим в свагер

http://127.0.0.1:8001/ugc_service/api/openapi 

3. Используем специально сгенерированный для тестирования токен
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRva2VuQHRva2VuLmNvbSIsImlhdCI6MTY4NDMyNzY2Ny4wMzE5ODYsImV4cCI6MTcxNTg2NzY2Ny4wMzE5ODMxLCJ0eXBlIjoiYWNjZXNzIiwicm9sZSI6ImFkbWluIn0.s6Wqw1DB_g3CKxGEptD3oD13vDTQBHbNHmoEk-GXX3k
```

4. Отправляем данные по Post запросу

5. Получаем данные по Get запросу.



# Вспомогалка для разработки:
docker-compose build --no-cache big_data
docker rm -f $(docker ps -aq )

docker login
docker build -t alexblacknn/big_data:0.0.1 .
docker push alexblacknn/big_data:0.0.1

https://my-organization-o0.sentry.io/projects/python-fastapi/?project=4505266902925312