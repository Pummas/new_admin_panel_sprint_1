import sqlite3
from logging import getLogger


def format_fields(elem: dict) -> dict:
    """Функция, исправляющая поля в датаклассах
    для корректной передачи в PostgeSQL"""
    if "created_at" in elem:
        elem["created"] = elem["created_at"]
        del (elem["created_at"])
    if "updated_at" in elem:
        elem["modified"] = elem["updated_at"]
        del (elem["updated_at"])
    if "file_path" in elem:
        del (elem["file_path"])
    return elem


class SQLiteLoader:
    def __init__(self, connection):
        self._connection = connection
        self._logger = getLogger()
        self.batch_size = 100

    def _dict_factory(self, cursor, row):
        """Метод для извлечения данных в формате dict из SQLite """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_data_sqlite(self, table: str):
        """Основной метод получения данных и таблиц SQLite"""
        try:
            self._connection.row_factory = self._dict_factory
            _curs = self._connection.cursor()
            try:
                _curs.execute(f"SELECT * FROM {table};")  # noqa: S608
            except sqlite3.Error as e:
                raise e
            while True:
                rows = _curs.fetchmany(size=self.batch_size)
                if not rows:
                    return
                yield from rows
        except Exception as exception:
            self._logger.error(exception)

    def format_dataclass_data(self, table: str, dataclass):
        """Метод для прокидывания данных в датакласс"""
        data = self.get_data_sqlite(table)
        return [dataclass(**format_fields(elem)) for elem in data]
