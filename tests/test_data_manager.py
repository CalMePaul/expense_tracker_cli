import sqlite3
import pytest

import src.data_manager as data_manager

@pytest.fixture
def temp_database(tmp_path, monkeypatch):
    """Create a temporary sqlite database for pure testing purposes."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            status      TEXT    NOT NULL,
            category    TEXT,
            necessity   TEXT    NOT NULL,
            creation_date   TEXT    NOT NULL,
            update_date     TEXT    NOT NULL
        )
    """)
    conn.commit()

    monkeypatch.setattr(data_manager, "conn", conn) # Replace data manager conn with fake conn
    monkeypatch.setattr(data_manager, "cursor", cursor) # Same for cursor

    yield conn # Yield upholds the function while the database is being accessed

    conn.close()
