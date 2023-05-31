import uuid
from typing import List

from pydantic import BaseModel


class BookmarkResponse(BaseModel):
    film_id: uuid.UUID
    email: str
    bookmark: bool


class BookmarkResponseAll(BaseModel):
    film_id: uuid.UUID
    bookmark: bool

