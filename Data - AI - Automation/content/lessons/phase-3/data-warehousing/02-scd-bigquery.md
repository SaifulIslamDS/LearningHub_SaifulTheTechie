---
title: "Slowly Changing Dimensions & BigQuery: History and the Cloud Warehouse"
order: 2
summary: "Keep dimension history with SCD type 2 (valid-from/valid-to rows, idempotent loads, as-was vs as-is reports), then take warehouse SQL to BigQuery: dialect differences, partitioning, clustering and paying by bytes scanned."
level: Intermediate
time: "55 min"
topics: ["SCD", "BigQuery"]
prerequisites: ["phase-3/data-warehousing/01-oltp-olap-star-schema"]
keywords: [slowly changing dimension, scd, scd type 1, scd type 2, valid_from, valid_to, is_current, history, point-in-time, as-was, as-is, idempotent load, bigquery, cloud data warehouse, partitioning, clustering, bytes scanned, on-demand pricing, dry run, sqlglot, sql dialect, duckdb, columnar]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Kimball techniques: Slowly changing dimensions"
    url: "https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/"
    source: "Kimball Group"
    note: "Types 0–7 explained by the people who named them."
  - title: "Enable the BigQuery sandbox"
    url: "https://cloud.google.com/bigquery/docs/sandbox"
    source: "Google Cloud docs"
    note: "Try BigQuery free, without a credit card (with limits)."
  - title: "Introduction to partitioned tables"
    url: "https://cloud.google.com/bigquery/docs/partitioned-tables"
    source: "Google Cloud docs"
    note: "Partitioning and clustering to scan (and pay for) less."
  - title: "sqlglot"
    url: "https://github.com/tobymao/sqlglot"
    source: "GitHub (open source)"
    note: "Translate SQL between 30+ dialects."
---

## What is it?

- A **slowly changing dimension (SCD)** is a dimension whose attributes change occasionally: a customer moves region, a product changes category. The SCD **type** decides what happens to history:

| Type | On change | Reports show | Use when |
|---|---|---|---|
| **Type 1** | Overwrite the old value | Everything under the **new** value ("as is") | Corrections; history doesn't matter |
| **Type 2** | Add a **new row** (new surrogate key), close the old one with dates | Each fact under the value **at the time** ("as was") | Region, segment, price tier, credit terms: anything you analyse over time |

- **BigQuery** is Google Cloud's serverless data warehouse: you load tables and run SQL; Google handles servers and scaling. You pay mainly for **storage** and **bytes scanned** by queries (on-demand), or for reserved capacity.

!!! job "Why it matters at work"
    "Did Dhaka's revenue really drop, or did a big customer move to Gazipur?" Without SCD type 2, nobody can answer that. It's a staple of warehouse design (and of dbt snapshots in Phase 3B). Cloud warehouses such as BigQuery, Snowflake, Redshift and Fabric are where most of this runs today, and their cost models change how you write SQL.

## Part 1: SCD type 2 in SQL

The script is `10_scd.sql` (run after `09_star_schema.sql`). The type 2 dimension has validity columns:

```sql
CREATE TABLE dw.dim_customer_scd2 (
    customer_key  serial PRIMARY KEY,                 -- surrogate key: one per VERSION
    customer_id   text NOT NULL,                      -- business key: one per customer
    customer_name text, segment text, region text, credit_days int,
    valid_from    date NOT NULL,
    valid_to      date NOT NULL DEFAULT '9999-12-31',
    is_current    boolean NOT NULL DEFAULT true
);
```

On **1 July**, customer C010 moves from Dhaka to Gazipur and is given 60-day credit. Apply the change in **one transaction**: close the current version, then insert the new one.

```sql
BEGIN;
UPDATE dw.dim_customer_scd2 d
SET valid_to = c.changed_on - 1, is_current = false
FROM staging.customer_changes c
WHERE d.customer_id = c.customer_id AND d.is_current
  AND (d.region, d.credit_days) IS DISTINCT FROM (c.region, c.credit_days);
INSERT INTO dw.dim_customer_scd2 (customer_id, customer_name, segment, region, credit_days, valid_from)
SELECT c.customer_id, c.customer_name, c.segment, c.region, c.credit_days, c.changed_on
FROM staging.customer_changes c
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_customer_scd2 d
                  WHERE d.customer_id = c.customer_id AND d.is_current
                    AND (d.region, d.credit_days) = (c.region, c.credit_days));
COMMIT;
```

```text
 customer_key | customer_id | region  | credit_days | valid_from |  valid_to  | is_current
--------------+-------------+---------+-------------+------------+------------+------------
           10 | C010        | Dhaka   |          15 | 2025-01-01 | 2025-06-30 | f
           64 | C010        | Gazipur |          60 | 2025-07-01 | 9999-12-31 | t
```

- Two rows for one customer: same **business key** (C010), different **surrogate keys** (10, 64).
- `valid_to = 9999-12-31` and `is_current = true` mark the live version.
- `IS DISTINCT FROM` compares values safely even when some are NULL.

### Idempotent: run it again, nothing changes

```text
 versions_of_c010
------------------
                2
```

Running exactly the same statements a second time adds nothing, because both steps check whether the change is already applied. **Idempotent** loads are safe to re-run after a failure: a habit for every pipeline (Phase 3B).

### As-was vs as-is reporting

```sql
-- as was: each order joins the version valid on its order date
SELECT d.region AS region_at_order_time, count(*) AS orders, round(sum(o.quantity * o.unit_price * (1 - o.discount)), 0) AS revenue
FROM shop.orders o
JOIN dw.dim_customer_scd2 d
  ON d.customer_id = o.customer_id AND o.order_date BETWEEN d.valid_from AND d.valid_to
WHERE o.customer_id = 'C010' AND o.status <> 'Cancelled'
GROUP BY d.region ORDER BY d.region;
```

```text
 region_at_order_time | orders | revenue
----------------------+--------+---------
 Dhaka                |     79 |  108935
 Gazipur              |    122 |  186479
```

```text
 current_region | orders
----------------+--------
 Gazipur        |    201
```

- **As was** (type 2 join on dates): Dhaka keeps the 108,935 it really earned in the first half of the year.
- **As is** (current version only): all 201 orders appear under Gazipur, and Dhaka's first-half revenue silently drops.

Both views are legitimate; the business must choose, and the model should support both. In a real fact table you'd store `customer_key` **at load time** (the version valid then), so the as-was join is a simple key join.

## Part 2: the same warehouse in BigQuery

BigQuery needs a Google Cloud account. You can try it free with the **BigQuery sandbox** (no credit card; storage and monthly query limits apply, and tables expire after a period: check the sandbox page for current limits). The script `11_bigquery_sql.py` does the parts that run **locally**, so every output below is real. **The BigQuery-only commands (DDL, `bq`) are shown for reference and were not executed for this lesson.**

### Dialects differ: translate, then review

```python
bq_sql = sqlglot.transpile(pg_sql, read="postgres", write="bigquery", pretty=True)[0]
```

Our PostgreSQL month-on-month query, translated to BigQuery's GoogleSQL:

```text
WITH monthly AS (
  SELECT
    CAST(TIMESTAMP_TRUNC(order_date, MONTH) AS DATE) AS month,
    SUM(quantity * unit_price * (
      1 - discount
    )) AS revenue
  FROM orders
  WHERE
    status <> 'Cancelled'
  GROUP BY
    1
)
SELECT
  month,
  ROUND(revenue, 0) AS revenue,
  ROUND(
    100.0 * (
      revenue - LAG(revenue) OVER (ORDER BY month NULLS LAST)
    ) / LAG(revenue) OVER (ORDER BY month NULLS LAST),
    1
  ) AS mom_pct
FROM monthly
ORDER BY
  month NULLS LAST
```

The **structure** is identical (CTEs and window functions are standard SQL); **functions** differ: `date_trunc('month', x)` becomes `…_TRUNC(x, MONTH)`. A translator can't see your column types: for a `DATE` column the idiomatic BigQuery function is `DATE_TRUNC(order_date, MONTH)`. Always review and test translated SQL.

The same query runs locally on **DuckDB**, a columnar engine like BigQuery, against the CSV:

```text
     month  revenue  mom_pct
2025-01-01 330192.0      NaN
2025-02-01 335736.0      1.7
2025-03-01 324249.0     -3.4
2025-04-01 336682.0      3.8
```

The same numbers as PostgreSQL in the window-functions lesson.

### You pay for the columns you read

On-demand BigQuery bills by **bytes scanned**, and it stores data by column. Our Parquet file gives a feel for it:

```text
all columns: 143 KB | columns the query uses: 44 KB (30%)
```

The query touches 5 of 16 columns, so it reads about 30% of the data. **`SELECT *` reads (and bills) every column**; `LIMIT` does not reduce bytes scanned. Name your columns.

### Partitioning and clustering (BigQuery DDL, not executed here)

```sql
CREATE TABLE sales.fact_sales
PARTITION BY order_date                -- one partition per day: date filters skip whole partitions
CLUSTER BY customer_id, region         -- rows sorted within partitions: filters on these read fewer blocks
AS SELECT * FROM staging.orders_2025;
```

```bash
# estimate bytes BEFORE paying for a query (not executed in this lesson)
bq query --use_legacy_sql=false --dry_run 'SELECT region, SUM(revenue) FROM sales.fact_sales WHERE order_date >= "2025-10-01" GROUP BY region'
```

| Habit | Effect on cost |
|---|---|
| Select only needed columns | Fewer bytes per column read |
| Filter on the partition column (dates) | Skips whole partitions |
| Cluster by common filters | Reads fewer blocks |
| Dry run / query validator first | Shows bytes before you pay |
| Pre-aggregate dashboards (gold tables) | Small tables for repeated queries |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Type 1 overwrite for analysed attributes | Past reports change silently | Type 2 for region, segment, terms |
| Joining facts to type 2 dims on the business key only | Every order duplicated once per version | Join on surrogate key, or business key + date range |
| Non-idempotent SCD loads | Duplicate versions after a re-run | Check "already applied" in both steps; one transaction |
| `SELECT *` in BigQuery | Paying to scan every column | Name columns; preview tables for free in the UI |
| Trusting translated SQL blindly | Wrong functions for your types | Review and test against known answers |

## Try it yourself

**Task:** Find customers that have more than one version in `dim_customer_scd2`, and their current region.

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT customer_id, count(*) AS versions, max(region) FILTER (WHERE is_current) AS current_region
FROM dw.dim_customer_scd2 GROUP BY customer_id HAVING count(*) > 1;
```

```text
 customer_id | versions | current_region
-------------+----------+----------------
 C010        |        2 | Gazipur
```

`FILTER (WHERE …)` applies a condition to one aggregate only, a tidy PostgreSQL feature (BigQuery writes it as `MAX(IF(is_current, region, NULL))`). Only C010 has changed so far.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. A customer moves region. You want last year's reports to keep showing the old region. Which SCD type?

1. Type 1
2. Type 2
3. Neither

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `valid_to = '9999-12-31'` usually mean?

1. The data is wrong
2. This is the current, still-valid version
3. The row was deleted

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. On-demand BigQuery charges by bytes scanned. Which change reduces cost most reliably?

1. Adding `LIMIT 10`
2. Selecting only the needed columns and filtering on the partition column
3. Sorting the results

<details markdown="1"><summary>Show answer</summary>
**B.** LIMIT doesn't reduce bytes scanned.
</details>
</div>

## Summary

- **SCD type 1** overwrites (as-is); **type 2** adds versions with `valid_from`, `valid_to`, `is_current` (as-was).
- Apply type 2 changes in one transaction, **idempotently**; join facts on the version valid at the time.
- **BigQuery**: serverless, columnar, billed by bytes scanned (on demand). Name columns, partition by date, cluster by common filters, dry-run first.
- SQL is portable in structure, not in every function: translate (e.g. sqlglot), then review and test.

!!! job "Job-ready check"
    **Interview question:** *"How would you track changes to customer attributes in a warehouse?"*

    **Strong answer:** "SCD type 2 for attributes we analyse over time: a surrogate key per version, valid-from and valid-to dates and a current flag. The load closes the current row and inserts the new one in a single, idempotent transaction, and facts store the surrogate key valid at load time, so reports show history as it was. For pure corrections I'd use type 1. In dbt this is a snapshot."

    **Mini project:** Apply a second change (C044 becomes a Trader on 1 October) to `dim_customer_scd2`, then rebuild the "revenue by segment by quarter" report both as-was and as-is and explain the difference in two sentences.
