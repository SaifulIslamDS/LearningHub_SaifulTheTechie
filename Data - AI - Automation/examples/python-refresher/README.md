# Python refresher — practice scripts

Scripts for the Phase 0 "Programming Refresher", "Debugging" and "Testing" lessons.

| File | Lesson |
|---|---|
| `01_basics.py` | Variables, conditions, loops & functions |
| `02_collections.py` | Lists, dictionaries, sets & tuples |
| `03_files_exceptions.py` | Files & exceptions (reads `data/orders.csv`) |
| `04_classes.py` | Classes, dataclasses & type hints |
| `debug_me.py` | Debugging — has two bugs on purpose |
| `testing/` | `sales.py`, `test_sales.py` (pytest) and `messy.py` (ruff) |
| `ai-review/` | `ai_suggestion.py` (AI-written code to review) and `test_ai_suggestion.py` (known-answer tests) |
| `data/` | `orders.csv` (12 clean orders) and `orders_raw.csv` (the messy export) |
| `solutions/` | Answers to every "Try it yourself" — try first! |

Run any script with `python 01_basics.py` (or `uv run 01_basics.py`).
Run the tests with `cd testing` then `python -m pytest` (or `uv run --with pytest pytest`).
