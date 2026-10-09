---
title: "SQL SELECT & WHERE: Get Exactly the Rows You Need"
order: 1
summary: "Pick the columns you want, filter the rows you need, and calculate new values — the base of every SQL query."
level: Beginner
time: "30 min"
topics: ["SELECT & WHERE"]
keywords: [select, where, from, filter, and, or, in, between, like, alias, as, computed column, sql basics]
reviewed: 2026-10-08
resources:
  - title: "SQLBolt — Lessons 1–4 (SELECT and filtering)"
    url: "https://sqlbolt.com/"
    source: "SQLBolt"
    note: "Short interactive exercises in the browser. Do lessons 1–4 after this page."
  - title: "Querying a Table"
    url: "https://www.postgresql.org/docs/current/tutorial-select.html"
    source: "PostgreSQL official docs"
    note: "The official explanation of SELECT and WHERE, with examples."
  - title: "Select Star SQL"
    url: "https://selectstarsql.com/"
    source: "Free interactive book"
    note: "Practise on a real dataset. Read chapter 1."
  - title: "Intro to SQL"
    url: "https://www.kaggle.com/learn/intro-to-sql"
    source: "Kaggle Learn (free course)"
    note: "Uses Google BigQuery on public datasets — good for practising on bigger tables."
files: [orders.sql, orders.csv, sql-solutions.sql]
---

## What is it?

`SELECT` tells the database **which columns** you want to see. `WHERE` tells it **which rows** to keep. Together they answer the most common question at work: *"Show me only the data I care about."*

Think of a spreadsheet with a filter: `SELECT` hides the columns you don't need, and `WHERE` is the filter on the rows.

!!! job "Why it matters at work"
    Almost every report, dashboard and data pipeline starts with a `SELECT ... WHERE` query. Data analyst and BI job interviews almost always open with questions like *"List all cancelled orders from last month."* If this feels easy, everything later in SQL gets easier.

## The practice table

Every example uses the `orders` table — 12 orders from a wholesale supplier. Load it using the steps on the [module page](index.html), or download [orders.sql](../../../downloads/orders.sql).

| order_id | order_date | customer | region | category | product | quantity | unit_price | status |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-01-05 | Rahim Traders | Dhaka | Fabric | Cotton Twill | 120 | 3.50 | Delivered |
| 2 | 2026-01-08 | Karim Garments | Chattogram | Trims | Metal Buttons | 5000 | 0.04 | Delivered |
| 3 | 2026-01-12 | Nova Apparel | Dhaka | Fabric | Denim 12oz | 300 | 5.20 | Delivered |
| 4 | 2026-01-15 | Rahim Traders | Dhaka | Trims | Zippers | 800 | 0.30 | Cancelled |
| … | … | … | … | … | … | … | … | … |

*(4 of 12 rows shown.)*

## The syntax

```sql
SELECT column1, column2      -- 1. which columns
FROM   table_name            -- 2. which table
WHERE  condition;            -- 3. which rows (optional)
```

- Write keywords like `SELECT` in capitals. SQL doesn't require this, but it makes queries easier to read.
- Text values go in **single quotes**: `'Dhaka'`. Numbers don't: `200`.
- End each query with a semicolon `;`.

## Example 1: choose columns

```sql
SELECT customer, product, quantity
FROM orders;
```

This returns all 12 rows, but only 3 columns. The first rows look like this:

| customer | product | quantity |
|---|---|---|
| Rahim Traders | Cotton Twill | 120 |
| Karim Garments | Metal Buttons | 5000 |
| Nova Apparel | Denim 12oz | 300 |

!!! note "What about `SELECT *`?"
    `SELECT *` returns every column. It is fine for a quick look at a table, but in reports and pipelines always name the columns. Then your query won't break or slow down when someone adds new columns to the table.

## Example 2: filter rows with WHERE

*Question: which orders came from Dhaka?*

```sql
SELECT order_id, customer, product, status
FROM orders
WHERE region = 'Dhaka';
```

| order_id | customer | product | status |
|---|---|---|---|
| 1 | Rahim Traders | Cotton Twill | Delivered |
| 3 | Nova Apparel | Denim 12oz | Delivered |
| 4 | Rahim Traders | Zippers | Cancelled |
| 7 | Nova Apparel | Metal Buttons | Shipped |
| 10 | Rahim Traders | Cotton Yarn 30s | Delivered |

### Comparison operators

| Operator | Meaning | Example |
|---|---|---|
| `=` | equal to | `status = 'Shipped'` |
| `<>` or `!=` | not equal to | `status <> 'Cancelled'` |
| `>` `<` | greater / less than | `quantity > 500` |
| `>=` `<=` | greater / less than or equal | `unit_price <= 3` |

## Example 3: combine conditions with AND / OR

*Question: which Fabric orders had at least 200 units?*

```sql
SELECT order_id, customer, product, quantity
FROM orders
WHERE category = 'Fabric'
  AND quantity >= 200;
```

| order_id | customer | product | quantity |
|---|---|---|---|
| 3 | Nova Apparel | Denim 12oz | 300 |
| 6 | Karim Garments | Cotton Twill | 200 |
| 12 | Karim Garments | Denim 12oz | 250 |

- `AND`: **both** conditions must be true.
- `OR`: **at least one** must be true.

!!! mistake "Common trap: mixing AND and OR without brackets"
    *Question: delivered orders from Dhaka or Gazipur.* This looks right but is **wrong**:

    ```sql
    WHERE region = 'Dhaka' OR region = 'Gazipur' AND status = 'Delivered'
    ```

    SQL evaluates `AND` before `OR`. So this returns *all* Dhaka orders (including the cancelled and shipped ones), plus delivered Gazipur orders: **7 rows**. Add brackets to say what you mean:

    ```sql
    WHERE (region = 'Dhaka' OR region = 'Gazipur')
      AND status = 'Delivered'
    ```

    Now you get the correct **5 rows**: orders 1, 3, 5, 8 and 10.

## Example 4: IN, BETWEEN and LIKE

These shortcuts make filters shorter and easier to read.

```sql
-- IN: matches any value in a list
SELECT order_id, customer, status
FROM orders
WHERE status IN ('Shipped', 'Pending');
-- returns orders 7, 9, 12

-- BETWEEN: a range, both ends included
SELECT order_id, order_date, customer
FROM orders
WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28';
-- returns orders 6, 7, 8, 9, 10 (all of February)

-- LIKE: text patterns. % means "any characters"
SELECT order_id, product
FROM orders
WHERE product LIKE 'Cotton%';
-- returns Cotton Twill and Cotton Yarn 30s (orders 1, 5, 6, 10)
```

!!! note "Empty values: use IS NULL"
    A missing value in SQL is `NULL`. It is never equal to anything, not even another `NULL`. So `WHERE delivered_date = NULL` returns nothing. Write `WHERE delivered_date IS NULL` or `IS NOT NULL` instead. (Our practice table has no empty values, but real company data almost always does.)

## Example 5: calculated columns with AS

You can calculate new values in the `SELECT` and name them with `AS` (an *alias*).

*Question: what is the value of each Fabric order?*

```sql
SELECT order_id,
       customer,
       quantity * unit_price AS order_value
FROM orders
WHERE category = 'Fabric';
```

| order_id | customer | order_value |
|---|---|---|
| 1 | Rahim Traders | 420.00 |
| 3 | Nova Apparel | 1560.00 |
| 6 | Karim Garments | 680.00 |
| 9 | Sun Fashion | 810.00 |
| 12 | Karim Garments | 1275.00 |

This `quantity * unit_price` pattern returns in the next lesson, where you add up revenue.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `WHERE region = Dhaka` (no quotes) | Error: the database looks for a *column* named Dhaka | `'Dhaka'` |
| `WHERE region = "Dhaka"` | Works in some databases, fails in others (e.g. PostgreSQL) | Always use single quotes for text |
| `= NULL` | Returns no rows | `IS NULL` |
| `AND` + `OR` without brackets | Returns too many rows | Add brackets |
| Using an alias in `WHERE` (`WHERE order_value > 500`) | Error in most databases: `WHERE` runs before the `SELECT` names exist | Repeat the formula: `WHERE quantity * unit_price > 500` |

## Try it yourself

**Task:** The sales manager asks: *"Which Trims orders were **not** cancelled? Show the customer, the product and the order value."*

Write the query in your SQL tool, run it, and only then check the answer.

<details markdown="1">
<summary>Show a hint</summary>

You need two conditions joined with `AND`: one on `category` and one on `status` using `<>`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT customer,
       product,
       quantity * unit_price AS order_value
FROM orders
WHERE category = 'Trims'
  AND status <> 'Cancelled';
```

| customer | product | order_value |
|---|---|---|
| Karim Garments | Metal Buttons | 200.00 |
| Nova Apparel | Metal Buttons | 320.00 |
| Sun Fashion | Zippers | 420.00 |

Did you get 3 rows? Order 4 (cancelled zippers) must be missing.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which clause decides **which rows** are returned?

1. `SELECT`
2. `FROM`
3. `WHERE`

<details markdown="1"><summary>Show answer</summary>
**C — `WHERE`.** `SELECT` picks columns and `FROM` picks the table.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. How many rows does `WHERE status IN ('Shipped', 'Pending')` return from the practice table?

1. 2
2. 3
3. 5

<details markdown="1"><summary>Show answer</summary>
**B — 3 rows:** orders 7 and 12 (Shipped) and order 9 (Pending).
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which filter correctly finds rows where `discount` has no value?

1. `WHERE discount = NULL`
2. `WHERE discount IS NULL`
3. `WHERE discount = ''`

<details markdown="1"><summary>Show answer</summary>
**B.** `NULL` means "unknown", so it is never *equal* to anything. Use `IS NULL`. Option C checks for an empty text value, which is a different thing.
</details>
</div>

## Summary

- `SELECT` picks **columns**, `FROM` picks the **table**, `WHERE` picks **rows**.
- Combine conditions with `AND` / `OR`, and use **brackets** when you mix them.
- `IN`, `BETWEEN` and `LIKE` make filters shorter. Use `IS NULL` for missing values.
- `AS` names a calculated column, such as `quantity * unit_price AS order_value`.

!!! job "Job-ready check"
    **Interview question:** *"What is the difference between `WHERE status <> 'Cancelled'` and `WHERE status = 'Delivered'` on this table?"*

    **Strong answer:** The first keeps every order that isn't cancelled: Delivered, Shipped and Pending (11 rows). The second keeps only Delivered orders (8 rows). Which one is right depends on the business definition of a "sale", so ask the stakeholder before you build the report.

    **Mini project:** Write three filters a sales manager would use every week, such as "this month's pending orders". Save them in a `.sql` file with a comment above each query explaining the business question.
