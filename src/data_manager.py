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

def new_expense(name, amount, status, necessary, category, created_date, updated_date):
    """Add the new expense to the database."""

    cursor.execute(
        "INSERT INTO expenses (name, amount, status, necessary, category, created_date, updated_date) VALUES (?, ?, ?, ?, ?)",
        (name, amount, status, necessary, category, created_date, updated_date)
    )

    conn.commit()

def update_expense(expense_id, name, amount, status, necessary, category, updated_date):
    """Update an existing expense."""

    arguments_list = [expense_id, name, amount, status, necessary, category, updated_date]
    new_arguments_list = []

    # Added comma to expense_id tuple to make the parentheses a tuple
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense_row = cursor.fetchone()

    for number, column in enumerate(arguments_list):
        argument_value = expense_row[number] # Fetch current value
        if expense_row[number] != column: # Compare with new value
            argument_value = column # If new value is different, make it the new value

        # Append the new value to a list to be fed into the INSERT later
        new_arguments_list.append(argument_value)

    cursor.execute(
        "INSERT INTO expenses(id, name, amount, status, necessary, category, updated_date) "
        "VALUES(?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(id) "
        "DO UPDATE SET "
            "name = excluded.name, "
            "amount = excluded.amount, "
            "status = excluded.status, "
            "necessary = excluded.necessary, "
            "category = excluded.category, "
            "updated_date = excluded.updated_date",
        tuple(new_arguments_list)
    )
