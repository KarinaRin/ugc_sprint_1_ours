CREATE TABLE IF NOT EXISTS replica.readings (
    email String Codec(LZ4),
    uuid String Codec(LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    timestamp Int32 Codec(DoubleDelta, LZ4)
) Engine = ReplicatedMergeTree('/clickhouse/tables/shard1/readings', 'replica_2')
PARTITION BY toYYYYMM(time)
ORDER BY (email, time);