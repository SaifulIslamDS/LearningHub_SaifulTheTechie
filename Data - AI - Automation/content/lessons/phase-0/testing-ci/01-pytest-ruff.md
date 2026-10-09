---
title: "pytest & ruff: Prove Your Code Works and Keep It Clean"
order: 1
summary: "Write automated tests with pytest (asserts, parametrize, expected errors), read a failing test, and use ruff to lint and format code in seconds."
level: Beginner
time: "50 min"
topics: ["pytest", "Linting with ruff"]
prerequisites: ["phase-0/programming-refresher/01-basics", "phase-0/dev-environment/02-uv-environments"]
keywords: [pytest, test, unit test, assert, test_ function, parametrize, pytest.raises, fixture, edge case, boundary, ruff, linter, lint, formatter, ruff check, ruff format, --fix, pyproject.toml, code quality]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip, phase-0/csv-cleaner-solution.zip]
resources:
  - title: "Get started with pytest"
    url: "https://docs.pytest.org/en/stable/getting-started.html"
    source: "pytest docs (official)"
    note: "Install, write and run your first tests; pytest.raises."
  - title: "Ruff tutorial"
    url: "https://docs.astral.sh/ruff/tutorial/"
    source: "Astral (official)"
    note: "Linting, formatting and configuring rules in pyproject.toml."
---

## What is it?

- A **test** is a small piece of code that checks your code gives the expected answer. **pytest** finds and runs every function whose name starts with `test_`.
- A **linter** reads code without running it and flags likely bugs and bad patterns (unused imports, `== None`). A **formatter** fixes the layout (spaces, line breaks) automatically.
- **ruff** does both, extremely fast.

!!! job "Why it matters at work"
    Tests let you change code without fear: if the business rule breaks, a test fails before a wrong number reaches a dashboard. Linting and formatting stop style arguments in code review. Most teams require both to pass before a PR can merge, and "how do you test your code?" is asked in almost every engineering interview. With AI writing more code, tests are how you **verify** it.

Use the `testing/` folder from [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip).

## Example 1: the code under test

`sales.py` has three small business functions:

```python
def size_band(order_value: float) -> str:
    if order_value >= 1000:
        return "Large"
    if order_value >= 500:
        return "Medium"
    return "Small"


def parse_quantity(text: str) -> int:
    """'5,000' -> 5000"""
    return int(text.replace(",", "").strip())


def net_revenue(orders: list[dict]) -> float:
    """Sum of value for all orders except Cancelled."""
    return sum(o["value"] for o in orders if o["status"] != "Cancelled")
```

## Example 2: tests

`test_sales.py`:

```python
import pytest
from sales import net_revenue, parse_quantity, size_band


def test_size_band_large():
    assert size_band(1560) == "Large"


@pytest.mark.parametrize(
    ("value", "expected"),
    [(1000, "Large"), (999.99, "Medium"), (500, "Medium"), (499, "Small")],
)
def test_size_band_boundaries(value, expected):
    assert size_band(value) == expected


def test_parse_quantity_removes_commas():
    assert parse_quantity("5,000") == 5000


def test_parse_quantity_rejects_text():
    with pytest.raises(ValueError):
        parse_quantity("lots")


def test_net_revenue_excludes_cancelled():
    orders = [
        {"value": 420.0, "status": "Delivered"},
        {"value": 240.0, "status": "Cancelled"},
        {"value": 320.0, "status": "Shipped"},
    ]
    assert net_revenue(orders) == 740.0
```

| Tool | Use it to… |
|---|---|
| `assert x == y` | Check a result |
| `@pytest.mark.parametrize` | Run one test with many inputs, especially **boundaries** (999.99, 1000) |
| `pytest.raises(ValueError)` | Check that bad input fails **loudly** |
| A small hand-made list | Test a business rule with a known answer (420 + 320 = 740) |

Run them from the `testing` folder:

```bash
uv run --with pytest pytest -v      # or: python -m pytest -v
```

```text
test_sales.py::test_size_band_large PASSED                               [ 12%]
test_sales.py::test_size_band_boundaries[1000-Large] PASSED              [ 25%]
test_sales.py::test_size_band_boundaries[999.99-Medium] PASSED           [ 37%]
test_sales.py::test_size_band_boundaries[500-Medium] PASSED              [ 50%]
test_sales.py::test_size_band_boundaries[499-Small] PASSED               [ 62%]
test_sales.py::test_parse_quantity_removes_commas PASSED                 [ 75%]
test_sales.py::test_parse_quantity_rejects_text PASSED                   [ 87%]
test_sales.py::test_net_revenue_excludes_cancelled PASSED                [100%]

============================== 8 passed in 0.02s ===============================
```

## Example 3: read a failing test

Break the rule on purpose: change `>= 1000` to `> 1000` in `sales.py`, and run `pytest` again:

```text
test_sales.py .F......                                                   [100%]

=================================== FAILURES ===================================
____________________ test_size_band_boundaries[1000-Large] _____________________

value = 1000, expected = 'Large'

    def test_size_band_boundaries(value, expected):
>       assert size_band(value) == expected
E       AssertionError: assert 'Medium' == 'Large'
E
E         - Large
E         + Medium

test_sales.py:14: AssertionError
=========================== short test summary info ============================
FAILED test_sales.py::test_size_band_boundaries[1000-Large] - AssertionError:...
========================= 1 failed, 7 passed in 0.03s ==========================
```

Read it like a traceback: **which test** (`[1000-Large]`), **what it got** (`'Medium'`) and **what it expected** (`'Large'`). The boundary test caught a one-character bug. Undo the change.

## Example 4: lint with ruff

`messy.py` works, but it's sloppy:

```python
import os
import json
def total(values):
    result=0
    for v in values :
        result = result+v
    return result
def report(orders, region = None):
    if region == None:
        return total([o["value"] for o in orders])
    return total([o["value"] for o in orders if o["region"]==region])
```

```bash
uvx ruff check --select E,F,I --output-format=concise messy.py
```

```text
messy.py:1:1: I001 [*] Import block is un-sorted or un-formatted
messy.py:1:8: F401 [*] `os` imported but unused
messy.py:2:8: F401 [*] `json` imported but unused
messy.py:9:18: E711 Comparison to `None` should be `cond is None`
Found 4 errors.
[*] 3 fixable with the `--fix` option (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```

- `uvx` runs a tool without adding it to the project. In a project, use `uv add --dev ruff` and `uv run ruff …`.
- `--fix` removes the unused imports automatically. Fix `== None` → `is None` yourself.

## Example 5: format with ruff

```bash
uvx ruff format --diff messy.py     # preview
uvx ruff format messy.py            # apply
```

```text
-    result=0
-    for v in values :
-        result = result+v
+    result = 0
+    for v in values:
+        result = result + v
     return result
-def report(orders, region = None):
+
+
+def report(orders, region=None):
```

Configure rules once in `pyproject.toml`, so everyone (and CI) uses the same ones. This is the csv-cleaner project's setting:

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]   # errors, pyflakes, imports, bugbear, pyupgrade
```

!!! tip "Format on save"
    Install the **Ruff** extension in VS Code and turn on *Format On Save*: files are tidied every time you save.

## What to test

| Test… | Example |
|---|---|
| The normal case | `size_band(1560) == "Large"` |
| **Boundaries** | 999.99, 1000, 500, 499 |
| Bad input | `parse_quantity("lots")` raises `ValueError` |
| Business rules | Cancelled orders excluded |
| A known answer | Clean file has 12 rows, net revenue 9,075 |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Testing only the "happy path" | Edge-case bugs slip through | Add boundary and bad-input tests |
| Test names like `test1` | Failures tell you nothing | `test_net_revenue_excludes_cancelled` |
| Comparing floats with `==` after maths | Rare false failures (0.1 + 0.2) | `pytest.approx(9075.0)` |
| Ignoring ruff warnings | Real bugs (unused variables, `== None`) stay | Fix them, or disable a rule deliberately in config |
| Arguing about style in reviews | Wasted time | Let `ruff format` decide |

## Try it yourself

**Task:** Add a test to `test_sales.py` checking that `parse_quantity(" 120 ")` (with spaces) returns `120`, and a test that `net_revenue([])` returns `0`. Run pytest. How many tests pass now?

<details markdown="1">
<summary>Show the solution</summary>

```python
def test_parse_quantity_strips_spaces():
    assert parse_quantity(" 120 ") == 120


def test_net_revenue_empty_list():
    assert net_revenue([]) == 0
```

`pytest` reports **10 passed**. `strip()` handles the spaces, and `sum()` of nothing is 0. Testing the empty case is a good habit: averages, for example, would crash with `ZeroDivisionError`.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which function will pytest run automatically?

1. `check_total()`
2. `test_total()`
3. `total_test_case()`

<details markdown="1"><summary>Show answer</summary>
**B.** Names starting with `test_`, in files named `test_*.py`.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why test 999.99 **and** 1000?

1. They're random values
2. Bugs hide at boundaries, like `>` vs `>=`
3. pytest requires two values

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does `ruff format` do?

1. Runs the tests
2. Rewrites code layout consistently
3. Installs packages

<details markdown="1"><summary>Show answer</summary>
**B.** `ruff check` finds problems; `ruff format` fixes layout.
</details>
</div>

## Summary

- pytest runs `test_*` functions; use `assert`, `parametrize` for boundaries, and `pytest.raises` for bad input.
- Read failures as: which test, got what, expected what.
- `ruff check` (with `--fix`) finds bugs and messy patterns; `ruff format` fixes layout.
- Put rules in `pyproject.toml` so your editor, your teammates and CI agree.

!!! job "Job-ready check"
    **Interview question:** *"How do you know your data transformation is correct?"*

    **Strong answer:** "I write unit tests for each rule, including boundaries and bad input, plus an end-to-end test that runs a small known input and compares the output with an expected file. Linting and formatting run with the tests, locally and in CI, so problems are caught before review."

    **Mini project:** Add `pytest.approx` and an end-to-end test that reads `orders.csv`, computes net revenue and checks **9,075**. Keep `ruff check` and `ruff format --check` clean.
