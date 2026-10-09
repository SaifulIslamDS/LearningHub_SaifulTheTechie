---
title: "dbt Documentation and Marts: Publish BI-Ready Data with Lineage"
order: 3
summary: "Structure staging, intermediate and mart layers, build a monthly revenue mart, document the model graph, and reconcile the result to the Phase 3 known answers."
level: Intermediate
time: "70 min"
topics: ["Documentation & marts"]
prerequisites: ["phase-3/dbt/02-snapshots-macros"]
keywords: [dbt docs, mart, staging, intermediate, lineage, documentation, gold layer, analytics engineering]
reviewed: 2026-10-09
files: [phase-3/dbt-orders-project.zip, phase-3/data-engineering-scripts.zip]
resources:
  - title: "About documentation"
    url: "https://docs.getdbt.com/docs/build/documentation"
    source: "dbt Developer Hub"
    note: "Official guide to model descriptions, docs blocks and generated dbt documentation."
  - title: "How we structure our dbt projects"
    url: "https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview?version=1.12"
    source: "dbt Developer Hub"
    note: "Explains the staging → intermediate → marts pattern used in this practice project."
  - title: "Best practices for workflows"
    url: "https://docs.getdbt.com/best-practices/best-practice-workflows"
    source: "dbt Developer Hub"
    note: "Practical guidance on model organization, tests and maintainable analytical workflows."
---

## Introduction

A technically correct transformation is not automatically a good data product.

A teammate still needs to know:

- Which table should a dashboard query?
- What is the row grain?
- Where did a column come from?
- Which upstream model breaks if this one changes?
- What does `net_revenue` mean?
- Which models are implementation details and which are intended for consumers?

This tutorial finishes the dbt mini-project by creating **marts** and making the model graph understandable through documentation and lineage.

## What you will learn

You will be able to:

- explain staging, intermediate and mart responsibilities;
- build a BI-ready fact table and monthly mart;
- use documentation blocks and model descriptions;
- generate dbt documentation locally;
- understand model lineage from `ref()` dependencies;
- reconcile the final output to the established Phase 3 business totals;
- see how dbt fits into the later Production Analytics Platform project.

## Mental model: layers have different audiences

A useful dbt project often separates transformation responsibilities:

```text
RAW SOURCE
    ↓
STAGING
    ↓
INTERMEDIATE
    ↓
MARTS
    ↓
BI / ANALYSIS / ML / AI
```

### Staging

Purpose: create clean, typed, consistently named entry points.

Audience: mostly other dbt models.

### Intermediate

Purpose: combine reusable business logic without prematurely exposing it as an end-user dataset.

Audience: downstream transformation developers.

### Marts

Purpose: present business entities and metrics in a form that analysts and BI tools can use directly.

Audience: data consumers.

This is conceptually similar to the bronze/silver/gold progression you already saw in the lakehouse module, but dbt focuses on the **SQL transformation graph** rather than storage-table format.

## Step 1 — build the fact table

The reference project creates `fct_orders.sql` from the enriched intermediate model:

```sql
select * from {{ ref('int_orders_enriched') }}
```

That line looks simple because the important cleanup and joins were already pushed upstream.

The fact table keeps **one row per order**.

Its key calculated fields include:

- `discount_band`;
- `net_revenue` (zero for Cancelled orders);
- `estimated_margin`.

The grain is protected by `not_null` + `unique` tests on `order_id`.

## Step 2 — build a monthly revenue mart

Now create a smaller table specifically for monthly reporting:

```sql
select
    cast(date_trunc('month', order_date) as date) as order_month,
    count(*) as order_count,
    sum(case when status <> 'Cancelled' then 1 else 0 end) as active_order_count,
    round(sum(net_revenue), 2) as net_revenue,
    round(sum(estimated_margin), 2) as estimated_margin
from {{ ref('fct_orders') }}
group by 1
order by 1
```

This model has **one row per month** instead of one row per order.

That makes it a good example of a mart built for a specific analytical use case.

## RUN-HERE — monthly mart reconciliation

The dbt engine itself is owner-run in this environment, but the exact monthly logic was executed independently against the same source data.

| Month | Orders | Net revenue |
|---|---:|---:|
| 2025-01 | 291 | 330,192.02 |
| 2025-02 | 248 | 335,736.27 |
| 2025-03 | 280 | 324,249.14 |
| 2025-04 | 252 | 336,681.97 |
| 2025-05 | 337 | 444,537.86 |
| 2025-06 | 245 | 324,326.11 |
| 2025-07 | 399 | 547,578.67 |
| 2025-08 | 382 | 499,336.45 |
| 2025-09 | 465 | 606,666.32 |
| 2025-10 | 498 | 637,896.70 |
| 2025-11 | 453 | 614,878.83 |
| 2025-12 | 396 | 476,277.45 |

The executed verifier reported:

```text
monthly mart: 12 rows | top month 2025-10 | net revenue 637896.70
known answer: rows 4246 | net revenue 5478357.79
```

The month-level table therefore reconciles to the full non-cancelled revenue total of **5,478,357.79**.

## Step 3 — document the mart in YAML

`models/marts/_marts.yml` contains model and column descriptions:

```yaml
version: 2

models:
  - name: fct_orders
    description: "BI-ready order fact table at one row per order."
    columns:
      - name: order_id
        data_tests: [not_null, unique]

  - name: mart_monthly_revenue
    description: '{{ doc("mart_monthly_revenue") }}'
    columns:
      - name: order_month
        description: "First day of the reporting month."
        data_tests: [not_null, unique]
      - name: net_revenue
        description: "Revenue from all non-cancelled orders in the month."
        data_tests: [not_null]
```

Documentation belongs close to the code that defines the data product.

## Step 4 — use a docs block for longer explanations

The reference project contains:

```text
models/marts/docs.md
```

with:

```text
{% docs mart_monthly_revenue %}
One row per calendar month for 2025. The mart reconciles all
non-cancelled order revenue into a small BI-ready table.
{% enddocs %}
```

The YAML calls it with:

```yaml
description: '{{ doc("mart_monthly_revenue") }}'
```

A docs block is useful when the description is too substantial to keep comfortably inside YAML.

## Step 5 — understand lineage

Every `ref()` creates a dependency edge.

The core graph in this project is:

```text
shop.orders_2025
      ↓
  stg_orders ─────────────┐
                         │
stg_customers ───────┐    │
                     ↓    ↓
stg_products ───→ int_orders_enriched
                         ↓
                     fct_orders
                         ↓
              mart_monthly_revenue
```

This lineage is not decorative. It helps answer operational questions:

- What will be affected if `stg_orders` changes?
- Which upstream source feeds this dashboard table?
- Which models can be rebuilt selectively?
- Where should a quality failure be investigated?

## Step 6 — generate documentation

On your machine:

```bash
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

`dbt docs generate` produces metadata and catalog artifacts. `dbt docs serve` starts a local documentation site where you can browse models, descriptions and lineage.

**RUN-BY-OWNER:** this sandbox does not contain dbt, so no fake `dbt docs` output is included.

## Step 7 — run the completed project

From `completed/`:

```bash
python -m venv .venv
# activate the environment
pip install -r requirements-dbt.txt

dbt debug --profiles-dir .
dbt seed --full-refresh --profiles-dir .
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
```

The project includes a singular reconciliation test. Your build should fail if the order count is no longer **4,246** or net revenue is no longer **5,478,357.79**.

That turns a business-known answer into a regression guard.

## Why marts should not simply expose every intermediate model

A common mistake in analytics engineering is to publish every transformation table to end users.

That creates confusion:

```text
Which table should I use?
Which one is stable?
Which one has the approved KPI definition?
```

Marts create a deliberate interface between transformation internals and data consumers.

For this project:

- `stg_*` = source-oriented cleanup;
- `int_*` = reusable implementation logic;
- `fct_*` / `dim_*` = business entities;
- `mart_*` = reporting-specific outputs.

## Build with me

In your `starter/` project:

1. create `int_orders_enriched.sql`;
2. create `fct_orders.sql` and `dim_customers.sql`;
3. create `mart_monthly_revenue.sql`;
4. add model/column descriptions;
5. add the reconciliation test;
6. run `dbt build`;
7. generate dbt docs;
8. inspect lineage from source → staging → intermediate → mart;
9. compare your result with `completed/` and the 12-row monthly known-answer table above.

## Practice files

Key completed files:

```text
models/intermediate/int_orders_enriched.sql
models/marts/fct_orders.sql
models/marts/dim_customers.sql
models/marts/mart_monthly_revenue.sql
models/marts/_marts.yml
models/marts/docs.md
tests/assert_fct_orders_reconciles.sql
```

## Professional context

A strong dbt project is not just a folder of SQL files. It provides a contract for analytical transformation:

- dependencies are explicit;
- tests are executable;
- documentation is versioned;
- model layers have clear responsibilities;
- lineage is visible;
- business totals can be reconciled;
- changes can be reviewed in Git.

This is why dbt sits naturally between ingestion/storage and BI-ready gold tables in the final Phase 3 architecture.

## Connection to the Phase 3 project

The final **Production Analytics Platform** will connect the pieces you are building across M8:

```text
API ingestion
   ↓
PostgreSQL / lakehouse
   ↓
dbt models + tests
   ↓
orchestrated daily run
   ↓
BI-ready gold/marts
   ↓
document pipeline for AI-ready retrieval
```

Your dbt mini-project is therefore not an isolated exercise. It becomes the transformation layer of the final Phase 3 system.

## Next tutorial

The next approved M8 milestone after dbt is **AI-Ready Data**: unstructured document pipelines, parsing/chunking, embedding refresh, and metadata/lineage for RAG.
