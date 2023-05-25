import uuid
from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str
    description: Optional[str]
