#!/bin/sh
docker-compose down
docker rm -f $(docker ps -aq )
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
