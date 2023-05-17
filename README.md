Запуск

```bash
./run.sh
```


docker-compose build --no-cache big_data
docker rm -f $(docker ps -aq )



docker login
docker build -t alexblacknn/big_data:0.0.1 .
docker push alexblacknn/big_data:0.0.1

