import uuid
from typing import Optional

from pydantic import BaseModel


class Review(BaseModel):
    text: str
    created: int
    likes: list = []
    dislikes: list = []


class ReviewResponse(BaseModel):
    email: str
    film_id: uuid.UUID
    likes: Optional[int]
    review: Review
    bookmark: bool
