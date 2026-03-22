import sqlite3

# Connect (creates file if it doesn't exist)
conn = sqlite3.connect("src/expenses.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        amount      REAL    NOT NULL,
        category    TEXT,
        date        TEXT    NOT NULL
    )
""")
conn.commit()

def save_new_expense(description, amount, necessity, category, date):
    """Add the new expense to the database."""

    cursor.execute(
        "INSERT INTO expenses (name, amount, necessity, category, date) VALUES (?, ?, ?, ?, ?)",
        (description, amount, necessity, category, date)
    )

    conn.commit()
