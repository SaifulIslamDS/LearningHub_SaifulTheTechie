---
title: "OLTP vs OLAP, Facts & Dimensions: Build a Star Schema in SQL"
order: 1
summary: "Understand why analytics needs a different design from operational databases, define the grain, and build a star schema — a fact table with date, customer, product and channel dimensions — in PostgreSQL."
level: Intermediate
time: "55 min"
topics: ["OLTP vs OLAP", "Facts & dimensions", "Star schema"]
prerequisites: ["phase-3/database-engineering/01-postgresql-normalization", "phase-1/power-pivot-dax/01-relationships"]
keywords: [oltp, olap, data warehouse, dimensional modelling, dimensional modeling, kimball, fact table, dimension table, grain, measures, surrogate key, business key, natural key, date dimension, star schema, snowflake schema, conformed dimension, additive measure, denormalised]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Dimensional Modeling Techniques"
    url: "https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/"
    source: "Kimball Group"
    note: "The original reference for facts, dimensions, grain and SCDs."
  - title: "Understand star schema and the importance for Power BI"
    url: "https://learn.microsoft.com/en-us/power-bi/guidance/star-schema"
    source: "Microsoft Learn"
    note: "The same design from the BI side (Phase 1)."
  - title: "What is OLAP?"
    url: "https://aws.amazon.com/what-is/olap/"
    source: "AWS"
    note: "OLTP vs OLAP in plain language."
---

## What is it?

| | **OLTP** (online transaction processing) | **OLAP** (online analytical processing) |
|---|---|---|
| Purpose | Run the business: take orders, update stock | Understand the business: trends, comparisons |
| Typical query | Read or change **one** order by its key | Summarise **millions** of rows by several attributes |
| Design | Normalised (previous module) | **Dimensional**: star schemas |
| Optimised for | Many small, fast writes | Fast reads of large ranges |
| Examples | PostgreSQL, MySQL, SQL Server behind an app | BigQuery, Snowflake, Redshift, Fabric, Databricks SQL, DuckDB |

A **star schema** has one **fact table** in the middle and **dimension tables** around it:

```text
               dim_date
                  │
dim_customer ── fact_sales ── dim_product
                  │
             dim_channel
```

| | Fact table | Dimension table |
|---|---|---|
| Holds | Events and their **measures** (quantity, revenue, cost) | Descriptions to filter and group by (who, what, when, how) |
| Rows | Many (millions) | Few (dozens to thousands) |
| Keys | Foreign keys to every dimension | One **surrogate key** each |

!!! job "Why it matters at work"
    Dimensional modelling is the most common design in analytics: Power BI, Tableau, dbt projects and every cloud warehouse use it. Data and analytics engineers are expected to define the grain, choose facts and dimensions, and explain the trade-offs. It's a near-certain interview topic.

The script is `09_star_schema.sql`. It builds a `dw` schema from the normalised `shop` tables.

## Step 1: decide the grain first

The **grain** is what one fact row represents. Write it as a sentence before designing anything:

> **One row in `fact_sales` = one order** (one product line, as placed by a customer on a date through a channel).

Everything else follows from it: which dimensions apply (date, customer, product, channel), and which measures are true at that grain (quantity, revenue, cost, a cancelled flag). Mixing grains, such as orders and monthly targets in one table, is the most common modelling mistake (Phase 1 kept targets in their own fact table for this reason).

## Step 2: dimensions

```sql
CREATE TABLE dw.dim_date AS
SELECT to_char(d, 'YYYYMMDD')::int AS date_key, d::date AS full_date,
       extract(year FROM d)::int AS year, extract(quarter FROM d)::int AS quarter,
       extract(month FROM d)::int AS month, to_char(d, 'Mon') AS month_name,
       to_char(d, 'Dy') AS weekday, extract(isodow FROM d) IN (5) AS is_weekend   -- Friday weekend
FROM generate_series(date '2025-01-01', date '2025-12-31', interval '1 day') AS d;

CREATE TABLE dw.dim_customer AS
SELECT row_number() OVER (ORDER BY customer_id)::int AS customer_key, customer_id, customer_name,
       segment, region, credit_days
FROM shop.customers;
```

- The **date dimension** has one row per day, with every attribute an analyst might group by (quarter, month name, weekday, a weekend flag for Bangladesh's Friday). It's generated, not loaded.
- `customer_key` is a **surrogate key**: a meaningless integer owned by the warehouse. `customer_id` (C010) is the **business key** from the source system. Surrogate keys make history possible (next lesson) and protect the warehouse from changes in source IDs.
- `date_key` uses the readable `YYYYMMDD` form (20251002), a common convention.

## Step 3: the fact table

```sql
CREATE TABLE dw.fact_sales AS
SELECT o.order_id,
       to_char(o.order_date, 'YYYYMMDD')::int AS date_key,
       c.customer_key, o.product_id AS product_key, ch.channel_key,
       o.quantity, round(o.quantity * o.unit_price * (1 - o.discount), 2) AS revenue,
       round(o.quantity * p.unit_cost, 2) AS cost,
       (o.status = 'Cancelled')::int AS is_cancelled
FROM shop.orders o
JOIN dw.dim_customer c USING (customer_id)
JOIN dw.dim_channel ch USING (channel)
JOIN shop.products p USING (product_id);
```

```text
  table_name  | rows
--------------+------
 fact_sales   | 4246
 dim_date     |  365
 dim_customer |   63
 dim_product  |   12
 dim_channel  |    3
```

- The fact holds **keys + measures**, nothing descriptive. Names and segments live in the dimensions, stored once.
- Measures are **additive** where possible (quantity, revenue, cost can be summed in any direction). Percentages like margin are calculated *at query time* from the sums, never stored and summed.
- `is_cancelled` as 0/1 lets you count with `sum()` and filter easily.

## Step 4: OLTP vs OLAP questions

**OLTP:** one order, by its key: touches one row.

```text
 order_id | order_date | customer_id |  status
----------+------------+-------------+-----------
    12935 | 2025-10-02 | C032        | Delivered
```

**OLAP:** revenue and margin by quarter and segment: scans and groups thousands of rows.

```sql
SELECT d.quarter, c.segment,
       round(sum(f.revenue), 0) AS revenue,
       round(100 * (sum(f.revenue) - sum(f.cost)) / sum(f.revenue), 1) AS margin_pct
FROM dw.fact_sales f
JOIN dw.dim_date d USING (date_key)
JOIN dw.dim_customer c USING (customer_key)
WHERE f.is_cancelled = 0
GROUP BY d.quarter, c.segment
ORDER BY d.quarter, revenue DESC
LIMIT 8;
```

```text
 quarter |     segment     | revenue | margin_pct
---------+-----------------+---------+------------
       1 | Garment Factory |  752263 |       26.0
       1 | Knitting Mill   |  141136 |       25.8
       1 | Trader          |   82865 |       25.7
       1 | Retailer        |   13913 |       27.9
       2 | Garment Factory |  858015 |       25.0
       2 | Knitting Mill   |  172412 |       26.5
       2 | Trader          |   56332 |       26.4
       2 | Retailer        |   18788 |       30.0
```

Every star query has the same shape: **fact JOIN the dimensions you need, filter, GROUP BY dimension attributes, SUM measures.** BI tools generate exactly this SQL, which is why they love star schemas. Notice retailers' smaller orders carry a slightly **higher margin** (28–30%).

Any dimension can slice the same fact:

```text
 weekday |  channel  | orders
---------+-----------+--------
 Fri     | Phone     |      6
 Fri     | Portal    |     30
 Fri     | Sales rep |      8
 Sat     | Phone     |     80
 Sat     | Portal    |    224
 Sat     | Sales rep |    130
 Sun     | Phone     |    136
 Sun     | Portal    |    384
 Sun     | Sales rep |    233
```

On the Friday weekend, the **portal** still takes orders (30), while phone and sales reps almost stop: a self-service channel works when the office doesn't.

## Star vs snowflake vs one big table

| Design | What it is | Trade-off |
|---|---|---|
| **Star** | Denormalised dimensions around a fact | The default: simple joins, BI-friendly |
| **Snowflake** | Dimensions normalised further (product → category table) | Less duplication, more joins; rarely worth it |
| **One big table (OBT)** | Fact and all attributes in one wide table | Easiest to query; big; harder to change; common for single dashboards in columnar warehouses |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| No stated grain | Double counting, confusing totals | Write the grain sentence first |
| Mixing grains in one fact | Targets summed 30 times per month | One fact table per grain |
| Storing ratios as facts | Averages of percentages are wrong | Store additive measures; compute ratios at query time |
| Business keys as join keys | History and source changes break joins | Surrogate keys in dimensions |
| Descriptions in the fact table | Huge facts, inconsistent labels | Move them to dimensions |

## Try it yourself

**Task:** Write the star query for **net revenue by product category and month for Q4**.

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT p.category, d.month_name, round(sum(f.revenue), 0) AS revenue
FROM dw.fact_sales f JOIN dw.dim_date d USING (date_key) JOIN dw.dim_product p USING (product_key)
WHERE f.is_cancelled = 0 AND d.quarter = 4
GROUP BY p.category, d.month, d.month_name ORDER BY p.category, d.month;
```

```text
 category | month_name | revenue
----------+------------+---------
 Fabric   | Oct        |  281685
 Fabric   | Nov        |  231599
 Fabric   | Dec        |  212195
 Trims    | Oct        |   88334
 Trims    | Nov        |   97588
 Trims    | Dec        |   85822
 Yarn     | Oct        |  267877
 Yarn     | Nov        |  285692
 Yarn     | Dec        |  178260
```

Group by `d.month` as well as `month_name`, so you can sort in calendar order (alphabetical month names would put Dec first). Fabric peaks in October and Yarn a month later, in November: a pattern worth checking with the sales team before planning stock.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What belongs in a fact table?

1. Customer names and addresses
2. Foreign keys to dimensions plus numeric measures, at a stated grain
3. Only dates

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why use a surrogate key (customer_key) instead of the source's customer_id?

1. It looks nicer
2. It's owned by the warehouse, supports keeping history (several versions of a customer), and protects against source ID changes
3. Business keys can't be joined

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which workload is OLAP?

1. Updating one order's status
2. Revenue by quarter, segment and channel over three years
3. Inserting a new customer

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **OLTP** runs the business (normalised, small writes); **OLAP** analyses it (dimensional, large reads).
- Start with the **grain**. Facts hold keys and **additive measures**; dimensions hold descriptions with **surrogate keys**.
- Every star query: fact → join dimensions → filter → group by attributes → sum measures.
- Star is the default; snowflake rarely; one big table for simple, single-purpose use.

!!! job "Job-ready check"
    **Interview question:** *"Design a data model for sales reporting."*

    **Strong answer:** "I'd start by agreeing the grain, for example one row per order line, then a fact table with keys to date, customer, product, channel and maybe sales rep, plus additive measures like quantity, revenue and cost. Dimensions get surrogate keys and all the descriptive attributes people filter by, including a generated date dimension. Targets, at a monthly grain, get their own fact table sharing the date and product dimensions. Ratios like margin are computed in queries or the semantic layer."

    **Mini project:** Add `dim_region` (with division and manager) and a monthly `fact_targets` table to the `dw` schema, then write the "actual vs target by region and month" query.
