"""Command-line interface: read a CSV, clean it, write the result."""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

from csv_cleaner import __version__
from csv_cleaner.cleaner import MissingColumnsError, check_columns, clean_rows
from csv_cleaner.config import ConfigError, load_config

log = logging.getLogger("csv_cleaner")

EXIT_OK, EXIT_INPUT_ERROR, EXIT_REJECTED = 0, 2, 3


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="csv-clean", description="Clean a messy CSV file.")
    p.add_argument("input", type=Path, help="CSV file to clean")
    p.add_argument("-o", "--output", type=Path, help="where to write the clean CSV")
    p.add_argument("-c", "--config", type=Path, default=Path("config.toml"), help="rules file")
    p.add_argument("-v", "--verbose", action="store_true", help="show debug messages")
    p.add_argument("--log-file", type=Path, help="also write log messages to this file")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p.parse_args(argv)


def setup_logging(verbose: bool, log_file: Path | None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose, args.log_file)
    output = args.output or args.input.with_name(f"{args.input.stem}_clean.csv")

    try:
        cfg = load_config(args.config)
        with args.input.open(newline="", encoding=cfg.encoding) as f:
            reader = csv.DictReader(f)
            check_columns(reader.fieldnames or [], cfg.required_columns)
            rows = list(reader)
    except FileNotFoundError:
        log.error("Input file not found: %s", args.input)
        return EXIT_INPUT_ERROR
    except (ConfigError, MissingColumnsError, UnicodeDecodeError) as exc:
        log.error("%s", exc)
        return EXIT_INPUT_ERROR

    log.debug("Read %d data rows from %s", len(rows), args.input)
    cleaned, report = clean_rows(rows, cfg)

    if cleaned:
        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(cleaned[0].keys()))
            writer.writeheader()
            writer.writerows(cleaned)

    log.info(
        "Rows read: %d | blank removed: %d | duplicates removed: %d | rejected: %d | written: %d",
        report.rows_read,
        report.blank_removed,
        report.duplicates_removed,
        len(report.rejected),
        report.rows_written,
    )
    log.info("Clean file: %s", output)
    return EXIT_REJECTED if report.rejected else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
