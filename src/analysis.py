# This file is meant for analytics functions, as a module ran from main.py.
# It will use charts from charts.py
# The funtions will be: monthly and weekly spending trends (line chart) by day, monthly spending trends by category (bar chart)
# Other non chart functions will be burn rate, largest transactions

import sqlite3

from datetime import datetime, timedelta

import pandas

import src.charts as charts

conn = sqlite3.connect("src/expenses.db")
cursor = conn.cursor()


# Internal functions


def _build_daily_df(time_window):
    """Fetch spending data from last month, sort by day, and return it to the caller function."""

    # The time_window is a number of days, already transformed in main.py
    time_difference = datetime.now() - timedelta(days=time_window)

    cursor.execute(
        "SELECT * FROM expenses WHERE creation_date >= ?", (time_difference,)
    )

    expenses_from_month = cursor.fetchall()
    # Dictionary to hold sum of expenses from each day
    spending_by_day = {}

    # This function sums up the amount spent by each day
    # Process: get date (column 6) as day, get amount
    # then create new row in dictionary (or retrieve it if existent), and add the amount to it
    for expense in expenses_from_month:
        # In order for strptime to work, you have to provide the date without time (hours)
        date = expense[6]
        # We need to transform the date into a datetime instance and then remove the time
        # Here the format is for dates like: 2026-04-28 17:24:56.412804
        # The codes are fixed, with Y (year), m (month), d (day), H (hour), M (minute), S (second), f (microsecond)
        date_as_day = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").date()
        amount_spent = expense[2]
        print(expense)
        print(spending_by_day)
        print(spending_by_day.get(date_as_day, 0))
        print(amount_spent)

        spending_by_day[date_as_day] = (
            spending_by_day.get(date_as_day, 0) + amount_spent
        )

        print(spending_by_day)

    # Make a list of tuples containing the dict info, then feed it into the DataFrame by columns.
    return pandas.DataFrame(list(spending_by_day.items()), columns=["Date", "Amount"])


def _build_category_df(time_window):
    """Fetch spending data from last month, sort by category and return it to the caller."""
    time_difference = datetime.now() - timedelta(days=time_window)

    cursor.execute(
        "SELECT * FROM expenses WHERE creation_date >= ?", (time_difference,)
    )

    expenses_from_month = cursor.fetchall()
    # Dictionary to hold sum of expenses by categories
    spending_by_category = {}

    # This function sums up the amount spent by categories
    # Process: get category, get amount
    # then create new row in dictionary (or retrieve it if existent), and add the amount to it
    for expense in expenses_from_month:
        category = expense[4]
        amount_spent = expense[2]

        spending_by_category[category] = (
            spending_by_category.get(category, 0) + amount_spent
        )

    # Make a list of tuples containing the dict info, then feed it into the DataFrame by columns.
    return pandas.DataFrame(
        list(spending_by_category.items()), columns=["Category", "Amount"]
    )


# Public API functions


def daily_spending_over_time(time_window):
    """Feed daily spending data into chart maker."""

    df = _build_daily_df(time_window)
    charts.expenses_by_time(df, time_window)


def category_spending_over_time(time_window):
    """Feed spending data by category into chart maker."""

    df = _build_category_df(time_window)
    charts.expenses_by_category(df, time_window)
