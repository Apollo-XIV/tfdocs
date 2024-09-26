import pytest
from tfdocs.db import TEST_DB_URL
from tfdocs.db.handler import Db


class MockDb(Db):
    _connection = None
    _db_url: str = TEST_DB_URL

    def __init__(self):
        super().__init__()


@pytest.fixture(scope="function")
def test_db():
    return MockDb()


def test_singleton():
    db_cx_1 = MockDb()
    db_cx_2 = MockDb()
    assert db_cx_1.cx is db_cx_2.cx


def test_sql_method():
    exp_count = 8
    test_count = MockDb().sql("SELECT COUNT(*) FROM block;").fetchone()[0]
    assert exp_count == test_count


def test_context_manager():
    test_db = MockDb()
    cx_1 = None
    cx_2 = None
    with test_db.cx as cx:
        cx_1 = cx
        test = cx.execute("SELECT COUNT(*) FROM block;").fetchone()[0]
        exp = 8
        assert exp == test
    with test_db.cx as cx:
        cx_2 = cx
        test = cx.execute("SELECT COUNT(*) FROM attribute;").fetchone()[0]
        exp = 54
        assert exp == test
    assert cx_1 is cx_2
