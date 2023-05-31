import uuid
from typing import Optional

from pydantic import BaseModel


class FilmAverageRatingResponse(BaseModel):
    film_id: uuid.UUID
    average_movie_rating: float


class FilmLikesDislikesResponse(BaseModel):
    film_id: uuid.UUID
    likes: int
    dislikes: int


class LikeChangeModel(BaseModel):
    film_id: uuid.UUID
    like: Optional[int]


class FilmChangeLikeResponse(BaseModel):
    email: str
    film_id: uuid.UUID
    likes: Optional[int]
    review: dict
    bookmark: bool
