import pprint
import time
from datetime import datetime
import asyncio
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27117)

db = client.UserGeneratedContent

posts = db.UsersContent
posts.delete_many({})

# wait for deletig
time.sleep(5)


async def do_insert(post):
    result = await posts.insert_one(post)
    print('result %s' % repr(result.inserted_id))


loop = asyncio.get_event_loop()

# for i, like in enumerate((0, 0, 0, 10, 10, 10)):
for i, like in enumerate(('None', 'None1', '2', 'None', '1', 'None')):
    print(i)
    post = {
        "email": f"test{i}@test.com",
        "film_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        'likes': like,
        "review": {
            "review_id": "205-325-056",
            "text": "this was awsome!",
            'date': datetime.utcnow(),
            'likes': ['test2@test.com', 'test1@test.com'],
            'dislikes': ['test3@test.com', 'test4@test.com']
        },
        'bookmark': True
    }
    loop.run_until_complete(do_insert(post))

print('\n______________________\n')


async def do_find():
    documentes = posts.find()
    async for doc in documentes:
        pprint.pprint(doc)
        print('*************')


loop.run_until_complete(do_find())
