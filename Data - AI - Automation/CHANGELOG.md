# Changelog

Each release is packaged as `data-ai-automation-path-vX.Y[.Z].zip`, and its version shows under the site name in the top bar.

## v0.9.1 — M8 platform correction: ready-to-use generated site, AI Mentor Prompts & roadmap projections (2026-10-09)

This patch-style release fixes the gap between the source tree and the learner-facing product before M8 continues. M8 remains in progress; Phase 3 is still **40/55 topics** with **21 lessons**.

- **Generated site caught up to source:** the dbt tutorials are now present in `docs/` instead of the older placeholder snapshot. `python build.py` can use Python-Markdown when installed and an offline Pandoc fallback in environments where PyPI installation is unavailable.
- **AI Mentor Prompt on every written tutorial:** all 85 tutorial pages now receive a professional, detailed, lesson-specific interactive mentoring prompt with a copy button. It uses the tutorial title, level, curriculum topics, keywords and practice files; Phase 3 prompts also preserve the established 4,246-order / 5,478,357.79 reconciliation targets where relevant.
- **Reviewed YouTube companions across completed M8 work:** all 8 ETL/ELT, Data Quality and dbt tutorials now render a relevant privacy-enhanced `youtube-nocookie.com` frame with creator/context metadata; focused timestamps are included where they materially help.
- **No ambiguous future-status UI:** planned topics now show the roadmap milestone/version in which they are projected to be written (for example `M9 · v1.0` or `M11 · v1.2`).
- **Roadmap/product audit:** added `handover/v0.9.1-CODEBASE-AUDIT.md` documenting source/product mismatches, roadmap anomalies and the correction status.
- **Template v2:** documents the automatic mentor prompt and richer YouTube metadata.
- **Version:** the visible site version is now **v0.9.1**.
- **Next approved M8 module:** **AI-Ready Data**.

## v0.9 — M8 working checkpoint: ETL/ELT + Data Quality + dbt (in progress)

This is a **working source checkpoint**, not the final v0.9 release. Phase 3 now covers **40 of 55 topics** with **21 lessons**; the whole site source contains **85 lessons**.

- **ETL/ELT:** modular pipelines, idempotency, incremental loads, replayability and CDC.
- **Data Quality:** validation + pytest, Great Expectations, data contracts, freshness and alerting.
- **dbt (3 deep tutorials):** Models & Tests; Snapshots & Macros; Documentation & Marts. The synchronized `dbt-orders-project.zip` contains `starter/` and `completed/` local DuckDB projects.
- **dbt verification:** transformation logic and project structure run here; dbt CLI itself is **RUN-BY-OWNER** because dbt/duckdb are unavailable in this sandbox. Known answers still reconcile to 4,246 orders and 5,478,357.79 net revenue.
- **Tutorial architecture upgrade:** Template v2 makes old quiz/mistakes/summary/job-ready blocks optional, prioritizes mental models, verified output, step-by-step builds and synchronized practice files, and adds optional YouTube companion rendering.
- **Saiful The Techie UI:** navy/cyan documentation-oriented system retained. The exact approved circular logo is used only when its real binary is available; otherwise the header uses a text wordmark fallback.
- **Glossary:** 199 terms after adding dbt model, data test, materialization, dbt snapshot, Jinja macro, data mart, data lineage and staging model.
- **Next approved M8 module:** AI-Ready Data.


## v0.8 — Phase 3A: Data Engineering, storing & serving data (2026-10-09)

Milestone **M7**. Phase 3 (13 modules, 55 topics) is split into two releases; this one adds **13 lessons** in 6 modules (25 topics). Written so far: 135 of 371 topics, 77 lessons.

- **Data ingestion (2):** REST APIs with a Bearer token, `requests.Session`, timeouts, retries with back-off on 429/5xx, following pagination to the end, landing raw JSON and reconciling totals, incremental loads; responsible scraping (robots.txt, crawl delay, User-Agent) with Beautiful Soup; CSV vs JSON vs JSON Lines vs Parquet (size, types, column reads) and `json_normalize`.
- **Advanced SQL (2):** CTEs as named steps, a cohort count, recursive CTEs for a date spine and an org-chart hierarchy; window functions: group shares, running totals, moving averages, ROW_NUMBER/RANK/DENSE_RANK with ties, top-N per group, LAG/LEAD growth and gaps between orders.
- **Database engineering (3):** loading PostgreSQL with COPY into staging, normalising into `shop` with keys and constraints, update anomalies, NUMERIC vs float money (a real 1.31 difference explained); indexes and EXPLAIN ANALYZE on 2 million rows (145 ms → 7 ms), composite indexes, selectivity and functions on columns; transactions, ACID, rollback on failure, CHECK constraints and the lost-update race fixed with `SELECT … FOR UPDATE`.
- **Data warehousing (2):** OLTP vs OLAP, grain, facts, dimensions and surrogate keys in a PostgreSQL star schema; SCD type 2 with idempotent loads and as-was vs as-is reporting; BigQuery dialect translation (sqlglot), DuckDB as a local columnar stand-in, bytes-scanned cost and partitioning/clustering.
- **Lakehouse (2):** a local Delta Lake lakehouse with bronze/silver/gold layers, partitioning, schema enforcement, MERGE and time travel; Apache Iceberg with PyIceberg (snapshots, schema evolution, file pruning) and a Fabric / Databricks / Snowflake comparison.
- **Docker (2):** Dockerfile, layer caching, non-root user, containers on a network with environment variables and bind mounts, debugging; Docker Compose with health checks, `depends_on`, `.env`, exit codes, a real PID-1 stop-signal fix (`STOPSIGNAL`), and reproducible environments (pins, lock files, digests).
- **Practice API:** `mock_api.py`, a local API (token auth, pagination, rate limiting) and catalogue website serving the 2025 data, used by the ingestion and Docker lessons.
- **Files:** `data-engineering-scripts.zip` with 13 scripts/SQL files, the practice API and a `docker/` folder (Dockerfiles, compose.yaml, ingest job).
- **Glossary:** 182 terms (14 new: pagination, rate limit, web scraping, OLTP/OLAP, surrogate key, SCD, BigQuery, transaction, EXPLAIN ANALYZE, PostgreSQL, medallion, Delta Lake, Apache Iceberg, Docker Compose); CTE, window function, index, normalisation, Docker, data warehouse, lakehouse and API now link to their new lessons.
- **Roadmap:** Phase 3 split into M7 (v0.8, done) and M8 (v0.9, next); later milestones move one version later (Phase 5 → v1.0 … Platform upgrade 2 stays v2.0).
- **Roadmap and handover (docs update, same day):** `ROADMAP.md` now has a progress-by-phase table, open items, a lesson-by-lesson plan and verification plan for M8 (Phase 3B), and the scope of M9–M13. New `handover/` folder with `HANDOVER.md` and a ready-to-paste prompt (`CHATGPT-PROMPT.md`) for continuing the work in another AI assistant.
- **Verification:** all outputs come from real runs: PostgreSQL 16.15 (the SQL works on 16–18), Docker Engine 29.8 and Compose 5.5, Python 3.13, requests 2.34, Beautiful Soup 4.15, pandas 3.0, psycopg 3.3, DuckDB 1.5, sqlglot 30, deltalake 1.6, PyIceberg 0.12. Docker Hub wasn't reachable from the build machine, so the Docker outputs used a local stand-in for `python:3.14-slim` (stated in the lessons). BigQuery commands, the uv-in-Docker variant and the Postgres compose service are shown for reference and marked as not executed.

## v0.7 — Phase 2: Python, Statistics & Data Science (2026-10-09)

Milestone **M6**. 21 new lessons; **Phase 2 is complete** (41 of 41 topics). Written so far: 110 of 371 topics, 64 lessons.

- **NumPy (2):** arrays, dtypes, indexing and boolean masks; vectorized maths, broadcasting, NaN handling, floating-point care and seeded random numbers.
- **pandas (4):** DataFrame basics; cleaning a messy 4,264-line ERP export into the reference file (checked with `assert_frame_equal`); merge with `validate`, anti-joins and groupby; pivot tables, datetime, resampling and rolling averages.
- **Polars & DuckDB (2):** Polars expressions and lazy queries; DuckDB SQL on CSV and Parquet, and working with a multi-million-row local file (`make_big_data.py`).
- **EDA (2):** analytical questions, profiles, skewed distributions, weekly and monthly patterns; crosstabs, rates with counts, Spearman correlation, confounding and reverse causation; anomalies with IQR and rolling-median rules, classified as error, event, outlier or unexplained.
- **Statistics (2):** mean, median, trimmed mean, IQR, standard deviation and CV; normal, log-normal, Poisson and binomial distributions; Pearson vs Spearman; t, Wilson and bootstrap confidence intervals.
- **A/B testing (2):** a full readout of a checkout experiment (SRM check, two-proportion z-test, CI, guardrails, segments); power analysis, a peeking simulation (4.5% → 26.5% false positives) and confounding in observational data.
- **Visualization (2):** matplotlib Figure/Axes, annotations and small multiples; seaborn bar plots with CIs, box plots and heatmaps; Plotly interactive charts; a before/after storytelling redesign and a five-sentence data story.
- **ML foundations (3):** scikit-learn pipelines, baselines, ROC AUC, thresholds and time-based splits; target leakage (AUC 1.000) and aggregate leakage, scaling for KNN; feature engineering, cross-validation and a bias/variance curve.
- **Research thinking (2):** research questions, units of randomisation and feasibility via power analysis; reproducibility (environment, data hashes, seeds, provenance), evaluation against a baseline with bootstrap CIs, sensitivity checks and reporting.
- **Phase 2 milestone project page:** Business Analytics Study, with requirements, nine known answers, a repository layout and a rubric.
- **Practice data and files:** `tools/make_phase2_data.py` generates the 2025 datasets with a fixed seed (orders, raw export, customers, products, A/B test). `data-science-scripts.zip` holds all 21 lesson scripts with solutions. New templates: experiment plan and analysis report. 18 lesson charts (colour-blind-checked palette).
- **Glossary:** 168 terms (29 new, from p-value and statistical power to data leakage and DuckDB); existing Phase 2 terms now link to their lessons.
- **Tools:** `package_examples.py` now builds the Phase 2 zip and copies lesson charts into `content/images/`. Large generated files are git-ignored.
- **Verification:** every printed result and chart comes from running the scripts (Python 3.13; numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, statsmodels 0.15.0, scikit-learn 1.9.1, polars 2.0.0, duckdb 1.5.6, matplotlib 3.11.2, seaborn 0.13.2, plotly 7.1.0). All 21 scripts run end to end; generated data is byte-identical across runs.

## v0.6 — Platform upgrade 1: glossary, quiz scoring, SEO (2026-10-09)

Milestone **M5**.

- **Glossary:** a new Glossary page with 139 plain-English terms in 11 categories, from SQL and DAX to RAG, MCP and AI governance. It has A–Z navigation, a live text filter and a category filter. Each term links to the lesson where it is taught (or the module where it will be), and lists other lessons that use it. Terms are searchable from the top bar. Added to the top bar and the curriculum menu.
- **Key terms in every lesson:** a "Key terms in this lesson" box (matched from the lesson's keywords, or forced with `terms:`), each chip linking to its definition, with the definition on hover.
- **Quiz scoring:** quiz options are now clickable. Correct and wrong answers are marked, the explanation opens, and a score out of 3 appears with **Try again**. The best score per lesson is saved in the browser and shown next to the lesson on its module page. The build reads the answer letter of all 129 questions and warns if one can't be scored. "Reset progress" also clears quiz scores.
- **SEO & sharing:** Open Graph and Twitter card tags on every page (lessons as articles), a 1200×630 share image (`assets/og-image.png`, made by `tools/make_og_image.py`), `robots.txt`, and, once `site_url` is set, canonical links, absolute share URLs and `sitemap.xml` (155 URLs, lessons dated by their review date).
- **External link check:** the weekly workflow now writes a report and opens (or comments on) a GitHub issue labelled `broken-links`, using the built-in GitHub CLI. It also checks the glossary and README.
- **Top bar:** links stay on one line; on narrower screens the lower-priority links move to the curriculum menu.
- **Docs:** CONTRIBUTING explains the quiz answer format and how to add glossary terms; How to learn explains quiz scores and Key terms; README covers sitemap submission and share previews.
- **Verification:** the glossary filter, quiz scoring, retry, saved best scores, module badges, search results and layout (1500, 1300, 1000 and 390 px wide) were tested in Chromium with no script errors. The sitemap was validated as XML with a test `site_url`. External links could not be checked from the build environment (no outbound web access), so the first scheduled link check on GitHub is the review step.

## v0.5 — Phase 0: Engineering Foundations, practice-file library (2026-10-09)

Milestone **M4: Phase 0**. 16 new lessons; **Phase 0 is complete** (26 of 26 topics). Phases 0 and 1 together: 69 of 371 topics, 43 lessons.

- **Development Environment (3):** Python 3.14 + VS Code and interpreters; uv, virtual environments, `pyproject.toml` and `uv.lock`; debugging with tracebacks, breakpoints and `breakpoint()`.
- **Git & GitHub (3):** repositories, staging, commits and `.gitignore`; branches, fast-forward merges and a real merge conflict; remotes, pull requests, code review, README and project structure.
- **Linux Essentials (2):** filesystem, paths, permissions and terminal habits (with WSL); grep, pipes, redirection, a safe shell script and cron schedules.
- **Programming Refresher (4):** variables, conditions, loops and functions; lists, dicts, sets and tuples; files, CSV/JSON and exceptions; dataclasses, OOP and type hints (with mypy).
- **Testing & CI (2):** pytest (parametrize, `pytest.raises`, reading failures) and ruff lint/format; GitHub Actions with uv, scheduled workflows and secrets.
- **AI-Assisted Development (2):** coding agents and copilots, four-part prompts and `AGENTS.md`; reviewing and testing an AI-written function that runs cleanly but returns 5,875 instead of 9,075.
- **Phase 0 Gate project page:** CSV Data Cleaning CLI, with a **starter** (CLI, config and 17 tests ready; 7 functions to write) and a **reference solution** (17 passing tests, CI workflow, AGENTS.md).
- **Practice-file library:** a "Practice files" page with every file grouped and described, a "Practice files for this page" box on every lesson, module and project page, and a one-click bundle `downloads/practice-files.zip`. The build warns about missing or uncatalogued files.
- **New practice files:** `products.csv`, `regions.csv`, `targets_long.csv`, `known_answers.csv` (24 checks), `sql-solutions.sql`, `excel-solutions.xlsx`, three Markdown templates (KPI dictionary, executive summary, decision memo) and four Phase 0 zips (`python-refresher`, `linux-practice`, `csv-cleaner-starter`, `csv-cleaner-solution`).
- **Phase 1 lessons:** every lesson now lists its practice files.
- **Tools:** `tools/make_practice_files.py` rebuilds the Excel workbooks; `tools/package_examples.py` rebuilds the Phase 0 zips from `examples/`. Both produce identical files on every run.
- **Fix:** GitHub removed Node 20 from Actions runners on 2026-09-23, so the repository workflows now use `actions/checkout@v7` and `actions/setup-python@v7`.
- **Verification:** every command and script output was pasted from a real run (Python 3.13 and 3.14, uv, Git, bash, pytest 9.1, ruff 0.16, mypy 2.3). All 17 csv-cleaner tests pass; the starter gives 13 failed / 4 passed as documented. SQL answer keys were run in SQLite and Excel answer keys recalculated in LibreOffice (XLOOKUP, FILTER and LET were checked against equivalent formulas, because LibreOffice 24.2 doesn't support them). Tool versions and commands were checked against official docs (October 2026).

## v0.4 — Phase 1B: Power BI stack, Phase 1 complete (2026-10-09)

Milestone **M3: Phase 1B**. 14 new lessons; **Phase 1 is complete** (43 of 43 topics, 27 lessons).

- **Power Query (3):** cleaning a messy export (locale-correct dates, trim, de-duplicate, with full M code); merge (join kinds, anti join) & append; unpivot & combining a folder of monthly files.
- **Power Pivot & DAX (3):** star schema, relationships and a date table; measures & KPI logic (Net Revenue, AOV, Target, Achievement %, Gap); CALCULATE & filter context (delivered revenue, share of total, month-on-month growth).
- **Power BI (4):** model hygiene and a KPI overview page; drill-through and bookmarks; row-level security (static and dynamic); publishing, licences, refresh, and Copilot requirements with answer validation.
- **Semantic models (1), AI-assisted analytics (1), data storytelling (2):** one KPI definition and reuse in Excel and AI; prompting and validating AI formulas, DAX and SQL; executive summaries, decision memos and stakeholder communication.
- **Phase 1 milestone project page:** Executive BI System brief, requirements, known answers, repository layout, README template and rubric.
- **New practice data:** `orders_raw.csv`, `monthly/orders_2026-01..03.csv`, `targets_wide.csv`, `sales_model.xlsx`.
- **Build:** optional milestone project page per phase (`content/projects/<phase-id>.md`), linked from the phase page and the curriculum menu.
- **Verification:** the Power Query cleaning steps were replayed in pandas, and the result is identical to `orders.csv`. All DAX and report numbers were recomputed in pandas from the model tables. Power BI / Power Query features and requirements were checked against Microsoft Learn (October 2026). The M and DAX code was not executed, because there is no Power BI engine in the build environment.

## v0.3 — Phase 1A: SQL, Excel & Pivot (2026-10-09)

Milestone **M2: Phase 1A**. 11 new lessons; 3 modules now complete (17 topics).

- **Analytical SQL (complete, 5 lessons):** new lessons on CASE expressions, JOINs (INNER / LEFT, anti-join, the LEFT JOIN + WHERE trap) and subqueries (IN, EXISTS, derived tables, first look at CTEs).
- **Excel for Analysis (complete, 5 lessons):** IF/IFS/AND/OR; SUMIFS/COUNTIFS/AVERAGEIFS; XLOOKUP and INDEX/MATCH; FILTER and LET; conditional formatting.
- **Pivot Analysis (complete, 3 lessons):** PivotTables and grouping; slicers and timelines; What-If Analysis (Data Table, Scenario Manager) and Goal Seek.
- **Practice data:** new `customers` table (in `orders.sql` and `customers.csv`) and an Excel workbook `orders.xlsx` (Orders, Products and Customers sheets).
- **Verification:** every SQL result was run in SQLite. Excel results were recalculated in LibreOffice, and pivot and What-If numbers were cross-checked in pandas.
- **Fixes:** added `order_id` tie-breakers to "top n" queries (orders 5 and 8 share a value), so every database returns the same rows.
- **Build:** keywords such as `on` / `true` are now always treated as text.

## v0.2 — Go-live package (2026-10-09)

Milestone **M1: Go live**.

- **Version display:** the release number shows under the site name in the top bar and in the footer. It is set in `site.yml`.
- **Licences:** MIT for the code (`LICENSE`) and CC BY-NC-SA 4.0 for the lesson content (`LICENSE-CONTENT.md`). There is also a licence page on the site, linked from every footer.
- **404 page:** a friendly "Page not found" page for the live site, with a working link home.
- **Go-live guide:** README steps for GitHub Desktop and the command line, GitHub Pages setup, a live-site checklist and how to update to new versions.
- **Site name confirmed:** "Data, AI & Automation Path".
- **Lesson template locked as Template v1**, based on the two SQL pilot lessons.
- **Curriculum menu:** opens and closes only with the ☰ button (or `M`) and remembers its state between pages.

## v0.1 — Platform skeleton (2026-10-09)

Milestone **M0**.

- Python build script (Markdown → static HTML) with an internal link check.
- Design: sage palette, light/dark mode, curriculum menu, offline search, progress tracking, copy buttons.
- All 10 phase pages and 93 module pages, generated from `curriculum.yml`.
- 2 pilot lessons: SQL SELECT/WHERE and ORDER BY/GROUP BY/HAVING, plus practice data.
- README, CONTRIBUTING, ROADMAP, CI build check, weekly link check and issue templates.
