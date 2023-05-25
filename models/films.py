import uuid
from typing import Optional

from pydantic import BaseModel


class FilmPerson(BaseModel):
    uuid: uuid.UUID
    full_name: str


class FilmGenre(BaseModel):
    uuid: uuid.UUID
    name: str


class Film(BaseModel):
    uuid: uuid.UUID
    imdb_rating: float
    genre: list[FilmGenre] = []
    title: str
    description: Optional[str]
    actors: list[FilmPerson] = []
    writers: list[FilmPerson] = []
    directors: list[FilmPerson] = []


class FilmResponse(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[FilmGenre] = []
    actors: list[FilmPerson] = []
    writers: list[FilmPerson] = []
    directors: list[FilmPerson] = []


class FilmListResponse(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: float
