"""Code an AI assistant suggested for this prompt:

    "Write a Python function that reads orders_raw.csv and returns
     net revenue by month."

It runs without errors. Is it correct? Review it before you trust it.
"""

import csv
from collections import defaultdict
from datetime import datetime


def net_revenue_by_month(path):
    totals = defaultdict(float)
    with open(path) as f:
        for row in csv.DictReader(f):
            try:
                qty = int(row["Qty"])
                price = float(row["Unit Price"])
                month = datetime.strptime(row["Order Date"], "%m/%d/%Y").strftime("%Y-%m")
                totals[month] += qty * price
            except Exception:
                continue
    return dict(sorted(totals.items()))


if __name__ == "__main__":
    from pathlib import Path

    result = net_revenue_by_month(Path(__file__).parent.parent / "data" / "orders_raw.csv")
    for month, revenue in result.items():
        print(month, round(revenue, 2))
    print("Total:", round(sum(result.values()), 2))
