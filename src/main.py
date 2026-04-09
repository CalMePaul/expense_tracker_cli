from enum import Enum
from datetime import datetime, date

import click
import typer

import src.data_manager as data_manager

app = typer.Typer(no_args_is_help=True)

class Status(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Category(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    LEARNING = "learning"
    SUBSCRIPTION = "subscription"
    OTHER = "other"

class TimeWindow(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    EVER = "ever"

class DateType(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)  # expects YYYY-MM-DD
        except ValueError:
            self.fail(f"'{value}' is not a valid date (expected YYYY-MM-DD)", param, ctx)


@app.command()
def add(
    name: str = typer.Argument(..., help="Name of the expense"),
    amount: str = typer.Argument(..., help="Amount spent"),
    status: str = typer.Option(Status.DONE, "--status", "--s"), #DONE is the default state
    category: Category = typer.Option(Category.OTHER, "--category", "-c"), #OTHER is the default state
    necessary: bool = typer.Argument(..., help="Whether the expense was necessary"),
):
    """Add an expense to the tracker."""

    created_at = datetime.now()
    updated_at = datetime.now()

    data_manager.new_expense(name, amount, status, necessary, category, created_at, updated_at)


@app.command()
def update(
    expense_id: str = typer.Argument(..., help="Id of the expense to update"),
    name: str = typer.Option(None, "--name", "--n"),
    amount: str = typer.Option(None, "--amount", "--a"),
    status: str = typer.Option(Status.DONE, "--status", "--s"),
    category: Category = typer.Option(Category.OTHER, "--category", "-c"),
    necessary: bool = typer.Option(None, "--necessary", "--n"),
):
    """Update an expense."""

    updated_at = datetime.now()

    data_manager.update_expense(expense_id, name, amount, status, category, necessary, updated_at)


@app.command()
def delete(expense_id):
    """Delete an expense from the tracker."""

    data_manager.delete_expense(expense_id)


@app.command()
def list_expenses(
    time_window: TimeWindow = typer.Argument(..., help="The time window of the listed expenses (hour, day, week, month, year, ever)"),
    category: Category = typer.Option(Category.OTHER, "--category", "--c"),
    necessary: bool = typer.Option(None, "--necessary", "--n"),
    creation_date: date = typer.Option(None, "--date", click_type=DateType())
):
    """List all expenses."""

    data_manager.list_expenses(time_window, category, necessary, creation_date)


if __name__ == "__main__":
    app()
