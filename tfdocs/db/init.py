# file for initializing the database.async def create_db(cursor: sqlite3.Cursor, cx: sqlite3.Connection) -> None:
import asyncio
import sqlite3
from sqlite3 import Cursor, Connection

from tfdocs.db import DB_URL
from tfdocs.db.handler import Db
from .tables import create_block_table, create_attribute_table
import logging


def main():
    with Db().cx as cx:
        cursor = cx.cursor()
        create_db(cursor)
        cursor.close()


def create_db(cursor: Cursor):
    log = logging.getLogger(__name__)
    # check if it already exists
    res = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='block';"
    ).fetchone()
    if res != None:
        log.error("Existing Table Found, please remove it to continue")
        return
    create_block_table(cursor)
    create_attribute_table(cursor)
