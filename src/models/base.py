import uuid
from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    email: str
    film_id: uuid.UUID
    likes: Optional[int]
    review: dict
    bookmark: bool
