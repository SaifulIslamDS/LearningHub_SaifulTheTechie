---
title: "SQL JOINs: Combine Data from Several Tables"
order: 4
summary: "Connect orders to customer details with INNER and LEFT JOIN, and find the records that have no match."
level: Beginner
time: "45 min"
topics: ["JOINs"]
prerequisites: ["phase-1/analytical-sql/02-order-group-by"]
keywords: [join, inner join, left join, right join, full outer join, "on", alias, anti join, foreign key, primary key, relationship, missing match]
reviewed: 2026-10-09
resources:
  - title: "SQLBolt — Lessons 6–7 (multi-table queries and OUTER JOINs)"
    url: "https://sqlbolt.com/lesson/select_queries_with_joins"
    source: "SQLBolt"
    note: "Interactive JOIN practice. Do lesson 7 (OUTER JOINs) next."
  - title: "Joins Between Tables"
    url: "https://www.postgresql.org/docs/current/tutorial-join.html"
    source: "PostgreSQL official docs"
    note: "A clear walk-through of inner and outer joins."
  - title: "Intro to SQL (includes a Joining Data lesson)"
    url: "https://www.kaggle.com/learn/intro-to-sql"
    source: "Kaggle Learn (free course)"
    note: "JOINs on real public datasets in BigQuery."
files: [orders.sql, customers.csv, sql-solutions.sql]
---

## What is it?

Real databases split information across several tables. Our `orders` table knows **what** was ordered. A second table, `customers`, knows **who** the customer is: segment, city and account manager. A `JOIN` combines the two, so one query can answer *"revenue by customer segment"*.

!!! tip "New practice table"
    This lesson uses a second table, `customers`. Run the latest [orders.sql](../../../downloads/orders.sql) again; it now creates both tables. Or download [customers.csv](../../../downloads/customers.csv).

| customer_id | customer_name | segment | city | account_manager |
|---|---|---|---|---|
| 1 | Rahim Traders | Trader | Dhaka | Anika |
| 2 | Karim Garments | Garment Factory | Chattogram | Tanvir |
| 3 | Nova Apparel | Garment Factory | Dhaka | Anika |
| 4 | Delta Knit | Knitting Mill | Gazipur | Tanvir |
| 5 | Sun Fashion | Garment Factory | Narayanganj | Anika |
| 6 | Blue Thread Ltd | Trader | Dhaka | Tanvir |

Blue Thread Ltd is a new customer with **no orders yet**. Keep an eye on it. It shows the difference between JOIN types.

!!! job "Why it matters at work"
    Every BI model, data warehouse and dashboard joins facts (orders, sales) to descriptions (customers, products, dates). Choosing the wrong JOIN quietly drops or duplicates rows, and that kind of error only shows up when the CFO's numbers don't match. Interviewers almost always ask *"What's the difference between INNER and LEFT JOIN?"*

## The syntax

```sql
SELECT o.order_id, c.segment
FROM orders AS o                       -- left table, nickname "o"
INNER JOIN customers AS c              -- right table, nickname "c"
        ON o.customer = c.customer_name;  -- how rows match
```

- `ON` says **which columns must match**.
- `AS o` and `AS c` are **table aliases**: short nicknames that keep queries readable. `o.order_id` means "order_id from orders".
- `JOIN` on its own means `INNER JOIN`.

!!! note "Matching on names vs IDs"
    Here we match on the customer name to keep things simple. Real databases match on an **ID** instead, e.g. `orders.customer_id = customers.customer_id`, because names can be misspelled or changed. You'll design tables like that in Phase 3.

## INNER JOIN: only rows that match in both tables

*Question: show each order with the customer's segment.*

```sql
SELECT o.order_id,
       o.customer,
       c.segment,
       o.quantity * o.unit_price AS order_value
FROM orders AS o
INNER JOIN customers AS c
        ON o.customer = c.customer_name
WHERE o.order_id <= 4
ORDER BY o.order_id;
```

| order_id | customer | segment | order_value |
|---|---|---|---|
| 1 | Rahim Traders | Trader | 420.00 |
| 2 | Karim Garments | Garment Factory | 200.00 |
| 3 | Nova Apparel | Garment Factory | 1560.00 |
| 4 | Rahim Traders | Trader | 240.00 |

*(First 4 orders shown. Without the `WHERE`, you get all 12.)*

Now the real business question: *revenue by segment.*

```sql
SELECT c.segment,
       COUNT(*)                       AS orders,
       SUM(o.quantity * o.unit_price) AS revenue
FROM orders AS o
JOIN customers AS c
  ON o.customer = c.customer_name
WHERE o.status <> 'Cancelled'
GROUP BY c.segment
ORDER BY revenue DESC;
```

| segment | orders | revenue |
|---|---|---|
| Garment Factory | 7 | 5265.00 |
| Knitting Mill | 2 | 2520.00 |
| Trader | 2 | 1290.00 |

Garment factories bring in more than half of all revenue (5,265 of 9,075).

## LEFT JOIN: keep every row from the left table

*Question: how many orders has each customer placed, including customers with none?*

```sql
SELECT c.customer_name,
       c.segment,
       COUNT(o.order_id) AS orders
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer = c.customer_name
GROUP BY c.customer_name, c.segment
ORDER BY orders DESC, c.customer_name;
```

| customer_name | segment | orders |
|---|---|---|
| Karim Garments | Garment Factory | 3 |
| Rahim Traders | Trader | 3 |
| Delta Knit | Knitting Mill | 2 |
| Nova Apparel | Garment Factory | 2 |
| Sun Fashion | Garment Factory | 2 |
| Blue Thread Ltd | Trader | 0 |

With an `INNER JOIN`, Blue Thread Ltd would **disappear**, because it has no matching order. `LEFT JOIN` keeps every customer and fills the missing order columns with `NULL`.

!!! tip "COUNT(column), not COUNT(*)"
    `COUNT(o.order_id)` counts only real orders, so Blue Thread gets 0. `COUNT(*)` counts rows, and the LEFT JOIN creates one row for Blue Thread, so it would wrongly show 1.

## Find what's missing (the "anti-join")

*Question: which customers have never ordered? Sales wants to call them.*

```sql
SELECT c.customer_name, c.account_manager
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer = c.customer_name
WHERE o.order_id IS NULL;
```

| customer_name | account_manager |
|---|---|
| Blue Thread Ltd | Tanvir |

`LEFT JOIN` + `WHERE right_table.column IS NULL` = "rows in the left table with **no** match". This pattern is used daily to find unbilled orders, inactive customers and missing data.

## The JOIN types at a glance

| JOIN | Keeps | Rows with our data |
|---|---|---|
| `INNER JOIN` | only matching rows | 12 (every order has a customer) |
| `LEFT JOIN` | all rows from the left table + matches | 13 when customers is on the left (12 orders + Blue Thread) |
| `RIGHT JOIN` | all rows from the right table + matches | the mirror of LEFT. Most people just swap the tables and use LEFT |
| `FULL OUTER JOIN` | all rows from both | not available in MySQL |

## The most common LEFT JOIN trap

*Question: count each customer's non-cancelled orders, keeping customers with none.*

This looks right, but it **removes Blue Thread Ltd**:

```sql
SELECT c.customer_name, COUNT(o.order_id) AS orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer = c.customer_name
WHERE o.status <> 'Cancelled'          -- ✗ filters out the NULL rows
GROUP BY c.customer_name;
```

Blue Thread's `status` is `NULL`, and `NULL <> 'Cancelled'` is not true, so `WHERE` drops it. The LEFT JOIN quietly turns into an INNER JOIN.

**Fix:** put conditions on the right table **in the `ON` clause**:

```sql
SELECT c.customer_name, COUNT(o.order_id) AS orders
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer = c.customer_name
      AND o.status <> 'Cancelled'      -- ✓ filter while joining
GROUP BY c.customer_name
ORDER BY c.customer_name;
```

| customer_name | orders |
|---|---|
| Blue Thread Ltd | 0 |
| Delta Knit | 2 |
| Karim Garments | 3 |
| Nova Apparel | 2 |
| Rahim Traders | 2 |
| Sun Fashion | 2 |

Rahim Traders now shows 2, because its cancelled order is excluded, and Blue Thread is back.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `INNER JOIN` when you need every customer | Customers without orders vanish | `LEFT JOIN` from the table you must keep |
| Filtering the right table in `WHERE` after a LEFT JOIN | LEFT JOIN behaves like INNER JOIN | Move the condition into `ON` |
| `COUNT(*)` after a LEFT JOIN | Customers with no orders count as 1 | `COUNT(right_table.id)` |
| Ambiguous column (`SELECT customer_id` when both tables have it) | Error | Prefix with the alias: `c.customer_id` |
| Joining on a column that isn't unique | Rows multiply and totals are too high | Check that the lookup table has one row per key |

## Try it yourself

**Task:** *"Show non-cancelled revenue and order count for each account manager."*

<details markdown="1">
<summary>Show a hint</summary>

`account_manager` lives in `customers`, and the values live in `orders`. Join them, filter out cancelled orders, and group by the manager.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT c.account_manager,
       COUNT(*)                       AS orders,
       SUM(o.quantity * o.unit_price) AS revenue
FROM orders AS o
JOIN customers AS c
  ON o.customer = c.customer_name
WHERE o.status <> 'Cancelled'
GROUP BY c.account_manager
ORDER BY revenue DESC;
```

| account_manager | orders | revenue |
|---|---|---|
| Tanvir | 5 | 4675.00 |
| Anika | 6 | 4400.00 |

Anika handles more orders, but Tanvir's bring in more revenue. Tanvir also owns Blue Thread Ltd, the customer with no orders yet.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. You `INNER JOIN` customers to orders. Does Blue Thread Ltd (no orders) appear?

1. Yes, with NULL values
2. No
3. Yes, with 0 orders

<details markdown="1"><summary>Show answer</summary>
**B — No.** `INNER JOIN` keeps only rows that match in both tables. Use `LEFT JOIN` from customers to keep it.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which query pattern finds customers who have never ordered?

1. `INNER JOIN ... WHERE o.order_id IS NULL`
2. `LEFT JOIN ... WHERE o.order_id IS NULL`
3. `LEFT JOIN ... WHERE o.order_id IS NOT NULL`

<details markdown="1"><summary>Show answer</summary>
**B.** The LEFT JOIN keeps unmatched customers with `NULL` order columns, and the `WHERE` keeps only those.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. After a `LEFT JOIN` from customers to orders, you add `WHERE o.status = 'Delivered'`. What happens to customers with no orders?

1. They stay, with NULLs
2. They are removed
3. The query errors

<details markdown="1"><summary>Show answer</summary>
**B — removed.** Their `status` is `NULL`, so the `WHERE` condition is not true. Put the condition in `ON` to keep them.
</details>
</div>

## Summary

- A `JOIN` combines tables by matching columns in the `ON` clause. Use aliases (`o`, `c`) to keep it readable.
- `INNER JOIN` keeps only matches. `LEFT JOIN` keeps every row from the left table.
- `LEFT JOIN ... WHERE right.id IS NULL` finds rows with **no** match.
- Filter the right table in `ON`, not `WHERE`, when you need to keep unmatched rows.
- Count with `COUNT(right.id)` after a LEFT JOIN.

!!! job "Job-ready check"
    **Interview question:** *"Explain INNER JOIN vs LEFT JOIN, with a business example."*

    **Strong answer:** "INNER JOIN returns only customers who have orders. LEFT JOIN returns all customers, with NULLs where there's no order. That's how I'd find inactive customers: LEFT JOIN, then `WHERE order_id IS NULL`. I'd also compare row counts before and after a join, to catch rows that were dropped or duplicated."

    **Mini project:** Add two queries to your Sales Pack: revenue by segment, and a list of customers with no orders in the last 30 days, with their account manager. Note how you checked the row counts.
