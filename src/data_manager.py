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

# C from CRUD
def new_expense(name, amount, status, necessary, category, created_date, updated_date):
    """Add the new expense to the database."""

    cursor.execute(
        "INSERT INTO expenses (name, amount, status, necessary, category, created_date, updated_date) VALUES (?, ?, ?, ?, ?)",
        (name, amount, status, necessary, category, created_date, updated_date)
    )

    conn.commit()

# R from CRUD
def read_expense(expense_id):
    """Read an expense by ID."""

    cursor.execute(
        "SELECT * FROM expenses WHERE id = ?", (expense_id,)
    )
    expense_row = cursor.fetchone()

    if expense_row is None:
        print("Expense not found.")
        return

    column_names = [description[0] for description in cursor.description]

    print(f"{expense_row[1]}\n")

    for name, value in zip(column_names, expense_row):
        print(f"- {name}: {value}")

# U from CRUD
def update_expense(expense_id, name, amount, status, category, necessary, updated_date):
    """Update an existing expense."""

    arguments_list = [expense_id, name, amount, status, category, necessary, None, updated_date]
    new_arguments_list = []

    # Added comma to expense_id tuple to make the parentheses a tuple
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense_row = cursor.fetchone()

    for number, column in enumerate(arguments_list):
        argument_value = expense_row[number] # Fetch current value
        if expense_row[number] != column and column is not None: # Compare with new value
            argument_value = column # If new value is different, make it the new value

        # Append the new value to a list to be fed into the INSERT later
        new_arguments_list.append(argument_value)

    cursor.execute(
        "INSERT INTO expenses(id, name, amount, status, category, necessary, created_date, updated_date) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(id) "
        "DO UPDATE SET "
            "name = excluded.name, "
            "amount = excluded.amount, "
            "status = excluded.status, "
            "necessary = excluded.necessary, "
            "category = excluded.category, "
            "created_date = excluded.created_date, "
            "updated_date = excluded.updated_date",
        tuple(new_arguments_list)
    )

    conn.commit()

# D from CRUD
def delete_expense(expense_id):
    """Delete an existing expense from the tracker."""

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    conn.commit()

def list_expenses(start_date, end_date, category, necessary):
    """List all the expenses within the specified timeframe."""

    # SELECT all expenses where created_time < end_date and > start_date, and that possibly belongs to the same category or necessary
    # Fetch all these expenses
    # Display all info briefly using read_expense
