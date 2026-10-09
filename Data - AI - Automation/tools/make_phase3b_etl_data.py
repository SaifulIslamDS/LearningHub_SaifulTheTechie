#!/usr/bin/env python3
"""Generate deterministic Phase 3B ETL/ELT practice change events.

This script DOES NOT modify the shared Phase 2 generator or its datasets.
It derives a tiny CDC event log from the clean 2025 orders and restores every
changed business row by the end, so the known 2025 answers remain unchanged.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "examples" / "phase-3" / "data" / "orders_2025.csv"
EXAMPLE_OUT = ROOT / "examples" / "phase-3" / "data" / "orders_cdc_events.jsonl"
DOWNLOAD_OUT = ROOT / "content" / "downloads" / "phase-3" / "orders_cdc_events.jsonl"
SEED = 2026


def clean_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def row_dict(row: pd.Series) -> dict[str, Any]:
    return {str(k): clean_value(v) for k, v in row.to_dict().items()}


def event(seq: int, op: str, order_id: int, before: dict[str, Any] | None,
          after: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "event_id": f"evt-{seq:03d}",
        "sequence": seq,
        "op": op,
        "key": {"order_id": order_id},
        "source": {"table": "orders", "file": "orders_2025.csv"},
        "ts_ms": 1767592800000 + seq * 1000,  # fixed 2026-01-05 demo timestamps
        "before": before,
        "after": after,
    }


def main() -> None:
    orders = pd.read_csv(SOURCE)
    eligible = orders[(orders["status"] == "Delivered") & orders["delivery_days"].notna()].copy()
    rng = random.Random(SEED)
    picked = rng.sample(eligible.index.tolist(), 2)
    first = row_dict(eligible.loc[picked[0]])
    second = row_dict(eligible.loc[picked[1]])

    first_cancelled = dict(first)
    first_cancelled["status"] = "Cancelled"

    temp = dict(first)
    temp["order_id"] = 99999
    temp["order_date"] = "2025-12-31"
    temp["customer_id"] = "C001"
    temp["status"] = "Delivered"

    second_changed = dict(second)
    second_changed["region"] = "Gazipur" if second["region"] != "Gazipur" else "Dhaka"

    events = [
        event(1, "u", int(first["order_id"]), first, first_cancelled),
        event(2, "u", int(first["order_id"]), first_cancelled, first),
        event(3, "c", 99999, None, temp),
        event(4, "d", 99999, temp, None),
        event(5, "u", int(second["order_id"]), second, second_changed),
        event(6, "u", int(second["order_id"]), second_changed, second),
    ]

    text = "\n".join(json.dumps(e, sort_keys=True, separators=(",", ":"), allow_nan=False) for e in events) + "\n"
    for path in (EXAMPLE_OUT, DOWNLOAD_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    print(f"seed {SEED} | source rows {len(orders)}")
    print(f"selected order ids: {int(first['order_id'])}, {int(second['order_id'])}")
    print(f"wrote {len(events)} CDC events -> {EXAMPLE_OUT.relative_to(ROOT)}")
    print(f"copied download -> {DOWNLOAD_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
