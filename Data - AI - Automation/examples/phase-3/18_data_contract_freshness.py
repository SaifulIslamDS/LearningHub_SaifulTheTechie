"""Phase 3 · Data Quality · Data contract, freshness status and alerting.

Uses JSON Schema Draft 2020-12 through jsonschema. Freshness is evaluated against
fixed demonstration dates so lesson output is deterministic instead of depending
on the learner's wall clock.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data" / "orders_2025.csv"
CONTRACT = HERE / "contracts" / "orders_contract.schema.json"


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def records_for_contract(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Normalise pandas/numpy values to plain JSON-compatible Python values."""
    clean = df.copy()
    clean["order_date"] = pd.to_datetime(clean["order_date"]).dt.strftime("%Y-%m-%d")
    # Convert NaN to None through JSON, also normalising numpy scalar types.
    return json.loads(clean.to_json(orient="records"))


def validate_contract(df: pd.DataFrame, schema: dict[str, Any]) -> tuple[int, int]:
    validator = Draft202012Validator(schema)
    errors = 0
    for row in records_for_contract(df):
        errors += sum(1 for _ in validator.iter_errors(row))
    duplicate_ids = int(df["order_id"].duplicated().sum())
    return errors, duplicate_ids


def freshness_status(latest_date: date, as_of: date) -> tuple[str, int]:
    """PASS <=1 day, WARN at 2 days, ERROR at 3+ days."""
    age_days = (as_of - latest_date).days
    if age_days <= 1:
        return "PASS", age_days
    if age_days == 2:
        return "WARN", age_days
    return "ERROR", age_days


def main() -> None:
    df = pd.read_csv(SOURCE)
    schema = load_contract()
    schema_errors, duplicate_ids = validate_contract(df, schema)
    contract_ok = schema_errors == 0 and duplicate_ids == 0 and len(df) == 4246
    print(
        f"contract: {'PASS' if contract_ok else 'FAIL'} | rows {len(df)} | "
        f"schema errors {schema_errors} | duplicate order_ids {duplicate_ids}"
    )

    latest = pd.to_datetime(df["order_date"]).max().date()
    print(f"latest source date: {latest.isoformat()}")
    for as_of in (date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 4)):
        status, age = freshness_status(latest, as_of)
        print(f"freshness at {as_of.isoformat()}: {status} | age {age} day{'s' if age != 1 else ''}")

    status, age = freshness_status(latest, date(2026, 1, 4))
    if status == "ERROR":
        print(f"alert: ERROR -> stop downstream publish and notify data owner | age {age} days")


if __name__ == "__main__":
    main()
