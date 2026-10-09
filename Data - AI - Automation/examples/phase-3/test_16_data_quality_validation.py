"""Tests for 16_data_quality_validation.py."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "16_data_quality_validation.py"
spec = importlib.util.spec_from_file_location("data_quality_validation", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


@pytest.fixture
def orders() -> pd.DataFrame:
    return module.load_orders()


def failed_checks(df: pd.DataFrame) -> set[str]:
    return {result.name for result in module.validate_orders(df) if not result.passed}


def test_clean_dataset_passes_all_checks(orders: pd.DataFrame) -> None:
    assert all(result.passed for result in module.validate_orders(orders))


def test_known_answers(orders: pd.DataFrame) -> None:
    assert len(orders) == 4246
    assert orders["order_id"].nunique() == 4246
    assert module.net_revenue(orders) == 5_478_357.79


@pytest.mark.parametrize(
    ("column", "value", "expected_check"),
    [
        ("status", "Returned", "status domain"),
        ("quantity", 0, "positive quantity"),
        ("discount", 0.50, "discount range"),
        ("order_date", "2026-01-01", "order date"),
        ("revenue", -1.0, "revenue formula"),
    ],
)
def test_bad_value_is_detected(
    orders: pd.DataFrame, column: str, value: object, expected_check: str
) -> None:
    bad = orders.copy()
    bad.loc[0, column] = value
    assert expected_check in failed_checks(bad)


def test_duplicate_order_id_is_detected(orders: pd.DataFrame) -> None:
    bad = orders.copy()
    bad.loc[1, "order_id"] = bad.loc[0, "order_id"]
    assert "order_id grain" in failed_checks(bad)


def test_cancelled_order_with_delivery_days_is_detected(orders: pd.DataFrame) -> None:
    bad = orders.copy()
    idx = bad.index[bad["status"].eq("Cancelled")][0]
    bad.loc[idx, "delivery_days"] = 3
    assert "cancelled delivery" in failed_checks(bad)
