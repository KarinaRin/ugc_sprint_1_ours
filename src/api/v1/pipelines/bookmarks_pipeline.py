class BookmarksPipline:
    """Provider of mongo pipline"""
    @staticmethod
    def all_user_bookmarks(user_email):
        return [
            # Match the documents possible
            {"$match": {"email": user_email, "bookmark": True}},
        ]
