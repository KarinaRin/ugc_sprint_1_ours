import pprint
a = [{'_id': {'film_id': '155-15-515', 'likes': 10}, 'count': 5}, {'_id': {'film_id': '155-15-515', 'likes': 0}, 'count': 4}]

pprint.pprint(a)

response = None
if a:
    response = {
        'film_id': a[0]['_id']['film_id'],
        'likes': 0,
        'dislikes': 0
    }
    for item in a:
        if item['_id']['likes'] == 10:
            response['likes'] = item['count']
        else:
            response['dislikes'] = item['count']


a  = [{'_id': {'film_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'}, 'average_movie_rating': 5.0}]

response = None
if a:
    response = {
        'film_id': a[0]['_id']['film_id'],
        'average_movie_rating': None
    }
    response['average_movie_rating'] = a[0]['average_movie_rating']
print(response)
