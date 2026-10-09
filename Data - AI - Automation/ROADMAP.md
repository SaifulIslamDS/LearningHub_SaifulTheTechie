# Development Roadmap

How this site grows from a skeleton to a complete, job-ready tutorial site.

- **Scope:** 10 phases · 93 modules · 371 planned topics (from `curriculum.yml`).
- **Estimated size:** about 250–300 lessons, because one lesson often covers 1–2 topics.
- **Rule:** finish one module completely before starting the next. A half-written module is less useful than a finished small one.

Status key: ✅ done · 🔄 in progress · ⏳ planned

**Current release: v0.9.1** · M8 remains in progress · **Next approved module: AI-Ready Data**

**Release rule:**

- Every release is packaged as `data-ai-automation-path-vX.Y[.Z].zip`. Patch releases may ship platform/content corrections inside an in-progress milestone.
- The version shows under the site name in the top bar (set in `site.yml`).
- When a version is complete, its milestone is marked ✅ here and listed in `CHANGELOG.md`.

---

## Milestone overview

| # | Milestone | Release | Delivers | Status |
|---|---|---|---|---|
| M0 | Platform skeleton | v0.1 | Site engine, design, all phase/module pages, 2 pilot lessons | ✅ |
| M1 | Go live | v0.2 | Go-live package: name, licences, version display, 404 page, publish guide, template v1 | ✅ |
| M2 | Phase 1A: SQL + Excel | v0.3 | Analytical SQL, Excel, Pivot modules complete (13 lessons) | ✅ |
| M3 | Phase 1B: Power BI stack | v0.4 | Power Query, DAX, Power BI, semantic models, AI-assisted analytics, storytelling, Phase 1 milestone project (14 lessons) | ✅ |
| M4 | Phase 0: Foundations | v0.5 | Dev environment, Git, Linux, Python refresher, testing, AI-assisted dev (16 lessons), Gate project, practice-file library | ✅ |
| M5 | Platform upgrade 1 | v0.6 | Glossary (139 terms), scored quizzes, sitemap/robots, Open Graph share cards, link-check issues | ✅ |
| M6 | Phase 2: Data Science | v0.7 | NumPy → research thinking (21 lessons), Phase 2 project, 2025 practice data | ✅ |
| M7 | Phase 3A: Data Engineering — storing & serving | v0.8 | Ingestion, advanced SQL, database engineering, warehousing, lakehouse, Docker (13 lessons) | ✅ |
| M8 | Phase 3B: Data Engineering — moving & trusting | v0.9.x | ETL/ELT, data quality, orchestration, dbt, cloud & IaC, AI-ready data, Spark & Kafka, Phase 3 project | 🔄 in progress |
| M9 | Phase 5: LLM & RAG | v1.0 | NLP → RAG evaluation, Phase 5 project | ⏳ |
| M10 | Phase 6: Agents & Automation | v1.1 | Agents, n8n, MCP, frameworks, Phase 6 project | ⏳ |
| M11 | Phase 4: ML Engineering | v1.2 | Regression → MLOps | ⏳ |
| M12 | Phase 7: LLMOps & Governance | v1.3 | Deployment → AI governance | ⏳ |
| M13 | Phases 8–9: Capstone + Career | v1.4 | Capstone build guide, portfolio, interviews, freelancing | ⏳ |
| M14 | Platform upgrade 2 | v2.0 | Runnable SQL in the browser, installable offline app (PWA), optional Bangla | ⏳ |

**Why this order:**

- **Phase 1 first:** it is the strongest existing skill base, the fastest to verify, and the most common entry-level job target.
- **Phase 0 next:** every later phase depends on it.
- **Phases 5–6 before Phase 4:** LLM, RAG and agent skills currently carry the highest market demand. They also need only basic ML concepts, which Phase 2 already covers.

## Progress by phase (M8 working checkpoint)

| Phase | Topics written | Lessons | Project page | Milestone |
|---|---|---|---|---|
| 0 Engineering Foundations | 26 / 26 | 16 | ✅ | M4 ✅ |
| 1 Analytics & BI | 43 / 43 | 27 | ✅ | M2–M3 ✅ |
| 2 Python, Statistics & Data Science | 41 / 41 | 21 | ✅ | M6 ✅ |
| 3 Data Engineering | 40 / 55 | 21 | ⏳ (in M8) | M7 ✅ · M8 🔄 |
| 4 ML & Deep Learning | 0 / 34 | — | ⏳ | M11 |
| 5 NLP, LLM & RAG | 0 / 38 | — | ⏳ | M9 |
| 6 Agents & Automation | 0 / 47 | — | ⏳ | M10 |
| 7 LLMOps & Governance | 0 / 30 | — | ⏳ | M12 |
| 8 Integrated Capstone | 0 / 27 | — | ⏳ | M13 |
| 9 Career & Commercialisation | 0 / 30 | — | ⏳ | M13 |
| **Total** | **150 / 371 (40%)** | **85** | 3 of 10 | |

Remaining: 221 topics, roughly 120–125 more lessons (estimate).

## Open items (outside the milestones)

- [ ] **Go live (owner step):** create the GitHub repository, push, turn on Pages (`main` / `docs`), then set `site_url` and `github_repo` in `site.yml` and rebuild. This switches on the sitemap, canonical links and "Suggest an edit" links.
- [ ] Submit `sitemap.xml` in Google Search Console, and run the link-check workflow once.
- [ ] A learner test of one full project (Phase 2 or Phase 3) before v1.0.
- [ ] Work can continue in another AI assistant: give it `handover/HANDOVER.md` and the prompt in `handover/CHATGPT-PROMPT.md` together with the latest release zip.

---

## M0: Platform skeleton (v0.1) ✅

- Python build script: Markdown → static HTML, with an internal link check.
- Design: sage palette, light/dark mode, toggleable curriculum menu, search, progress tracking, copy buttons.
- All 10 phase pages and 93 module pages, generated from `curriculum.yml`.
- 2 pilot lessons: SQL SELECT/WHERE and ORDER BY/GROUP BY/HAVING.
- Lesson template, practice data (`orders.sql`, `orders.csv`), README and CI check.

## M1: Go live (v0.2) ✅

- [x] Site name confirmed: **Data, AI & Automation Path**.
- [x] Licences: **MIT** for the code (`LICENSE`) + **CC BY-NC-SA 4.0** for the lesson content (`LICENSE-CONTENT.md`), plus a licence page on the site.
- [x] Version display under the site name; versioned release package.
- [x] GitHub Pages ready: `docs/` folder, `.nojekyll`, `404.html`.
- [x] Publish guide in README (GitHub Desktop and command line) with a live-site checklist.
- [x] Lesson template locked as **Template v1**.
- [ ] **Owner step:** create the repository, push, turn on Pages, set `site_url` + `github_repo` (README → *Go live on GitHub*).
- **Done when:** the package is complete *(done)*, and the live URL opens after the owner step.

## M2: Phase 1A — SQL, Excel & Pivot (v0.3) ✅

- [x] Analytical SQL: 5 lessons. SELECT/WHERE, ORDER BY/GROUP BY/HAVING, CASE, JOINs, subqueries.
- [x] Excel for Analysis: 5 lessons. IF & logical, SUMIFS/COUNTIFS, XLOOKUP & INDEX/MATCH, FILTER & LET, conditional formatting.
- [x] Pivot Analysis: 3 lessons. PivotTables & grouping, slicers & timelines, What-If & Goal Seek.
- [x] Practice data extended: `customers` table and `orders.xlsx` workbook.
- [x] Every example verified: SQLite, LibreOffice recalculation, pandas cross-checks.
- [x] 17 of 371 planned topics written (Phase 1: 17 of 43).

## M3: Phase 1B — Power BI stack (v0.4) ✅

- [x] Power Query: 3 lessons. Cleaning; merge & append; reshape (unpivot) & folder workflows.
- [x] Power Pivot & DAX: 3 lessons. Relationships (star schema, date table); measures & KPI logic; CALCULATE & filter context.
- [x] Power BI: 4 lessons. Model hygiene & KPI page; drill-through & bookmarks; row-level security; publishing, licences & Copilot.
- [x] Semantic Models, AI-Assisted Analytics: 1 lesson each. Data Storytelling: 2 lessons.
- [x] Phase 1 milestone project page (Executive BI System) with requirements, known answers and a rubric. The build now supports a project page for every phase.
- [x] New practice data: `orders_raw.csv` (messy), monthly files, `targets_wide.csv`, `sales_model.xlsx` (5 Excel Tables).
- [x] **Phase 1 complete: 43 of 43 topics.** Overall: 43 of 371.

## M4: Phase 0 — Engineering Foundations (v0.5) ✅

- [x] Development Environment: 3 lessons. VS Code & Python; uv, virtual environments & packages; debugging.
- [x] Git & GitHub: 3 lessons. Repositories & commits; branches & merge (with a real conflict); pull requests, README & project structure.
- [x] Linux Essentials: 2 lessons. Filesystem & terminal workflow (WSL); grep, sort & pipes, shell scripts and cron.
- [x] Programming Refresher: 4 lessons. Basics; collections; files & exceptions; OOP & type hints.
- [x] Testing & CI: 2 lessons. pytest & ruff; GitHub Actions with uv.
- [x] AI-Assisted Development: 2 lessons. Coding agents, prompting & AGENTS.md; reviewing & testing AI-written code.
- [x] Phase 0 Gate project page (CSV Data Cleaning CLI) with a starter (17 tests to make pass) and a reference solution (CI workflow, AGENTS.md).
- [x] Practice-file library: a catalogue (`content/downloads/files.yml`), a "Practice files" page, a files box on every lesson, and a one-click bundle (`practice-files.zip`). Answer keys for SQL and Excel added.
- [x] Every command and script output pasted from a real run (Python 3.14, uv, Git, bash, pytest 9, ruff 0.16, mypy).
- [x] **Phase 0 complete: 26 of 26 topics.** Overall: 69 of 371.

## M5: Platform upgrade 1 (v0.6) ✅

- [x] **Glossary page**: 139 terms in 11 categories (`content/glossary.yml`), A–Z navigation, live filter and category filter. Each term links to the lesson (or future module) where it is taught.
- [x] **Linked from lessons**: every lesson shows its **Key terms** (matched from its keywords), and each glossary entry lists the lessons that use it. Terms are also in search.
- [x] **Quiz scoring**: click an answer to check it; score out of 3, best score saved per lesson and shown on module pages; "Try again". All 129 quiz questions are read and checked by the build.
- [x] **Milestone project pages**: brief, requirements, grading checklist and an example README (done early, in v0.4–v0.5).
- [x] **SEO and sharing**: Open Graph and Twitter card tags on every page, a 1200×630 share image, canonical links, `sitemap.xml` and `robots.txt` (absolute URLs switch on when `site_url` is set).
- [x] **Weekly external link check**: now reports broken links in a GitHub issue (`broken-links`) instead of only failing. 109 unique external links are checked.

## M6: Phase 2 — Python, Statistics & Data Science (v0.7) ✅

- [x] NumPy (2), pandas (4), Polars & DuckDB (2), EDA (2), Statistics (2), A/B testing (2), Visualization (2), ML foundations (3), Research thinking (2): **21 lessons**.
- [x] New practice data for 2025 (synthetic, fixed seed, `tools/make_phase2_data.py`): 4,246 orders, a messy raw export, 63 customers, 12 products and a 10,836-session A/B test, with planted patterns (seasonality, Eid holidays, a Friday weekend, delivery times by region, cancellation drivers, a confounder).
- [x] One script per lesson (`examples/phase-2/`, zipped as `data-science-scripts.zip`), 18 charts, and two new templates (experiment plan, analysis report).
- [x] Phase 2 milestone project page (Business Analytics Study) with known answers and a rubric.
- [x] Glossary grows to 168 terms (statistics, experiments, ML and data tools).
- [x] Every output pasted from a real run (numpy 2.5, pandas 3.0, scipy 1.18, statsmodels 0.15, scikit-learn 1.9, polars 2.0, duckdb 1.5, matplotlib 3.11, seaborn 0.13, plotly 7.1).
- [x] **Phase 2 complete: 41 of 41 topics.** Overall: 110 of 371.

## M7: Phase 3A — Data Engineering: storing & serving data (v0.8) ✅

Phase 3 (13 modules, 55 topics) is split into two releases. 3A covers 6 modules and 25 topics.

- [x] Data ingestion (2): REST APIs with tokens, pagination, retries and incremental loads; responsible scraping; CSV vs JSON vs Parquet.
- [x] Advanced SQL (2): CTEs and recursive CTEs (date spines, hierarchies); window functions (running totals, RANK, LAG/LEAD, top-N per group).
- [x] Database engineering (3): PostgreSQL loading with COPY and normalisation with constraints; indexing and EXPLAIN ANALYZE on 2 million rows; transactions, ACID and lost updates.
- [x] Data warehousing (2): OLTP vs OLAP and a star schema; SCD type 2 (idempotent loads, as-was vs as-is) and BigQuery (dialects, bytes scanned, partitioning).
- [x] Lakehouse (2): Delta Lake medallion layers (bronze/silver/gold, MERGE, time travel); Apache Iceberg and the Fabric / Databricks / Snowflake comparison.
- [x] Docker (2): images and containers; Docker Compose and reproducible environments.
- [x] A local **practice API and website** (`mock_api.py`) with tokens, pagination and rate limits, so learners can practise real HTTP offline.
- [x] Every output from a real run: PostgreSQL 16.15, Docker Engine 29.8 / Compose 5.5, deltalake 1.6, PyIceberg 0.12, sqlglot 30, DuckDB 1.5. BigQuery-only commands are shown for reference and marked as not executed.
- [x] Glossary: 182 terms (14 new). Phase 3A: 25 of 25 topics. Overall: 135 of 371.

## M8: Phase 3B — Data Engineering: moving & trusting data (v0.9.x release family) 🔄 in progress

Finishes Phase 3: 7 modules, 30 topics, about **18 lessons**, plus the **Phase 3 milestone project page**.

**Current release checkpoint (v0.9.1):** ETL/ELT ✅ · Data Quality ✅ · dbt ✅. Phase 3 is **40/55 topics** with **21 lessons**. v0.9.1 also fixes learner-facing generated pages, adds roadmap projections instead of a generic future-status label, adds a professional AI Mentor Prompt to every written tutorial, and adds reviewed YouTube companions to every M8 tutorial completed so far (ETL/ELT, Data Quality and dbt). **Next approved module: AI-Ready Data.**

**Planned lessons** (topics in brackets must match `curriculum.yml` exactly):

| Module | Lesson | Topics covered |
|---|---|---|
| etl-elt | 01 Modular, idempotent pipelines with incremental loads | Modular pipelines · Idempotency · Incremental loads |
| etl-elt | 02 Replayable pipelines and change data capture | Replayability · CDC |
| data-quality | 01 Validation rules and pytest for data | Validation · pytest for data |
| data-quality | 02 Great Expectations | Great Expectations |
| data-quality | 03 Data contracts, freshness and alerting | Data contracts · Freshness & alerting |
| orchestration | 01 Airflow DAGs for the orders pipeline | Airflow DAGs |
| orchestration | 02 Retries, backfills, Dagster and Prefect | Retries & backfills · Dagster & Prefect alternatives |
| dbt | 01 dbt models and tests | Models · Tests |
| dbt | 02 Snapshots and macros | Snapshots · Macros |
| dbt | 03 Documentation and marts | Documentation & marts |
| cloud-iac | 01 IAM and object storage (S3/GCS) | IAM · S3/GCS |
| cloud-iac | 02 BigQuery in practice | BigQuery |
| cloud-iac | 03 Terraform basics and cost control | Terraform basics · Cost control |
| ai-ready-data | 01 Document pipelines: parsing and chunking | Unstructured document pipelines · Parsing & chunking |
| ai-ready-data | 02 Embedding refresh, metadata and lineage for RAG | Embedding refresh · Metadata & lineage for RAG |
| big-data-streaming | 01 PySpark basics on the orders data | PySpark |
| big-data-streaming | 02 Partitions, shuffle and caching | Partitions, shuffle & caching |
| big-data-streaming | 03 Kafka producers and consumers | Kafka producers/consumers |

**Build on what exists:**

- Reuse the 2025 data, the practice API (`mock_api.py`), the PostgreSQL `shop` schema and the Delta/Iceberg tables from Phase 3A.
- New scripts go in `examples/phase-3/` (numbered 14 onwards), and are added to `phase-3/data-engineering-scripts.zip`.
- Point the glossary entries for ETL/ELT, CDC, idempotency, data contract, Airflow/DAG, dbt, Terraform, IAM, chunking, Spark and Kafka to the new lessons; add any missing terms.

**Verification plan (decide per tool, and say so in the lesson):**

| Tool | Preferred way to verify | If it can't run in the build environment |
|---|---|---|
| dbt | `dbt-duckdb` or `dbt-postgres`, real `dbt build` output | Run on the learner's machine; mark output "not executed" |
| Great Expectations | Real run on the 2025 data | Fall back to pandera/pytest, and say why |
| Airflow | `airflow dags test` with a local install | Show the DAG; test the task functions with pytest |
| Terraform | `terraform validate` / `plan` with a local provider | Show code; mark "not executed" |
| Cloud (S3/GCS, IAM, BigQuery) | Free tiers / sandbox, or a local mock (e.g. moto for S3) | Mark commands "not executed" |
| Spark / Kafka | Local PySpark; Kafka via Docker Compose | Mark broker output "not executed" |

**Phase 3 project page:** *Production Analytics Platform*: API ingestion → PostgreSQL/lakehouse → dbt marts with tests → orchestrated daily run → BI-ready gold tables → a document pipeline feeding a vector store. Known answers come from the Phase 3A numbers (4,246 orders; 5,478,357.79 net revenue).

**Done when:** Phase 3 shows 55 of 55 topics; the project page is live; the build has no warnings; every output is either real or clearly marked "not executed".

## M9: Phase 5 — NLP, LLM & RAG Engineering (v1.0) ⏳

- 10 modules, 38 topics, about **22 lessons**: NLP foundations, transformers, LLM application engineering, prompt and context engineering, open and small models (Ollama), fine-tuning basics, frameworks (LangChain, LlamaIndex), vector databases (FAISS, Chroma, Qdrant, pgvector), advanced RAG, RAG evaluation.
- **Project:** Enterprise Knowledge Assistant: hybrid retrieval, citations, fallback handling, an eval dataset and traces.
- **Practice data:** a small document set about the textile wholesaler (policies, product sheets, FAQs) with a golden Q&A set, so retrieval scores can be checked.
- **Verification:** prefer local models and local embeddings so outputs are reproducible. Hosted API calls are shown with the exact model name and date, and with the note that answers vary between runs.
- **Why v1.0:** with Phases 0–3 and 5 done, the site covers the full Data → AI Engineer path for the first time.

## M10: Phase 6 — AI Agents & Intelligent Automation (v1.1) ⏳

- 13 modules, 47 topics, about **27 lessons**: agent architecture, workflow vs agent, APIs and webhooks, n8n, Make/Zapier, code-first frameworks (LangGraph, OpenAI Agents SDK, Claude Agent SDK), MCP and A2A, human-in-the-loop, agent memory, Langflow, multi-agent systems, voice AI, browser agents.
- **Project:** AI Operations Agent that retrieves information, performs approved actions, escalates to humans and logs every step.
- **Note:** these tools change monthly. Check the official docs on the day of writing, record the version, and set `reviewed:`.

## M11: Phase 4 — ML & Deep Learning Engineering (v1.2) ⏳

- 8 modules, 34 topics, about **20 lessons**: regression, classification (incl. gradient boosting), unsupervised ML, forecasting, neural networks (PyTorch), computer vision, applied CV (YOLO, ONNX), MLOps (FastAPI, Docker, MLflow, drift).
- **Project:** Production ML API with `/predict`, `/health` and `/info`, containerised, versioned in MLflow and monitored.
- **Reuse:** the Phase 2 cancellation model and sales data for forecasting and the ML API.

## M12: Phase 7 — Production AI, LLMOps & Governance (v1.3) ⏳

- 8 modules, 30 topics, about **17 lessons**: deployment, reliability, security (OWASP LLM Top 10, prompt injection), LLM observability (Langfuse/LangSmith, OpenTelemetry), evaluation, model routing, AI FinOps, AI governance (EU AI Act, NIST AI RMF).
- **Project:** deploy one AI system publicly with traces, an eval suite, health checks, a cost dashboard and security controls.
- **Note:** for regulation, cite the official text and give the date checked; no legal advice.

## M13: Phases 8–9 — Capstone, Career & Commercialisation (v1.4) ⏳

- **Phase 8** (8 layers, 27 topics, about **10 guide pages**): a build guide for the Intelligent Business Operations Platform that ties every earlier project together, layer by layer.
- **Phase 9** (9 modules, 30 topics, about **15 lessons**): GitHub portfolio, LinkedIn, CV and job search, interview prep, certifications, freelancing, case studies, productisation, Ilmento Digital.
- **After M13:** all 371 topics are written; the site is "complete v1".

## Rules for every remaining milestone

The curriculum remains authoritative for **topic coverage**, but it does not dictate a one-topic/one-page tutorial structure. Split or combine topics when that produces a clearer learning sequence. For each module: cover every approved curriculum topic exactly, add a `_module.md` introduction, teach with the deep-tutorial standard, verify every executable result honestly, synchronize practice files with the written lesson, and list downloadable assets in `content/downloads/files.yml`. Every written tutorial automatically receives the professional **AI Mentor Prompt**. Add one carefully reviewed YouTube companion only when a strong video genuinely reinforces that tutorial; never insert an unreviewed placeholder merely to fill the frame. Resources are curated for usefulness rather than forced to a fixed count. Each phase also gets a milestone project page in `content/projects/<phase-id>.md` when that project is due in the roadmap.

For fast-changing tools (LangGraph, agent SDKs, MCP, Fabric, Langfuse, dbt, orchestration/cloud services):

- [ ] Check current official documentation on the day the tutorial is written or materially revised.
- [ ] Record the relevant tool/version context where it affects syntax or behaviour.
- [ ] Re-review time-sensitive material using the lesson `reviewed:` date.
- [ ] Label execution evidence honestly as RUN-HERE, RUN-BY-OWNER or REFERENCE-ONLY where useful.

## M14: Platform upgrade 2 (v2.0)

- [ ] **Runnable SQL** in the browser (sql.js), so learners can try queries without installing anything.
- [ ] **Installable offline app (PWA).**
- [ ] **Bangla** or bilingual lessons, if there is learner demand.
- [ ] Privacy-friendly visitor statistics, if needed.

---

## Definition of done: one tutorial

- [ ] Covers its declared `curriculum.yml` topic strings exactly and fits a logical learning sequence.
- [ ] Uses the deep-tutorial structure where appropriate: mental model → explanation → code/data/config → real output → explanation → guided build → completed implementation → practice/resources → next tutorial.
- [ ] Every shown executable result is real. If the current environment cannot run a tool, the tutorial gives exact owner-side verification steps and does not invent output.
- [ ] Practice files, when referenced, exist and stay synchronized with the tutorial.
- [ ] The generated page includes the professional **AI Mentor Prompt** and its copy control.
- [ ] A YouTube companion is included only when a relevant video has been reviewed; the written tutorial remains complete without it.
- [ ] Time-sensitive facts were checked against official documentation and the `reviewed:` date is current.
- [ ] Curated resources were checked and explain why they are useful.
- [ ] Quiz, common-mistakes, summary and job-ready sections are optional rather than compulsory.
- [ ] The full source-driven build passes with no warnings and no broken internal links before a release is declared ready.
- [ ] The generated tutorial is readable at mobile width and in both light and dark appearance.

## Working rhythm (suggested)

- **Effort estimate:** about 2–3 hours per lesson, including testing examples and checking links. Your pace will set the real number.
- **Release:** after each module, tag a version (`git tag v0.3.1`) and push. GitHub Pages updates on its own.
- **Track:** use GitHub Issues with one issue per module, labelled by phase.
