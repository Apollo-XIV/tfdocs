import os
import sqlite3
from tfdocs.db import DB_URL
from typing import Tuple


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
        #     print("initialising new cx to "+ cls._db_url)
        # else:
        #     print("reusing cx" + cls._db_url)
        return cls._connection

    def sql(self, query: str, params: Tuple | None = None):
        if params is None:
            return self.cursor.execute(query)
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
            print("Emptied the table")
        except Exception as e:
            print("Couldn't confirm empty table")
        return self

    @classmethod
    def delete(cls):
        file_path = cls._db_url
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"{file_path} deleted successfully.")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
