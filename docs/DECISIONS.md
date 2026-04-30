# Design Decisions

## SQLite over a flat file
Needed querying and filtering by date, category, and necessity. A CSV would've required manual parsing for every operation and had no native support for filtering.

## No classes for expenses
Expenses are pure data with no behavior. A class would've been an empty container with no meaningful methods — which the database row already handles. The one exception would've been complex validation logic, but that's handled with a few conditionals in the add command.

## No ORM
The schema is simple and fixed. An ORM adds a translation layer between Python objects and the database with no payoff at this scale. Raw SQL is more explicit and easier to debug. Also needed to learn SQL basics.

## Typer over argparse
Cleaner decorator-based syntax, automatic --help generation, and built-in enum support for validating option choices (category, status, time window) out of the box.

## Plotly over matplotlib
Interactive charts (hover, zoom) with less boilerplate. More useful for exploring spending data than static images.

## Internal functions prefixed with underscore
Functions like `_build_daily_df` and `_build_category_df` are implementation details not meant to be called from outside their module. The underscore signals this without needing to enforce it.

## update_expense compares against existing values before saving
When updating, the new arguments are compared against the current row fetched from the database. Only values that are explicitly provided override the existing ones — empty options default to None and are ignored. This prevents partial updates from wiping fields the user didn't intend to change.