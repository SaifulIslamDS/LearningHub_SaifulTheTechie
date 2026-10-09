> **Continuation notice (v0.9.1):** This file originated with the v0.8 handover. For current M8 decisions, read `handover/M8-UPGRADE-CONTINUATION.md` and `handover/v0.9.1-CODEBASE-AUDIT.md` first. The current release checkpoint is **v0.9.1**; ETL/ELT, Data Quality and dbt are complete; **AI-Ready Data** is next.

# Handover: "Data, AI & Automation Path" tutorial site

> **For:** ChatGPT (or any AI assistant or developer) continuing this project.
> **Current release:** v0.8 (2026-10-09) · **Next:** M8 → v0.9.x release family (Phase 3B, Data Engineering)
> **Package:** `data-ai-automation-path-v0.8.zip` (unzips to the folder `data-ai-automation-path-v0.8/`)
> **Read sections 1–6 before changing anything.** The project owner is the user you are talking to.
> **Current M8 working checkpoint (2026-10-09):** ETL/ELT ✅ · Data Quality ✅ · dbt ✅ · Phase 3 **40/55 topics** · **85 total lessons**.  
> **Next approved module:** **AI-Ready Data**.  
> **Governing upgrade:** read `handover/M8-UPGRADE-CONTINUATION.md` before adding new M8 lessons. It supersedes Template v1's compulsory section rules with the approved deep-tutorial Template v2.

---

## 1. The project in brief

- **What:** a free, offline-capable, w3schools-style **static tutorial website** for the owner's 10-phase curriculum, *Data, AI & Automation Path*. It runs from Excel, SQL and Power BI through Python, data science, data engineering, ML, LLMs/RAG, AI agents and LLMOps, then a capstone and career. The goal is beginner to job-ready.
- **How it's built:** a Python generator, `build.py`, turns Markdown and YAML into static HTML in `docs/`.
  - Offline use: open `index.html`.
  - Hosting: ready for **GitHub Pages** (branch `main`, folder `/docs`).
- **Who:** the owner runs "Applied AI, Data & Automation Lab" and the educational brand "Saiful The Techie", and works in Bangladesh. Examples use a Bangladeshi textile wholesaler (BDT amounts, regions such as Dhaka, Chattogram and Gazipur).
- **Status:**
  - 85 lessons covering 150 of 371 curriculum topics (40%).
  - Phases 0, 1 and 2 are complete; Phase 3 is 40 of 55. M8 has completed ETL/ELT, Data Quality and dbt.
  - 199 glossary terms. The generated page count increases after rebuilding the M8 source checkpoint.
- **Still the owner's step:** create the GitHub repo, push, enable Pages, then set `site_url` and `github_repo` in `site.yml`.

---

## 2. Owner preferences and standing rules (must follow)

**Release rules (non-negotiable):**

1. Every release is a **zipped folder named with the version**: `data-ai-automation-path-vX.Y[.Z].zip`, containing the folder `data-ai-automation-path-vX.Y[.Z]/`.
2. The version shows **under "Data, AI & Automation Path" in the top bar**. Set it with `version:` in `site.yml`.
3. When a version is complete:
   - Update `ROADMAP.md`: mark the milestone ✅ and the next one 🔄, and update "Current version … Next" and the progress table.
   - Add a `CHANGELOG.md` entry.

**How the owner wants answers:**

- Bullet points; simple, concise, coherent language.
- Think in what / why / how / when / so what.
- Add a **"Sources:"** list (source names + links) after each deliverable. Check recent web sources for anything that changes, such as tool versions, prices or free tiers.
- **Always suggest one better question** the owner could ask to improve the output.

**Content quality rules:**

- **Never fabricate outputs.** Every code example is run, and its real output is pasted in.
  - If something can't be run (cloud services, BI tools, a broker), show it as reference and **say clearly that it was not executed**.
- Facts are checked against official docs, and the date is recorded in `reviewed:`.
- Free resources only; links checked.
- Original text, never copied from other tutorial sites.
- All numbers must agree with the shared datasets' **known answers** (section 8).

**UI rule:**

- The left curriculum menu opens and closes **only** with the ☰ button or the `M` key.
- It must **not** close on an outside click or a topic click.
- It stays docked on wide screens, and its state is remembered (`localStorage` key `daa-nav`).

---

## 3. Milestones

| # | Release | Content | Status |
|---|---|---|---|
| M0 | v0.1 | Engine, design, all phase/module pages, 2 pilot SQL lessons | ✅ |
| M1 | v0.2 | Go-live package: licences (MIT code, CC BY-NC-SA 4.0 content), 404, version display, publish guide, Template v1 | ✅ |
| M2 | v0.3 | Phase 1A: SQL (5), Excel (5), Pivot (3) | ✅ |
| M3 | v0.4 | Phase 1B: Power Query, DAX, Power BI, semantic models, AI-assisted analytics, storytelling, Phase 1 project. **Phase 1 complete** | ✅ |
| M4 | v0.5 | **Phase 0 complete** (16 lessons), Gate project (CSV cleaner CLI), practice-file library | ✅ |
| M5 | v0.6 | Glossary, scored quizzes, SEO/Open Graph/sitemap, link-check issues | ✅ |
| M6 | v0.7 | **Phase 2 complete** (21 lessons), Phase 2 project, 2025 synthetic data | ✅ |
| M7 | v0.8 | **Phase 3A** (13 lessons): ingestion, advanced SQL, PostgreSQL, indexing, transactions, warehousing, SCD, BigQuery, Delta/Iceberg, Docker | ✅ current |
| **M8** | **v0.9.x** | **Phase 3B** (about 18 lessons): etl-elt, data-quality, orchestration, dbt, cloud-iac, ai-ready-data, big-data-streaming + **Phase 3 project page** | 🔄 **in progress** |
| M9 | v1.0 | Phase 5: NLP, LLM & RAG | ⏳ |
| M10 | v1.1 | Phase 6: Agents & Automation | ⏳ |
| M11 | v1.2 | Phase 4: ML & Deep Learning | ⏳ |
| M12 | v1.3 | Phase 7: LLMOps & Governance | ⏳ |
| M13 | v1.4 | Phases 8–9: Capstone, Career & Commercialisation | ⏳ |
| M14 | v2.0 | Runnable SQL in the browser (sql.js), PWA, optional Bangla | ⏳ |

`ROADMAP.md` has the detailed lesson plan for M8 (lesson titles mapped to exact topics), a verification plan, and the scope of M9–M13.

---

## 4. Repository layout

```text
index.html            redirects to docs/ (offline entry point)
build.py              generator (~920 lines): Markdown + YAML -> docs/
site.yml              name, current version, tagline, author, site_url (empty), github_repo (empty), release_date
curriculum.yml        10 phases, 93 modules, 371 topics. A lesson's `topics:` must match this text EXACTLY
requirements.txt      markdown, pygments, pyyaml (all the build needs)
assets/               style.css (sage theme, light/dark), app.js (menu, theme, search, progress, quizzes, glossary filter), og-image.png
content/
  lessons/<phase-id>/<module-id>/NN-slug.md   lessons; _module.md = module intro page
  projects/<phase-id>.md                     milestone project pages (phase-0, phase-1, phase-2 exist; phase-3 is due in M8)
  pages/*.md                                 about (status paragraph), how-to-learn
  glossary.yml                               182 terms, 11 categories
  downloads/                                 practice files + files.yml catalogue (EVERY file must be listed)
    phase-0/*.zip, phase-2/*.csv + data-science-scripts.zip, phase-3/data-engineering-scripts.zip, templates/*.md
  images/phase-2/*.png                       lesson charts
  curriculum-map.html                        one-page curriculum, copied to docs/curriculum.html
  _templates/lesson-template.md              Template v2 (deep tutorial model; optional quiz/mistakes/summary blocks)
examples/             source projects that are zipped into downloads/
  csv-cleaner/, csv-cleaner-starter/, linux-practice/, python-refresher/   (Phase 0)
  phase-2/            21 lesson scripts, chart_style.py, ml_data.py, data/
  phase-3/            mock_api.py, 01–13 scripts/SQL, README.md, data/, docker/
tools/
  make_practice_files.py   Phase 1 Excel workbooks
  make_phase2_data.py      2025 synthetic data, SEED=2025, deterministic
  package_examples.py      deterministic zips of examples/ (PACKAGES list) + copies Phase 2 charts
  make_og_image.py         1200x630 share image (needs Pillow; the build does not)
docs/                 GENERATED. Never edit by hand; commit it (GitHub Pages serves it)
.github/workflows/    build-check.yml (build + "docs/ up to date"), link-check.yml (weekly lychee → "broken-links" issue)
handover/             this file + the ChatGPT prompt
README.md, ROADMAP.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE (MIT), LICENSE-CONTENT.md (CC BY-NC-SA 4.0), .gitignore
```

---

## 5. Build, verify and release

```bash
pip install -r requirements.txt
python tools/package_examples.py      # after changing anything in examples/
python build.py                       # rebuilds docs/; prints WARNING/NOTE lines; fails on broken internal links/images
```

**Release checklist:**

1. Bump `version:` and `release_date:` in `site.yml`.
2. Add the `CHANGELOG.md` entry: what's new per module, files, glossary changes, and verification (tool versions; what was **not** executed).
3. Update `ROADMAP.md` (status, current/next line, progress table, milestone section).
4. Update `README.md` version references (lines with `v0.8`: folder name, commit message, tag, checklist).
5. Update the status paragraph in `content/pages/about.md` (lesson count, glossary count, what's next).
6. Run `python build.py`. Expect **no WARNING** lines and "Internal links: all OK". A NOTE about the empty `site_url` is expected.
7. **Determinism:** build twice and compare the two `docs/` folders (`diff -rq`); they must be identical. CI fails if the committed `docs/` doesn't match.
8. Check in a browser:
   - Pages load and images show.
   - Quizzes are clickable and score correctly.
   - The console shows no JS errors.
   - There's no horizontal scroll at 390 px width.
   - Both light and dark modes work.
9. Package the release:
   - Copy the project into a folder named `data-ai-automation-path-vX.Y[.Z]/`.
   - **Exclude** `examples/phase-2/data/orders_big.*` and `units_by_year.parquet` (about 150 MB, regenerated locally), plus `__pycache__`, `.venv`, `results/` and other generated folders.
   - Zip it as `data-ai-automation-path-vX.Y[.Z].zip`.
10. Finish with a short bullet summary: what's new, honest verification notes, next step, Sources and a better question.

---

## 6. Build-system features (already implemented; don't rebuild them)

**Lesson front matter:**

```yaml
---
title: "…"
order: 1
summary: "…"
level: Beginner | Intermediate | Advanced
time: "45 min"
topics: ["Exact topic text from curriculum.yml"]
prerequisites: ["phase-3/lakehouse/01-delta-lake-medallion"]
keywords: [lowercase, terms, used for search and glossary chips]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]      # paths under content/downloads, also listed in files.yml
resources:
  - title: "…"
    url: "https://…"
    source: "Official docs name"
    note: "Why it's useful."
# optional: terms: [Star schema]   draft: true
---
```

**YAML gotchas:** quote `on`, `true`, `false`, `NULL`, values containing `|`, and `list[str]`-style values.

**Lesson structure (Template v1).** Keep this order:

1. `## What is it?`
2. `!!! job "Why it matters at work"`
3. Steps or parts with code **and real output** in ` ```text ` blocks
4. `## Common mistakes` (a table: Mistake | What happens | Fix)
5. `## Try it yourself`, with `<details markdown="1">` hint and solution blocks
6. `## Quick quiz`, with exactly 3 questions
7. `## Summary`
8. `!!! job "Job-ready check"` (interview question + strong answer + mini project)

The resources list is rendered automatically from the front matter.

**Quiz format.** The build reads the answer letter, and warns if it can't:

```markdown
<div class="quiz-q" markdown="1">
1\. Question text?

1. Option A
2. Option B
3. Option C

<details markdown="1"><summary>Show answer</summary>
**B.** Optional one-line explanation.
</details>
</div>
```

**Glossary:**

- Each entry in `content/glossary.yml` has `term`, `aka`, `cat`, `def` (1–2 plain sentences) and `see`.
- `see` can be a lesson id, `phase-x/module`, `phase-x/project` or `phase-x`.
- "Key terms" chips appear when a lesson keyword exactly matches a term or one of its aka names.
- **Avoid ambiguous aka values.** These were removed earlier because they matched the wrong lessons: CV, CI, pipeline, variance, group by, normalization, append, FILTER, commit.

**Other features:**

- **Practice files:** every file is catalogued in `content/downloads/files.yml` (group + description). Each page gets a "Practice files" box, and a deterministic `practice-files.zip` bundle is built.
- **Project pages:** `content/projects/<phase-id>.md` becomes `docs/learn/<phase>/project.html`, linked from the phase page and the sidebar.
- **SEO:** Open Graph and Twitter tags. Canonical links and `sitemap.xml` appear only when `site_url` is set; `robots.txt` is always written.
- **Also present:** search (`/` key), progress tracking (`daa-progress-v1`), quiz best scores (`daa-quiz-v1`), copy buttons, an on-this-page TOC, and light/dark mode (`daa-theme`).

---

## 7. Phase 3A as delivered (v0.8)

| Module | Lessons (in `content/lessons/phase-3/`) | Script(s) in `examples/phase-3/` |
|---|---|---|
| data-ingestion | 01-rest-apis-auth-pagination, 02-scraping-file-formats | `mock_api.py`, 01, 02 |
| advanced-sql | 01-ctes-recursive, 02-window-functions | 04, 05 (PostgreSQL) |
| database-engineering | 01-postgresql-normalization, 02-indexing-explain-analyze, 03-transactions | 03, 06, 07, 08 |
| data-warehousing | 01-oltp-olap-star-schema, 02-scd-bigquery | 09, 10, 11 |
| lakehouse | 01-delta-lake-medallion, 02-iceberg-lakehouse-platforms | 12, 13 |
| docker | 01-images-containers, 02-compose-reproducible | `docker/` (Dockerfile, Dockerfile.api, compose.yaml, ingest_job.py) |

**Practice API** (`python mock_api.py`, port 8765):

- **Auth:** a Bearer token (`ORDERS_API_TOKEN`, default `practice-token-123`).
- **Endpoints:** `/api/v1/orders` (`page`, `page_size` ≤ 1000, `since`, `next` link, `total`) and `/api/v1/customers`.
- **Rate limit:** every 5th request returns **429** with `Retry-After: 1`.
- **Scraping practice:** an HTML catalogue at `/catalog/page/1..2` and a `robots.txt`.

**PostgreSQL connection:** scripts read `DATABASE_URL`. They create the schemas `staging`, `shop`, `dw` and the SCD tables.

**Verification environment (Phase 3A):**

- PostgreSQL 16.15; the SQL is compatible with 16–18.
- Docker Engine 29.8 / Compose 5.5.
- Python 3.13 (Docker image: Python 3.14.6).
- Libraries: requests 2.34, Beautiful Soup 4.15, pandas 3.0, psycopg 3.3, DuckDB 1.5, sqlglot 30, deltalake 1.6, PyIceberg 0.12.
- Docker Hub was blocked, so the Docker outputs used a local stand-in for `python:3.14-slim`. The lesson states this.
- **Not executed:** BigQuery commands, the uv-in-Docker variant, and the `postgres:18` Compose service. All three are marked in the lessons.

---

## 8. Shared datasets and known answers (keep numbers consistent)

**Phase 0–1, "12 orders":**

- Files: `orders.csv`, `orders.sql`, `orders.xlsx`, and `known_answers.csv` (24 checks).
- Net revenue (excl. Cancelled) **9,075**; target 9,600 (94.5%); Dhaka 3,170.
- Average order value 825.
- The customer with no orders is Blue Thread Ltd.

**Phase 2–3, "2025 data":**

| File | Size |
|---|---|
| `orders_2025.csv` | 4,246 orders |
| `orders_2025_raw.csv` | 4,264 lines, messy |
| `customers_2025.csv` | 63 customers |
| `products_2025.csv` | 12 products |
| `ab_test_checkout.csv` | 10,836 sessions |

| Check | Value |
|---|---|
| Statuses | Delivered 3,872 · Cancelled 283 · Shipped 46 · Pending 45 |
| **Net revenue** | **5,478,357.79** (float) · 5,478,359.10 in PostgreSQL NUMERIC (131 half-cent rows round differently; taught on purpose) |
| Late deliveries | 919 of 3,872 (23.7%) |
| A/B conversion | A 6.70% vs B 7.91%, p = 0.0158 |
| API ingest | 9 pages, 4,246 rows; 396 orders since 2025-12-01 |
| Index demo | 2M rows: 145.6 ms → 6.7 ms |
| Star schema | fact 4,246; dims date 365, customer 63, product 12, channel 3 |
| SCD C010 | Dhaka 79 orders / 108,935; Gazipur 122 orders / 186,479 |
| Delta | silver 4,246; gold 48 rows = 5,478,357.79 |
| Iceberg | snapshots 1,653 → 4,246 rows; cancelled 116 → 283; Dhaka Q4 434 orders / 606,561.85 |
| Q4 revenue by segment (gold) | Garment Factory 1,365,651 · Knitting Mill 220,870 · Trader 110,905 · Retailer 31,627 |

The data is generated by `tools/make_phase2_data.py` with SEED 2025. **Do not change the generator**: every lesson's numbers depend on it. If Phase 3B needs new data (documents, CDC events, a second load), add a **new** generator script with a fixed seed.

---

## 9. Current task family: M8 → v0.9.x (Phase 3B)

- **Scope:** 7 modules, 30 topics, about 18 lessons + the Phase 3 project page. Lesson titles and topic mapping are in `ROADMAP.md` → "M8".
- **Order suggestion:**
  - First, tools that run fully on a laptop: etl-elt → data-quality → dbt → ai-ready-data.
  - Then orchestration → big-data-streaming → cloud-iac, which need more setup or cloud accounts.
- **Per module:**
  - A `_module.md` intro and the lessons (Template v1).
  - Scripts numbered 14+ in `examples/phase-3/`.
  - Glossary `see:` updates and new terms.
  - The `files.yml` entry and re-running `package_examples.py`.
- **Verification:** run everything you can and paste real output. For anything that can't run in your environment:
  - **(a)** give the owner a command or script to run locally and paste back; or
  - **(b)** mark it "shown for reference, not executed".
  - Never invent output.
- **Phase 3 project page:** *Production Analytics Platform* (milestone text in `curriculum.yml`), with requirements, known answers from section 8 and a grading rubric. Follow the format of `content/projects/phase-2.md`.
- **Done when:**
  - Phase 3 shows 55/55 topics, and the build has no warnings.
  - The roadmap and changelog are updated.
  - `data-ai-automation-path-v0.9.zip` is delivered.

---

## 10. Lessons learned (avoid these mistakes)

- **Inspect before you generate.** One resumed session nearly overwrote the Phase 2 data with a different generator. Read the existing `content/`, `examples/` and `tools/` first, and never regenerate shared data.
- **Ties and rounding:**
  - Add tie-breakers in rankings (`ORDER BY revenue DESC, product`).
  - Python's `round()` is banker's rounding, unlike Excel.
  - Floats vs NUMERIC differ on half-cents.
- **SQL:** don't name an alias `month` if you then `ORDER BY` it as text; use `mon`. Use `SET TimeZone = 'UTC'` for reproducible timestamps.
- **Script hygiene:**
  - Make scripts **idempotent** (re-runnable) and deterministic (fixed seeds, fixed timestamps in demo data).
  - Keep the build and zips deterministic too: no build dates in the output.
- **Docker:**
  - Python as PID 1 ignores SIGTERM, so use `STOPSIGNAL SIGINT`.
  - Port clashes with a locally running API are common.
  - Inline comments after a Dockerfile instruction break the build.
- **Charts:** check them visually, since label overlaps happened several times.
- **Glossary:** new aka names can collide with keywords in other lessons. Check the "Key terms" chips after the build.
- **Honesty is a feature:** "not executed because …" is acceptable; a fabricated output is not.
