"""Pure cleaning functions: no file access here, so they are easy to test."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

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
    missing = [c for c in required if c not in header]
    if missing:
        raise MissingColumnsError(f"Missing required columns: {', '.join(missing)}")


def is_blank(row: Row) -> bool:
    return all((v or "").strip() == "" for v in row.values())


def to_int(text: str) -> int:
    """'5,000' -> 5000. Raises ValueError for anything that isn't a whole number."""
    return int(text.replace(",", "").strip())


def to_decimal(text: str) -> float:
    return float(text.replace(",", "").strip())


def to_iso_date(text: str, fmt: str) -> str:
    """'05/01/2026' with '%d/%m/%Y' -> '2026-01-05'."""
    return datetime.strptime(text.strip(), fmt).date().isoformat()


def clean_row(row: Row, cfg: Config) -> Row:
    """Return a cleaned copy of one row. Raises ValueError if a value can't be converted."""
    out = dict(row)
    for col in cfg.trim:
        out[col] = (out.get(col) or "").strip()
    for col in cfg.title_case:
        out[col] = (out.get(col) or "").title()
    for col in cfg.integers:
        out[col] = str(to_int(out[col]))
    for col in cfg.decimals:
        out[col] = f"{to_decimal(out[col]):.2f}"
    if cfg.date_column:
        out[cfg.date_column] = to_iso_date(out[cfg.date_column], cfg.date_format)
    return out


def clean_rows(rows: list[Row], cfg: Config) -> tuple[list[Row], Report]:
    """Clean all rows: drop blanks, clean values, reject bad rows, drop duplicates, rename."""
    report = Report(rows_read=len(rows))
    cleaned: list[Row] = []
    seen: set[tuple[str, ...]] = set()

    for line_no, row in enumerate(rows, start=2):  # line 1 is the header
        if is_blank(row):
            report.blank_removed += 1
            continue
        try:
            new = clean_row(row, cfg)
        except (ValueError, KeyError) as exc:
            report.rejected.append((line_no, str(exc)))
            log.warning("Line %d rejected: %s", line_no, exc)
            continue
        key = tuple(new.values())
        if cfg.drop_duplicates and key in seen:
            report.duplicates_removed += 1
            continue
        seen.add(key)
        cleaned.append({cfg.rename.get(k, k): v for k, v in new.items()})

    report.rows_written = len(cleaned)
    return cleaned, report
