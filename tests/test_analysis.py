import sqlite3
import pytest
from datetime import date

import src.analysis as analysis


@pytest.fixture
def temp_database(tmp_path, monkeypatch):
    """Fixture that builds a temporary database and yields the connection before closing."""

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

    # Monkeypatch the analysis.py conn with the local conn
    monkeypatch.setattr(
        analysis, "conn", conn
    )
    # Apply the same monkeypatch to cursor
    monkeypatch.setattr(
        analysis, "cursor", cursor
    )

    yield conn

    conn.close()


# Test unit: _build_daily_df

# First test case: multiple normal expenses in same category
# We will use already established expense rows so they can be reused
def test_build_daily_df_two_expenses_same_day_are_summed(temp_database):
    cursor = temp_database.cursor()

    cursor.executemany(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("Coffee", 10, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
            ("Burger", 40, "done", "food", 1, "2026-04-29 12:00:00.000000", "2026-04-29 12:00:00.000000")
        ]
    )

    temp_database.commit()

    df = analysis._build_daily_df(time_window=31)

    assert len(df) == 1
    assert df.loc[0, "Amount"] == 50.0

# Multiple normal expenses on different days 
def test_build_daily_df_two_expenses_different_days_not_summed(temp_database):
    cursor = temp_database.cursor()

    cursor.executemany(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("Coffee", 10, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
            ("Burger", 40, "done", "food", 1, "2026-04-30 12:00:00.000000", "2026-04-30 12:00:00.000000")
        ]
    )

    temp_database.commit()

    df = analysis._build_daily_df(time_window=31)

    assert len(df) == 2
    assert df.loc[0, "Amount"] == 10.0

# Expense that didn't cost anything
def test_build_daily_df_with_free_expense(temp_database):
    cursor = temp_database.cursor()

    cursor.execute(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Coffee", 0, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
    )

    temp_database.commit()

    df = analysis._build_daily_df(time_window=31)

    assert len(df) == 1
    assert df.loc[0, "Amount"] == 0

# Expense exactly on the boundary date
def test_build_daily_df_expense_with_boundary_date(temp_database):
    cursor = temp_database.cursor()

    cursor.execute(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Coffee", 10, "done", "food", 0, "2026-03-30 00:00:00.000000", "2026-03-30 00:00:00.000000"),
    )

    temp_database.commit()

    df = analysis._build_daily_df(time_window=31)

    assert len(df) == 1
    assert df.loc[0, "Date"] == date(2026, 3, 30)