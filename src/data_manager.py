import sqlite3

# Connect (creates file if it doesn't exist)
conn = sqlite3.connect("src/expenses.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        amount      REAL    NOT NULL,
        status      TEXT    NOT NULL,
        category    TEXT,
        necessary   TEXT    NOT NULL,
        created_date        TEXT    NOT NULL,
        updated_date        TEXT    NOT NULL,
    )
""")
conn.commit()

def new_expense(description, amount, status, necessary, category, created_date, updated_date):
    """Add the new expense to the database."""

    cursor.execute(
        "INSERT INTO expenses (name, amount, status, necessary, category, created_date, updated_date) VALUES (?, ?, ?, ?, ?)",
        (description, amount, status, necessary, category, created_date, updated_date)
    )

    conn.commit()

def update_expense(expense, description, amount, status, necessary, category, updatedAt):
    """Update an existing expense."""

    cursor.execute(
        ""
    )
