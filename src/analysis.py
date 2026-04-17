# This file is meant for analytics functions, as a module ran from main.py.
# It will use charts from charts.py
# The funtions will be: monthly and weekly spending trends (line chart) by day, monthly spending trends by category (bar chart)
# Other non chart functions will be burn rate, largest transactions

import sqlite3

from datetime import datetime, timedelta

conn = sqlite3.connect("src/expenses.db")
cursor = conn.cursor()

def monthly_spending_by_day():
    """Fetch spending data from last month, sort by day, and feed it into the chart maker."""
    time_difference = datetime.now() - timedelta(days=31)

    cursor.execute(
        "SELECT * FROM expenses "
        "WHERE creation_date >= ?",
        (time_difference,)
    )

    expenses_from_month = cursor.fetchall()
    # Dictionary to hold sum of expenses from each day
    spending_by_day = {}

    # This function sums up the amount spent by each day
    # Process: get date (column 6) as day, get amount
    # then create new row in dictionary (or retrieve it if existent), and add the amount to it
    for expense in expenses_from_month:
        date = expense[6]
        # We need to remove the time component, and then make 
        date_as_day = datetime.strptime(date, "%Y-%m-%d").date()
        amount_spent = expense[2]

        spending_by_day[date_as_day] += amount_spent

def weekly_spending_by_day():
    """Fetch spending data from last week, sort by day, and feed it into the chart maker."""


def monthly_spending_by_category():
    """Fetch spending data from last month, sort by category and feed into chart maker."""

