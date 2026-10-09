"""Phase 3 · ETL/ELT · Modular, idempotent pipeline with incremental loads.

Runs with pandas only. The demo starts from an empty target, loads orders through
November, then loads only December. It retries the same December batch to prove
that the upsert load is idempotent.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data" / "orders_2025.csv"
RESULTS = HERE / "results" / "etl_incremental"
TARGET = RESULTS / "orders_curated.csv"
STATE = RESULTS / "state.json"


def extract_orders(start_exclusive: str | None = None, end_inclusive: str | None = None) -> pd.DataFrame:
    """Extract the requested date window from the source export."""
    df = pd.read_csv(SOURCE, parse_dates=["order_date"])
    if start_exclusive:
        df = df[df["order_date"] > pd.Timestamp(start_exclusive)]
    if end_inclusive:
        df = df[df["order_date"] <= pd.Timestamp(end_inclusive)]
    return df.copy()


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Apply deterministic checks and column ordering before the load."""
    out = df.copy()
    if out["order_id"].duplicated().any():
        raise ValueError("source batch contains duplicate order_id values")
    if (out["quantity"] <= 0).any():
        raise ValueError("quantity must be positive")
    if out["status"].isna().any():
        raise ValueError("status must not be null")
    out["order_date"] = pd.to_datetime(out["order_date"]).dt.strftime("%Y-%m-%d")
    return out.sort_values("order_id").reset_index(drop=True)


def load_upsert(batch: pd.DataFrame) -> pd.DataFrame:
    """Upsert by business key so a retry replaces rows instead of duplicating them."""
    RESULTS.mkdir(parents=True, exist_ok=True)
    if TARGET.exists():
        current = pd.read_csv(TARGET)
        combined = pd.concat([current, batch], ignore_index=True)
    else:
        combined = batch.copy()
    combined = (combined.drop_duplicates(subset=["order_id"], keep="last")
                        .sort_values("order_id")
                        .reset_index(drop=True))
    combined.to_csv(TARGET, index=False, lineterminator="\n")
    return combined


def save_watermark(value: str) -> None:
    STATE.write_text(json.dumps({"last_order_date": value}, sort_keys=True) + "\n", encoding="utf-8")


def run_window(label: str, start_exclusive: str | None, end_inclusive: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    extracted = extract_orders(start_exclusive, end_inclusive)
    transformed = transform_orders(extracted)
    target = load_upsert(transformed)
    save_watermark(end_inclusive)
    print(f"{label}: extracted {len(extracted)} | target {len(target)} | watermark {end_inclusive}")
    return transformed, target


def net_revenue(df: pd.DataFrame) -> float:
    return round(df.loc[df["status"] != "Cancelled", "revenue"].sum(), 2)


def main() -> None:
    shutil.rmtree(RESULTS, ignore_errors=True)

    run_window("initial", None, "2025-11-30")
    december, full = run_window("incremental", "2025-11-30", "2025-12-31")

    # Retry the exact same December batch. The row count must stay unchanged.
    retried = load_upsert(december)
    duplicate_ids = int(retried["order_id"].duplicated().sum())
    print(f"retry same batch: extracted {len(december)} | target {len(retried)} | duplicate order_ids {duplicate_ids}")

    print(f"known answer: rows {len(full)} | net revenue {net_revenue(full):.2f}")


if __name__ == "__main__":
    main()
