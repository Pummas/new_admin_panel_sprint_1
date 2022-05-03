import os
import sqlite3
import psycopg2
import pytest
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import datetime
import postgres_dataclasses

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}


class TestDataSQL:

    @pytest.fixture
    def connect(self):
        with sqlite3.connect(os.environ.get('DB_FILE')) as sqlite_conn, \
                psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            yield sqlite_conn, pg_conn

    def test_assert_film_work(self, connect):
        """Тест проверяющий наличие фильма из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = postgres_dataclasses.FilmWork(
            id='145524fb-6c49-45c7-ade3-ec430355a3ca',
            title='2-Star',
            description='After finding each other through '
                        'an on-line dating site, '
                        'Sara and Derek meet in a Los Angeles hotel for an '
                        'adult rendezvous only to discover '
                        'they have far more in common than meets the eye.',
            rating=7.4,
            type='movie',
            creation_date=None,
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 265500,
                tzinfo=datetime.timezone.utc
            ),
            modified=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 265516,
                tzinfo=datetime.timezone.utc
            ),
        )
        cursor.execute(f"SELECT * FROM content.film_work "  # noqa: S608
                       f"WHERE id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = postgres_dataclasses.FilmWork(
            title=data['title'],
            description=data['description'],
            creation_date=data['creation_date'],
            created=data['created'],
            type=data['type'],
            modified=data['modified'],
            rating=data['rating'],
            id=data['id']
        )
        assert row_sqlite == row_postgres_data

    def test_assert_genre(self, connect):
        """Тест проверяющий наличие жанра из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = postgres_dataclasses.Genre(
            id='237fd1e4-c98e-454e-aa13-8a13fb7547b5',
            name='Romance',
            description=None,
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 310057,
                tzinfo=datetime.timezone.utc
            ),
            modified=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 310073,
                tzinfo=datetime.timezone.utc
            ),
        )
        cursor.execute(f"SELECT * FROM content.genre "  # noqa: S608
                       f"WHERE id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = postgres_dataclasses.Genre(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            created=data['created'],
            modified=data['modified'],
        )
        assert row_sqlite == row_postgres_data

    def test_assert_person(self, connect):
        """Тест проверяющий наличие актера из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = postgres_dataclasses.Person(
            full_name='Steve Stamatiadis',
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 331792,
                tzinfo=datetime.timezone.utc
            ),
            modified=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 331811,
                tzinfo=datetime.timezone.utc
            ),
            id='c098fec8-851b-4946-b6bc-c1142236ed12'
        )
        cursor.execute(f"SELECT * FROM content.person "  # noqa: S608
                       f"WHERE id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = postgres_dataclasses.Person(
            full_name=data['full_name'],
            created=data['created'],
            modified=data['modified'],
            id=data['id']
        )
        assert row_sqlite == row_postgres_data

    def test_assert_genre_film_work(self, connect):
        """Тест проверяющий наличие промежуточных данных
        из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = postgres_dataclasses.GenreFilmwork(
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 582707,
                tzinfo=datetime.timezone.utc
            ),
            film_work_id='2b7bde28-9d77-49c7-ae05-1baa6e8df2d4',
            genre_id='1cacff68-643e-4ddd-8f57-84b62538081a',
            id='73641115-7f75-451e-a49d-9019d2da880d',
        )
        cursor.execute(f"SELECT * FROM content.genre_film_work "  # noqa: S608
                       f"WHERE id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = postgres_dataclasses.GenreFilmwork(
            created=data['created'],
            film_work_id=data['film_work_id'],
            genre_id=data['genre_id'],
            id=data['id'],

        )
        assert row_sqlite == row_postgres_data

    def test_assert_person_film_work(self, connect):
        """Тест проверяющий наличие промежуточных данных
                из SQLite в PostgreSQl"""
        connection, pg_conn = connect
        cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        row_sqlite = postgres_dataclasses.PersonFilmWork(
            created=datetime.datetime(
                2021, 6, 16, 20, 14, 9, 704139,
                tzinfo=datetime.timezone.utc
            ),
            film_work_id='2b7bde28-9d77-49c7-ae05-1baa6e8df2d4',
            person_id='866ada31-ac09-48cd-85db-56bf27d01069',
            id='d51d4f87-d13c-41f9-a7ad-fe5f12e75b7a',
            role='director'
        )
        cursor.execute(f"SELECT * FROM content.person_film_work "  # noqa: S608
                       f"WHERE id = '{row_sqlite.id}'")
        data = cursor.fetchone()
        row_postgres_data = postgres_dataclasses.PersonFilmWork(
            created=data['created'],
            film_work_id=data['film_work_id'],
            person_id=data['person_id'],
            id=data['id'],
            role=data['role']

        )
        assert row_sqlite == row_postgres_data

    def test_number_records(self, connect):
        """Тест проверяющий количество записей SQLite и PostgreSQl"""
        connection, pg_conn = connect
        sqlite_cursor = connection.cursor()
        pg_cursor = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sqlite_cursor.execute(
            "SELECT count(*) FROM film_work"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.film_work"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM genre"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.genre"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM person"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.person"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM genre_film_work"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.genre_film_work"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
        sqlite_cursor.execute(
            "SELECT count(*) FROM person_film_work"
        )
        pg_cursor.execute(
            "SELECT count(*) FROM content.person_film_work"
        )
        assert sqlite_cursor.fetchone()[0] == pg_cursor.fetchone()[0]
