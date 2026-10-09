---
title: "Indexing & EXPLAIN ANALYZE: Make the Right Queries Fast"
order: 2
summary: "Read PostgreSQL query plans, see a sequential scan become an index scan (145 ms → 7 ms on 2 million rows), design composite indexes, and learn when an index can't or shouldn't help."
level: Intermediate
time: "50 min"
topics: ["Indexing", "EXPLAIN ANALYZE"]
prerequisites: ["phase-3/database-engineering/01-postgresql-normalization"]
keywords: [index, b-tree, create index, composite index, multicolumn index, selectivity, sequential scan, seq scan, index scan, bitmap scan, explain, explain analyze, query plan, planner, statistics, analyze, sargable, function on column, index size, write overhead, query performance, postgresql]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Using EXPLAIN"
    url: "https://www.postgresql.org/docs/current/using-explain.html"
    source: "PostgreSQL official docs"
    note: "How to read plans, costs and actual times."
  - title: "Indexes"
    url: "https://www.postgresql.org/docs/current/indexes.html"
    source: "PostgreSQL official docs"
    note: "B-tree, multicolumn, expression and partial indexes."
  - title: "Use The Index, Luke"
    url: "https://use-the-index-luke.com/"
    source: "Markus Winand (free online book)"
    note: "The classic guide to SQL indexing for developers."
---

## What is it?

- An **index** is a separate, sorted structure (usually a **B-tree**) that lets the database jump to matching rows instead of reading the whole table, like the index at the back of a book.
- **`EXPLAIN`** shows the **plan** the database will use; **`EXPLAIN ANALYZE`** runs the query and shows what actually happened: which scan, how many rows, how long.

| Plan node | Means |
|---|---|
| **Seq Scan** | Read every row of the table |
| **Index Scan** / **Bitmap Index Scan** | Use an index to find matching rows |
| **Parallel …**, **Gather** | Several workers share the work |
| `rows=` | Rows produced by that step |
| `actual time=a..b` | Milliseconds to first row .. to last row |

!!! job "Why it matters at work"
    "This dashboard is slow" usually ends in a query plan. Data engineers add indexes to support pipeline lookups, joins and incremental loads, and must also know when an index won't help (or slows down writes). Reading `EXPLAIN ANALYZE` is a standard skill for database, analytics-engineering and backend roles.

The script is `07_indexing_explain.sql`. It first builds `shop.orders_big`: **2 million synthetic orders** (5 years, 2,000 customers), because indexes only matter at scale:

```text
 table_size |  count
------------+---------
 139 MB     | 2000000
```

*Timings below are from our test machine; yours will differ. Compare the **ratios** and the plan shapes.*

## Step 1: without an index

```sql
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT * FROM shop.orders_big WHERE customer_id = 'C0042';
```

```text
 Gather (actual time=0.322..145.544 rows=979 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on orders_big (actual time=0.119..104.160 rows=326 loops=3)
         Filter: (customer_id = 'C0042'::text)
         Rows Removed by Filter: 666340
 Planning Time: 0.246 ms
 Execution Time: 145.643 ms
```

Read plans **from the innermost line outwards**: three workers each scanned a third of the table, threw away 666,340 rows each, and kept 326 (979 in total). **2 million rows read to return 979.**

## Step 2: with an index

```sql
CREATE INDEX idx_orders_big_customer ON shop.orders_big (customer_id);
```

```text
 Bitmap Heap Scan on orders_big (actual time=0.277..6.609 rows=979 loops=1)
   Recheck Cond: (customer_id = 'C0042'::text)
   Heap Blocks: exact=950
   ->  Bitmap Index Scan on idx_orders_big_customer (actual time=0.148..0.148 rows=979 loops=1)
         Index Cond: (customer_id = 'C0042'::text)
 Planning Time: 0.336 ms
 Execution Time: 6.680 ms
```

```text
 index_size
------------
 14 MB
```

**145 ms → 6.7 ms (about 20× faster).** The index found the 979 rows' locations, then PostgreSQL read just the 950 table blocks that contain them. The price: 14 MB of extra storage, plus a little extra work on every insert and update.

## Step 3: composite indexes for combined filters

```sql
CREATE INDEX idx_orders_big_cust_date ON shop.orders_big (customer_id, order_date);
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT order_date, revenue FROM shop.orders_big
WHERE customer_id = 'C0042' AND order_date >= '2025-01-01' AND order_date < '2025-04-01';
```

```text
 Bitmap Heap Scan on orders_big (actual time=0.068..0.152 rows=43 loops=1)
   ...
   ->  Bitmap Index Scan on idx_orders_big_cust_date (actual time=0.052..0.052 rows=43 loops=1)
         Index Cond: ((customer_id = 'C0042'::text) AND (order_date >= '2025-01-01'::date) AND (order_date < '2025-04-01'::date))
 Execution Time: 0.200 ms
```

**0.2 ms.** Both conditions are answered inside the index. Column **order** matters: `(customer_id, order_date)` serves "this customer" and "this customer in this date range", but not "all customers in this date range" (for that, `order_date` must come first or have its own index). Rule of thumb: **equality columns first, then range columns.**

## Step 4: when the planner ignores an index

```sql
CREATE INDEX idx_orders_big_status ON shop.orders_big (status);
EXPLAIN (COSTS OFF) SELECT count(*) FROM shop.orders_big WHERE status = 'Delivered';
EXPLAIN (COSTS OFF) SELECT count(*) FROM shop.orders_big WHERE status = 'Shipped';
```

```text
 Finalize Aggregate
   ->  Gather
         ->  Partial Aggregate
               ->  Parallel Seq Scan on orders_big
                     Filter: (status = 'Delivered'::text)

 Aggregate
   ->  Bitmap Heap Scan on orders_big
         Recheck Cond: (status = 'Shipped'::text)
         ->  Bitmap Index Scan on idx_orders_big_status
               Index Cond: (status = 'Shipped'::text)
```

Same index, two decisions. About 90% of orders are Delivered: jumping through an index to read 90% of the table is slower than reading it straight through, so the planner chooses a **Seq Scan**. Shipped is rare (about 4%), so the index wins. The planner decides using **statistics** that `ANALYZE` collects. Indexes help **selective** filters: ones that keep a small fraction of rows.

## Step 5: don't hide the column inside a function

```sql
-- function on the column: the date index can't be used
SELECT count(*) FROM shop.orders_big WHERE date_trunc('month', order_date) = '2025-03-01';
-- the same question as a range: the index is used
SELECT count(*) FROM shop.orders_big WHERE order_date >= '2025-03-01' AND order_date < '2025-04-01';
```

```text
 ->  Parallel Seq Scan on orders_big (actual time=0.111..298.431 rows=11322 loops=3)
       Filter: (date_trunc('month'::text, (order_date)::timestamp with time zone) = …)
 Execution Time: 350.435 ms

 ->  Bitmap Index Scan on idx_orders_big_date (actual time=3.743..3.744 rows=33967 loops=1)
       Index Cond: ((order_date >= '2025-03-01'::date) AND (order_date < '2025-04-01'::date))
 Execution Time: 188.526 ms
```

The index is on `order_date`, not on `date_trunc('month', order_date)`, so wrapping the column in a function forces a full scan. Rewriting it as a **range** lets the index work. The gain here is smaller (350 → 189 ms) because the 34,000 matching rows are **scattered** over 15,180 table blocks (our synthetic dates are random). In real tables loaded in date order, matching rows sit together and the gain is much bigger.

## Step 6: indexes cost space (and write time)

```text
 table_only | all_indexes
------------+-------------
 139 MB     | 95 MB
```

Four indexes already take **two-thirds of the table's size**. Every `INSERT`/`UPDATE` must update every index. Index what the important queries need, check with `EXPLAIN ANALYZE`, and drop indexes nothing uses.

## Indexing checklist

| Index these | Usually skip |
|---|---|
| Primary keys (automatic) and foreign keys used in joins | Low-selectivity columns on their own (status, true/false) |
| Columns in frequent, selective `WHERE` filters | Small tables (a few thousand rows) |
| Combined filters → composite index (equality columns first) | Columns you only ever wrap in functions (or use an expression index) |
| Columns used for incremental loads (`updated_at`) | Write-heavy staging tables during bulk loads |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Guessing instead of measuring | Indexes that are never used | `EXPLAIN ANALYZE` before and after |
| Functions or casts on indexed columns | Silent full scans | Rewrite as ranges; or an expression index |
| Wrong column order in composite indexes | Index unused for some queries | Equality first; match common query patterns |
| Indexing everything | Slow writes, wasted storage | Index for real queries; monitor usage |
| Stale statistics after big loads | Bad plans | `ANALYZE` (autovacuum usually does this) |

## Try it yourself

**Task:** Run `EXPLAIN ANALYZE` on "total revenue per region for 2024". Which index (if any) does the planner use, and why isn't the query as fast as the single-customer lookup?

<details markdown="1">
<summary>Show the solution</summary>

```sql
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT region, round(sum(revenue), 0) FROM shop.orders_big
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01' GROUP BY region;
```

```text
 Finalize GroupAggregate (actual time=171.029..179.892 rows=5 loops=1)
   ...
   ->  Parallel Bitmap Heap Scan on orders_big (actual time=9.124..90.499 rows=133284 loops=3)
         Recheck Cond: ((order_date >= '2024-01-01'::date) AND (order_date < '2025-01-01'::date))
         ->  Bitmap Index Scan on idx_orders_big_date (actual time=34.253..34.254 rows=399851 loops=1)
```

It uses the **date index**, but a year is about 400,000 rows (20% of the table) that still have to be read and summed. Indexes make *finding* rows fast; they don't make *reading lots of rows* free. Large aggregations like this are what analytical (columnar) databases and pre-aggregated warehouse tables are for: the next module.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does "Rows Removed by Filter: 666340" in a Seq Scan tell you?

1. Rows were deleted
2. The database read many rows only to throw them away, so an index might help
3. The query failed

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why might PostgreSQL ignore an index on `status` for `WHERE status = 'Delivered'`?

1. The index is broken
2. 90% of rows match, so reading the whole table is cheaper
3. Text columns can't be indexed

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which WHERE clause can use an index on `order_date`?

1. `WHERE date_trunc('month', order_date) = '2025-03-01'`
2. `WHERE order_date >= '2025-03-01' AND order_date < '2025-04-01'`
3. Both equally

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- `EXPLAIN ANALYZE` shows the real plan: read from the inside out, and look at scan types, rows and times.
- Indexes make **selective** lookups fast (145 → 7 ms); composite indexes serve combined filters (equality columns first).
- The planner skips indexes for low-selectivity filters, and can't use them through functions: write ranges.
- Indexes cost storage and write time; measure before and after, and index for real queries.

!!! job "Job-ready check"
    **Interview question:** *"A query on a large table is slow. How do you investigate?"*

    **Strong answer:** "I run EXPLAIN ANALYZE to see the actual plan: whether it's a sequential scan discarding most rows, a bad join order, or a misestimate between planned and actual rows. Then I check the WHERE and JOIN columns for missing or unusable indexes, such as functions on indexed columns or the wrong composite order, add or fix an index, refresh statistics, and compare the plan and timing again. If it's a big aggregation, I consider a summary table or a columnar warehouse instead."

    **Mini project:** On `shop.orders_big`, find the three queries your pipeline would run most (by customer, by date range, by customer and date). Index for them, record before/after execution times in a table, and check the total index size.
