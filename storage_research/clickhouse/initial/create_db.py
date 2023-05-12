from clickhouse_driver import Client

if __name__ == '__main__':
    client = Client(host='localhost')
    client.execute('CREATE DATABASE IF NOT EXISTS research')
    client.execute('DROP TABLE IF EXISTS research.views')
    client.execute(
        '''
        CREATE TABLE IF NOT EXISTS research.views (
            user_id UUID,
            movie_id UUID,
            timestamp UInt32
        ) ENGINE = MergeTree()
        ORDER BY (user_id, movie_id);
        '''
    )
