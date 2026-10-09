---
title: "SQL Subqueries: Use One Query's Answer Inside Another"
order: 5
summary: "Compare against averages, filter by a list from another table, and build totals-of-totals — with subqueries and a first look at CTEs."
level: Beginner–Intermediate
time: "40 min"
topics: ["Subqueries"]
prerequisites: ["phase-1/analytical-sql/04-joins"]
keywords: [subquery, nested query, in, exists, not exists, derived table, cte, with, average, above average, not in null]
reviewed: 2026-10-09
resources:
  - title: "SQLBolt — SQL Topic: Subqueries"
    url: "https://sqlbolt.com/topic/subqueries"
    source: "SQLBolt"
    note: "A short intro to the different kinds of subqueries."
  - title: "Subquery Expressions"
    url: "https://www.postgresql.org/docs/current/functions-subquery.html"
    source: "PostgreSQL official docs"
    note: "Reference for EXISTS, IN, NOT IN and comparisons with subqueries."
  - title: "WITH Queries (Common Table Expressions)"
    url: "https://www.postgresql.org/docs/current/queries-with.html"
    source: "PostgreSQL official docs"
    note: "Read the first section for the basics of CTEs."
  - title: "Select Star SQL"
    url: "https://selectstarsql.com/"
    source: "Free interactive book"
    note: "Uses subqueries for real analytical questions."
files: [orders.sql, customers.csv, sql-solutions.sql]
---

## What is it?

A **subquery** is a query inside another query, written in brackets. The inner query runs first, and its answer is used by the outer query.

You need one when a question has two steps, like *"Which orders are **above average**?"* First you calculate the average, then you compare each order with it. A subquery does both steps in one statement.

!!! job "Why it matters at work"
    "Above average", "customers in segment X", "customers who never ordered", "average of the customer totals": these two-step questions come up in every analytics job. Subqueries and their cleaner cousin, the **CTE**, are standard interview topics, and they lead into Advanced SQL in Phase 3.

## Where a subquery can go

| Position | Returns | Typical use |
|---|---|---|
| In `WHERE` with `>`, `=`, `<` | one value | compare with an average or maximum |
| In `WHERE ... IN (...)` | a list | filter by values from another table |
| In `FROM (...) AS name` | a whole table | aggregate the results of an aggregation |
| `WHERE EXISTS (...)` | true / false | check whether related rows exist |

## Example 1: compare with an average (single value)

*Question: which non-cancelled orders are above the average order value?*

```sql
SELECT order_id,
       customer,
       quantity * unit_price AS order_value
FROM orders
WHERE status <> 'Cancelled'
  AND quantity * unit_price > (
        SELECT AVG(quantity * unit_price)
        FROM orders
        WHERE status <> 'Cancelled'
      )
ORDER BY order_value DESC, order_id;
```

The inner query returns **825.00**, the average from the earlier lesson. The outer query keeps orders above it:

| order_id | customer | order_value |
|---|---|---|
| 3 | Nova Apparel | 1560.00 |
| 12 | Karim Garments | 1275.00 |
| 5 | Delta Knit | 1260.00 |
| 8 | Delta Knit | 1260.00 |
| 10 | Rahim Traders | 870.00 |

!!! tip "Why not just `WHERE value > AVG(value)`?"
    Aggregates such as `AVG` aren't allowed in `WHERE`, because `WHERE` runs before any grouping. The subquery calculates the average separately, so the comparison works.

## Example 2: filter by a list from another table (IN)

*Question: show all orders from Garment Factory customers.*

```sql
SELECT order_id, customer, product
FROM orders
WHERE customer IN (
        SELECT customer_name
        FROM customers
        WHERE segment = 'Garment Factory'
      )
ORDER BY order_id;
```

| order_id | customer | product |
|---|---|---|
| 2 | Karim Garments | Metal Buttons |
| 3 | Nova Apparel | Denim 12oz |
| 6 | Karim Garments | Cotton Twill |
| 7 | Nova Apparel | Metal Buttons |
| 9 | Sun Fashion | Denim 12oz |
| 11 | Sun Fashion | Zippers |
| 12 | Karim Garments | Denim 12oz |

The inner query returns the list *Karim Garments, Nova Apparel, Sun Fashion*. A JOIN could give the same result. Use `IN` when you only **filter** by the other table and don't need its columns.

## Example 3: a subquery in FROM (totals of totals)

*Question: what is the average revenue per customer, and what is the top customer's revenue?*

You can't nest aggregates like `AVG(SUM(...))`. Instead, build a small table of customer totals first, then aggregate it:

```sql
SELECT ROUND(AVG(revenue), 2) AS avg_revenue_per_customer,
       MAX(revenue)           AS top_customer_revenue
FROM (
        SELECT customer,
               SUM(quantity * unit_price) AS revenue
        FROM orders
        WHERE status <> 'Cancelled'
        GROUP BY customer
     ) AS customer_totals;
```

| avg_revenue_per_customer | top_customer_revenue |
|---|---|
| 1815.00 | 2520.00 |

The inner query is a **derived table**. It must have a name (`AS customer_totals`) in most databases.

## Example 4: EXISTS and NOT EXISTS

*Question: which customers have never ordered?* (You solved this with a LEFT JOIN in the previous lesson. Here is another way.)

```sql
SELECT customer_name
FROM customers AS c
WHERE NOT EXISTS (
        SELECT 1
        FROM orders AS o
        WHERE o.customer = c.customer_name
      );
```

| customer_name |
|---|
| Blue Thread Ltd |

This is a **correlated** subquery: it refers to `c` from the outer query, so it is checked once for each customer. `SELECT 1` is a convention, because `EXISTS` only cares whether any row exists.

!!! mistake "The NOT IN trap"
    `WHERE customer_name NOT IN (SELECT customer FROM orders)` gives the right answer here. But if the inner list ever contains a `NULL`, `NOT IN` returns **no rows at all**, with no error. `NOT EXISTS` doesn't have this problem, so prefer it.

## A cleaner way: CTEs (WITH)

Nested brackets get hard to read. A **CTE** (Common Table Expression) gives the inner query a name **at the top**:

```sql
WITH customer_totals AS (
    SELECT customer,
           SUM(quantity * unit_price) AS revenue
    FROM orders
    WHERE status <> 'Cancelled'
    GROUP BY customer
)
SELECT customer, revenue
FROM customer_totals
WHERE revenue > (SELECT AVG(revenue) FROM customer_totals)
ORDER BY revenue DESC;
```

| customer | revenue |
|---|---|
| Delta Knit | 2520.00 |
| Karim Garments | 2155.00 |
| Nova Apparel | 1880.00 |

The query reads top to bottom: *build customer totals → keep the ones above average*. CTEs are covered in depth in Phase 3 (Advanced SQL). Most analysts prefer them for anything with more than one step.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `WHERE value > AVG(value)` | Error: aggregates aren't allowed in `WHERE` | Calculate the average in a subquery |
| A subquery after `=` returns several rows | Error ("more than one row") | Use `IN`, or make the subquery return one value |
| No name for a subquery in `FROM` | Error in most databases | Add `AS some_name` |
| `NOT IN` with a list that contains `NULL` | Returns no rows, silently | Use `NOT EXISTS` |
| Three levels of nested brackets | Hard to read and debug | Rewrite as a CTE |

## Try it yourself

**Task:** *"Which customers have total (non-cancelled) revenue above the average customer revenue?"* Write it **with a subquery**, not a CTE.

<details markdown="1">
<summary>Show a hint</summary>

Group orders by customer, then use `HAVING SUM(...) > (subquery)`. The subquery itself needs a derived table of customer totals (Example 3) to calculate their average.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT customer,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY customer
HAVING SUM(quantity * unit_price) > (
        SELECT AVG(revenue)
        FROM (
               SELECT customer, SUM(quantity * unit_price) AS revenue
               FROM orders
               WHERE status <> 'Cancelled'
               GROUP BY customer
             ) AS t
      )
ORDER BY revenue DESC;
```

| customer | revenue |
|---|---|
| Delta Knit | 2520.00 |
| Karim Garments | 2155.00 |
| Nova Apparel | 1880.00 |

The average customer revenue is 1,815. Compare this with the CTE version: same result, much easier to read.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Why can't you write `WHERE quantity * unit_price > AVG(quantity * unit_price)`?

1. AVG doesn't work on calculated values
2. Aggregates aren't allowed in WHERE
3. You need DISTINCT first

<details markdown="1"><summary>Show answer</summary>
**B.** `WHERE` filters single rows before any aggregation. Calculate the average in a subquery instead.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which is safest for "customers who never ordered" when the orders table may contain NULL customer values?

1. `NOT IN (subquery)`
2. `NOT EXISTS (subquery)`
3. `<> ANY (subquery)`

<details markdown="1"><summary>Show answer</summary>
**B — NOT EXISTS.** `NOT IN` returns nothing if the list contains a NULL.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What is the main benefit of a CTE (`WITH ...`) over a nested subquery?

1. It is always faster
2. It is easier to read, and you can reuse its name in the query
3. It works without SELECT

<details markdown="1"><summary>Show answer</summary>
**B.** CTEs name each step so the query reads top to bottom. Speed is usually similar.
</details>
</div>

## Summary

- A subquery is a query in brackets whose answer feeds the outer query.
- **One value** → compare with `>`, `=`. **A list** → `IN`. **A table** → `FROM (...) AS name`.
- `EXISTS` / `NOT EXISTS` check whether related rows exist. Prefer `NOT EXISTS` over `NOT IN`.
- For multi-step logic, a **CTE** (`WITH name AS (...)`) is clearer than nesting.

!!! job "Job-ready check"
    **Interview question:** *"Find customers whose revenue is above the average customer revenue."*

    **Strong answer:** "First I build customer totals, then compare each total with their average. I'd write it as a CTE, `WITH customer_totals AS (...)`, then select from it with `WHERE revenue > (SELECT AVG(revenue) FROM customer_totals)`. That keeps each step readable and testable."

    **Mini project:** Finish your **Monthly Sales Pack** with an "Above-average customers" section written as a CTE. Put the whole pack, five or more queries with comments, into a GitHub repository with a README that states each business question and its answer. That is your first SQL portfolio piece.
