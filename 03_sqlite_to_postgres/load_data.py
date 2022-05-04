import os
import sqlite3
from logging import getLogger

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_dataclasses import FilmWork, Genre, PersonFilmWork, \
    Person, GenreFilmwork
from postres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection,
                     pg_conn: _connection, logger):
    """Основной метод загрузки данных из SQLite в Postgres"""
    try:
        postgres_saver = PostgresSaver(pg_conn)
        sqlite_loader = SQLiteLoader(connection)
        film_works = sqlite_loader.load_filmworks('film_work')
        genres = sqlite_loader.load_genre('genre')
        persons = sqlite_loader.load_person('person')
        genres_film_works = sqlite_loader.load_genre_filmwork(
            'genre_film_work'
        )
        person_film_works = sqlite_loader.load_person_filmwork(
            'person_film_work'
        )
        data = {
            'film_work': [film_works, FilmWork],
            'genre': [genres, Genre],
            'person': [persons, Person],
            'genre_film_work': [genres_film_works, GenreFilmwork],
            'person_film_work': [person_film_works, PersonFilmWork],
        }
        for key, value in data.items():
            postgres_saver.save_all_data(key, value[0], value[1])
        return data
    except Exception as exception:
        logger.error(exception)


if __name__ == '__main__':
    logger = getLogger()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    with sqlite3.connect(os.environ.get('DB_FILE')) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn, logger)
