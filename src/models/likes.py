import uuid
from typing import Optional

from pydantic import BaseModel, Extra


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
    class Config:
        extra = Extra.allow


class FilmChangeLikeResponse(BaseModel):
    email: str
    film_id: uuid.UUID
    likes: Optional[int]
    review: dict
    bookmark: bool
