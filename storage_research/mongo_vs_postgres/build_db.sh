docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
docker exec -it mongors1n1 bash -c 'echo "use research" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"research\")" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"research.likes\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"research.likes\", {\"film_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"research.reviews\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"research.reviews\", {\"film_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"research.bookmarks\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"research.bookmarks\", {\"film_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "show collections" | mongosh'
