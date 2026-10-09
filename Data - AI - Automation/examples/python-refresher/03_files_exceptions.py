"""Lesson: reading/writing files and handling errors."""

import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"


def read_orders(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def order_value(row: dict[str, str]) -> float:
    return int(row["quantity"]) * float(row["unit_price"])


rows = read_orders(DATA / "orders.csv")
print("Rows:", len(rows))
print("First row:", rows[0])

net = [r for r in rows if r["status"] != "Cancelled"]
summary = {
    "orders": len(net),
    "revenue": round(sum(order_value(r) for r in net), 2),
}
print(summary)

# Write the summary as JSON
out = DATA / "summary.json"
out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("Wrote", out.name)

# Handling errors: a missing file
try:
    read_orders(DATA / "missing.csv")
except FileNotFoundError as exc:
    print("Could not open file:", Path(exc.filename).name)

# Handling errors: a bad value in one row — skip it, keep going
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
