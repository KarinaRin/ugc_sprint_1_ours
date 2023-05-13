
#########################################################################
clickhouse-node1

CREATE DATABASE IF NOT EXISTS shard;
CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE IF NOT EXISTS shard.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = ReplicatedMergeTree('/clickhouse/tables/shard1/readings', 'replica_1')
PARTITION BY toYYYYMM(time)
ORDER BY (readings_id, time); 


CREATE TABLE IF NOT EXISTS replica.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = ReplicatedMergeTree('/clickhouse/tables/shard2/readings', 'replica_2')
PARTITION BY toYYYYMM(time)
ORDER BY (readings_id, time); 


CREATE TABLE IF NOT EXISTS default.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = Distributed('company_cluster', '', readings, rand());


######################################################################### 
clickhouse-node3

CREATE DATABASE IF NOT EXISTS shard;
CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE shard.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = ReplicatedMergeTree('/clickhouse/tables/shard2/readings', 'replica_1')
PARTITION BY toYYYYMM(time)
ORDER BY (readings_id, time); 


CREATE TABLE replica.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = ReplicatedMergeTree('/clickhouse/tables/shard1/readings', 'replica_2')
PARTITION BY toYYYYMM(time)
ORDER BY (readings_id, time); 


CREATE TABLE default.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    temperature Decimal(5,2) Codec(T64, LZ4)
) Engine = Distributed('company_cluster', '', readings, rand());
