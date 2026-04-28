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

    monkeypatch.setattr(
        data_manager, "conn", conn
    )  # Replace data manager conn with fake conn
    monkeypatch.setattr(data_manager, "cursor", cursor)  # Same for cursor

    yield conn  # Yield upholds the function while the database is being accessed

    conn.close()


# Unit tests covering the new_expense function
def test_new_expense_for_correct_values(temp_database):
    """Test if a normal entry of a Claude subscription would get registered in the database."""
    expense = {
        "name": "Claude monthly subscription",
        "amount": 20.0,
        "status": "DONE",
        "category": "Productivity",
        "necessity": "False",
        "creation_date": "2026-01-01",
        "update_date": "2026-01-01",
    }

    data_manager.new_expense(**expense)

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (1,))

    subscription_row = cursor.fetchone()

    assert subscription_row[1] == expense["name"]  # Check for same name
    assert subscription_row[2] == expense["amount"]  # Check for same amount
    assert subscription_row[3] == expense["status"]
    assert subscription_row[4] == expense["category"]
    assert subscription_row[5] == expense["necessity"]
    assert subscription_row[6] == expense["creation_date"]
    assert subscription_row[7] == expense["update_date"]


def test_autoincrement_after_few_expenses(temp_database):
    """Test that IDs autoincrement correctly after multiple inserts."""
    expenses = [
        {
            "name": "Shoes",
            "amount": 150.0,
            "status": "DONE",
            "category": "Clothing",
            "necessity": "True",
            "creation_date": "2026-01-01",
            "update_date": "2026-01-01",
        },
        {
            "name": "Burger",
            "amount": 12.0,
            "status": "DONE",
            "category": "Food",
            "necessity": "True",
            "creation_date": "2026-01-02",
            "update_date": "2026-01-02",
        },
        {
            "name": "Toothpaste",
            "amount": 5.0,
            "status": "DONE",
            "category": "Hygiene",
            "necessity": "True",
            "creation_date": "2026-01-03",
            "update_date": "2026-01-03",
        },
        {
            "name": "Bike pedals",
            "amount": 40.0,
            "status": "DONE",
            "category": "Sport",
            "necessity": "False",
            "creation_date": "2026-01-04",
            "update_date": "2026-01-04",
        },
        {
            "name": "Book",
            "amount": 25.0,
            "status": "DONE",
            "category": "Education",
            "necessity": "False",
            "creation_date": "2026-01-05",
            "update_date": "2026-01-05",
        },
    ]

    for expense in expenses:
        data_manager.new_expense(**expense)

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()

    assert last_row[0] == 5


# Unit tests covering the test case of the update_expense function
def test_update_expense_name(temp_database):
    """Test that updating the name changes only the name."""
    data_manager.new_expense(
        "Old name", 20.0, "DONE", "True", "Food", "2026-01-01", "2026-01-01"
    )
    data_manager.update_expense(1, "New name", None, None, None, None, "2026-01-02")

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (1,))
    row = cursor.fetchone()

    assert row[1] == "New name"
    assert row[2] == 20.0  # amount unchanged


def test_update_expense_amount(temp_database):
    """Test that updating the amount changes only the amount."""
    data_manager.new_expense(
        "Shoes", 50.0, "DONE", "True", "Clothing", "2026-01-01", "2026-01-01"
    )
    data_manager.update_expense(1, None, 99.0, None, None, None, "2026-01-02")

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (1,))
    row = cursor.fetchone()

    assert row[2] == 99.0
    assert row[1] == "Shoes"  # name unchanged


def test_update_expense_category(temp_database):
    """Test that updating the category changes only the category."""
    data_manager.new_expense(
        "Book", 25.0, "DONE", "True", "Education", "2026-01-01", "2026-01-01"
    )
    data_manager.update_expense(
        1, None, None, None, "Entertainment", None, "2026-01-02"
    )

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (1,))
    row = cursor.fetchone()

    assert row[4] == "Entertainment"
    assert row[1] == "Book"  # name unchanged


# Unit tests covering the test case of the delete_expense function
def test_delete_expense_row_gone(temp_database):
    """Test that a deleted expense no longer exists in the database."""
    data_manager.new_expense(
        "Coffee", 3.0, "DONE", "True", "Food", "2026-01-01", "2026-01-01"
    )
    data_manager.delete_expense(1)

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (1,))
    row = cursor.fetchone()

    assert row is None


def test_delete_expense_other_id_unchanged(temp_database):
    """Test that deleting one row does not affect the ID of another."""
    data_manager.new_expense(
        "Coffee", 3.0, "DONE", "True", "Food", "2026-01-01", "2026-01-01"
    )
    data_manager.new_expense(
        "Burger", 12.0, "DONE", "True", "Food", "2026-01-02", "2026-01-02"
    )
    data_manager.delete_expense(1)

    cursor = temp_database.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (2,))
    row = cursor.fetchone()

    assert row[0] == 2


def test_delete_expense_wrong_id_no_crash(temp_database):
    """Test that deleting a non-existent ID does not raise an exception."""
    data_manager.new_expense(
        "Coffee", 3.0, "DONE", "True", "Food", "2026-01-01", "2026-01-01"
    )
    data_manager.delete_expense(999)
    assert True
