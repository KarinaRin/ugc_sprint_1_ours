import uuid
from typing import Optional

from pydantic import BaseModel


class Review(BaseModel):
    text: str
    created: int
    likes: list = []
    dislikes: list = []


class ReviewListForUser(Review):
    film_id: uuid.UUID


class ReviewListForFilm(Review):
    email: str


class ReviewResponse(BaseModel):
    email: str
    film_id: uuid.UUID
    likes: Optional[int]
    review: Review
    bookmark: bool


class ReviewsListToFilm(BaseModel):
    film_id: uuid.UUID
    review: ReviewListForFilm


class ReviewsListToUser(BaseModel):
    email: str
    review: ReviewListForUser


class ReviewAdd(BaseModel):
    film_id: uuid.UUID
    text: str
