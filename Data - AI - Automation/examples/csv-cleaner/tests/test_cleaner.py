"""Unit tests for the pure cleaning functions."""

import pytest

from csv_cleaner.cleaner import (
    MissingColumnsError,
    check_columns,
    clean_rows,
    is_blank,
    to_int,
    to_iso_date,
)
from csv_cleaner.config import Config


def test_to_int_removes_thousand_separators():
    assert to_int("5,000") == 5000


def test_to_int_rejects_text():
    with pytest.raises(ValueError):
        to_int("five")


def test_to_iso_date_reads_day_first():
    # 05/01/2026 is 5 January, not 1 May
    assert to_iso_date("05/01/2026", "%d/%m/%Y") == "2026-01-05"


def test_is_blank():
    assert is_blank({"a": "", "b": "  "})
    assert not is_blank({"a": "x", "b": ""})


def test_check_columns_lists_missing():
    with pytest.raises(MissingColumnsError, match="Status"):
        check_columns(["Order ID", "Qty"], ["Order ID", "Status"])


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("  dhaka ", "Dhaka"), ("DHAKA", "Dhaka"), ("chattogram", "Chattogram")],
)
def test_region_is_trimmed_and_title_cased(raw, expected):
    cfg = Config(trim=["Region"], title_case=["Region"])
    rows, _ = clean_rows([{"Region": raw}], cfg)
    assert rows[0]["Region"] == expected


def test_duplicates_are_removed_after_cleaning():
    cfg = Config(trim=["Customer"])
    rows, report = clean_rows([{"Customer": "Rahim "}, {"Customer": "Rahim"}], cfg)
    assert len(rows) == 1
    assert report.duplicates_removed == 1


def test_bad_row_is_rejected_not_crashed():
    cfg = Config(integers=["Qty"])
    rows, report = clean_rows([{"Qty": "10"}, {"Qty": "ten"}], cfg)
    assert [r["Qty"] for r in rows] == ["10"]
    assert report.rejected[0][0] == 3  # line 3 of the file (line 1 is the header)
