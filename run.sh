#!/bin/sh
docker-compose down
docker rm $(docker ps -aq )
docker-compose up -d

echo "init clickhouse_node1"
cat clickhouse_node1_sql/create_shard.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_replica.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_shard_readings.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_replica_readings.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_default_readings.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/show_databases.sql | docker-compose exec -T clickhouse-node1 clickhouse-client

echo "init clickhouse_node2"
cat clickhouse_node2_sql/create_shard.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_replica.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_shard_readings.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_replica_readings.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_default_readings.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/show_databases.sql | docker-compose exec -T clickhouse-node2 clickhouse-client

# Wait for an HTTP endpoint to return 200 OK with Bash and curl, if timeout (300 sec) is reached, it exits with error (1)
timeout 300 bash -c 'while [[ "$(curl -o /dev/null -w ''%{http_code}'' localhost:8083/connectors)" != "200" ]]; do sleep 5; done' || false


echo "init etl kafka - redis"
curl -X POST -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors

echo "init etl kafka - clickhouse"
python clickhouse_kafka_etl.py

echo "run script"
python kafka_producer_redis_consumer.py