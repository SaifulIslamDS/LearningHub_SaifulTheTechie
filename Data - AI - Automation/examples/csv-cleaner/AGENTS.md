# AGENTS.md

Instructions for AI coding agents (and new humans) working on this repository.

## Project
`csv-cleaner` cleans messy CSV exports using rules in `config.toml`.
Code lives in `src/csv_cleaner/` (`cleaner.py` = rules, `cli.py` = command line, `config.py` = settings).

## Setup and commands
- Install: `uv sync --dev`
- Run: `uv run csv-clean data/orders_raw.csv`
- Test: `uv run pytest`
- Lint and format: `uv run ruff check .` and `uv run ruff format .`

## Rules
- Python 3.12+ syntax, type hints on every function.
- Never hard-code paths or column names in code: they belong in `config.toml`.
- Never swallow errors with a bare `except`. Reject the row, log the line number and reason, and count it in the report.
- Every change to cleaning behaviour needs a test in `tests/`.
- Known answer: `data/orders_raw.csv` → 12 rows written, matching `tests/expected_orders.csv`. Do not change the expected file to make a test pass.
- Don't add new dependencies without asking.

## Before you finish
Run `uv run ruff check . && uv run ruff format --check . && uv run pytest` — all must pass.
