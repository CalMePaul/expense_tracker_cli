# Expense Tracker CLI

Expense Tracker CLI is a command-line application for storing, accessing, and analyzing expenses and purchases. The goal is to make it easier to understand spending patterns while also serving as a practical learning project for Python, SQLite, CLI design, and data visualization.

## Table of contents

- [File Structure](#file-structure)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Personal Goals](#personal-goals)
- [Installation](#installation)
- [License](#license)

## File structure

expense_tracker_cli
  .vscode/
    settings.json
  docs/
    ARCHITECTURE.md
  src/
    __init__.py
    analysis.py
    charts.py
    data_manager.py
    main.py
  tests/
    test_analysis.py
    test_data_manager.py
  .gitignore
  .pylintrc
  LICENSE
  pyproject.toml
  README.md

## Tech stack

- Python 3.14.2
- Typer 0.24.1
- Plotly 6.6.0
- Pandas 3.0.2
- Pytest 9.0.2
- Rich 14.3.3

## Features

- Call the CLI app by typing "et", for expense tracker, in your terminal
- et --help or et (command) --help for individual properties
- et add "name" amount true/false --category "category" --status "status"
- et update id --name "name" --amount amount --necessity true/false --status "status" --category "category"
- et delete id
- et list timewindow (with timewindow being "hour" "day" "week" "month" "year" "ever") --> allows for checking id to perform operations on expenses (like update or delete)
- et plot-daily timewindow (with timewindow being either "week" or "month")
- et plot-by-category timewindow (with timewindow being either "week" or "month")

## Personal goals

- Learn how Typer works (useful for advanced CLIs)
- Learn how to write basic SQL, learn what is SQL injection
- Get better at plotting charts with plotly and analyzing data with pandas
- Get better at testing code
- Get better at writing documentation and comments in code

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the current project dependencies:

```powershell
python -m pip install typer plotly pandas pytest rich
```

Install the package in editable mode to enable the `et` command:

```powershell
pip install -e .
```

## License

MIT License - see [LICENSE](LICENSE) for details.