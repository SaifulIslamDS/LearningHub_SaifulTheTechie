---
title: "Phase 2 Project: Business Analytics Study"
summary: "Run a complete, reproducible analytics study on a year of sales: clean the data, explore it, quantify uncertainty, analyse an A/B test, build a simple honest model, and turn it all into recommendations a manager can act on."
level: Intermediate
time: "20–30 hours (estimate)"
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025_raw.csv, phase-2/orders_2025.csv, phase-2/customers_2025.csv, phase-2/products_2025.csv, phase-2/ab_test_checkout.csv, templates/analysis_report_template.md, templates/experiment_plan_template.md]
---

## The brief

The managing director of the textile supplies wholesaler (the same company as Phase 1, now with a full year of data) writes:

> *"2025 is closed. I want to know what really drove our sales, where we're losing money to cancellations and late deliveries, whether the new one-page checkout should stay, and what we should change next year. Give me evidence, not opinions."*

Deliver a **business analytics study**: a reproducible Python project and a short report. It's your Phase 2 milestone and a strong data science portfolio piece.

## What you'll prove

| Skill (Phase 2 module) | Evidence in your project |
|---|---|
| NumPy & pandas | A cleaning script from `orders_2025_raw.csv` that reproduces `orders_2025.csv` exactly |
| Polars & DuckDB | One summary query written in DuckDB SQL (or Polars), matching the pandas result |
| EDA | 4–6 analytical questions, each answered with a number and at most one chart |
| Statistics | Key KPIs reported with 95% confidence intervals |
| A/B testing | A full experiment readout for the checkout test, plus one designed (future) experiment |
| Visualization | One before/after chart redesign and a consistent chart style |
| ML foundations | A leakage-free cancellation-risk model, evaluated against a baseline with a time-based split |
| Research thinking | A reproducible project (lock file, seeds, data hashes) and a report with limitations |

## Data

All files are synthetic but realistic (fixed seed, so your numbers can be checked):

| File | Rows | What it is |
|---|---|---|
| `orders_2025_raw.csv` | 4,264 | The messy ERP export (duplicates, typos, mixed formats) |
| `orders_2025.csv` | 4,246 | The clean reference: use it to check your cleaning |
| `customers_2025.csv` | 63 | Segment, region, sign-up date, credit terms |
| `products_2025.csv` | 12 | List price and unit cost |
| `ab_test_checkout.csv` | 10,836 | Portal sessions, 1–28 November, checkout A vs B |

**Option B (stronger portfolio):** apply the same study to a public dataset or anonymised data from your work, keeping the same structure of questions.

## Requirements

### 1. Reproducible project
- [ ] A repository with `pyproject.toml` + `uv.lock`, `data/`, `src/` or numbered scripts, `results/`, `reports/`, `README.md`.
- [ ] One command (or a short documented sequence) runs everything from the raw file to the report numbers.
- [ ] Fixed seeds; a `results/*.json` file with the data SHA-256 hashes and package versions.

### 2. Data preparation
- [ ] Clean `orders_2025_raw.csv`: types, text tidy-up, duplicates, price typos, negative quantities; every rule documented with counts.
- [ ] A check that your result equals `orders_2025.csv` (same rows and values).

### 3. EDA & statistics
- [ ] 4–6 analytical questions written **before** the analysis.
- [ ] Distributions (with skew handled), patterns over time (weekly and monthly), relationships (with confounders discussed) and anomalies (classified).
- [ ] Median order value, cancellation rate and late-delivery rate, overall and by segment, each with a 95% CI.

### 4. Experimentation
- [ ] Checkout A/B readout: health check (SRM), conversion test with CI, guardrails, segments, decision.
- [ ] One experiment plan (template) for a 2026 change, including a power analysis and the unit of randomisation.

### 5. Model
- [ ] Cancellation-risk model with order-time features only, a written feature audit, a pipeline, a time-based split, a baseline, ROC AUC with a bootstrap CI, and a business threshold.

### 6. Communication
- [ ] `reports/ANALYSIS_REPORT.md` (template): bottom line first, results table with CIs, 4–6 charts with action titles, limitations, recommendations with owners.
- [ ] One before/after chart redesign.

## Known answers (practice data)

Your project must reproduce these. If one doesn't match, find out why before you continue.

| Check | Expected |
|---|---|
| Clean orders | 4,246 (from 4,264 raw lines: 18 duplicates removed) |
| Status counts | Delivered 3,872 · Cancelled 283 · Shipped 46 · Pending 45 |
| Net revenue (excluding Cancelled) | 5,478,357.79 |
| Median order value (excl. Cancelled), 95% bootstrap CI | 1,060 (about 1,023–1,099) |
| Late deliveries (delivery days > promised) | 919 of 3,872 = 23.7% (95% CI 22.4–25.1%) |
| Cancellation rate by credit terms | 0 days 3.3% · 15 days 4.3% · 30 days 8.1% · 60 days 13.9% |
| A/B conversion A vs B | 6.70% vs 7.91%; +1.21 pts (95% CI 0.23–2.19); p = 0.016 |
| A/B revenue per session | 50.53 vs 56.27 (+11.4%), p = 0.20 (not significant) |
| Cancellation model, time split (segment, channel, credit days) | ROC AUC 0.639 (bootstrap 95% CI about 0.57–0.70) |

*(Rates by credit terms use all 4,246 orders; the model and research lessons drop the 45 pending orders, giving 3.3 / 4.4 / 8.2 / 14.1%.)*

## Suggested repository structure

```text
phase2-business-analytics/
├── README.md                 ← question, findings, how to reproduce, screenshots
├── pyproject.toml / uv.lock
├── data/                     ← raw + reference files (or a download script)
├── src/                      ← 01_clean.py, 02_eda.py, 03_stats.py, 04_ab_test.py, 05_model.py
├── results/                  ← JSON/CSV outputs with data hashes and versions
├── charts/                   ← PNGs used in the report
└── reports/
    ├── ANALYSIS_REPORT.md
    ├── EXPERIMENT_PLAN_2026.md
    └── FEATURE_AUDIT.md
```

## Self-assessment rubric

| Area | Meets the bar | Excellent |
|---|---|---|
| Reproducibility | Runs from raw data with documented steps | One command, lock file, seeds, hashes; reviewer gets identical numbers |
| Data preparation | Matches the reference file | Every rule documented with counts; checks automated (pytest) |
| EDA & statistics | Correct numbers and charts | Questions first; CIs everywhere; confounders and anomalies discussed |
| Experimentation | Correct test and decision | SRM, guardrails, segments as hypotheses; a sized, realistic 2026 plan |
| Model | Leakage-free, beats baseline | Feature audit, time split, CI, threshold tied to business capacity |
| Communication | Report with findings | Bottom line first; action titles; limitations; clear owners and next steps |

**Done when:** every requirement is checked, the known answers match, and a reviewer can clone your repository, run it, and reach the same conclusions without asking you anything.

!!! tip "Interview story"
    "I ran a full analytics study on a year of sales: a reproducible cleaning pipeline, EDA with confidence intervals, an A/B test readout that recommended keeping the new checkout (+1.2 points conversion, CI 0.2–2.2) while flagging that revenue per session wasn't yet significant, and a leakage-free cancellation-risk model with an honest ROC AUC of 0.64. I also showed that a proposed credit-terms experiment wasn't feasible with only seven customers, and designed a per-order alternative instead."
