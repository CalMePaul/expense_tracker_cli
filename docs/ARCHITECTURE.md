# Architecture

## Overview

Expense Tracker CLI is a single-user command-line application that stores expense records in a local SQLite database and provides spending analysis through interactive charts. There is no server, no network layer, and no external dependencies beyond the local filesystem.

## Data Flow

### Write operations (add, update, delete)
```
User input → main.py (Typer parses command) → data_manager.py → SQLite (expenses.db)
```

### Read operations (list)
```
User input → main.py (Typer parses command) → data_manager.py → SQLite → Rich (terminal output)
```

### Analysis operations (plot-daily, plot-by-category)
```
User input → main.py (Typer parses command) → analysis.py → SQLite → Pandas (DataFrame) → charts.py → Plotly (interactive chart)
```

## Module Responsibilities

| File | Responsibility |
|---|---|
| `src/main.py` | CLI entry point — defines all commands and their arguments/options via Typer |
| `src/data_manager.py` | All direct database operations — CRUD functions and list with filtering |
| `src/analysis.py` | Fetches and aggregates expense data into Pandas DataFrames for charting |
| `src/charts.py` | Receives DataFrames and renders interactive Plotly charts |

## Database Schema

Single table: `expenses`

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key, auto-incremented |
| `name` | TEXT | Name of the expense |
| `amount` | REAL | Amount spent |
| `status` | TEXT | `planned`, `in_progress`, or `done` |
| `category` | TEXT | `food`, `transport`, `entertainment`, `learning`, `productivity`, `health`, or `other` |
| `necessity` | TEXT | Whether the expense was necessary |
| `creation_date` | TEXT | Datetime the record was created |
| `update_date` | TEXT | Datetime the record was last modified |
