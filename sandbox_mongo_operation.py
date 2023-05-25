import pymongo
import datetime
import pprint
from bson.son import SON

client = pymongo.MongoClient('localhost', 27117)
db = client.UserGeneratedContent

posts = db.UsersContent
posts.delete_many({})

post = {
    "doc_id": "123-45-678",
    "user_id": "121-12-516",
    "film_id": "155-15-515",
    'likes': 10,
    "review": {
        "review_id": "205-325-056",
        "text": "this was awsome!",
        'date': datetime.datetime.utcnow(),
        'author': 'test@test.com',
        'likes': ['test2@test.com', 'test1@test.com'],
        'dislikes': ['test3@test.com', 'test4@test.com']
    },
    'bookmark': True
}
post_id = posts.insert_one(post).inserted_id

post = {
    "doc_id": "163-45-678",
    "user_id": "141-12-516",
    "film_id": "155-15-515",
    'likes': None,
    "review": {
        "review_id": "205-115-056",
        "text": "this was good!",
        'date': datetime.datetime.utcnow(),
        'author': 'test@test.com',
        'likes': ['test2@test.com', 'test1@test.com'],
        'dislikes': ['test3@test.com', 'test4@test.com']
    },
    'bookmark': True
}
post_id = posts.insert_one(post).inserted_id

post = {
    "doc_id": "000-45-678",
    "user_id": "000-13-518",
    "film_id": "155-15-515",
    'likes': 0,
    "review": {
        "review_id": "201-321-055",
        "text": "this was bad!",
        'date': datetime.datetime.utcnow(),
        'author': 'test@test.com',
        'likes': ['test3@test.com', 'test4@test.com'],
        'dislikes': ['test0@test.com', 'test5@test.com']
    },
    'bookmark': True
}
post_id = posts.insert_one(post).inserted_id

post = {
    "doc_id": "00110-45-678",
    "user_id": "001110-13-518",
    "film_id": "999-15-515",
    'likes': 111111110,
    "review": {
        "review_id": "20221-32221-0515",
        "text": "this was bad!",
        'date': datetime.datetime.utcnow(),
        'author': 'test@test.com',
        'likes': ['test3@test.com', 'test4@test.com'],
        'dislikes': ['test0@test.com', 'test5@test.com']
    },
    'bookmark': True
}

post_id = posts.insert_one(post).inserted_id

# for doc in posts.find():
#         pprint.pprint(doc)

print('\n\nПросмотр средней пользовательской оценки фильма')
pipeline = [
    # Matchn the documents possible
    {"$match": {"film_id": "155-15-515"}},

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
pprint.pprint(list(posts.aggregate(pipeline)))

print('\n\nПросмотр количества лайков у фильма')
pipeline = [
    # Matchn the documents possible
    {"$match": {"film_id": "155-15-515", "likes": 10}},

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
    {"$match": {"film_id": "155-15-515", "likes": 0}},

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
query = {"film_id": "155-15-515", "user_id": "141-12-516"}
present_data = posts.find_one(query)
print(present_data)
new_data = {'$set': {"likes": 10}}
posts.update_one(present_data, new_data)
query = {"film_id": "155-15-515", "user_id": "141-12-516"}
present_data = posts.find_one(query)
print(present_data)