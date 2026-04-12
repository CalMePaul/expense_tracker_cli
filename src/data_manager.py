import sqlite3
from rich.tree import Tree
from rich.padding import Padding
from rich import print

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
        necessity   TEXT    NOT NULL,
        creation_date   TEXT    NOT NULL,
        update_date     TEXT    NOT NULL
    )
""")
conn.commit()


# C from CRUD
def new_expense(name, amount, status, necessity, category, creation_date, update_date):
    """Add the new expense to the database."""

    cursor.execute(
        "INSERT INTO expenses (name, amount, status, necessity, category, creation_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, amount, status, necessity, category, creation_date, update_date),
    )

    conn.commit()


# R from CRUD
def read_expense(expense_id):
    """Read an expense by ID."""

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense_row = cursor.fetchone()

    if expense_row is None:
        print("Expense not found.")
        return

    column_names = [description[0] for description in cursor.description]

    tree = Tree(expense_row[1])
    for name, value in zip(column_names, expense_row):
        tree.add(f"{name}: {value}")
    print(Padding(tree, (0, 0, 0, 4)))


# U from CRUD
def update_expense(expense_id, name, amount, status, category, necessity, update_date):
    """Update an existing expense."""

    arguments_list = [
        expense_id,
        name,
        amount,
        status,
        category,
        necessity,
        None,
        update_date,
    ]
    new_arguments_list = []

    # Added comma to expense_id tuple to make the parentheses a tuple
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense_row = cursor.fetchone()

    for number, column in enumerate(arguments_list):
        argument_value = expense_row[number]  # Fetch current value
        if (
            expense_row[number] != column and column is not None
        ):  # Compare with new value
            argument_value = column  # If new value is different, make it the new value

        # Append the new value to a list to be fed into the INSERT later
        new_arguments_list.append(argument_value)

    cursor.execute(
        "INSERT INTO expenses(id, name, amount, status, category, necessity, creation_date, update_date) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(id) "
        "DO UPDATE SET "
        "name = excluded.name, "
        "amount = excluded.amount, "
        "status = excluded.status, "
        "necessity = excluded.necessity, "
        "category = excluded.category, "
        "creation_date = excluded.creation_date, "
        "update_date = excluded.update_date",
        tuple(new_arguments_list),
    )

    conn.commit()


# D from CRUD
def delete_expense(expense_id):
    """Delete an existing expense from the tracker."""

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    conn.commit()


def list_expenses(cutoff, category, necessity, creation_date):
    """List all the expenses within the specified timeframe."""

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if cutoff is not None:
        query += " AND creation_date >= ?"
        params.append(cutoff)

    if category is not None:
        query += " AND category = ?"
        params.append(category)

    if necessity is not None:
        query += " AND necessity = ?"
        params.append(necessity)

    if creation_date is not None:
        query += " AND creation_date = ?"
        params.append(creation_date)

    query += " ORDER BY creation_date"
    cursor.execute(query, tuple(params))

    expense_rows = cursor.fetchall()

    if not expense_rows:
        print("No expenses were tracked during the specified time period.")
    else:
        print("Expenses tracked during the specified time period:\n")

        for expense_row in expense_rows:
            read_expense(expense_row[0])
