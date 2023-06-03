import random

import pymongo
from datetime import datetime, timedelta
import pprint
from bson.son import SON

client = pymongo.MongoClient('localhost', 27117)
db = client.UserGeneratedContent

collection = db.UsersContent
print('11111111111111111111', collection.index_information())


print('\n\nПросмотр средней пользовательской оценки фильма')

end_time = '2023-06-03 21:06'
start_time = '2023-06-03 00:56'


data = collection.find({
        'date':  {'$lte':  datetime.strptime(end_time, '%Y-%m-%d %H:%M'),
                  '$gt': datetime.strptime(start_time, '%Y-%m-%d %H:%M'),
                  }
    })

for d in data:
    print(d)
