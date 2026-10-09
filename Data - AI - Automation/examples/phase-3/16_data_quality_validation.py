"""Phase 3 · Data Quality · Validation rules for the 2025 orders dataset.

Runs with pandas only. The checks are intentionally plain Python so learners can
see the rules before using a data-quality framework. The functions are imported
by test_16_data_quality_validation.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data" / "orders_2025.csv"

EXPECTED_COLUMNS = [
    "order_id", "order_date", "customer_id", "region", "segment", "channel",
    "category", "product", "quantity", "unit_price", "discount", "unit_cost",
    "status", "promised_days", "delivery_days", "revenue",
]
ALLOWED_STATUSES = {"Delivered", "Cancelled", "Shipped", "Pending"}


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


def load_orders() -> pd.DataFrame:
    return pd.read_csv(SOURCE, parse_dates=["order_date"])


def validate_orders(df: pd.DataFrame) -> list[CheckResult]:
    """Return deterministic dataset-level validation results."""
    results: list[CheckResult] = []

    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    unexpected = [c for c in df.columns if c not in EXPECTED_COLUMNS]
    results.append(CheckResult(
        "schema",
        not missing and not unexpected,
        f"required {len(EXPECTED_COLUMNS)} columns | missing {len(missing)} | unexpected {len(unexpected)}",
    ))

    results.append(CheckResult(
        "row count",
        len(df) == 4246,
        f"expected 4246 | actual {len(df)}",
    ))

    id_nulls = int(df["order_id"].isna().sum()) if "order_id" in df else len(df)
    duplicates = int(df["order_id"].duplicated().sum()) if "order_id" in df else len(df)
    results.append(CheckResult(
        "order_id grain",
        id_nulls == 0 and duplicates == 0,
        f"nulls {id_nulls} | duplicates {duplicates}",
    ))

    statuses = set(df["status"].dropna().astype(str)) if "status" in df else set()
    invalid_statuses = sorted(statuses - ALLOWED_STATUSES)
    status_nulls = int(df["status"].isna().sum()) if "status" in df else len(df)
    results.append(CheckResult(
        "status domain",
        not invalid_statuses and status_nulls == 0,
        f"invalid {invalid_statuses or 'none'} | nulls {status_nulls}",
    ))

    bad_quantity = int((pd.to_numeric(df["quantity"], errors="coerce") <= 0).sum())
    results.append(CheckResult(
        "positive quantity",
        bad_quantity == 0,
        f"invalid rows {bad_quantity}",
    ))

    discounts = pd.to_numeric(df["discount"], errors="coerce")
    bad_discount = int((~discounts.between(0, 0.08, inclusive="both")).sum())
    results.append(CheckResult(
        "discount range",
        bad_discount == 0,
        f"outside 0.00..0.08: {bad_discount}",
    ))

    dates = pd.to_datetime(df["order_date"], errors="coerce")
    bad_dates = int((dates.isna() | (dates.dt.year != 2025)).sum())
    results.append(CheckResult(
        "order date",
        bad_dates == 0,
        f"unparseable/outside 2025: {bad_dates}",
    ))

    expected_revenue = (
        pd.to_numeric(df["quantity"]) *
        pd.to_numeric(df["unit_price"]) *
        (1 - pd.to_numeric(df["discount"]))
    ).round(2)
    actual_revenue = pd.to_numeric(df["revenue"])
    revenue_mismatches = int(((actual_revenue - expected_revenue).abs() > 0.001).sum())
    results.append(CheckResult(
        "revenue formula",
        revenue_mismatches == 0,
        f"mismatches {revenue_mismatches}",
    ))

    cancelled = df["status"].eq("Cancelled")
    cancelled_with_delivery = int((cancelled & df["delivery_days"].notna()).sum())
    results.append(CheckResult(
        "cancelled delivery",
        cancelled_with_delivery == 0,
        f"cancelled rows with delivery_days: {cancelled_with_delivery}",
    ))

    return results


def net_revenue(df: pd.DataFrame) -> float:
    return round(df.loc[df["status"] != "Cancelled", "revenue"].sum(), 2)


def corruption_demo(df: pd.DataFrame) -> list[str]:
    """Make four deterministic defects and report which validation rules fail."""
    bad = df.copy()
    bad.loc[1, "order_id"] = bad.loc[0, "order_id"]
    bad.loc[2, "status"] = "Returned"
    bad.loc[3, "quantity"] = 0
    bad.loc[4, "revenue"] = float(bad.loc[4, "revenue"]) + 10.0
    return [r.name for r in validate_orders(bad) if not r.passed]


def main() -> None:
    df = load_orders()
    results = validate_orders(df)
    passed = sum(r.passed for r in results)
    print(f"validation summary: {passed}/{len(results)} checks passed | rows {len(df)}")
    for result in results:
        label = "PASS" if result.passed else "FAIL"
        print(f"{label:4} | {result.name:<20} | {result.detail}")
    print(
        f"known answer: rows {len(df)} | unique order_ids {df['order_id'].nunique()} | "
        f"net revenue {net_revenue(df):.2f}"
    )
    failed = corruption_demo(df)
    print(f"corruption demo: {len(failed)} failed checks | {', '.join(failed)}")


if __name__ == "__main__":
    main()
