---
title: "Phase 0 Gate Project: CSV Data Cleaning CLI"
summary: "Build a command-line tool that cleans messy CSV exports with configurable rules, logging, error handling, tests and CI — your first engineering-grade portfolio project."
level: Beginner
time: "10–20 hours (estimate)"
reviewed: 2026-10-09
files: [phase-0/csv-cleaner-starter.zip, phase-0/csv-cleaner-solution.zip, orders_raw.csv, orders.csv, known_answers.csv]
---

## The brief

Every month, the operations team exports orders from the ERP system. The file is messy: blank rows, extra spaces, `DHAKA` vs `Dhaka`, quantities like `"5,000"`, day-first dates, and duplicated lines. Someone fixes it by hand in Excel, differently each time.

> *"Give us a tool that cleans the export the same way every time, tells us what it changed, and fails loudly when something is wrong."*

Build **`csv-clean`**, a Python command-line tool. It's the **gate** for Phase 0: if you can build, test and ship this, you have the engineering foundations the later phases rely on.

```text
orders_raw.csv (14 rows: blanks, spaces, CAPITALS, "5,000", dd/mm dates, duplicates)
        │  uv run csv-clean data/orders_raw.csv
        ▼
orders_raw_clean.csv (12 tidy rows, ISO dates, numbers, snake_case columns)
```

## What you'll prove

| Skill (Phase 0 module) | Evidence in your project |
|---|---|
| Dev environment | `pyproject.toml`, `uv.lock`, `.python-version`; installs with `uv sync` |
| Git & GitHub | A public repo with small commits, at least one merged PR, and a clear README |
| Linux & terminal | A shell script and a cron line that run the tool daily and keep a log |
| Programming | Functions, a dataclass config, file handling, specific exceptions, type hints |
| Testing & CI | pytest unit and end-to-end tests, ruff clean, a green GitHub Actions badge |
| AI-assisted development | An `AGENTS.md`, and a short log of AI suggestions you reviewed and tested |

## Two ways to start

| Option | Start from | Good for |
|---|---|---|
| **A — Guided (recommended)** | [csv-cleaner-starter.zip](../../downloads/phase-0/csv-cleaner-starter.zip): CLI, config loader, config file and **17 tests** are ready. You implement 7 functions in `cleaner.py` | A first project; learn test-driven development |
| **B — From scratch** | `uv init csv-cleaner`, and this page | A stronger portfolio story, if you're already comfortable |

The reference solution is in [csv-cleaner-solution.zip](../../downloads/phase-0/csv-cleaner-solution.zip). Open it only after a real attempt, or to compare designs at the end.

### Option A in 5 commands

```bash
unzip csv-cleaner-starter.zip && cd csv-cleaner
uv sync --dev
uv run pytest                 # 13 failed, 4 passed: your to-do list
# implement src/csv_cleaner/cleaner.py one function at a time, re-running pytest
uv run csv-clean data/orders_raw.csv
```

| Function | Rule it implements |
|---|---|
| `check_columns` | Raise an error listing **all** missing required columns |
| `is_blank` | A row where every cell is empty or spaces |
| `to_int` | `"5,000"` → `5000`; text like `"lots"` raises `ValueError` |
| `to_decimal` | `"3.50"` → `3.5` |
| `to_iso_date` | `"05/01/2026"` with `%d/%m/%Y` → `"2026-01-05"` |
| `clean_row` | Apply trim, title case, numbers, date and renames from the config |
| `clean_rows` | Remove blanks, clean each row, reject bad rows (with line numbers), drop duplicates, return a report |

## Requirements

### 1. Behaviour
- [ ] `csv-clean INPUT [-o OUTPUT] [-c CONFIG] [-v] [--log-file FILE]`.
- [ ] Trim spaces, title-case Region and Status, convert `"5,000"` → `5000`, convert day-first dates to ISO `YYYY-MM-DD`, rename columns to snake_case.
- [ ] Remove blank rows and exact duplicates (**after** cleaning, so `Dhaka ` and `Dhaka` match).
- [ ] Bad rows are **rejected, logged with their line number, and counted**, never silently dropped and never crashing the run.

### 2. Configuration
- [ ] All rules (columns, formats, renames) live in `config.toml`, read with `tomllib`, so no column names are hard-coded in the code.
- [ ] A broken or missing config file gives a clear error message.

### 3. Logging & exit codes
- [ ] A one-line summary: `Rows read | blank removed | duplicates removed | rejected | written`.
- [ ] Messages go to stderr (and optionally a log file); `-v` shows debug detail.
- [ ] Exit codes a scheduler can act on:

| Code | Meaning |
|---|---|
| `0` | Success |
| `2` | Can't run: input file or config missing/invalid, required columns missing |
| `3` | Finished, but some rows were rejected: check the log |

### 4. Tests & quality
- [ ] Unit tests for every cleaning rule, including boundaries and bad input.
- [ ] An end-to-end test comparing the output with `tests/expected_orders.csv`.
- [ ] `uv run ruff check .` and `uv run ruff format --check .` pass.
- [ ] GitHub Actions runs lint, format check and tests on every push and PR.

### 5. Operations & documentation
- [ ] `scripts/daily_clean.sh` with `set -euo pipefail`, plus the crontab line in the README.
- [ ] README: purpose, quick start, example output, options, exit codes, how it works, what you'd do next.
- [ ] `AGENTS.md` with setup commands, rules and the known answer.

## Known answers

Your tool must produce these results with the practice file. If it doesn't, find out why before you continue.

| Check | Expected |
|---|---|
| `uv run pytest` (solution) | **17 passed** |
| Summary line | `Rows read: 14 | blank removed: 1 | duplicates removed: 1 | rejected: 0 | written: 12` |
| Output | Identical to `tests/expected_orders.csv`, same 12 orders as `orders.csv` |
| Net revenue of the output (excluding Cancelled) | **9,075** |
| Missing input file | `ERROR … Input file not found: nope.csv`, exit code **2** |
| One quantity changed to `lots` | `WARNING … Line 10 rejected: invalid literal for int() with base 10: 'lots'`, 11 written, exit code **3** |

Reference run (solution):

```text
INFO csv_cleaner: Rows read: 14 | blank removed: 1 | duplicates removed: 1 | rejected: 0 | written: 12
INFO csv_cleaner: Clean file: data/orders_raw_clean.csv
```

```text
order_id,order_date,customer,region,category,product,quantity,unit_price,status
1,2026-01-05,Rahim Traders,Dhaka,Fabric,Cotton Twill,120,3.50,Delivered
2,2026-01-08,Karim Garments,Chattogram,Trims,Metal Buttons,5000,0.04,Delivered
3,2026-01-12,Nova Apparel,Dhaka,Fabric,Denim 12oz,300,5.20,Delivered
```

## Repository structure

```text
csv-cleaner/
├── .github/workflows/ci.yml
├── .gitignore
├── .python-version
├── AGENTS.md
├── README.md
├── config.toml
├── data/orders_raw.csv
├── docs/ai-log.md            ← AI suggestions you reviewed, what you changed
├── pyproject.toml
├── scripts/daily_clean.sh
├── src/csv_cleaner/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── cli.py
│   └── config.py
├── tests/
│   ├── expected_orders.csv
│   ├── test_cleaner.py
│   ├── test_cli.py
│   └── test_config.py
└── uv.lock
```

## Stretch goals

- Process every CSV in a **folder** (like the Power Query folder lesson), with one summary per file.
- Write rejected rows to `rejected.csv` with a `reason` column.
- Add a `--dry-run` flag that reports without writing.
- Publish a release tag (`v1.0.0`) and a CHANGELOG.

## Self-assessment rubric

| Area | Meets the bar | Excellent |
|---|---|---|
| Correctness | Known answers match | Edge cases tested (blank, duplicates after cleaning, bad dates, missing columns) |
| Code quality | Functions, type hints, ruff clean | Small pure functions, config-driven, clear names and docstrings |
| Error handling | No crashes on bad rows | Specific exceptions, line numbers, meaningful exit codes |
| Testing & CI | Tests pass locally | Unit + end-to-end tests, green CI badge, branch protection |
| Git & docs | README with quick start | Small commits, PR history, README tells the story in 60 seconds |
| AI use | — | AGENTS.md, plus an AI log showing what you verified and fixed |

**Done when:** every requirement is checked, the known answers match, CI is green, and someone else can install and run your tool from the README alone.

!!! tip "Interview story"
    "I built a config-driven CSV cleaning CLI in Python with uv. It logs a summary and returns exit codes a scheduler can act on, rejects bad rows with line numbers instead of failing silently, and has 17 tests running in GitHub Actions. I used an AI assistant for parts of it, with an AGENTS.md and known-answer tests to verify every suggestion."
