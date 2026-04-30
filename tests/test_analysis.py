import sqlite3
import pytest

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
    """Test whether two expenses the same day are summed (length of df, amount)."""
    cursor = temp_database.cursor()

    # Execute the SQL code for each iteration of the list provided as a collection of arguments.
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
    # Use df.loc to access the 0 row's "Amount" column (int)
    assert df.loc[0, "Amount"] == 50.0

# Multiple normal expenses on different days
def test_build_daily_df_two_expenses_different_days_not_summed(temp_database):
    """Test whether two expenses on different days are not summed (length of df, amount)."""
    cursor = temp_database.cursor()

    # Execute the SQL code for each iteration of the list provided as a collection of arguments.
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
    # Use df.loc to access the 0 row's "Amount" column (int)
    assert df.loc[0, "Amount"] == 10.0

# Expense that didn't cost anything
def test_build_daily_df_with_free_expense(temp_database):
    """Test whether a free expense gets added properly to the df."""
    cursor = temp_database.cursor()

    # Execute the SQL code with the provided arguments.
    cursor.execute(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Coffee", 0, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
    )

    temp_database.commit()

    df = analysis._build_daily_df(time_window=31)

    assert len(df) == 1
    # Use df.loc to access the 0 row's "Amount" column (int)
    assert df.loc[0, "Amount"] == 0

# Expense outside of boundary date
def test_build_daily_df_expense_outside_boundary_date_is_excluded(temp_database):
    """Test whether an expense outside of the boundary date is excluded of the dataframe."""
    cursor = temp_database.cursor()

    # Execute the SQL code with the provided arguments.
    cursor.execute(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Coffee", 10, "done", "food", 0, "2026-03-29 00:00:00.000000", "2026-03-29 00:00:00.000000"),
    )

    temp_database.commit()

    df = analysis._build_daily_df(time_window=31)

    assert len(df) == 0


# Unit test for _build_category_df

# Multiple normal expenses in same category
def test_build_category_df_two_expenses_same_category_are_summed(temp_database):
    """Test whether two expenses of the same category are summed (length of df, amount)."""
    cursor = temp_database.cursor()

    # Execute the SQL code for each iteration of the list provided as a collection of arguments.
    cursor.executemany(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("Coffee", 10, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
            ("Burger", 40, "done", "food", 1, "2026-04-29 12:00:00.000000", "2026-04-29 12:00:00.000000")
        ]
    )

    temp_database.commit()

    df = analysis._build_category_df(time_window=31)

    assert len(df) == 1
    # Use df.loc to access the 0 row's "Amount" column (int)
    assert df.loc[0, "Amount"] == 50.0

# Multiple normal expenses in different categories
def test_build_category_df_two_expenses_different_categories_not_summed(temp_database):
    """Test whether two expenses in different categories are not summed (length of df, amount)."""
    cursor = temp_database.cursor()

    # Execute the SQL code for each iteration of the list provided as a collection of arguments.
    cursor.executemany(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("Coffee", 10, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
            ("Netflix", 40, "done", "entertainment", 1, "2026-04-29 12:00:00.000000", "2026-04-29 12:00:00.000000")
        ]
    )

    temp_database.commit()

    df = analysis._build_category_df(time_window=31)

    assert len(df) == 2
    # Use df.loc to access the 0 row's "Amount" column (int)
    assert df.loc[0, "Amount"] == 10.0

# Expense with amount = 0
def test_build_category_df_with_free_expense(temp_database):
    """Test whether a free expense gets properly registered in df (1 row, but no amount shown)."""
    cursor = temp_database.cursor()

    # Execute the SQL code with the provided arguments.
    cursor.execute(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Coffee", 0, "done", "food", 0, "2026-04-29 10:00:00.000000", "2026-04-29 10:00:00.000000"),
    )

    temp_database.commit()

    df = analysis._build_category_df(time_window=31)

    assert len(df) == 1
    # Use df.loc to access the 0 row's "Amount" column (int)
    assert df.loc[0, "Amount"] == 0

# Expense outside of boundary date
def test_build_category_df_expense_outside_boundary_date_is_excluded(temp_database):
    """Test whether an expense outside of the boundary date is excluded of the dataframe."""
    cursor = temp_database.cursor()

    # Execute the SQL code with the provided arguments.
    cursor.execute(
        "INSERT INTO expenses (name, amount, status, category, necessity, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Coffee", 10, "done", "food", 0, "2026-03-29 00:00:00.000000", "2026-03-29 00:00:00.000000"),
    )

    temp_database.commit()

    df = analysis._build_category_df(time_window=31)

    assert len(df) == 0
