
1. Запускаем компоуз (ждем пока все запуститься)

```bash
docker-compose up
```
2. C помощью conduktor подсоединяемся к кафке и создаем топик readings 

3. Запускаем проект в pycharm
  pip install -r requirements.txt  

4. Идем в clickhouse.ipynb и создаем таблицы в clickhouse (3 штуки)


5. Заходим внуть контейнера с портом 9092

```bash
docker ps
docker exec -it 1ca379db1a67 bash
```

6. В нем отправляем данные в брокер

kafka-console-producer --broker-list broker:9092 --topic readings <<END
11,"2020-05-16 23:55:44",14.2
12,"2020-05-16 23:55:45",20.1
31,"2020-05-16 23:55:51",12.9
END

7. Смотрим появились ли данные в clickhouse
 
8. Проверка с помощью lighthouse UI данных clickhouse 
```bash
cd lighthouse
``` 
а. Запускам файл index.html 
б. Коннектимся к clickhouse

# Удалить все контейнеры
docker-compose down
docker rm $( docker ps -aq ) 

sudo docker-compose down
sudo docker rm $( sudo docker ps -aq ) 
sudo docker-compose up
# 
https://stackoverflow.com/questions/57941813/write-kafka-topic-data-to-redis-using-docker

curl -X POST -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors
http://localhost:8083/connector-plugins  
http://localhost:8083/connectors/RedisSinkConnector1/status 
sudo docker-compose exec redis redis-cli MONITOR 
sudo docker-compose exec redis bash 
redis-cli
SELECT 1
https://forum.confluent.io/t/redis-sink-connector-records-missing/4675

скачать =>>>> 
https://www.confluent.io/hub/jcustenborder/kafka-connect-redis







##################################################
# Exception: Syntax error (Multi-statements are not allowed): failed at position 36 (end of query) (line 1, col 36): ;
https://groups.google.com/g/clickhouse/c/GXHMTGXR0wg 
