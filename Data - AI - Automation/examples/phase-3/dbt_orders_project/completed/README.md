# Phase 3 dbt Orders Project — Completed

A local DuckDB-backed dbt Core project for the Saiful The Techie Data, AI & Automation Path.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dbt.txt
```

## First build

```bash
dbt debug --profiles-dir .
dbt seed --full-refresh --profiles-dir .
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
```

The reconciliation test expects **4,246 rows** and **5,478,357.79** net revenue.

## Snapshot change demo

```bash
python scripts/reset_snapshot_demo.py
dbt seed --select customers_2025 --full-refresh --profiles-dir .
dbt snapshot --select customers_snapshot --profiles-dir .
python scripts/apply_snapshot_change.py
dbt seed --select customers_2025 --full-refresh --profiles-dir .
dbt snapshot --select customers_snapshot --profiles-dir .
python scripts/inspect_snapshot.py
```

The second snapshot run should create a second historical version for customer `C007`.
