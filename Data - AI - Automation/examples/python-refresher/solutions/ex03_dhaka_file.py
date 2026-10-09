"""Exercise 03 — write all Dhaka orders to dhaka_orders.csv, safely."""

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
    print(f"Wrote {len(dhaka)} rows to {out.name}")  # 5 rows
