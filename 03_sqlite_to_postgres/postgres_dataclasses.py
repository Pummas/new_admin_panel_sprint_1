import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class FilmWork:
    title: str
    created: datetime.datetime
    modified: datetime.datetime
    creation_date: datetime.date = field(default=datetime.datetime.now())
    type: str = field(default="")
    description: str = field(default="")
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created: datetime.datetime
    modified: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    description: str
    created: datetime.datetime
    modified: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmwork:
    created: datetime.datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    role: str
    created: datetime.datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
