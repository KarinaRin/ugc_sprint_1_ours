class BookmarksPipline:
    """Provider of mongo pipline"""
    @staticmethod
    def all_user_bookmarks(user_email):
        return [
            # Match the documents possible
            {"$match": {"email": user_email, "bookmark": True}},

            # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {
                    "film_id": "$film_id",
                    "bookmark": "$bookmark"
                }
            }}
        ]
