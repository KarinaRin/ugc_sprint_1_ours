import pprint
from datetime import datetime
import asyncio
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27117)

db = client.UserGeneratedContent

posts = db.UsersContent
posts.delete_many({})

post = {
    "doc_id": "123-45-678",
    "user_email": "121-12-516",
    "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    'likes': 10,
    "review": {
        "review_id": "205-325-056",
        "text": "this was awsome!",
        'date': datetime.utcnow(),
        'author': 'test@test.com',
        'likes': ['test2@test.com', 'test1@test.com'],
        'dislikes': ['test3@test.com', 'test4@test.com']
    },
    'bookmark': True
}


async def do_insert():
    result = await posts.insert_one(post)
    print('result %s' % repr(result.inserted_id))


loop = asyncio.get_event_loop()
loop.run_until_complete(do_insert())

post = {
    "doc_id": "163-45-678",
    "user_email": "141-12-516",
    "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    'likes': None,
    "review": {
        "text": "this was good!",
        'date': datetime.utcnow(),
        'author': 'test@test.com',
        'likes': ['test2@test.com', 'test1@test.com'],
        'dislikes': ['test3@test.com', 'test4@test.com']
    },
    'bookmark': True
}
loop.run_until_complete(do_insert())

post = {
    "doc_id": "000-45-678",
    "email": "test@test.com",
    "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    'likes': 0,
    "review": {
        "text": "this was bad!",
        'date': datetime.utcnow(),
        'likes': ['test3@test.com', 'test4@test.com'],
        'dislikes': ['test0@test.com', 'test5@test.com']
    },
    'bookmark': True
}
loop.run_until_complete(do_insert())

post = {
    "doc_id": "00110-45-678",
    "email": "test@test.com",
    "film_id": "11185f64-5717-4562-b3fc-2c963f66afa6",
    'likes': 100,
    "review": {
        "review_id": "20221-32221-0515",
        "text": "this was bad!",
        'date': datetime.utcnow(),
        'likes': ['test3@test.com', 'test4@test.com'],
        'dislikes': ['test0@test.com', 'test5@test.com']
    },
    'bookmark': True
}

loop.run_until_complete(do_insert())


async def do_find():
    documentes = posts.find()
    async for doc in documentes:
        pprint.pprint(doc)


loop.run_until_complete(do_find())
#
# print('\n\nПросмотр средней пользовательской оценки фильма')
#
# pipeline = [
#     # Matchn the documents possible
#     {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}},
#
#     # # Group the documents and "count" via $sum on the values
#     {"$group": {
#         "_id": {
#             "film_id": "$film_id",
#             # "likes": "$likes"
#         },
#         "total_sum": {"$sum": "$likes"},
#         'count': {"$sum": 1},
#         'average_movie_rating': {"$avg": "$likes"},
#
#     }}
# ]
#
#
# async def do_aggregate(pipeline):
#     result = await posts.aggregate(pipeline).to_list(length=None)
#     print(result)
#
#
# loop.run_until_complete(do_aggregate(pipeline))
#
# print('\n\nПросмотр количества лайков у фильма')
# pipeline = [
#     # Matchn the documents possible
#     {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "likes": 10}},
#
#     # # Group the documents and "count" via $sum on the values
#     {"$group": {
#         "_id": {
#             "film_id": "$film_id",
#             # "likes": "$likes"
#         },
#         'count': {"$sum": 1},
#     }}
# ]
# loop.run_until_complete(do_aggregate(pipeline))
#
# print('\n\nПросмотр количества дизлайков у фильма')
# pipeline = [
#     # Matchn the documents possible
#     {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "likes": 0}},
#
#     # # Group the documents and "count" via $sum on the values
#     {"$group": {
#         "_id": {
#             "film_id": "$film_id",
#             # "likes": "$likes"
#         },
#         'count': {"$sum": 1},
#     }}
# ]
# loop.run_until_complete(do_aggregate(pipeline))
#
# print('\n\nПросмотр количества лайков и дизлайков у фильма')
# pipeline = [
#     # Matchn the documents possible
#     {"$match": {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "likes": {"$ne": None}}},
#
#     # # Group the documents and "count" via $sum on the values
#     {"$group": {
#         "_id": {
#             "film_id": "$film_id",
#             "likes": "$likes"
#         },
#         'count': {"$sum": 1},
#     }}
# ]
# loop.run_until_complete(do_aggregate(pipeline))
#
# print('\n\nДобавление, удаление или изменение лайка, дизлайка или оценки.')
#
# # Изменение лайка - любое значение. Удаление ставим None. Добавление любое значение вместо None
# query = {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#          "user_email": "141-12-516"}
#
#
# async def change_likes(query):
#     present_data = await posts.find_one(query)
#     print(present_data)
#     new_data = {'$set': {"likes": 10}}
#     await posts.update_one(present_data, new_data)
#
#
# loop.run_until_complete(change_likes(query))
#
#
# async def check():
#     query = {"film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#              "user_email": "141-12-516"}
#     present_data = await posts.find_one(query)
#     print(present_data)
#
#
# loop.run_until_complete(change_likes(query))
