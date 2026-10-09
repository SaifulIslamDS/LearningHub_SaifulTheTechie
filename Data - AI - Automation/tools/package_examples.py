#!/usr/bin/env python3
"""
Zip the example projects in examples/ into content/downloads/ (phase-0/, phase-2/), and copy the
Phase 2 charts used in lessons into content/images/phase-2/.

    python tools/package_examples.py

Zips are deterministic (fixed timestamps, sorted names), so rebuilding without
changes produces identical files.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "examples"
DOWNLOADS = ROOT / "content" / "downloads"
IMAGES = ROOT / "content" / "images"

# (source folder in examples/, zip path in content/downloads/, folder name inside the zip)
PACKAGES = [
    ("csv-cleaner-starter", "phase-0/csv-cleaner-starter.zip", "csv-cleaner"),
    ("csv-cleaner", "phase-0/csv-cleaner-solution.zip", "csv-cleaner"),
    ("linux-practice", "phase-0/linux-practice.zip", "practice"),
    ("python-refresher", "phase-0/python-refresher.zip", "python-refresher"),
    ("phase-2", "phase-2/data-science-scripts.zip", "data-science"),
]
SKIP_DIRS = {".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".git", "charts", "results"}
SKIP_FILES = {"orders_big.csv", "orders_big.parquet", "units_by_year.parquet"}   # large, regenerated locally
SKIP_SUFFIXES = {".pyc"}


def wanted(path: Path) -> bool:
    return (not any(part in SKIP_DIRS for part in path.parts)
            and path.suffix not in SKIP_SUFFIXES
            and path.name not in SKIP_FILES
            and not path.name.endswith("_clean.csv"))


def make_zip(src: Path, dest: Path, root_name: str) -> int:
    files = sorted(p for p in src.rglob("*") if p.is_file() and wanted(p.relative_to(src)))
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            info = zipfile.ZipInfo(f"{root_name}/{p.relative_to(src).as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if p.suffix == ".sh" else 0o644) << 16
            zf.writestr(info, p.read_bytes())
    return len(files)


def main():
    for folder, zip_name, root_name in PACKAGES:
        src = EX / folder
        if not src.is_dir():
            print(f"skip {folder} (not found)")
            continue
        dest = DOWNLOADS / zip_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        n = make_zip(src, dest, root_name)
        print(f"{zip_name}: {n} files, {dest.stat().st_size // 1024} KB")
    charts = EX / "phase-2" / "charts"
    if charts.is_dir():
        (IMAGES / "phase-2").mkdir(parents=True, exist_ok=True)
        pngs = sorted(charts.glob("*.png"))
        for png in pngs:
            (IMAGES / "phase-2" / png.name).write_bytes(png.read_bytes())
        print(f"copied {len(pngs)} charts to content/images/phase-2/")


if __name__ == "__main__":
    main()
