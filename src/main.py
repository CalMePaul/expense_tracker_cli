import typer
from enum import Enum
from datetime import datetime, date

app = typer.Typer(no_args_is_help=True)

class Category(str, Enum):
    food = "food"
    transport = "transport"
    entertainment = "entertainment"
    learning = "learning"
    subscription = "subscription"
    other = "other"

class Time_window(str, Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"
    ever = "ever"

@app.command()
def add(
    description: str = typer.Argument(..., help="Description of the expense"),
    amount: str = typer.Argument(..., help="Amount spent"),
    necessity: bool = typer.Argument(..., help="Whether the expense was necessary"),
    category: Category = typer.Option(Category.other, "--category", "-c"),
):
    """Add an expense to the tracker."""

    createdAt = datetime.now()

    print("add")


@app.command()
def update(expense):
    """Update an expense."""

    print("update")


@app.command()
def delete(expense):
    """Delete an expense from the tracker."""

    print("delete")


@app.command()
def list_expenses(
    time_window: Time_window = typer.Argument(..., help="The time window of the listed expenses (hour, day, week, month, year, ever)")
):
    """List all expenses."""



if __name__ == "__main__":
    app()
