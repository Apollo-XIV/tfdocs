import os
import time
import sqlite3
import asyncio
import pytest
import time
from unittest import mock

from tfdocs.db import TEST_DB_URL
from tfdocs.db.init import create_db, main
from tfdocs.db.test_handler import MockDb


class WrappedDb(MockDb):
    _connection = None
    _db_url = ".wrapped.db"


def test_main():
    with mock.patch("tfdocs.db.init.Db") as mock_db:
        mock_db = WrappedDb()
        with mock.patch("tfdocs.db.init.create_db") as mock_create_db:
            main()
            mock_create_db.assert_called_once()
        mock_db.delete()


def test_db_creation():
    test_db = MockDb()
    create_db(test_db.cursor)
    res = test_db.cursor.execute(
        "SELECT * FROM sqlite_master WHERE type='table' AND name IN ('block', 'attribute');"
    ).fetchall()
    test_db.cursor.close()
    assert len(res) == 2
