---
title: "Phase 1 Project: Executive BI System"
summary: "Combine everything from Phase 1 into one portfolio-ready BI system: clean data, a trusted semantic model, a KPI dashboard, and an executive summary that drives a decision."
level: Beginner–Intermediate
time: "15–25 hours (estimate)"
reviewed: 2026-10-09
files: [orders_raw.csv, monthly/orders_2026-01.csv, monthly/orders_2026-02.csv, monthly/orders_2026-03.csv, customers.csv, products.csv, targets_wide.csv, sales_model.xlsx, known_answers.csv, templates/kpi_dictionary_template.md, templates/executive_summary_template.md, templates/decision_memo_template.md]
---

## The brief

You are the new BI analyst at a textile supplies wholesaler. Management says:

> *"Every month we argue about the numbers. Build us **one** trusted view of sales vs target, show us where we're behind, and tell us what to do about it."*

Build an **Executive BI System** that a manager could use on Monday morning. It also becomes your **first portfolio project**.

## What you'll prove

| Skill (Phase 1 module) | Evidence in your project |
|---|---|
| Analytical SQL | A commented `sales_pack.sql` with 5+ business queries |
| Excel for Analysis / Pivot | A workbook with a SUMIFS summary, a lookup, and one What-If model |
| Power Query | A refreshable cleaning query (raw → clean) and a folder or unpivot query |
| Power Pivot & DAX | A star-schema model with 8+ measures, including achievement %, share of total and MoM growth |
| Power BI | Overview page, drill-through, bookmarks and RLS roles |
| Semantic model | A KPI dictionary, with descriptions on every measure |
| AI-assisted analytics | A "known answers" sheet and a log of AI suggestions you checked |
| Data storytelling | A one-page executive summary and one decision memo |

## Data

**Option A (recommended for a first run):** use the practice files from this phase: `orders_raw.csv`, the monthly files, `customers.csv`, `targets_wide.csv`, or the ready-made `sales_model.xlsx`.

**Option B (stronger portfolio):** use a public dataset, or **anonymised** data from your own work. Remove names, prices and anything confidential, and get permission. Keep the same structure: orders (facts), customers, products, regions, dates and targets.

## Requirements

### 1. Data preparation (Power Query)
- [ ] Clean the raw export: blanks, spaces, capitals, locale-correct dates, number text, duplicates.
- [ ] Combine monthly files from a **folder**, and **unpivot** the targets.
- [ ] Include a **Checks** table: row counts and totals against the source.

### 2. Model (Power BI or Power Pivot)
- [ ] Star schema: Orders and Targets facts. Customers, Products, Regions and Date dimensions.
- [ ] Marked date table. One-to-many, single-direction relationships. Fact keys hidden.
- [ ] Measures (minimum): Revenue, Net Revenue, Net Orders, Avg Order Value, Target, Achievement %, Gap to Target, Delivered Revenue, Share of Total, MoM Growth %.
- [ ] Every measure formatted, in a display folder, and described.

### 3. Report (Power BI)
- [ ] **Overview page:** KPI cards, a region matrix with status colours, revenue vs target by month, and slicers that respect the target grain.
- [ ] **Drill-through:** customer details and region details.
- [ ] **Bookmarks:** "All orders" / "Open orders" buttons.
- [ ] **RLS:** one static and one dynamic role, tested with *View as*.
- [ ] Action titles on every chart.

### 4. SQL & Excel companions
- [ ] `sales_pack.sql`: revenue by region, top customers, status overview (CASE), customers without orders (JOIN), above-average customers (CTE).
- [ ] An Excel summary sheet (SUMIFS) that matches the Power BI totals.

### 5. Communication
- [ ] `KPI_DICTIONARY.md`: name, definition, DAX, owner.
- [ ] `EXECUTIVE_SUMMARY.md`: BLUF, 3 findings, a recommendation, data caveats.
- [ ] `DECISION_MEMO.md`: decision, options, recommendation, risks, next steps.

## Known answers (practice data)

If you use Option A, your system must reproduce these numbers. If it doesn't, find out why before you continue.

| Check | Expected |
|---|---|
| Clean orders loaded | 12 |
| Revenue (all statuses) | 9,315 |
| Net Revenue (excluding Cancelled) | 9,075 |
| Net Orders / Avg Order Value | 11 / 825 |
| Q1 Target / Achievement % | 9,600 / 94.5% |
| Dhaka: Net Revenue / Target / Achievement | 3,170 / 3,600 / 88.1% |
| Delivered Revenue / Delivered % | 6,670 / 73.5% |
| MoM growth: Feb / Mar | +14.5% / −57.0% |
| Customers with no orders | 1 (Blue Thread Ltd) |

## Suggested repository structure

```text
phase1-executive-bi/
├── README.md               ← start here: the problem, the screenshots, the results
├── data/                   ← raw and clean practice files (or anonymised samples)
├── power-query/            ← exported M code (Advanced Editor) as .m or .txt
├── powerbi/
│   └── sales-model.pbix
├── sql/sales_pack.sql
├── excel/sales_summary.xlsx
├── docs/
│   ├── KPI_DICTIONARY.md
│   ├── EXECUTIVE_SUMMARY.md
│   ├── DECISION_MEMO.md
│   └── AI_VALIDATION_LOG.md
└── images/                 ← model view, overview page, drill-through, RLS test
```

## README template

```markdown
# Executive BI System — Sales vs Target (Q1 2026)

**Business question:** Are we on target, where aren't we, and what should we do?
**Tools:** Power Query · Power BI (DAX, RLS) · SQL · Excel

## Result (bottom line)
Q1 net revenue 9,075 = 94.5% of target (−525). March and two regions drive the gap.

## What I built
- Cleaning pipeline (raw export → 12 clean orders, checks table)
- Star-schema semantic model with 10 documented measures
- 3-page Power BI report with drill-through, bookmarks and RLS
- SQL sales pack and Excel reconciliation

## Screenshots
![Overview](images/overview.png)

## How I validated
Known-answers table + reconciliation between SQL, Excel and Power BI totals.

## What I'd do next
Add Q2 data via the folder query; automate refresh from SharePoint.
```

## Self-assessment rubric

| Area | Meets the bar | Excellent |
|---|---|---|
| Data prep | Clean, refreshable query | Checks table, folder + unpivot, documented steps |
| Model | Star schema, correct measures | Descriptions, display folders, known answers all match |
| Report | Readable overview + 1 extra feature | Drill-through, bookmarks, RLS, action titles throughout |
| Accuracy | Totals match across tools | Reconciliation documented, AI suggestions logged and checked |
| Communication | Summary with numbers | BLUF, insights with comparisons, a clear decision memo |
| Portfolio | Repository with README | README tells the story in 60 seconds, with screenshots |

**Done when:** every requirement is checked, the known answers match (Option A), and someone else can understand your README in one minute.

!!! tip "Certification link"
    This project covers most skill areas of the **Microsoft PL-300 (Power BI Data Analyst)** exam: prepare, model, visualise and analyse, and manage and secure. Finishing it is solid preparation if you choose to take the exam.
