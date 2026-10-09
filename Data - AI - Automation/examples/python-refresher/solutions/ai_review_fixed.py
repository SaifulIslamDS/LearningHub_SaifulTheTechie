"""Reviewed and fixed version of ai-review/ai_suggestion.py.

Copy this over ai_suggestion.py (keep the name) and the tests pass.
"""

from __future__ import annotations

import csv
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)


def net_revenue_by_month(path: Path | str) -> dict[str, float]:
    """Net revenue (excluding Cancelled) per month from the raw export.

    The export uses dd/mm/yyyy dates and can contain blank rows, "5,000"-style
    quantities, mixed-case statuses and exact duplicate rows.
    """
    totals: dict[str, float] = defaultdict(float)
    seen: set[tuple[str, ...]] = set()
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            values = tuple((v or "").strip().lower() for v in row.values())
            if not any(values):
                continue  # blank row
            if values in seen:
                continue  # exact duplicate
            seen.add(values)
            if row["Status"].strip().lower() == "cancelled":
                continue
            try:
                qty = int(row["Qty"].replace(",", "").strip())
                price = float(row["Unit Price"])
                when = datetime.strptime(row["Order Date"].strip(), "%d/%m/%Y")
            except ValueError as exc:
                log.warning("Line %d rejected: %s", line_no, exc)
                continue
            totals[when.strftime("%Y-%m")] += qty * price
    return {month: round(value, 2) for month, value in sorted(totals.items())}


if __name__ == "__main__":
    raw = Path(__file__).parent.parent / "data" / "orders_raw.csv"
    result = net_revenue_by_month(raw)
    for month, revenue in result.items():
        print(month, revenue)
    print("Total:", round(sum(result.values()), 2))
