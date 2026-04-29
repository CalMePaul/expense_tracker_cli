from enum import Enum
from datetime import datetime, date, timedelta

import click
import typer

import src.data_manager as data_manager
import src.analysis as analysis

app = typer.Typer(no_args_is_help=True)

# The classes for option choices


class Status(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Category(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    LEARNING = "learning"
    PRODUCTIVITY = "productivity"
    HEALTH = "health"
    OTHER = "other"


class TimeWindow(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    EVER = "ever"

    # Type hints datetime and None (what the function can return)
    def cutoff(self) -> datetime | None:
        """Return the earliest datetime for this window, or None for EVER."""
        now = datetime.now()
        match self:
            case TimeWindow.HOUR:
                return now - timedelta(hours=1)
            case TimeWindow.DAY:
                return now - timedelta(days=1)
            case TimeWindow.WEEK:
                return now - timedelta(weeks=1)
            case TimeWindow.MONTH:
                return now - timedelta(days=30)
            case TimeWindow.YEAR:
                return now - timedelta(days=365)
            case TimeWindow.EVER:
                return None


class DateType(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)  # expects YYYY-MM-DD
        except ValueError:
            self.fail(
                f"'{value}' is not a valid date (expected YYYY-MM-DD)", param, ctx
            )


# Dictionary for helping translate time window words into numbers of days
time_windows_in_days = {"week": 7, "month": 31}


# The CLI commands


@app.command()
def add(
    name: str = typer.Argument(..., help="Name of the expense"),
    amount: int = typer.Argument(..., help="Amount spent"),
    status: Status = typer.Option(
        Status.DONE, "--status", "--s"
    ),  # DONE is the default state
    category: Category = typer.Option(
        Category.OTHER, "--category", "--c"
    ),  # OTHER is the default state
    necessity: bool = typer.Argument(..., help="Whether the expense was necessary"),
):
    """Add an expense to the tracker."""

    name = name.strip().lower() or None
    amount = amount or None
    status = status.value
    category = category.value
    creation_date = datetime.now()
    update_date = datetime.now()

    data_manager.new_expense(
        name, amount, status, necessity, category, creation_date, update_date
    )


@app.command()
def update(
    expense_id: str = typer.Argument(..., help="Id of the expense to update"),
    name: str = typer.Option(None, "--name", "--n"),
    amount: int = typer.Option(None, "--amount", "--a"),
    status: Status = typer.Option(Status.DONE, "--status", "--s"),
    category: Category = typer.Option(Category.OTHER, "--category", "--c"),
    necessity: bool = typer.Option(None, "--necessary", "--n"),
):
    """Update an expense."""

    name = name.strip().lower() if name is not None else None
    amount = amount if amount is not None else None
    status = status.value
    category = category.value
    update_date = datetime.now()

    data_manager.update_expense(
        expense_id, name, amount, status, category, necessity, update_date
    )


@app.command()
def delete(expense_id):
    """Delete an expense from the tracker."""

    data_manager.delete_expense(expense_id)


@app.command()
def list(
    time_window: TimeWindow = typer.Argument(
        ...,
        help="The time window of the listed expenses (hour, day, week, month, year, ever)",
    ),
    category: Category = typer.Option(None, "--category", "--c"),
    necessity: bool = typer.Option(None, "--necessary", "--n"),
    creation_date: date = typer.Option(None, "--date", click_type=DateType()),
):
    """List all expenses."""

    category = category.value if category is not None else None
    creation_date = creation_date.strip().lower() if creation_date is not None else None

    data_manager.list_expenses(
        time_window.cutoff(), category, necessity, creation_date
    )


@app.command()
def plot_daily(
    time_window: str = typer.Argument(..., help="Time window must be a week or a month")
):
    """Start plotting daily spending over a week or a month."""
    if time_window.lower() == "week" or time_window.lower() == "month":
        analysis.daily_spending_over_time(time_windows_in_days[time_window])
    else:
        print("The time window provided for the plot was neither a week or a month.")


@app.command()
def plot_by_category(
    time_window: str = typer.Argument(..., help="Time window must be a week or a month")
):
    """Start plotting spending by category over a week or a month."""
    if time_window.lower() == "week" or time_window.lower() == "month":
        analysis.category_spending_over_time(time_windows_in_days[time_window])
    else:
        print("The time window provided for the plot was neither a week or a month.")


if __name__ == "__main__":
    app()
