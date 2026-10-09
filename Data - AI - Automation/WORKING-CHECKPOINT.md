# Working checkpoint — M8 / v0.9

**Brand:** Saiful The Techie  
**Checkpoint:** ETL/ELT + Data Quality + dbt complete  
**Release status:** Working source checkpoint; final v0.9 is not released yet.

## Completed in this checkpoint

- ETL/ELT: modular pipelines, idempotency, incremental loads, replayability and CDC.
- Data Quality: validation, pytest for data, Great Expectations, data contracts, freshness and alerting.
- dbt: models, tests, snapshots, macros, documentation and marts.
- Phase 3 source coverage: **40/55 topics**.
- Phase 3 lessons: **21**.
- Total lesson source count: **85**.
- Glossary: **199 terms**.

## Tutorial architecture upgrade

New tutorials use **Template v2**: mental model → deep explanation → verified code/data → real output → step-by-step build → completed implementation → synchronized practice files → professional context → curated resources. Quiz/common-mistake/summary/job-ready blocks are optional rather than compulsory.

The generator now supports optional YouTube companion metadata.

## Saiful The Techie branding

The public identity is **Saiful The Techie — Data, AI & Automation Path**. The UI uses the approved navy/cyan documentation-oriented direction. The exact approved circular logo must be used only when its actual binary is available; otherwise the visible header uses the text wordmark fallback. The generic ST SVG from the previous checkpoint has been removed. Until the exact approved circular logo binary is directly available, the source generator uses the approved Saiful The Techie text-wordmark fallback.

## dbt verification

- `19_dbt_logic_verification.py`: **RUN-HERE**. Reconciles 4,246 orders and 5,478,357.79 net revenue.
- `20_dbt_project_audit.py`: **RUN-HERE**. Confirms required project files and dependency references.
- dbt Core / dbt-duckdb CLI: **RUN-BY-OWNER** in this environment because the packages are unavailable. No CLI output is fabricated.

## Full-site build

**Current sandbox result:** `RUN-BY-OWNER`. The source/package checks pass, but this sandbox cannot install the required Python-Markdown package because outbound PyPI resolution is unavailable. The existing `docs/` folder therefore remains the last generated site snapshot; it is not claimed as a freshly rebuilt dbt checkpoint.

Run locally:

```bash
pip install -r requirements.txt
python tools/package_examples.py
python build.py
```

Accept the final release build only with no `WARNING:` lines and `Internal links: all OK`.

## Next approved M8 module

**AI-Ready Data** — Unstructured document pipelines + Parsing & chunking → Embedding refresh + Metadata & lineage for RAG.
