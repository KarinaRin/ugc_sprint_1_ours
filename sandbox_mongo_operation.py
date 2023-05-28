import pymongo
import datetime
import pprint
from bson.son import SON

client = pymongo.MongoClient('localhost', 27117)
db = client.UserGeneratedContent

posts = db.UsersContent
print('11111111111111111111', posts.index_information())


print('\n\nПросмотр средней пользовательской оценки фильма')
pipeline = [
    # Matchn the documents possible
    {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}},

    # # Group the documents and "count" via $sum on the values
    {"$group": {
        "_id": {
            "film_id": "$film_id",
            # "likes": "$likes"
        },
        "total_sum": {"$sum": "$likes"},
        'count': {"$sum": 1},
        'average_movie_rating': {"$avg": "$likes"},

    }}
]
pprint.pprint(list(posts.aggregate(pipeline, explain=True)))

print('\n\nПросмотр количества лайков у фильма')
pipeline = [
    # Matchn the documents possible
    {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "likes": 10}},

    # # Group the documents and "count" via $sum on the values
    {"$group": {
        "_id": {
            "film_id": "$film_id",
            # "likes": "$likes"
        },
        'count': {"$sum": 1},
    }}
]
pprint.pprint(list(posts.aggregate(pipeline)))

print('\n\nПросмотр количества дизлайков у фильма')
pipeline = [
    # Matchn the documents possible
    {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "likes": 0}},

    # # Group the documents and "count" via $sum on the values
    {"$group": {
        "_id": {
            "film_id": "$film_id",
            # "likes": "$likes"
        },
        'count': {"$sum": 1},
    }}
]
pprint.pprint(list(posts.aggregate(pipeline)))

print('\n\nДобавление, удаление или изменение лайка, дизлайка или оценки.')

# Изменение лайка - любое значение. Удаление ставим None. Добавление любое значение вместо None
query = {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "email": "test1@test.com"}
present_data = posts.find_one(query)
print(present_data)
new_data = {'$set': {"likes": 10}}
posts.update_one(present_data, new_data)
query = {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "email": "test1@test.com"}
present_data = posts.find_one(query)
print(present_data)