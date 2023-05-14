CREATE TABLE IF NOT EXISTS default.readings (
    email String Codec(LZ4),
    film_id String Codec(LZ4),
    time DateTime Codec(DoubleDelta, LZ4),
    date ALIAS toDate(time),
    timestamp Int32 Codec(DoubleDelta, LZ4)
) Engine = Distributed('company_cluster', '', readings, rand());