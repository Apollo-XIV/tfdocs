import os
import sqlite3
import logging
from tfdocs.db import DB_URL
from typing import Tuple

log = logging.getLogger(__name__)

class Db:
    _connection: sqlite3.Connection | None = None
    _db_url: str = DB_URL

    def __init__(self):
        self.cx = self.get_connection()
        self.cursor = self.cx.cursor()

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._connection is None:
            cls._connection = sqlite3.connect(cls._db_url)
            log.debug("initialising new cx to "+ cls._db_url)
        else:
            log.debug("reusing cx" + cls._db_url)
        return cls._connection

    def sql(self, query: str, params: Tuple | None = None):
        if params is None:
            log.debug(f"executing query: {query}\nwith_params: {query}")
            return self.cursor.execute(query)
        log.debug(f"executing query {query}")
        return self.cursor.execute(query, params)

    def clear(self) -> "Db":
        cursor = self.cursor
        try:
            cursor.executescript(
                """
                PRAGMA foreign_keys = OFF;
                BEGIN TRANSACTION;
                DELETE FROM block;
                DELETE FROM attribute;
                COMMIT;
                PRAGMA foreign_keys = ON;
            """
            )
            log.debug(f"Emptied the database {self._db_url}")
        except Exception as e:
            log.error(f"Encountered an issue while clearing the table")
        return self

    @classmethod
    def delete(cls):
        file_path = cls._db_url
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"{file_path} deleted successfully.")
        else:
            log.info(f"DB '{file_path}' doesn't exist")
