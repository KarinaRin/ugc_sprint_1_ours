CREATE TABLE IF NOT EXISTS default.ugc (
    email String Codec(LZ4),
    film_id String Codec(LZ4),
    likes Int32 Codec(DoubleDelta, LZ4),
    review String Codec(LZ4),
    date DateTime Codec(DoubleDelta, LZ4),
    review_date DateTime Codec(DoubleDelta, LZ4),
    bookmark UInt8
) Engine = Distributed('company_cluster', '', ugc, rand());