"""Pure cleaning functions: no file access here, so they are easy to test.

STARTER VERSION — implement every function marked TODO until `uv run pytest` passes.
Read tests/test_cleaner.py first: the tests describe exactly what each function must do.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from csv_cleaner.config import Config

log = logging.getLogger(__name__)

Row = dict[str, str]


@dataclass
class Report:
    """What happened during cleaning — logged at the end and useful in tests."""

    rows_read: int = 0
    blank_removed: int = 0
    duplicates_removed: int = 0
    rejected: list[tuple[int, str]] = field(default_factory=list)  # (line number, reason)
    rows_written: int = 0


class MissingColumnsError(Exception):
    """Raised when the input file lacks required columns."""


def check_columns(header: list[str], required: list[str]) -> None:
    """TODO: raise MissingColumnsError naming every required column missing from header."""
    raise NotImplementedError


def is_blank(row: Row) -> bool:
    """TODO: True when every value in the row is empty or only spaces."""
    raise NotImplementedError


def to_int(text: str) -> int:
    """TODO: '5,000' -> 5000. Raise ValueError for anything that isn't a whole number."""
    raise NotImplementedError


def to_decimal(text: str) -> float:
    """TODO: '3.50' -> 3.5 (also remove thousand separators)."""
    raise NotImplementedError


def to_iso_date(text: str, fmt: str) -> str:
    """TODO: '05/01/2026' with '%d/%m/%Y' -> '2026-01-05'. Hint: datetime.strptime."""
    raise NotImplementedError


def clean_row(row: Row, cfg: Config) -> Row:
    """TODO: return a cleaned COPY of one row using the rules in cfg:
    trim -> title_case -> integers -> decimals (format with 2 decimals) -> date column.
    Let ValueError propagate if a value can't be converted.
    """
    raise NotImplementedError


def clean_rows(rows: list[Row], cfg: Config) -> tuple[list[Row], Report]:
    """TODO: clean all rows and fill in a Report.
    - skip blank rows (count them)
    - clean each row; on ValueError/KeyError add (line_number, reason) to report.rejected
      (line numbers start at 2 because line 1 is the header) and log a warning
    - skip duplicates AFTER cleaning when cfg.drop_duplicates is true (count them)
    - rename columns with cfg.rename
    """
    raise NotImplementedError
