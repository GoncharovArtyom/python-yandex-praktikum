from typing import List

from dataclasses import dataclass

from movies_api.domain.actor import Actor
from movies_api.domain.writer import Writer


@dataclass
class ShortMovie:
    id: str
    title: str
    imdb_rating: float


@dataclass
class Movie:
    id: str
    title: str
    description: str
    imdb_rating: float
    writers: List[Writer]
    actors: List[Actor]
    genre: List[str]
    director: List[str]
