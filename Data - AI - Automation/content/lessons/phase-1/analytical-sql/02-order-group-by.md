---
title: "Sort and Summarise: ORDER BY, GROUP BY & HAVING"
order: 2
summary: "Rank results, calculate totals and averages, and build the revenue-by-region tables behind every sales dashboard."
level: Beginner
time: "40 min"
topics: ["ORDER BY & LIMIT", "GROUP BY & aggregation"]
prerequisites: ["phase-1/analytical-sql/01-select-where"]
keywords: [order by, limit, top n, group by, having, count, sum, avg, min, max, aggregate, distinct, kpi, revenue]
reviewed: 2026-10-09
resources:
  - title: "SQLBolt — Lessons 10–12 (aggregates and query order)"
    url: "https://sqlbolt.com/"
    source: "SQLBolt"
    note: "Interactive practice of GROUP BY and HAVING."
  - title: "Aggregate Functions"
    url: "https://www.postgresql.org/docs/current/tutorial-agg.html"
    source: "PostgreSQL official docs"
    note: "A clear explanation of WHERE vs HAVING."
  - title: "Select Star SQL"
    url: "https://selectstarsql.com/"
    source: "Free interactive book"
    note: "The aggregation chapters use a real dataset."
files: [orders.sql, orders.csv, sql-solutions.sql]
---

## What is it?

So far every query has returned one row for each order. Managers rarely want that. They want **summaries** (*"total revenue by region"*) and **rankings** (*"our top 3 orders"*).

- `ORDER BY` **sorts** the result. `LIMIT` keeps only the first *n* rows.
- `GROUP BY` **collapses** many rows into one row per group.
- **Aggregate functions** such as `SUM` and `COUNT` calculate a value for each group.
- `HAVING` **filters groups** after they are calculated.

!!! job "Why it matters at work"
    Every KPI on a dashboard is an aggregate: revenue, order count, average order value. The tables behind Power BI reports and the "top 10" lists in management packs are `GROUP BY` queries. Interviewers test this more than any other SQL topic, especially **WHERE vs HAVING**.

## ORDER BY and LIMIT: rank your results

*Question: what are our 3 biggest orders by value?*

```sql
SELECT order_id,
       customer,
       quantity * unit_price AS order_value
FROM orders
ORDER BY order_value DESC, order_id
LIMIT 3;
```

| order_id | customer | order_value |
|---|---|---|
| 3 | Nova Apparel | 1560.00 |
| 12 | Karim Garments | 1275.00 |
| 5 | Delta Knit | 1260.00 |

- `ASC` (the default) sorts smallest to largest, or A to Z. `DESC` sorts largest to smallest.
- You **can** use an alias (`order_value`) in `ORDER BY`, because sorting happens after `SELECT`.
- Sort by several columns, such as `ORDER BY region, customer`. The second column breaks ties in the first.
- Orders 5 and 8 are both worth 1260.00. Without the tie-breaker `order_id`, different databases may return either one as the third row. Always add a tie-breaker to a "top n" query.

!!! note "LIMIT is not universal"
    `LIMIT` works in SQLite, PostgreSQL, MySQL, BigQuery and Snowflake. SQL Server uses `SELECT TOP 3 ...` instead, and the standard form is `FETCH FIRST 3 ROWS ONLY`. The idea is the same in each.

## Aggregate functions

| Function | Returns | Example |
|---|---|---|
| `COUNT(*)` | number of rows | how many orders |
| `COUNT(DISTINCT col)` | number of different values | how many customers |
| `SUM(expr)` | total | revenue |
| `AVG(expr)` | average | average order value |
| `MIN(expr)` / `MAX(expr)` | smallest / largest | first and last order date |

*Question: give me the headline numbers for all orders that were not cancelled.*

```sql
SELECT COUNT(*)                   AS orders,
       SUM(quantity * unit_price) AS revenue,
       AVG(quantity * unit_price) AS avg_order,
       MIN(order_date)            AS first_order,
       MAX(order_date)            AS last_order
FROM orders
WHERE status <> 'Cancelled';
```

| orders | revenue | avg_order | first_order | last_order |
|---|---|---|---|---|
| 11 | 9075.00 | 825.00 | 2026-01-05 | 2026-03-09 |

Without `GROUP BY`, the whole filtered table becomes **one group**, so you get one row.

!!! tip "Long decimals in your results?"
    Some databases (SQLite, for example) store prices as floating-point numbers, so a total can show a long tail of decimals. Wrap the result in `ROUND(..., 2)`, for example `ROUND(SUM(quantity * unit_price), 2)`. For real money in production tables, use the `DECIMAL`/`NUMERIC` type.

## GROUP BY: one row per group

*Question: how much revenue did each region bring in?*

```sql
SELECT region,
       COUNT(*)                   AS orders,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY region
ORDER BY revenue DESC;
```

| region | orders | revenue |
|---|---|---|
| Dhaka | 4 | 3170.00 |
| Gazipur | 2 | 2520.00 |
| Chattogram | 3 | 2155.00 |
| Narayanganj | 2 | 1230.00 |

**How it works:** the database removes cancelled rows (`WHERE`), puts the remaining rows into one bucket per region (`GROUP BY`), calculates `COUNT` and `SUM` for each bucket, and then sorts the buckets (`ORDER BY`).

!!! mistake "The golden rule of GROUP BY"
    Every column in `SELECT` must be **either** in the `GROUP BY` **or** inside an aggregate function.

    `SELECT region, customer, SUM(...) ... GROUP BY region` is an error in most databases. Each region has several customers, so which one should the database show? Either add `customer` to the `GROUP BY` or remove it from the `SELECT`.

## HAVING: filter the groups

*Question: which customers bought more than 1,500 in total (excluding cancellations)?*

```sql
SELECT customer,
       COUNT(*)                   AS orders,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY customer
HAVING SUM(quantity * unit_price) > 1500
ORDER BY revenue DESC;
```

| customer | orders | revenue |
|---|---|---|
| Delta Knit | 2 | 2520.00 |
| Karim Garments | 3 | 2155.00 |
| Nova Apparel | 2 | 1880.00 |

Rahim Traders (1290) and Sun Fashion (1230) are left out by `HAVING`.

### WHERE vs HAVING

| | `WHERE` | `HAVING` |
|---|---|---|
| Filters | individual **rows** | finished **groups** |
| Runs | before grouping | after grouping |
| Can use `SUM`, `COUNT`… | No | Yes |
| Example | `status <> 'Cancelled'` | `SUM(...) > 1500` |

Rule of thumb: if the condition is about **one order**, use `WHERE`. If it is about a **total**, use `HAVING`.

## The order SQL runs a query

You **write** a query in one order, but the database **runs** it in another. Knowing this order explains most SQL errors.

| Step | Clause | What happens |
|---|---|---|
| 1 | `FROM` | pick the table |
| 2 | `WHERE` | keep matching rows |
| 3 | `GROUP BY` | form groups |
| 4 | `HAVING` | keep matching groups |
| 5 | `SELECT` | calculate columns and aliases |
| 6 | `ORDER BY` | sort |
| 7 | `LIMIT` | cut to *n* rows |

This is why an alias works in `ORDER BY` (step 6, after `SELECT`) but not in `WHERE` (step 2, before `SELECT`).

## Try it yourself

**Task:** *"For **delivered** orders only, show each region's number of orders and total revenue. List only regions with revenue above 2,000, biggest first."*

<details markdown="1">
<summary>Show a hint</summary>

The "delivered only" condition is about single orders, so it goes in `WHERE`. "Revenue above 2,000" is about a total, so it goes in `HAVING`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT region,
       COUNT(*)                             AS orders,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY region
HAVING SUM(quantity * unit_price) > 2000
ORDER BY revenue DESC;
```

| region | orders | revenue |
|---|---|---|
| Dhaka | 3 | 2850.00 |
| Gazipur | 2 | 2520.00 |

Dhaka now has 3 orders, not 4: order 7 is *Shipped*, not *Delivered*.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. You want regions whose **total** revenue is above 2,000. Where does that condition go?

1. `WHERE`
2. `HAVING`
3. `ORDER BY`

<details markdown="1"><summary>Show answer</summary>
**B — `HAVING`.** The condition is about a group total, which only exists after `GROUP BY`.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `SELECT COUNT(DISTINCT customer) FROM orders;` return for the practice table?

1. 5
2. 11
3. 12

<details markdown="1"><summary>Show answer</summary>
**A — 5.** There are 12 orders but only 5 different customers.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why does `SELECT region, customer, SUM(quantity) FROM orders GROUP BY region;` fail in most databases?

1. `SUM` cannot be used with `GROUP BY`
2. `customer` is neither grouped nor aggregated
3. `region` must be sorted first

<details markdown="1"><summary>Show answer</summary>
**B.** Each region has several customers, so the database cannot pick one. Add `customer` to `GROUP BY` or remove it from `SELECT`.
</details>
</div>

## Summary

- `ORDER BY ... DESC` + `LIMIT n` gives a "top n" list.
- `COUNT`, `SUM`, `AVG`, `MIN` and `MAX` turn many rows into one number.
- `GROUP BY` gives one result row per group. Every selected column must be grouped or aggregated.
- `WHERE` filters rows **before** grouping, and `HAVING` filters groups **after**.
- SQL runs `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

!!! job "Job-ready check"
    **Interview question:** *"Explain the difference between WHERE and HAVING, with an example."*

    **Strong answer:** `WHERE` filters individual rows before grouping, for example removing cancelled orders. `HAVING` filters groups after aggregation, for example keeping only customers whose total revenue is above 1,500. Row-level conditions belong in `WHERE`, because filtering early means less data to group.

    **Mini project:** Build a small "Monthly Sales Pack": revenue by region, revenue by category, and the top 3 customers. Save the three queries in one `.sql` file and paste the results into a one-page summary with two sentences of insight per table. This becomes a piece of evidence for your portfolio.
