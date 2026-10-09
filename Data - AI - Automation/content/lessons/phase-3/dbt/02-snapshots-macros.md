---
title: "dbt Snapshots and Macros: Preserve History and Reuse SQL Logic"
order: 2
summary: "Track slowly changing customer attributes with a dbt snapshot, then use Jinja macros to keep repeated transformation logic readable and reusable."
level: Intermediate
time: "65 min"
topics: ["Snapshots", "Macros"]
prerequisites: ["phase-3/dbt/01-models-tests"]
keywords: [dbt snapshot, slowly changing dimension, SCD2, Jinja, macro, history, check strategy, timestamp strategy]
reviewed: 2026-10-09
files: [phase-3/dbt-orders-project.zip, phase-3/data-engineering-scripts.zip]
youtube:
  title: "dbt Full Course Part 11 | Snapshots SCD Type 2 and Macros in dbt"
  creator: "Time Variant"
  url: "https://www.youtube.com/watch?v=PL1mOo-NZuA"
  video_id: "PL1mOo-NZuA"
  language: "English"
  level: "Intermediate"
  reviewed: "2026-10-09"
  why_recommended: "A focused 2026 companion covering the same two ideas as this tutorial: SCD Type 2 snapshots and reusable Jinja macros. Its examples use Snowflake; use the supplied DuckDB practice project for your own hands-on work."
resources:
  - title: "Add snapshots to your DAG"
    url: "https://docs.getdbt.com/docs/build/snapshots"
    source: "dbt Developer Hub"
    note: "Official guide to snapshot configuration, strategies and version-history columns."
  - title: "Jinja and macros"
    url: "https://docs.getdbt.com/docs/build/jinja-macros"
    source: "dbt Developer Hub"
    note: "Explains reusable macros, Jinja expressions, compilation and debugging."
---

## Introduction

A current-state table answers:

> What is the customer's credit term **now**?

But business analysis often needs a second question:

> What was the customer's credit term **when an older event happened**?

If a source system overwrites `30` credit days with `45`, the old value disappears unless your analytical system preserves history.

This tutorial solves that with a **dbt snapshot**, then introduces a second dbt capability: **Jinja macros** for reusable SQL logic.

## What you will learn

You will be able to:

- explain why snapshots exist;
- distinguish current-state tables from historical versions;
- understand the timestamp and check strategies;
- configure a snapshot in modern dbt YAML;
- run a deterministic customer-change demo;
- understand Jinja inside dbt SQL;
- write and document a reusable macro;
- inspect compiled SQL when macro logic becomes confusing.

## Mental model: a snapshot turns overwrites into versions

Suppose customer `C007` starts like this:

```text
customer_id = C007
credit_days = 30
```

Later the ERP changes the same record:

```text
customer_id = C007
credit_days = 45
```

A normal table keeps only `45`.

A snapshot keeps history conceptually like this:

```text
C007 | 30 | valid from T1 | valid to T2
C007 | 45 | valid from T2 | still current
```

That is the analytical idea behind a **slowly changing dimension Type 2** pattern.

## Timestamp vs check strategy

A dbt snapshot needs a way to decide whether a source row changed.

### Timestamp strategy

Best when the source provides a trustworthy `updated_at` column.

Conceptually:

```yaml
strategy: timestamp
updated_at: updated_at
```

This is normally the preferred approach because the source explicitly tells you when the row changed.

### Check strategy

Useful when no reliable update timestamp exists.

You tell dbt which columns to compare:

```yaml
strategy: check
check_cols: ['segment', 'region', 'credit_days']
```

Our customer CSV has no `updated_at`, so the practice project deliberately uses **check**.

## Step 1 — configure the snapshot

Open:

```text
completed/snapshots/customers_snapshot.yml
```

It contains:

```yaml
version: 2

snapshots:
  - name: customers_snapshot
    description: "History of customer segment, region and credit-term changes."
    relation: source('shop', 'customers_2025')
    config:
      schema: snapshots
      unique_key: customer_id
      strategy: check
      check_cols: ['segment', 'region', 'credit_days']
```

Important pieces:

| Setting | Meaning |
|---|---|
| `unique_key` | Which source value identifies one business entity |
| `strategy` | How dbt detects change |
| `check_cols` | Which values matter for change detection |
| `schema` | Where snapshot history is stored |

On the first run, dbt stores the current customer rows plus snapshot metadata such as validity timestamps.

On later runs, changed entities receive a new version while the previous version is closed.

## Step 2 — run the first snapshot

On your machine:

```bash
cd completed
python scripts/reset_snapshot_demo.py
dbt seed --select customers_2025 --full-refresh --profiles-dir .
dbt snapshot --select customers_snapshot --profiles-dir .
```

**RUN-BY-OWNER:** dbt is unavailable in this sandbox, so no dbt terminal output is pasted here.

## Step 3 — change one source row deterministically

The project includes:

```text
scripts/apply_snapshot_change.py
```

It changes only `C007`:

```python
mask = df["customer_id"].eq("C007")
old = int(df.loc[mask, "credit_days"].iloc[0])
df.loc[mask, "credit_days"] = 45
```

The baseline data was executed here and confirms:

```text
snapshot demo input: C007 credit_days 30 -> 45
```

Now run:

```bash
python scripts/apply_snapshot_change.py
dbt seed --select customers_2025 --full-refresh --profiles-dir .
dbt snapshot --select customers_snapshot --profiles-dir .
python scripts/inspect_snapshot.py
```

The final command queries the local DuckDB snapshot table and should show two historical versions for `C007` after the second successful snapshot run.

When you finish, restore the deterministic seed:

```bash
python scripts/reset_snapshot_demo.py
```

## Why snapshots are not backups

A snapshot is analytical row history.

It is **not** a substitute for:

- database backups;
- point-in-time recovery;
- object-storage versioning;
- disaster recovery.

Snapshots help answer historical business questions. Backups help restore systems after loss or failure.

---

## Mental model: a macro is a function that writes SQL

Now look at repeated transformation logic.

Suppose several models classify discounts:

```sql
case
    when discount = 0 then 'none'
    when discount <= 0.03 then 'low'
    else 'high'
end
```

Copying that block into five models creates five places to maintain it.

A dbt **macro** lets you describe the reusable SQL-generating logic once.

## Step 4 — create `discount_band`

Open:

```text
completed/macros/discount_band.sql
```

```sql
{% macro discount_band(discount_column) -%}
case
    when {{ discount_column }} = 0 then 'none'
    when {{ discount_column }} <= 0.03 then 'low'
    else 'high'
end
{%- endmacro %}
```

Then call it from a model:

```sql
{{ discount_band('o.discount') }} as discount_band
```

The macro does not create a database table by itself. During compilation, Jinja produces SQL that the database engine can execute.

## Step 5 — see the macro inside a real model

`int_orders_enriched.sql` uses the macro while joining staged data:

```sql
select
    o.*,
    c.customer_name,
    p.list_price,
    {{ discount_band('o.discount') }} as discount_band,
    case
        when o.status = 'Cancelled' then cast(0 as decimal(18, 2))
        else o.revenue
    end as net_revenue
from {{ ref('stg_orders') }} as o
left join {{ ref('stg_customers') }} as c using (customer_id)
left join {{ ref('stg_products') }} as p using (product)
```

Our independent RUN-HERE verification found these actual discount-band counts:

```text
high 2166 | low 504 | none 1576
```

That gives you a concrete result to compare after running the dbt model locally.

## Step 6 — compile when Jinja feels invisible

One challenge with Jinja is that the SQL file you write is not always the final SQL the database sees.

Use:

```bash
dbt compile --select int_orders_enriched --profiles-dir .
```

Then inspect the compiled SQL under `target/compiled/`.

That is one of the best debugging habits in dbt: when a macro or `ref()` behaves unexpectedly, inspect the generated SQL rather than guessing.

Starting with dbt v1.12, snapshot SQL can also be inspected through compilation, which makes snapshot behavior easier to debug.

## Step 7 — document the macro arguments

The project includes `macros/schema.yml`:

```yaml
version: 2

macros:
  - name: discount_band
    description: "Convert a numeric discount expression into none, low or high."
    arguments:
      - name: discount_column
        type: string
        description: "A SQL expression or column name containing a decimal discount."
```

In dbt v1.12, macro-argument validation is stricter by default, so documented argument names should agree with the macro definition.

## Build with me

In `starter/`:

1. create `snapshots/customers_snapshot.yml`;
2. seed and snapshot the baseline customers;
3. run the deterministic change script;
4. reseed and snapshot again;
5. inspect the history;
6. create `macros/discount_band.sql`;
7. call the macro from an intermediate model;
8. compile that model and inspect the generated SQL;
9. compare your files with `completed/`.

## Practice files

The same **dbt-orders-project.zip** continues through this lesson.

Useful files:

```text
completed/snapshots/customers_snapshot.yml
completed/macros/discount_band.sql
completed/macros/schema.yml
completed/scripts/apply_snapshot_change.py
completed/scripts/reset_snapshot_demo.py
completed/scripts/inspect_snapshot.py
```

## Professional context

Snapshots are most valuable when analysts need to reproduce history consistently—for example:

- customer segment at the time of an order;
- account owner before a reassignment;
- supplier terms before renegotiation;
- subscription plan before an upgrade.

Macros are valuable when logic is repeated and truly belongs in one abstraction. Do not turn every three-line SQL expression into Jinja. dbt's own guidance emphasizes **readability over aggressive DRY abstraction**.

## Next tutorial

Next, you will organize the project into **marts**, document the outputs, generate lineage, and build a small monthly revenue table that reconciles to the full Phase 3 dataset.
