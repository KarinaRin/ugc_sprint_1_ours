CREATE TABLE IF NOT EXISTS shard.readings (
    readings_id Int32 Codec(DoubleDelta, LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    timestamp Int32 Codec(DoubleDelta, LZ4)
) Engine = ReplicatedMergeTree('/clickhouse/tables/shard2/readings', 'replica_1')
PARTITION BY toYYYYMM(time)
ORDER BY (readings_id, time);
