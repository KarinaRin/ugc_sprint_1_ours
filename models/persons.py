import uuid

from pydantic import BaseModel


class PersonFilm(BaseModel):
    uuid: uuid.UUID
    title: str
    role: list[str]


class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    films: list[PersonFilm]


class PersonListResponse(BaseModel):
    uuid: uuid.UUID
    full_name: str
    films: list[PersonFilm]


class PersonFilmResponse(BaseModel):
    uuid: uuid.UUID
    title: str
    rating: float
