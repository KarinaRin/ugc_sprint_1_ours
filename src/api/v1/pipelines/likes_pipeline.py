class LikesPipline:
    ''"Provider of mongo pipline"""

    @staticmethod
    def likes_dislikes_pipeline(film_id):
        return [
            # Match the documents possible
            {"$match": {"film_id": film_id}},

            # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {
                    "film_id": "$film_id",
                    "likes": "$likes"
                },
                'count': {"$sum": 1},
            }}
        ]

    @staticmethod
    def average_rating_pipeline(film_id):
        return [
            # Matchn the documents possible
            {"$match": {"film_id": film_id}},

            # # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {
                    "film_id": "$film_id",
                },
                'average_movie_rating': {"$avg": "$likes"}
            }}
        ]
