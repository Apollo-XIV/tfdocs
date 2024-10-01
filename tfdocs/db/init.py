# file for initializing the database.async def create_db(cursor: sqlite3.Cursor, cx: sqlite3.Connection) -> None:
import asyncio
import sqlite3
from sqlite3 import Cursor, Connection
from rich import print
from rich.prompt import Confirm
import logging

from tfdocs.db import DB_URL
from tfdocs.db.handler import Db
from .tables import create_block_table, create_attribute_table


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
        log.warning("Existing Table Found")
        # ask if user would like to delete and remake the database, else exit 1

        if Confirm.ask("The requested database already exists, would you like to delete and create a new one?"):
            print("deleting")
            
        else:
            log.critical("Cannot procede with existing database")
        return
    log.info("Creating tables in new DB")
    create_block_table(cursor)
    create_attribute_table(cursor)
    print(f"[green]created new local cache")
