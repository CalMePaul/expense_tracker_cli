# Expense Tracker CLI

Expense Tracker CLI is a command-line application for storing, accessing, and analyzing expenses and purchases. The goal is to make it easier to understand spending patterns while also serving as a practical learning project for Python, SQLite, CLI design, and data visualization.

## Features

- Create, read, update, and delete expense records
- Store expense data with SQLite
- Analyze spending data
- Generate charts to visualize spending trends

## Usage

The CLI is intended to be used through the `et` command (`et` stands for "expense tracker"). You add expenses from the terminal and generate reports from the stored data.

Example commands:

```text
et add "shoes" medium product
et add "claude subscription" expensive service
et report monthly-summary
et report consumption-by-category
```

Example meanings:

- `et add "shoes" medium product` adds an expense entry for shoes with a medium price level in the product category
- `et add "claude subscription" expensive service` adds a service expense with a higher price level
- `et report monthly-summary` generates a monthly spending summary
- `et report consumption-by-category` generates a category-based spending report

## Tech Stack

- Python
- SQLite
- Typer
- Pytest
- Matplotlib
- Plotly

## Project Structure

```text
expense_tracker_cli/
  .venv/
  docs/
  src/
  tests/
  .gitignore
  LICENSE
  README.md
```

As the project grows, `src/` will contain the application code and `tests/` will contain automated tests.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the current project dependencies:

```powershell
python -m pip install pytest black pylint typer matplotlib plotly
```

## Goals

This project is intended to become a simple but well-structured combination of:

- command-line interaction
- SQL data handling with SQLite
- data analysis
- data visualization

It is also a learning project focused on improving familiarity with Typer, SQLite, and Python project structure.

## License

This project is licensed under the terms described in the [LICENSE](/d:/Code/expense_tracker_cli/LICENSE) file.
