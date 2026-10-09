"""End-to-end tests: run the command on real files."""

import csv
from pathlib import Path

from csv_cleaner.cli import EXIT_INPUT_ERROR, EXIT_OK, EXIT_REJECTED, main

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "orders_raw.csv"
CONFIG = ROOT / "config.toml"
EXPECTED = Path(__file__).parent / "expected_orders.csv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_cleans_orders_raw_to_expected_output(tmp_path):
    out = tmp_path / "clean.csv"
    code = main([str(RAW), "-o", str(out), "-c", str(CONFIG)])
    assert code == EXIT_OK
    assert read(out) == read(EXPECTED)  # 12 clean orders, identical to orders.csv


def test_summary_is_logged(tmp_path, capsys):
    out = tmp_path / "clean.csv"
    main([str(RAW), "-o", str(out), "-c", str(CONFIG)])
    log_output = capsys.readouterr().err  # log messages go to stderr
    assert "blank removed: 1 | duplicates removed: 1 | rejected: 0 | written: 12" in log_output


def test_missing_input_file_returns_error_code(tmp_path):
    code = main([str(tmp_path / "nope.csv"), "-c", str(CONFIG)])
    assert code == EXIT_INPUT_ERROR


def test_missing_config_returns_error_code(tmp_path):
    code = main([str(RAW), "-c", str(tmp_path / "nope.toml")])
    assert code == EXIT_INPUT_ERROR


def test_rejected_rows_give_exit_code_3(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(RAW.read_text(encoding="utf-8").replace('"5,000"', "lots"), encoding="utf-8")
    code = main([str(bad), "-o", str(tmp_path / "out.csv"), "-c", str(CONFIG)])
    assert code == EXIT_REJECTED
