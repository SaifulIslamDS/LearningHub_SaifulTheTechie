# Phase 3 dbt Orders Project — Starter

This is the **starter** project used by the Saiful The Techie dbt tutorials.

The connection, deterministic seeds and source declarations are ready. You will create the staging models, tests, snapshot, macro and marts while following the three tutorials.

## Start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dbt.txt
dbt debug --profiles-dir .
dbt seed --full-refresh --profiles-dir .
```

Use the `completed/` folder next to this starter as the reference implementation after you finish.
