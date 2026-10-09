---
title: "Files & Exceptions: Read and Write Data Safely"
order: 3
summary: "Read CSV files, write JSON and CSV output with pathlib, and handle missing files and bad values with try/except so one bad row doesn't stop the job."
level: Beginner
time: "45 min"
topics: ["Files & exceptions"]
prerequisites: ["phase-0/programming-refresher/02-collections"]
keywords: [file, open, with, pathlib, path, csv, DictReader, DictWriter, json, encoding, utf-8, newline, exception, try, except, else, finally, raise, FileNotFoundError, ValueError, KeyError, traceback]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip, orders.csv]
resources:
  - title: "Reading and Writing Files (Python tutorial)"
    url: "https://docs.python.org/3/tutorial/"
    source: "Python official docs"
    note: "Section 7.2: open(), with, and JSON."
  - title: "Errors and Exceptions (Python tutorial)"
    url: "https://docs.python.org/3/tutorial/errors.html"
    source: "Python official docs"
    note: "try/except/else/finally and raising your own errors."
---

## What is it?

- **Files:** Python reads and writes text, CSV and JSON files. Use `pathlib.Path` for paths and `with` so files are always closed.
- **Exceptions** are Python's way of reporting problems at run time (a missing file, a bad number). With `try/except` you **decide** what happens instead of crashing.

!!! job "Why it matters at work"
    Real data is messy: files go missing, a row says `"ten"` instead of `10`. A pipeline that crashes on row 9,999 of 10,000, or silently skips rows without saying so, causes incidents. Handling exceptions well, and logging what was skipped, is a core data engineering skill and part of the Phase 0 project.

Open `03_files_exceptions.py` from [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip). It reads `data/orders.csv`.

## Example 1: read a CSV into dictionaries

```python
import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"     # folder next to this script


def read_orders(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


rows = read_orders(DATA / "orders.csv")
print("Rows:", len(rows))
print("First row:", rows[0])
```

```text
Rows: 12
First row: {'order_id': '1', 'order_date': '2026-01-05', 'customer': 'Rahim Traders', 'region': 'Dhaka', 'category': 'Fabric', 'product': 'Cotton Twill', 'quantity': '120', 'unit_price': '3.50', 'status': 'Delivered'}
```

- `with … as f:` closes the file automatically, even if an error happens.
- `DictReader` turns each row into a dict keyed by the header.
- **Every value is text** (`'120'`, `'3.50'`): convert before doing maths.
- `Path(__file__).parent / "data"` works no matter which folder you run the script from.

## Example 2: calculate, then write JSON

```python
def order_value(row: dict[str, str]) -> float:
    return int(row["quantity"]) * float(row["unit_price"])


net = [r for r in rows if r["status"] != "Cancelled"]
summary = {"orders": len(net), "revenue": round(sum(order_value(r) for r in net), 2)}
print(summary)

out = DATA / "summary.json"
out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("Wrote", out.name)
```

```text
{'orders': 11, 'revenue': 9075.0}
Wrote summary.json
```

## Example 3: handle a missing file

```python
try:
    read_orders(DATA / "missing.csv")
except FileNotFoundError as exc:
    print("Could not open file:", Path(exc.filename).name)
```

```text
Could not open file: missing.csv
```

## Example 4: skip a bad row, keep going

```python
bad_rows = [
    {"quantity": "10", "unit_price": "2.5"},
    {"quantity": "ten", "unit_price": "2.5"},
]
total = 0.0
for i, r in enumerate(bad_rows, start=1):
    try:
        total += order_value(r)
    except ValueError as exc:
        print(f"Row {i} skipped: {exc}")
print("Total of good rows:", total)
```

```text
Row 2 skipped: invalid literal for int() with base 10: 'ten'
Total of good rows: 25.0
```

This is exactly what the CSV cleaner project does: reject the bad row, **report** it, and process the rest.

## The full try statement

```python
try:
    f = path.open()          # code that might fail
except FileNotFoundError:
    ...                      # runs only for this error type
else:
    ...                      # runs only if nothing failed
finally:
    ...                      # always runs (clean-up)
```

| Exception | Typical cause |
|---|---|
| `FileNotFoundError` | Wrong path, or the file isn't there yet |
| `ValueError` | `int("ten")`, a bad date format |
| `KeyError` | A missing dict key / CSV column (`row["Status"]`) |
| `TypeError` | `"3170" / 3600` (text divided by a number) |
| `ZeroDivisionError` | Average of zero rows |

Raise your own when input breaks a rule: `raise ValueError(f"Missing required columns: {missing}")`.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `except:` or `except Exception: pass` | Real bugs are hidden silently | Catch **specific** errors, and log them |
| Forgetting `newline=""` with csv | Blank lines between rows on Windows | `open(..., newline="")` for CSV |
| No `encoding="utf-8"` | Garbled names on some systems | Always pass it |
| Hard-coded paths (`C:\Users\me\...`) | Breaks on every other computer | `Path(__file__).parent / "data"`, or a config setting |
| Doing maths on CSV text | `TypeError`, or `'120' * 2 = '120120'` | Convert with `int()` / `float()` |

## Try it yourself

**Task:** Write all **Dhaka** orders from `orders.csv` to `dhaka_orders.csv` (same columns), and print a friendly message instead of a traceback if `orders.csv` is missing.

<details markdown="1">
<summary>Show a hint</summary>

`csv.DictWriter(f, fieldnames=reader.fieldnames)`, then `.writeheader()` and `.writerows(rows)`. Put the reading in `try`, and the writing in `else`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
import csv
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

try:
    with (DATA / "orders.csv").open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        dhaka = [row for row in reader if row["region"] == "Dhaka"]
except FileNotFoundError:
    print("orders.csv not found — check the data folder")
else:
    out = DATA / "dhaka_orders.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dhaka)
    print(f"Wrote {len(dhaka)} rows to {out.name}")
```

```text
Wrote 5 rows to dhaka_orders.csv
```

(File: `solutions/ex03_dhaka_file.py`.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Why use `with path.open() as f:`?

1. It's faster
2. The file is closed automatically, even after an error
3. It's required for CSV

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. `int("ten")` raises which exception?

1. `KeyError`
2. `ValueError`
3. `FileNotFoundError`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What's wrong with `except Exception: pass`?

1. Nothing
2. It hides every error, including real bugs, without a trace
3. It only catches `ValueError`

<details markdown="1"><summary>Show answer</summary>
**B.** Catch specific errors and log what you skipped.
</details>
</div>

## Summary

- Use `pathlib.Path` and `with … open(…, encoding="utf-8")`; add `newline=""` for CSV.
- `csv.DictReader` / `DictWriter` handle CSV rows as dicts; `json.dumps` writes JSON. CSV values are text.
- `try/except` handles **specific** exceptions; `else` runs on success; `finally` always runs.
- Skip bad rows **and report them**, rather than crashing or failing silently.

!!! job "Job-ready check"
    **Interview question:** *"Your script processes 10,000 rows and one has a bad date. What should happen?"*

    **Strong answer:** "It depends on the agreed rule, but usually: reject that row, log its line number and the reason, process the rest, and report the counts (read, written, rejected) at the end. If rejections pass a threshold, fail the job, because silent data loss is worse than a visible failure."

    **Mini project:** Extend `03_files_exceptions.py` to read `orders_raw.csv` (from the downloads), skip rows that fail conversion, and print **read / written / rejected** counts.
