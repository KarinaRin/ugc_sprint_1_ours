# Запуск

```bash
./run.sh
```


swager => 
http://127.0.0.1:8001/ugc_service/api/openapi 

Сначала отправляем данные по пост запросу потом получаем данные гет запросом.


# Вспомогалка для разработки:
docker-compose build --no-cache big_data
docker rm -f $(docker ps -aq )


docker login
docker build -t alexblacknn/big_data:0.0.1 .
docker push alexblacknn/big_data:0.0.1

