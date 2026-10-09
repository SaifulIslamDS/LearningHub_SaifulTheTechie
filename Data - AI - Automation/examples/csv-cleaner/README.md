# csv-cleaner

Clean messy CSV exports with repeatable, configurable rules. This is the reference solution for the **Phase 0 Gate** project (Data, AI & Automation Path).

```text
orders_raw.csv (14 rows: blanks, spaces, CAPITALS, "5,000", dd/mm dates, duplicates)
        │  csv-clean data/orders_raw.csv
        ▼
orders_raw_clean.csv (12 tidy rows, ISO dates, numbers, snake_case columns)
```

## Quick start

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev                          # create .venv, install pytest + ruff
uv run csv-clean data/orders_raw.csv   # writes data/orders_raw_clean.csv
uv run pytest                          # 17 tests
uv run ruff check . && uv run ruff format --check .
```

Example output:

```text
INFO csv_cleaner: Rows read: 14 | blank removed: 1 | duplicates removed: 1 | rejected: 0 | written: 12
INFO csv_cleaner: Clean file: data/orders_raw_clean.csv
```

## Usage

```text
csv-clean INPUT [-o OUTPUT] [-c CONFIG] [-v] [--log-file FILE]
```

| Option | Meaning |
|---|---|
| `-o, --output` | Output file (default: `<input>_clean.csv`) |
| `-c, --config` | Rules file (default: `config.toml`) |
| `-v, --verbose` | Show debug messages |
| `--log-file` | Also write the log to a file |

**Exit codes:** `0` OK · `2` input or config problem (missing file, invalid TOML, missing columns) · `3` finished, but some rows were rejected (see the log).

## Configuration

All cleaning rules live in `config.toml`: which columns to trim, title-case, convert to numbers and dates, the date format, de-duplication and column renames. To support a new export, change the config, not the code.

## Project structure

```text
src/csv_cleaner/
  cli.py       argument parsing, file reading/writing, logging, exit codes
  cleaner.py   pure cleaning functions (no file access, so easy to test)
  config.py    loads and validates config.toml
tests/         unit tests + end-to-end tests against expected output
.github/workflows/ci.yml   ruff + pytest on every push
```

## Design decisions

- **Bad rows are rejected, not fatal.** One bad value is logged with its line number, and the rest of the file is still cleaned.
- **Duplicates are removed after cleaning**, so `"Rahim "` and `"Rahim"` count as the same.
- **Dates use an explicit format** (`%d/%m/%Y`), so `05/01/2026` is always 5 January.
- **Standard library only** at runtime. pytest and ruff are dev tools.
