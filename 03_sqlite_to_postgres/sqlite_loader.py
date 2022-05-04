import sqlite3
from logging import getLogger

from postgres_dataclasses import FilmWork, Genre, Person, \
    GenreFilmwork, PersonFilmWork


class SQLiteLoader:
    def __init__(self, connection):
        self._connection = connection
        self._logger = getLogger()

    def get_data_sqlite(self, table: str):
        """Основной метод получения данных и таблиц SQLite"""
        try:
            self._connection.row_factory = sqlite3.Row
            _curs = self._connection.cursor()
            _curs.execute(f"SELECT * FROM {table};")  # noqa: S608
            data = _curs.fetchall()
            return data
        except Exception as exception:
            self._logger.error(exception)

    def load_filmworks(self, table: str):
        """Выгрузка фильмов из SQLite в dataclass"""
        data = self.get_data_sqlite(table)
        film_works = []
        for elem in data:
            film_works.append(FilmWork(
                title=elem['title'],
                description=elem['description'],
                creation_date=elem['creation_date'],
                created=elem['created_at'],
                type=elem['type'],
                modified=elem['updated_at'],
                rating=elem['rating'],
                id=elem['id']
            ))
        return film_works

    def load_genre(self, table: str):
        """Выгрузка жанров из SQLite в dataclass"""
        data = self.get_data_sqlite(table)
        genres = []
        for elem in data:
            genres.append(Genre(
                name=elem['name'],
                description=elem['description'],
                created=elem['created_at'],
                modified=elem['updated_at'],
                id=elem['id']
            ))
        return genres

    def load_person(self, table: str):
        """Выгрузка актеров из SQLite в dataclass"""
        data = self.get_data_sqlite(table)
        persons = []
        for elem in data:
            persons.append(Person(
                full_name=elem['full_name'],
                created=elem['created_at'],
                modified=elem['updated_at'],
                id=elem['id']
            ))
        return persons

    def load_genre_filmwork(self, table: str):
        """Выгрузка промежуточной таблицы жанров
        и фильмов из SQLite в dataclass"""
        data = self.get_data_sqlite(table)
        genre_filmworks = []
        for elem in data:
            genre_filmworks.append(GenreFilmwork(
                created=elem['created_at'],
                film_work_id=elem['film_work_id'],
                genre_id=elem['genre_id'],
                id=elem['id']
            ))
        return genre_filmworks

    def load_person_filmwork(self, table: str):
        """Выгрузка промежуточной таблицы актеров
        и фильмов из SQLite в dataclass"""
        data = self.get_data_sqlite(table)
        person_filmworks = []
        for elem in data:
            person_filmworks.append(PersonFilmWork(
                role=elem['role'],
                created=elem['created_at'],
                film_work_id=elem['film_work_id'],
                person_id=elem['person_id'],
                id=elem['id']
            ))
        return person_filmworks
