---
title: "dbt Models and Tests: Turn SQL into a Trusted Transformation Graph"
order: 1
summary: "Build a local dbt project on DuckDB, transform the 2025 orders through staging models, and make core data assumptions executable with dbt data tests."
level: Intermediate
time: "70 min"
topics: ["Models", "Tests"]
prerequisites: ["phase-3/data-quality/03-data-contracts-freshness-alerting"]
keywords: [dbt, dbt core, duckdb, model, source, ref, data test, staging, lineage, ELT]
reviewed: 2026-10-09
files: [phase-3/dbt-orders-project.zip, phase-3/data-engineering-scripts.zip]
resources:
  - title: "What is dbt?"
    url: "https://docs.getdbt.com/docs/introduction?version=1.12"
    source: "dbt Developer Hub"
    note: "Official overview of the dbt language, engine, project model and current version generations."
  - title: "Add data tests to your DAG"
    url: "https://docs.getdbt.com/docs/build/data-tests?version=1.12"
    source: "dbt Developer Hub"
    note: "Official reference for built-in and custom data tests; in v1.12 the preferred YAML key is data_tests."
  - title: "Staging: preparing atomic building blocks"
    url: "https://docs.getdbt.com/best-practices/how-we-structure/2-staging"
    source: "dbt Developer Hub"
    note: "Explains why staging models are normally one-to-one with source tables and where reusable cleanup belongs."
---

## Introduction

You already know how to write SQL. The problem dbt solves is what happens **after the first SQL file works**.

A real analytics transformation layer quickly needs answers to questions like:

- Which query depends on which other query?
- What should run first?
- Which tables are raw sources and which are derived models?
- How do we test primary keys and relationships every run?
- How do teammates review SQL changes in Git?
- How do we generate lineage and documentation from the same project?

**dbt** turns SQL transformations into a project with dependencies, tests, metadata and repeatable commands.

!!! note "Version choice for this learning project"
    dbt v2 is the current recommended generation in October 2026. This hands-on project deliberately uses **dbt Core v1.12 with dbt-duckdb 1.11.x** because it is a transparent, local Python-based workflow that works well for learning model files, tests, snapshots and Jinja without needing a cloud account.

## What you will learn

By the end of this tutorial you will be able to:

1. explain what a dbt model is;
2. understand a local dbt project structure;
3. declare raw inputs with `source()`;
4. connect models with `ref()`;
5. understand materializations;
6. add built-in dbt data tests;
7. distinguish `dbt run`, `dbt test` and `dbt build`;
8. verify the transformation logic against the Phase 3 known answers.

## Mental model: dbt is a transformation compiler + runner

Think of the ELT flow as:

```text
CSV / API / database source
          ↓
      raw tables
          ↓
     dbt sources
          ↓
    staging models
          ↓
 intermediate logic
          ↓
        marts
          ↓
   dashboard / ML / AI
```

A **dbt model** is normally a SQL `select` statement stored in a `.sql` file. dbt compiles that model, resolves dependencies, then creates a view/table (depending on its materialization) in the target database.

The important shift is this:

> You stop thinking in isolated SQL scripts and start thinking in a directed transformation graph.

## Open the practice project

Download **dbt-orders-project.zip** and extract it.

You will see:

```text
dbt-orders-project/
├── starter/
└── completed/
```

Use `starter/` first.

Inside it, the connection and source data are already prepared:

```text
starter/
├── dbt_project.yml
├── profiles.yml
├── requirements-dbt.txt
├── seeds/
│   ├── orders_2025.csv
│   ├── customers_2025.csv
│   └── products_2025.csv
└── models/
    └── staging/
        └── _sources.yml
```

The `completed/` folder is the reference implementation.

## Step 1 — understand `dbt_project.yml`

The reference project begins with:

```yaml
name: phase3_orders
version: "1.0.0"
config-version: 2
profile: phase3_orders

model-paths: ["models"]
seed-paths: ["seeds"]
snapshot-paths: ["snapshots"]
test-paths: ["tests"]
macro-paths: ["macros"]
```

This file tells dbt **what this project is** and **where its resources live**.

Farther down, we set default materializations:

```yaml
models:
  phase3_orders:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
```

The design choice is intentional:

| Layer | Default | Why |
|---|---|---|
| Staging | View | Lightweight one-to-one cleanup of raw sources |
| Intermediate | View | Reusable logic without creating unnecessary stored tables |
| Marts | Table | BI-facing outputs should be fast and stable to query |

A **materialization** is simply the strategy dbt uses to turn a model query into a database object.

## Step 2 — connect locally with DuckDB

`profiles.yml` contains the connection:

```yaml
phase3_orders:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: data/phase3.duckdb
      schema: main
      threads: 4
```

After installation, dbt will create a local DuckDB database at:

```text
data/phase3.duckdb
```

No external database server is required.

## Step 3 — load deterministic raw data with seeds

The three CSVs in `seeds/` are copies of the Phase 3 practice data.

Run on your machine:

```bash
dbt seed --full-refresh --profiles-dir .
```

Because the project config assigns seeds to `raw`, DuckDB receives them under the generated schema `main_raw`.

The source declaration then names them explicitly:

```yaml
version: 2

sources:
  - name: shop
    schema: main_raw
    tables:
      - name: orders_2025
      - name: customers_2025
      - name: products_2025
```

This lets models refer to a source semantically instead of hard-coding a physical table name:

```sql
from {{ source('shop', 'orders_2025') }}
```

## Step 4 — create the first staging model

Create `models/staging/stg_orders.sql`:

```sql
select
    cast(order_id as bigint) as order_id,
    cast(order_date as date) as order_date,
    customer_id,
    region,
    segment,
    channel,
    category,
    product,
    cast(quantity as bigint) as quantity,
    cast(unit_price as decimal(12, 4)) as unit_price,
    cast(discount as decimal(8, 4)) as discount,
    cast(unit_cost as decimal(12, 4)) as unit_cost,
    status,
    cast(promised_days as integer) as promised_days,
    cast(delivery_days as integer) as delivery_days,
    cast(revenue as decimal(18, 2)) as revenue
from {{ source('shop', 'orders_2025') }}
```

The staging model does not try to answer a business question. It creates a **clean, typed entry point** for downstream models.

Repeat the same pattern for customers and products. The completed project contains all three files.

## `source()` vs `ref()`

These two functions are central to dbt.

Use `source()` when entering the dbt graph from a declared external/raw relation:

```sql
{{ source('shop', 'orders_2025') }}
```

Use `ref()` when depending on another dbt resource:

```sql
{{ ref('stg_orders') }}
```

Why `ref()` matters:

1. it resolves the physical relation name;
2. it creates a dependency edge in the DAG;
3. it lets dbt build models in the correct order;
4. it powers lineage/documentation.

## Step 5 — add data tests

A transformation can run successfully and still be wrong.

Create model properties in `models/staging/_staging.yml`:

```yaml
version: 2

models:
  - name: stg_orders
    columns:
      - name: order_id
        data_tests: [not_null, unique]

      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('stg_customers')
                field: customer_id

      - name: status
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Delivered', 'Cancelled', 'Shipped', 'Pending']
```

These tests state the grain and business domains in machine-executable form.

### What each test protects

| Test | Protects against |
|---|---|
| `not_null` | Missing keys or required values |
| `unique` | Duplicate business keys |
| `relationships` | Orphan foreign keys |
| `accepted_values` | Unexpected categorical values |

In dbt v1.12, **data tests** is the preferred terminology because dbt also has unit tests. The older YAML key `tests:` remains accepted, but this project uses `data_tests:`.

## Step 6 — add a reconciliation test

Generic tests validate columns. A **singular data test** can validate a business result.

The completed project includes:

```sql
-- tests/assert_fct_orders_reconciles.sql
with totals as (
    select
        count(*) as row_count,
        round(sum(net_revenue), 2) as net_revenue
    from {{ ref('fct_orders') }}
)
select *
from totals
where row_count <> 4246
   or abs(net_revenue - 5478357.79) > 0.01
```

A dbt data test passes when its query returns **zero failing rows**.

This one protects the two shared Phase 3 known answers.

## Step 7 — understand the commands

### `dbt run`

Builds selected models.

```bash
dbt run --profiles-dir .
```

### `dbt test`

Runs data tests (and unit tests when present/selected).

```bash
dbt test --profiles-dir .
```

### `dbt build`

Builds DAG-selected resources in dependency order and runs tests as part of the workflow.

```bash
dbt build --profiles-dir .
```

For this project, seed the raw CSV data first because the declared dbt `source()` does not itself create those tables:

```bash
dbt seed --full-refresh --profiles-dir .
dbt build --profiles-dir .
```

## Verification in this checkpoint

The actual dbt CLI is not installed in this sandbox, so dbt execution is **RUN-BY-OWNER**.

However, the business logic was independently executed against the exact Phase 3 dataset.

Run-HERE script:

```bash
python 19_dbt_logic_verification.py
```

**RUN-HERE — real output:**

```text
source rows: orders 4246 | customers 63 | products 12
grain/tests: duplicate order_id 0 | invalid statuses none
relationships: missing customers 0 | missing products 0
known answer: rows 4246 | net revenue 5478357.79
discount bands: high 2166 | low 504 | none 1576
monthly mart: 12 rows | top month 2025-10 | net revenue 637896.70
snapshot demo input: C007 credit_days 30 -> 45
```

The project structure was also audited:

```bash
python 20_dbt_project_audit.py
```

**RUN-HERE — real output:**

```text
dbt project audit: 19/19 required files present
models: 7 | refs: 5 resolved | source() pairs: 3
profile: duckdb | path data/phase3.duckdb | target schema main
snapshot: customer_id | check strategy | 3 tracked columns
dbt CLI execution: RUN-BY-OWNER (dbt and duckdb packages are not installed in this sandbox)
```

## Build with me

Use `starter/` and create the project in this order:

1. install the requirements;
2. run `dbt debug --profiles-dir .`;
3. seed the three CSVs;
4. create the three staging models;
5. add the staging YAML tests;
6. run `dbt run --select staging --profiles-dir .`;
7. run `dbt test --select staging --profiles-dir .`;
8. compare your project with `completed/`.

Do not copy the completed files first. The goal is to understand how `source()`, model files and tests connect.

## Practice files

Inside **dbt-orders-project.zip**:

```text
starter/     ← begin here
completed/   ← reference implementation
```

The completed project includes the files used across all three dbt tutorials, so you will keep extending the same mini-project rather than starting over.

## Professional context

In a production team, dbt models normally live in Git. A pull request can show:

- which SQL model changed;
- which downstream models depend on it;
- which tests pass or fail;
- whether documentation changed;
- whether a business reconciliation broke.

That is the real benefit: **SQL becomes software-like work** with versioning, dependencies and automated checks.

## Next tutorial

Next, you will preserve customer history with a **snapshot** and remove repeated SQL logic with a reusable **macro**.
