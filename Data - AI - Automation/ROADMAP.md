# Development Roadmap

How this site grows from a skeleton to a complete, job-ready tutorial site.

- **Scope:** 10 phases · 93 modules · 371 planned topics (from `curriculum.yml`).
- **Estimated size:** about 250–300 lessons, because one lesson often covers 1–2 topics.
- **Rule:** finish one module completely before starting the next. A half-written module is less useful than a finished small one.

Status key: ✅ done · 🔄 in progress · ⏳ planned

**Current version: v0.7** · Next: **M7 → v0.8**

**Release rule:**

- Every release is packaged as `data-ai-automation-path-vX.Y.zip`.
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
| M7 | Phase 3: Data Engineering | v0.8 | 13 modules, split into 3A (SQL/DB/warehouse) and 3B (pipelines/cloud/AI-ready data) | 🔄 next |
| M8 | Phase 5: LLM & RAG | v0.9 | NLP → RAG evaluation, Phase 5 project | ⏳ |
| M9 | Phase 6: Agents & Automation | v1.0 | Agents, n8n, MCP, frameworks, Phase 6 project | ⏳ |
| M10 | Phase 4: ML Engineering | v1.1 | Regression → MLOps | ⏳ |
| M11 | Phase 7: LLMOps & Governance | v1.2 | Deployment → AI governance | ⏳ |
| M12 | Phases 8–9: Capstone + Career | v1.3 | Capstone build guide, portfolio, interviews, freelancing | ⏳ |
| M13 | Platform upgrade 2 | v2.0 | Runnable SQL in the browser, installable offline app (PWA), optional Bangla | ⏳ |

**Why this order:**

- **Phase 1 first:** it is the strongest existing skill base, the fastest to verify, and the most common entry-level job target.
- **Phase 0 next:** every later phase depends on it.
- **Phases 5–6 before Phase 4:** LLM, RAG and agent skills currently carry the highest market demand. They also need only basic ML concepts, which Phase 2 already covers.

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

## M7–M12: Remaining phases

For each module: write a lesson for every planned topic, run every example and paste the real result, add 3–4 checked free resources, add a `_module.md` intro, and list the module's practice files in `content/downloads/files.yml`. Follow the same pattern as M2–M4. Each phase also gets a milestone project page in `content/projects/<phase-id>.md`. For fast-changing tools (LangGraph, agent SDKs, MCP, Fabric, Langfuse):

- [ ] Check the official docs on the day you write the lesson.
- [ ] Put the tool version in the lesson.
- [ ] Re-review after 6 months, using the `reviewed:` date in each lesson.

## M13: Platform upgrade 2 (v2.0)

- [ ] **Runnable SQL** in the browser (sql.js), so learners can try queries without installing anything.
- [ ] **Installable offline app (PWA).**
- [ ] **Bangla** or bilingual lessons, if there is learner demand.
- [ ] Privacy-friendly visitor statistics, if needed.

---

## Definition of done: one lesson

- [ ] Follows the lesson template, including the exercise, 3 quiz questions and the job-ready check.
- [ ] Every code example was run, and every shown result matches the actual output.
- [ ] Facts were checked against official docs, and the `reviewed:` date is set.
- [ ] Free resources were opened and work.
- [ ] `python build.py` passes with no warnings and no broken links.
- [ ] Read once on a phone in both light and dark mode.

## Working rhythm (suggested)

- **Effort estimate:** about 2–3 hours per lesson, including testing examples and checking links. Your pace will set the real number.
- **Release:** after each module, tag a version (`git tag v0.3.1`) and push. GitHub Pages updates on its own.
- **Track:** use GitHub Issues with one issue per module, labelled by phase.
