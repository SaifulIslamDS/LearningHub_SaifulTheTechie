This module turns the Phase 3 raw order data into a **version-controlled analytical transformation project**. You will use dbt to declare sources, build staging and mart models, test assumptions, preserve slowly changing customer history with a snapshot, reuse SQL logic with a macro, and generate documentation/lineage.

!!! tip "Practice project"
    Download **dbt-orders-project.zip**. Start in `starter/` while following the tutorials, then compare your work with `completed/`.

    The reference project is intentionally local: **dbt Core v1.12 + dbt-duckdb** writes to `data/phase3.duckdb`, so you do not need a cloud warehouse to learn the workflow.

!!! info "Verification status"
    The business logic and project structure are **RUN-HERE** verified in this checkpoint. The actual `dbt` CLI is **RUN-BY-OWNER** because `dbt-core` and `dbt-duckdb` are not installed in this sandbox. No dbt command output is fabricated.

**By the end of this module you can:** explain what dbt adds to SQL, build dependency-aware models with `source()` and `ref()`, write data tests, preserve history with snapshots, create reusable Jinja macros, structure staging/intermediate/mart layers, generate documentation, and reconcile a BI-ready mart to known business totals.
