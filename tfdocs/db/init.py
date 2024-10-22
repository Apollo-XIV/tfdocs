# file for initializing the database.async def create_db(cursor: sqlite3.Cursor, cx: sqlite3.Connection) -> None:
import asyncio
import sqlite3
from sqlite3 import Cursor, Connection
from rich import print
from rich.prompt import Confirm
import logging
import time

from tfdocs.db import DB_URL
from tfdocs.db.handler import Db
from tfdocs.db.sync import load_local_schemas
from .tables import create_block_table, create_attribute_table

log = logging.getLogger()


def main():
    # open a connection to the DB
    with Db().cx as cx:
        cursor = cx.cursor()
        # instantiate with correct tables
        create_db(cursor)
        start = time.time()
        # run the cache generation functions
        asyncio.run(load_local_schemas(cursor))
        log.info("Finished building DB")
        cursor.close()
        # calculate how long it took and tell the user
        end = time.time()
        exec_time = end - start
        log.debug(f"Cache generated in {exec_time:.4f} seconds")
        print(f"[green]Cache Generation took {exec_time:.4f} seconds to execute.")


def create_db(cursor: Cursor):
    # check if it already exists
    res = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='block';"
    ).fetchone()
    if res != None:
        log.warning("Existing Table Found")
        # ask if user would like to delete and remake the database, else exit 1

        if Confirm.ask(
            "The requested database already exists, would you like to delete and create a new one?"
        ):
            print("[red]Deleting...")

        else:
            log.fatal("Cannot procede with existing database")
            exit(1)
    log.info("Creating tables in new DB")
    create_block_table(cursor)
    create_attribute_table(cursor)
    print(f"[green]Created new local cache")
