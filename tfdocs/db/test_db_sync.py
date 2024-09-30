import asyncio
import sqlite3
import pytest
from tfdocs.db import TEST_DB_URL
from tfdocs.db.test_handler import MockDb
from tfdocs.db.sync import parse_schemas


async def fetch_test_schemas() -> asyncio.StreamReader:
    print()
    process = await asyncio.subprocess.create_subprocess_exec(
        *["cat", "tests/test_schemas.json"],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    if process.stdout is None:
        raise OSError("Couldn't fetch the test data to parse")
    return process.stdout


@pytest.mark.asyncio
async def test_db_sync():
    with MockDb().cx as cx:
        cursor = cx.cursor()
        await parse_schemas(cursor, await fetch_test_schemas())

        # Verify the block table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='block';"
        )
        assert cursor.fetchone() is not None, "Block table was not created"

        # Verify the attribute table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='attribute';"
        )
        assert cursor.fetchone() is not None, "Attribute table was not created"

        # Verify columns in block table
        cursor.execute("PRAGMA table_info(block);")
        block_columns = [info[1] for info in cursor.fetchall()]
        expected_block_columns = [
            "block_id",
            "block_type",
            "block_name",
            "parent_path",
        ]
        for col in expected_block_columns:
            assert col in block_columns, f"Column '{col}' is missing from block table"

        # Verify columns in attribute table
        cursor.execute("PRAGMA table_info(attribute);")
        attribute_columns = [info[1] for info in cursor.fetchall()]
        expected_attribute_columns = [
            "attribute_id",
            "attribute_type",
            "attribute_name",
            "description",
            "description_type",
            "optional",
            "computed",
            "block_id",
        ]
        for col in expected_attribute_columns:
            assert (
                col in attribute_columns
            ), f"Column '{col}' is missing from attribute table"
