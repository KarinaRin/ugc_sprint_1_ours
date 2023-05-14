#!/bin/sh
docker-compose down
docker rm $(docker ps -aq )
docker-compose up -d
sleep 1
echo "init clickhouse_node1"
cat clickhouse_node1_sql/create_shard.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_replica.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_shard_readings.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_replica_readings.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/create_default_readings.sql | docker-compose exec -T clickhouse-node1 clickhouse-client
cat clickhouse_node1_sql/show_databases.sql | docker-compose exec -T clickhouse-node1 clickhouse-client

echo "init clickhouse_node3"
cat clickhouse_node2_sql/create_shard.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_replica.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_shard_readings.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_replica_readings.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/create_default_readings.sql | docker-compose exec -T clickhouse-node2 clickhouse-client
cat clickhouse_node2_sql/show_databases.sql | docker-compose exec -T clickhouse-node2 clickhouse-client

echo "waiting for 30 sec"
sleep 30

echo "init etl"
curl -X POST -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors
python clickhouse_kafka_etl.py

echo "run script"
python kafka_producer_redis_consumer.py