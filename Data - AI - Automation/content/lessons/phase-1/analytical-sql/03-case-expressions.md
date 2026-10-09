---
title: "SQL CASE: Add If-Then Logic to Your Queries"
order: 3
summary: "Label rows, build categories and split one total into several columns, using SQL's version of IF."
level: Beginner
time: "35 min"
topics: ["CASE expressions"]
prerequisites: ["phase-1/analytical-sql/02-order-group-by"]
keywords: [case, when, then, else, end, if, conditional, bucket, band, segment, conditional aggregation, pivot, sql]
reviewed: 2026-10-09
resources:
  - title: "Conditional Expressions (CASE)"
    url: "https://www.postgresql.org/docs/current/functions-conditional.html"
    source: "PostgreSQL official docs"
    note: "Both CASE forms, explained with short examples."
  - title: "SQLBolt — Lesson 9 (queries with expressions)"
    url: "https://sqlbolt.com/lesson/select_queries_with_expressions"
    source: "SQLBolt"
    note: "Practice calculated columns, the foundation for CASE."
  - title: "Select Star SQL"
    url: "https://selectstarsql.com/"
    source: "Free interactive book"
    note: "Uses CASE inside aggregations on a real dataset."
files: [orders.sql, sql-solutions.sql]
---

## What is it?

`CASE` lets a query make decisions: *if this is true, show that; otherwise show something else*. It is SQL's version of the `IF` function in Excel.

You use it to **label** rows (for example "Large" / "Small"), to **group** rows into categories you invent, and to **split** a total into separate columns (for example delivered revenue vs open revenue).

!!! job "Why it matters at work"
    Business rules rarely match the raw data. "Large order", "on time", "high-value customer": these labels don't exist in the table. Analysts create them with `CASE`. Reports that show several statuses side by side, called **conditional aggregation**, are a favourite interview task.

## The syntax

```sql
CASE
    WHEN condition_1 THEN result_1
    WHEN condition_2 THEN result_2
    ELSE result_if_nothing_matched
END
```

- SQL checks the `WHEN` lines **from top to bottom** and stops at the **first** true one.
- `ELSE` is optional. Without it, rows that match nothing get `NULL`.
- Always finish with `END`, and usually name the result with `AS`.

## Example 1: label every order by size

*Question: classify each order as Large (1,000 or more), Medium (500 or more) or Small.*

```sql
SELECT order_id,
       customer,
       quantity * unit_price AS order_value,
       CASE
           WHEN quantity * unit_price >= 1000 THEN 'Large'
           WHEN quantity * unit_price >= 500  THEN 'Medium'
           ELSE 'Small'
       END AS size_band
FROM orders
ORDER BY order_id;
```

| order_id | customer | order_value | size_band |
|---|---|---|---|
| 1 | Rahim Traders | 420.00 | Small |
| 2 | Karim Garments | 200.00 | Small |
| 3 | Nova Apparel | 1560.00 | Large |
| 4 | Rahim Traders | 240.00 | Small |
| 5 | Delta Knit | 1260.00 | Large |
| 6 | Karim Garments | 680.00 | Medium |
| 7 | Nova Apparel | 320.00 | Small |
| 8 | Delta Knit | 1260.00 | Large |
| 9 | Sun Fashion | 810.00 | Medium |
| 10 | Rahim Traders | 870.00 | Medium |
| 11 | Sun Fashion | 420.00 | Small |
| 12 | Karim Garments | 1275.00 | Large |

Order 3 (1560.00) is also `>= 500`, but it gets "Large" because the first true `WHEN` wins.

!!! mistake "Order matters"
    Put the strictest condition first. If `>= 500` came before `>= 1000`, every big order would match `>= 500` first and be labelled "Medium". No order would ever be "Large".

## Example 2: the short form for exact matches

When you compare **one column** with fixed values, a shorter form works:

```sql
SELECT order_id, status,
       CASE status
           WHEN 'Delivered' THEN 'Closed'
           WHEN 'Cancelled' THEN 'Closed'
           ELSE 'Open'
       END AS stage
FROM orders
WHERE region = 'Dhaka';
```

| order_id | status | stage |
|---|---|---|
| 1 | Delivered | Closed |
| 3 | Delivered | Closed |
| 4 | Cancelled | Closed |
| 7 | Shipped | Open |
| 10 | Delivered | Closed |

The short form only checks equality. For ranges (`>=`) or several columns, use the full form from Example 1.

## Example 3: group by your own categories

*Question: how many orders, and how much revenue, fall in each size band? Exclude cancelled orders.*

```sql
SELECT CASE
           WHEN quantity * unit_price >= 1000 THEN 'Large'
           WHEN quantity * unit_price >= 500  THEN 'Medium'
           ELSE 'Small'
       END AS size_band,
       COUNT(*)                   AS orders,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY size_band
ORDER BY revenue DESC;
```

| size_band | orders | revenue |
|---|---|---|
| Large | 4 | 5355.00 |
| Medium | 3 | 2360.00 |
| Small | 4 | 1360.00 |

The three bands add up to 11 orders and 9,075. Those are the same totals as the headline numbers in the previous lesson, which is a good check that no rows were lost.

!!! note "Grouping by an alias"
    `GROUP BY size_band` works in SQLite, PostgreSQL, MySQL and BigQuery. SQL Server does not allow it, so there you repeat the whole `CASE ... END` in the `GROUP BY`.

## Example 4: conditional aggregation (one total → several columns)

*Question: for each region, show delivered revenue, open revenue (Shipped or Pending) and the number of cancelled orders, side by side.*

```sql
SELECT region,
       SUM(CASE WHEN status = 'Delivered'
                THEN quantity * unit_price ELSE 0 END)           AS delivered_revenue,
       SUM(CASE WHEN status IN ('Shipped', 'Pending')
                THEN quantity * unit_price ELSE 0 END)           AS open_revenue,
       SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)     AS cancelled_orders
FROM orders
GROUP BY region
ORDER BY delivered_revenue DESC;
```

| region | delivered_revenue | open_revenue | cancelled_orders |
|---|---|---|---|
| Dhaka | 2850.00 | 320.00 | 1 |
| Gazipur | 2520.00 | 0.00 | 0 |
| Chattogram | 880.00 | 1275.00 | 0 |
| Narayanganj | 420.00 | 810.00 | 0 |

**How it works:** for each row, the `CASE` returns the order value if the status matches, and `0` if it doesn't. `SUM` then adds only the matching values. `SUM(CASE ... THEN 1 ELSE 0 END)` counts rows that match.

This is how you build a "pivot table" in SQL. Chattogram has more open revenue than delivered revenue: a useful insight that a single revenue total would hide.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Looser condition first (`>= 500` before `>= 1000`) | Rows get the wrong label | Strictest condition first |
| Forgetting `END` | Syntax error | Every `CASE` needs `END` |
| No `ELSE` | Unmatched rows become `NULL` (e.g. orders 4 and 7 show `NULL` instead of "Open") | Add `ELSE` with a sensible default |
| `ELSE NULL` instead of `ELSE 0` inside `SUM` | Usually the same total, but a group with no matches shows `NULL` instead of `0` | Use `ELSE 0` for sums and counts |
| Mixing types (`THEN 'High' ELSE 0`) | Error in many databases | All results must be the same type |

## Try it yourself

**Task:** *"For each customer, show delivered revenue and in-progress revenue (Shipped or Pending) in two columns. Sort by delivered revenue, biggest first."*

<details markdown="1">
<summary>Show a hint</summary>

It's the same pattern as Example 4: two `SUM(CASE WHEN ... THEN quantity * unit_price ELSE 0 END)` columns, grouped by `customer`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT customer,
       SUM(CASE WHEN status = 'Delivered'
                THEN quantity * unit_price ELSE 0 END)   AS delivered,
       SUM(CASE WHEN status IN ('Shipped', 'Pending')
                THEN quantity * unit_price ELSE 0 END)   AS in_progress
FROM orders
GROUP BY customer
ORDER BY delivered DESC;
```

| customer | delivered | in_progress |
|---|---|---|
| Delta Knit | 2520.00 | 0.00 |
| Nova Apparel | 1560.00 | 320.00 |
| Rahim Traders | 1290.00 | 0.00 |
| Karim Garments | 880.00 | 1275.00 |
| Sun Fashion | 420.00 | 810.00 |

Karim Garments has more value in progress than delivered. Worth a follow-up call.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. An order is worth 1,200. Using the `CASE` from Example 1, which label does it get?

1. Large
2. Medium
3. Both

<details markdown="1"><summary>Show answer</summary>
**A — Large.** `CASE` stops at the first true `WHEN`, which is `>= 1000`.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)` calculate?

1. The value of cancelled orders
2. The number of cancelled orders
3. The share of cancelled orders

<details markdown="1"><summary>Show answer</summary>
**B.** Each cancelled row adds 1, and every other row adds 0, so the total is a count.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A `CASE` has no `ELSE` and a row matches none of the `WHEN`s. What is the result for that row?

1. 0
2. An empty text value
3. NULL

<details markdown="1"><summary>Show answer</summary>
**C — NULL.** Add an `ELSE` if you need a different default.
</details>
</div>

## Summary

- `CASE WHEN ... THEN ... ELSE ... END` adds if-then logic to any query.
- The **first** true `WHEN` wins, so put the strictest condition first.
- Use the result to label rows, or put it in `GROUP BY` to create your own categories.
- `SUM(CASE WHEN ... THEN value ELSE 0 END)` splits one total into several columns (conditional aggregation).

!!! job "Job-ready check"
    **Interview question:** *"Show revenue for each region with one column per order status."*

    **Strong answer:** "I'd group by region and use conditional aggregation: one `SUM(CASE WHEN status = '...' THEN amount ELSE 0 END)` per status. It needs only one pass over the table, and adding a status means adding one more column line."

    **Mini project:** Add a "Status Overview" query to your Monthly Sales Pack: delivered, open and cancelled values by category. Write one sentence on what stands out.
