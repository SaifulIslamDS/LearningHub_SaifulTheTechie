---
title: "CTEs and Recursive CTEs: Readable Multi-Step SQL"
order: 1
summary: "Break complex SQL into named steps with WITH, then use recursive CTEs to generate calendars that keep empty months and to walk hierarchies like an org chart — in PostgreSQL."
level: Intermediate
time: "45 min"
topics: ["CTEs", "Recursive CTEs"]
prerequisites: ["phase-1/analytical-sql/05-subqueries"]
keywords: [cte, common table expression, with clause, chained ctes, recursive cte, with recursive, anchor, recursive member, union all, hierarchy, org chart, tree, calendar, date spine, generate_series, cohort, postgresql]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "WITH Queries (Common Table Expressions)"
    url: "https://www.postgresql.org/docs/current/queries-with.html"
    source: "PostgreSQL official docs"
    note: "CTEs, recursive queries, cycle detection and materialisation."
  - title: "PostgreSQL Exercises"
    url: "https://pgexercises.com/"
    source: "pgexercises.com (free)"
    note: "Interactive practice, including recursive queries."
  - title: "SQL Tutorial for Data Analysis"
    url: "https://mode.com/sql-tutorial/"
    source: "Mode (free)"
    note: "Intermediate and advanced SQL with business examples."
---

## What is it?

- A **CTE** (common table expression) is a named, temporary result defined with `WITH name AS (...)` at the top of a query. You can chain several, each using the ones before it.
- A **recursive CTE** (`WITH RECURSIVE`) refers to **itself**: it starts from an *anchor* row set and keeps adding rows until a stop condition is met. It generates sequences and walks trees.

!!! job "Why it matters at work"
    Real analytics SQL is long: filter, then aggregate, then compare, then rank. CTEs turn that into readable steps that reviewers can follow and test one at a time, and they're the building blocks of dbt models (Phase 3B). Recursive CTEs answer "who reports to whom", "which parts make up this product" and "show every month, even empty ones": classic interview questions.

The script is `04_ctes.sql`, run against the `shop` schema created by `03_load_postgres.py`.

## Part 1: a CTE as named steps

*"Which customers beat their own segment's average revenue?"* needs three steps. Each gets a name:

```sql
WITH net_orders AS (                      -- step 1: only orders that count
    SELECT o.*, o.quantity * o.unit_price * (1 - o.discount) AS revenue
    FROM shop.orders o
    WHERE o.status <> 'Cancelled'
),
customer_revenue AS (                     -- step 2: one row per customer
    SELECT c.customer_id, c.customer_name, c.segment, round(sum(n.revenue), 0) AS revenue
    FROM net_orders n JOIN shop.customers c USING (customer_id)
    GROUP BY c.customer_id, c.customer_name, c.segment
),
segment_avg AS (                          -- step 3: one row per segment
    SELECT segment, round(avg(revenue), 0) AS avg_revenue
    FROM customer_revenue GROUP BY segment
)
SELECT cr.segment, count(*) AS customers_above_avg, max(sa.avg_revenue) AS segment_avg
FROM customer_revenue cr JOIN segment_avg sa USING (segment)
WHERE cr.revenue > sa.avg_revenue
GROUP BY cr.segment
ORDER BY cr.segment;
```

```text
     segment     | customers_above_avg | segment_avg
-----------------+---------------------+-------------
 Garment Factory |                  12 |      169387
 Knitting Mill   |                   4 |       73352
 Retailer        |                   6 |        6390
 Trader          |                   6 |       32160
```

- Read it **top to bottom**, like a recipe. Compare that with three nested subqueries read inside-out.
- To debug, temporarily end the query after any step with `SELECT * FROM customer_revenue LIMIT 5;`.
- `USING (customer_id)` is shorthand for `ON a.customer_id = b.customer_id` when the column has the same name on both sides.

### Chained CTEs: a quick cohort

```sql
WITH first_order AS (
    SELECT customer_id, min(order_date) AS first_date FROM shop.orders GROUP BY customer_id
)
SELECT to_char(date_trunc('quarter', first_date), 'YYYY-"Q"Q') AS first_quarter, count(*) AS customers
FROM first_order GROUP BY 1 ORDER BY 1;
```

```text
 first_quarter | customers
---------------+-----------
 2025-Q1       |        59
 2025-Q2       |         1
```

59 of the 60 ordering customers placed their first 2025 order in Q1. One started in Q2. That's the start of a **cohort analysis**: group customers by when they started, then track what they do afterwards.

## Part 2: recursive CTE #1, a calendar ("date spine")

Customer C053 didn't order every month. A plain `GROUP BY month` simply **skips** empty months, and a chart of it would quietly join May to July. Generate every month first, then LEFT JOIN the orders:

```sql
WITH RECURSIVE months(m) AS (
    SELECT date '2025-01-01'                        -- anchor: where to start
    UNION ALL
    SELECT (m + interval '1 month')::date FROM months
    WHERE m < date '2025-12-01'                     -- stop condition
)
SELECT to_char(m, 'Mon') AS month, count(o.order_id) AS orders     -- count(column) gives 0 for no match
FROM months
LEFT JOIN shop.orders o ON date_trunc('month', o.order_date) = months.m AND o.customer_id = 'C053'
GROUP BY m ORDER BY m;
```

```text
 month | orders
-------+--------
 Jan   |      0
 Feb   |      0
 Mar   |      0
 Apr   |      0
 May   |      3
 Jun   |      0
 Jul   |      2
 Aug   |      3
 Sep   |      0
 Oct   |      4
 Nov   |      2
 Dec   |      2
```

How recursion runs:

1. The **anchor** produces the first row: 1 January.
2. The **recursive part** takes the previous rows and produces new ones (1 February), and then again, and again.
3. It stops when the `WHERE` produces no new rows (after 1 December). **Always** have a stop condition, or the query runs until it fails.

!!! tip "PostgreSQL shortcut"
    PostgreSQL also has `generate_series(date '2025-01-01', date '2025-12-01', interval '1 month')`. The recursive pattern works in almost every database (SQL Server, Snowflake, BigQuery, DuckDB), so it's worth knowing.

## Part 3: recursive CTE #2, walking a hierarchy

`shop.staff` stores each person's manager in `manager_id` (a self-reference):

```sql
WITH RECURSIVE org AS (
    SELECT staff_id, name, title, 1 AS level, name::text AS path
    FROM shop.staff WHERE manager_id IS NULL                       -- anchor: the top of the tree
    UNION ALL
    SELECT s.staff_id, s.name, s.title, org.level + 1, org.path || ' > ' || s.name
    FROM shop.staff s JOIN org ON s.manager_id = org.staff_id     -- recursive step: their reports
)
SELECT level, repeat('    ', level - 1) || name AS person, title, path FROM org ORDER BY path;
```

```text
 level |      person       |                 title                 |               path
-------+-------------------+---------------------------------------+----------------------------------
     1 | Farhana           | Head of Sales                         | Farhana
     2 |     Anika         | Regional Manager, Dhaka & Gazipur     | Farhana > Anika
     3 |         Mitu      | Sales Rep                             | Farhana > Anika > Mitu
     3 |         Rafi      | Sales Rep                             | Farhana > Anika > Rafi
     2 |     Tanvir        | Regional Manager, Chattogram & Khulna | Farhana > Tanvir
     3 |         Nadia     | Key Account Lead                      | Farhana > Tanvir > Nadia
     4 |             Imran | Sales Rep                             | Farhana > Tanvir > Nadia > Imran
     3 |         Sohel     | Sales Rep                             | Farhana > Tanvir > Sohel
```

Each round of recursion goes one level deeper; `level` and `path` are built up as it goes. The same pattern handles product categories, bills of materials and folder trees, at any depth, with no change to the query.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| No stop condition in a recursive CTE | Runs until memory or a limit is hit | `WHERE` in the recursive part; cap the depth (`level < 20`) |
| `UNION` instead of `UNION ALL` | Slower, and can hide data issues | `UNION ALL` unless you need de-duplication |
| Cycles in hierarchy data (A manages B, B manages A) | Infinite recursion | Track the path and stop on repeats (PostgreSQL 14+: `CYCLE` clause) |
| `count(*)` after a LEFT JOIN | Empty months show 1, not 0 | `count(o.order_id)` counts only matches |
| One giant CTE chain nobody can test | Hard to debug | Name steps clearly; check each step's row count |

## Try it yourself

**Task:** List everyone who reports to **Tanvir**, directly or indirectly.

<details markdown="1">
<summary>Show a hint</summary>

Start the anchor at Tanvir instead of at the top of the tree, then remove Tanvir from the final result.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
WITH RECURSIVE team AS (
    SELECT staff_id, name FROM shop.staff WHERE name = 'Tanvir'
    UNION ALL
    SELECT s.staff_id, s.name FROM shop.staff s JOIN team t ON s.manager_id = t.staff_id
)
SELECT name FROM team WHERE name <> 'Tanvir' ORDER BY name;
```

```text
 name
-------
 Imran
 Nadia
 Sohel
```

Imran reports to Nadia, who reports to Tanvir, so the recursion finds him at the second level. A simple `WHERE manager_id = 3` would have missed him.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What's the main benefit of a CTE over nested subqueries?

1. It's always faster
2. The query reads as named steps, top to bottom, which is easier to read, test and review
3. It stores data permanently

<details markdown="1"><summary>Show answer</summary>
**B.** A CTE lasts only for that one query.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What are the two parts of a recursive CTE?

1. SELECT and FROM
2. An anchor query and a recursive query joined with UNION ALL
3. A table and an index

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A monthly report skips months with no orders. What's the fix?

1. Use `count(*)`
2. Generate all months first (a date spine), then LEFT JOIN the orders
3. Add `ORDER BY month`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **CTEs** (`WITH a AS (...), b AS (...)`) turn complex SQL into readable, testable steps.
- **Recursive CTEs** = anchor + recursive part (`UNION ALL`) + a stop condition.
- Use them for **date spines** (keep empty periods) and **hierarchies** (org charts, categories, bills of materials).
- After a LEFT JOIN, count a column from the right-hand table to get real zeros.

!!! job "Job-ready check"
    **Interview question:** *"An employees table has a manager_id column. How do you find everyone under a given manager at any level?"*

    **Strong answer:** "A recursive CTE: the anchor selects the manager, the recursive part joins employees whose manager_id is in the previous level, combined with UNION ALL. I'd track the level and path, add a depth cap or cycle check in case the data has loops, and exclude the manager from the final result."

    **Mini project:** Using a date spine, produce a 12-month × customer table of order counts for the 10 biggest customers (zeros included), and flag customers with two or more consecutive empty months.
