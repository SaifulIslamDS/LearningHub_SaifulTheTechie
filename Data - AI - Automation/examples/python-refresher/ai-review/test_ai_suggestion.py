"""Known-answer tests for the AI-suggested function. Run: python -m pytest -v"""

from pathlib import Path

import pytest
from ai_suggestion import net_revenue_by_month

RAW = Path(__file__).parent.parent / "data" / "orders_raw.csv"
HEADER = "Order ID,Order Date,Customer,Region,Category,Product,Qty,Unit Price,Status\n"


def write_csv(tmp_path, rows):
    f = tmp_path / "orders.csv"
    f.write_text(HEADER + "".join(rows), encoding="utf-8")
    return f


def test_only_q1_months():
    assert list(net_revenue_by_month(RAW)) == ["2026-01", "2026-02", "2026-03"]


def test_known_monthly_totals():
    expected = {"2026-01": 3440.0, "2026-02": 3940.0, "2026-03": 1695.0}
    assert net_revenue_by_month(RAW) == pytest.approx(expected)


def test_total_matches_known_answer():
    assert sum(net_revenue_by_month(RAW).values()) == pytest.approx(9075.0)


def test_day_first_dates(tmp_path):
    f = write_csv(tmp_path, ["1,15/01/2026,A,Dhaka,F,P,10,1.00,Delivered\n"])
    assert net_revenue_by_month(f) == pytest.approx({"2026-01": 10.0})


def test_cancelled_excluded(tmp_path):
    f = write_csv(
        tmp_path,
        [
            "1,05/01/2026,A,Dhaka,F,P,10,1.00,Delivered\n",
            "2,06/01/2026,A,Dhaka,F,P,10,1.00,CANCELLED\n",
        ],
    )
    assert net_revenue_by_month(f) == pytest.approx({"2026-01": 10.0})


def test_quantity_with_thousands_separator(tmp_path):
    f = write_csv(tmp_path, ['1,05/01/2026,A,Dhaka,F,P,"5,000",0.04,Delivered\n'])
    assert net_revenue_by_month(f) == pytest.approx({"2026-01": 200.0})
