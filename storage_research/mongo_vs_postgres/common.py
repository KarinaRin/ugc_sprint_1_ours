from enum import Enum

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB = "research"

USERS_COUNT = 1_000_000
MOVIES_COUNT = 10_000


class Collections(str, Enum):
    reviews = "reviews"
    likes = "likes"
    bookmarks = "bookmarks"