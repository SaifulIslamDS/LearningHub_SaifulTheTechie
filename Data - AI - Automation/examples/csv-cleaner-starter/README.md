# csv-cleaner — STARTER

Your Phase 0 Gate project. The command-line part (`cli.py`), the config loader (`config.py`), the config file and **all the tests** are ready. Your job is to implement the cleaning functions in `src/csv_cleaner/cleaner.py`.

## Steps

1. Install [uv](https://docs.astral.sh/uv/), then run `uv sync --dev`.
2. Run `uv run pytest`: **13 failed, 4 passed**. The 4 passing tests cover the parts already done (config loading, missing files); the rest fail with `NotImplementedError`.
3. Open `tests/test_cleaner.py` and `src/csv_cleaner/cleaner.py`. Implement one function at a time, re-running `uv run pytest` after each.
4. When all tests pass, run `uv run csv-clean data/orders_raw.csv` and check the summary:
   `Rows read: 14 | blank removed: 1 | duplicates removed: 1 | rejected: 0 | written: 12`.
5. Run `uv run ruff check .` and `uv run ruff format .`.
6. Push to GitHub and make sure the **CI** workflow is green.

Stuck? Compare with the solution package (`csv-cleaner-solution.zip`), but only after a real attempt.
