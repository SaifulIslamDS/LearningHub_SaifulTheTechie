---
title: "Window Functions: Running Totals, Rankings, LAG & LEAD"
order: 2
summary: "Calculate across related rows without losing detail: shares of a group, running totals and moving averages, ROW_NUMBER vs RANK vs DENSE_RANK, top-N per group, and period-over-period growth with LAG and LEAD."
level: Intermediate
time: "55 min"
topics: ["Window functions", "RANK, LAG & LEAD"]
prerequisites: ["phase-3/advanced-sql/01-ctes-recursive"]
keywords: [window function, over, partition by, order by, window frame, rows between, running total, cumulative sum, moving average, row_number, rank, dense_rank, top n per group, lag, lead, month over month, mom growth, gaps between orders, named window, postgresql]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Tutorial: Window Functions"
    url: "https://www.postgresql.org/docs/current/tutorial-window.html"
    source: "PostgreSQL official docs"
    note: "A gentle introduction to OVER and PARTITION BY."
  - title: "Window Functions (reference)"
    url: "https://www.postgresql.org/docs/current/functions-window.html"
    source: "PostgreSQL official docs"
    note: "Every window function: row_number, rank, lag, lead, ntile …"
  - title: "PostgreSQL Exercises"
    url: "https://pgexercises.com/"
    source: "pgexercises.com (free)"
    note: "Includes an aggregation section with window-function exercises."
---

## What is it?

A **window function** calculates over a set of rows *related to the current row* (its "window"), but, unlike `GROUP BY`, it **keeps every row**.

```sql
function(...) OVER (PARTITION BY <groups> ORDER BY <order> <frame>)
```

| Part | Meaning | Example |
|---|---|---|
| `PARTITION BY` | Restart the calculation for each group | Per segment, per customer |
| `ORDER BY` | Order rows inside the window | By month, by revenue |
| Frame (`ROWS BETWEEN …`) | Which rows around the current one to include | The last 3 months |

!!! job "Why it matters at work"
    Running totals, rankings, "top 3 per region", month-on-month growth, first and last purchases, gaps between events: all window functions. They're among the most-asked SQL topics in data analyst and data engineer interviews, and they replace pages of self-joins.

The script is `05_window_functions.sql`. It first creates a view, `shop.net_orders`: non-cancelled orders with segment, region, product and revenue.

## Example 1: keep the detail, add the group total

```sql
SELECT order_id, segment, revenue,
       round(sum(revenue) OVER (PARTITION BY segment), 0)                    AS segment_total,
       round(100 * revenue / sum(revenue) OVER (PARTITION BY segment), 3)    AS pct_of_segment
FROM shop.net_orders
ORDER BY order_id
LIMIT 4;
```

```text
 order_id |    segment    | revenue | segment_total | pct_of_segment
----------+---------------+---------+---------------+----------------
    10001 | Knitting Mill |  189.26 |        806868 |          0.023
    10003 | Trader        |  248.11 |        353758 |          0.070
    10004 | Knitting Mill | 1988.18 |        806868 |          0.246
    10005 | Trader        | 2921.21 |        353758 |          0.826
```

Each order keeps its own row **and** knows its segment's total. With `GROUP BY` you'd get one row per segment and lose the orders.

## Example 2: running total and moving average

```sql
WITH monthly AS (
    SELECT date_trunc('month', order_date)::date AS month, round(sum(revenue), 0) AS revenue
    FROM shop.net_orders GROUP BY 1
)
SELECT to_char(month, 'Mon') AS mon, revenue,
       sum(revenue) OVER (ORDER BY month)                                         AS running_total,
       round(avg(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS moving_avg_3m
FROM monthly ORDER BY month;
```

```text
 mon | revenue | running_total | moving_avg_3m
-----+---------+---------------+---------------
 Jan |  330192 |        330192 |        330192
 Feb |  335736 |        665928 |        332964
 Mar |  324249 |        990177 |        330059
 Apr |  336682 |       1326859 |        332222
 May |  444538 |       1771397 |        368490
 Jun |  324326 |       2095723 |        368515
 Jul |  547579 |       2643302 |        438814
 Aug |  499337 |       3142639 |        457081
 Sep |  606667 |       3749306 |        551194
 Oct |  637897 |       4387203 |        581300
 Nov |  614879 |       5002082 |        619814
 Dec |  476278 |       5478360 |        576351
```

- `ORDER BY` inside `OVER` makes `sum` **cumulative**: each month adds itself to all earlier months.
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` = this month and the two before: a **3-month moving average** that smooths the June Eid dip.
- The year ends at 5,478,360 (monthly totals were rounded; the exact total is 5,478,357.79).

!!! warning "Name your output columns carefully"
    If the output column were called `month` (the same name as the date column), `ORDER BY month` would sort the **text** alphabetically: Apr, Aug, Dec… That's why the label is `mon`. It's a real bug that's easy to miss.

## Example 3: ROW_NUMBER vs RANK vs DENSE_RANK

```sql
WITH product_orders AS (
    SELECT category, product, count(*) AS orders FROM shop.net_orders GROUP BY category, product
)
SELECT category, product, orders,
       row_number() OVER (PARTITION BY category ORDER BY orders DESC, product) AS row_number,   -- tie-breaker
       rank()       OVER w AS rank,
       dense_rank() OVER w AS dense_rank
FROM product_orders
WINDOW w AS (PARTITION BY category ORDER BY orders DESC)
ORDER BY category, orders DESC, product;
```

```text
 category |     product     | orders | row_number | rank | dense_rank
----------+-----------------+--------+------------+------+------------
 Fabric   | Cotton Twill    |    348 |          1 |    1 |          1
 Fabric   | Jersey Knit     |    348 |          2 |    1 |          1
 Fabric   | Denim 12oz      |    335 |          3 |    3 |          2
 Fabric   | Poplin White    |    314 |          4 |    4 |          3
 Trims    | Zippers         |    345 |          1 |    1 |          1
 …
```

| Function | Ties (348, 348) | Next value | Use it for |
|---|---|---|---|
| `row_number()` | 1, 2 (arbitrary unless you add a tie-breaker) | 3 | Exactly one row per group ("latest order") |
| `rank()` | 1, 1 | **3** (skips) | Competition-style ranking |
| `dense_rank()` | 1, 1 | **2** (no gap) | "Top 3 distinct values" |

Always give `row_number()` a **tie-breaker** (here `product`), or the result can change between runs. `WINDOW w AS (...)` names a window you use more than once.

## Example 4: top N per group

```sql
WITH customer_rev AS (
    SELECT region, customer_id, round(sum(revenue), 0) AS revenue,
           rank() OVER (PARTITION BY region ORDER BY sum(revenue) DESC) AS rnk
    FROM shop.net_orders GROUP BY region, customer_id
)
SELECT region, rnk, customer_id, revenue FROM customer_rev WHERE rnk <= 2 ORDER BY region, rnk;
```

```text
   region    | rnk | customer_id | revenue
-------------+-----+-------------+---------
 Chattogram  |   1 | C014        |  223499
 Chattogram  |   2 | C017        |  223207
 Dhaka       |   1 | C010        |  295414
 Dhaka       |   2 | C044        |  255781
 Gazipur     |   1 | C020        |  158376
 Gazipur     |   2 | C012        |  139817
 Khulna      |   1 | C037        |  225647
 Khulna      |   2 | C041        |  103458
 Narayanganj |   1 | C019        |  212038
 Narayanganj |   2 | C051        |  210604
```

You can't filter on a window function in `WHERE` (it's calculated after `WHERE`), so rank in a CTE, then filter outside. Window functions can also wrap aggregates (`ORDER BY sum(revenue)`) in a grouped query.

## Example 5: LAG and LEAD for growth

```sql
SELECT to_char(month, 'Mon') AS mon, revenue,
       lag(revenue)  OVER (ORDER BY month) AS prev_month,
       lead(revenue) OVER (ORDER BY month) AS next_month,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY month)) / lag(revenue) OVER (ORDER BY month), 1) AS mom_pct
FROM monthly ORDER BY month LIMIT 6;
```

```text
 mon | revenue | prev_month | next_month | mom_pct
-----+---------+------------+------------+---------
 Jan |  330192 |            |     335736 |
 Feb |  335736 |     330192 |     324249 |     1.7
 Mar |  324249 |     335736 |     336682 |    -3.4
 Apr |  336682 |     324249 |     444538 |     3.8
 May |  444538 |     336682 |     324326 |    32.0
 Jun |  324326 |     444538 |     547579 |   -27.0
```

`lag()` looks back one row; `lead()` looks forward. January has no previous month, so its growth is NULL (not 0). This is the SQL version of the DAX month-on-month measure from Phase 1.

## Example 6: LAG per customer — gaps between orders

```sql
WITH gaps AS (
    SELECT customer_id, order_date,
           order_date - lag(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS days_since_prev
    FROM shop.net_orders
)
SELECT customer_id, count(*) AS orders, round(avg(days_since_prev), 1) AS avg_gap_days, max(days_since_prev) AS longest_gap
FROM gaps GROUP BY customer_id ORDER BY longest_gap DESC NULLS LAST LIMIT 3;
```

```text
 customer_id | orders | avg_gap_days | longest_gap
-------------+--------+--------------+-------------
 C006        |     21 |         17.8 |         102
 C016        |     14 |         27.4 |          85
 C057        |      9 |         36.4 |          81
```

C006 usually orders every 2–3 weeks but once went **102 days** without ordering: a churn-risk signal worth a call from the account manager.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Filtering on a window result in `WHERE` | Error: window functions aren't allowed in WHERE | Compute in a CTE, filter outside |
| `row_number()` without a tie-breaker | Different rows on different runs | Add a unique column to `ORDER BY` |
| Forgetting `PARTITION BY` | One ranking across everything | Partition by the group |
| Default frame with `ORDER BY` | `RANGE` frame groups equal values; surprising running totals on ties | Use `ROWS BETWEEN …` explicitly |
| Output alias shadows the sort column | Months sorted alphabetically | Use distinct alias names |

## Try it yourself

**Task:** For each segment, find its **best month** and what share of the segment's yearly revenue that month represents.

<details markdown="1">
<summary>Show a hint</summary>

Two windows in one CTE: `row_number()` partitioned by segment and ordered by revenue, and `sum(revenue) OVER (PARTITION BY segment)` for the year total.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```sql
WITH seg_month AS (
    SELECT segment, date_trunc('month', order_date)::date AS month, sum(revenue) AS revenue
    FROM shop.net_orders GROUP BY 1, 2
), ranked AS (
    SELECT segment, month, revenue,
           row_number() OVER (PARTITION BY segment ORDER BY revenue DESC) AS rn,
           revenue / sum(revenue) OVER (PARTITION BY segment) AS share
    FROM seg_month
)
SELECT segment, to_char(month, 'Mon') AS best_month, round(revenue, 0) AS revenue, round(100 * share, 1) AS pct_of_year
FROM ranked WHERE rn = 1 ORDER BY segment;
```

```text
     segment     | best_month | revenue | pct_of_year
-----------------+------------+---------+-------------
 Garment Factory | Oct        |  510834 |        12.1
 Knitting Mill   | Aug        |   96769 |        12.0
 Retailer        | Oct        |   12039 |        14.5
 Trader          | Sep        |   52365 |        14.8
```

Every segment's best month is in the August–October export season, and no single month exceeds 15% of a segment's year (an even spread would be 8.3%).
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What's the key difference between a window function and GROUP BY?

1. Window functions are faster
2. A window function keeps every row; GROUP BY collapses rows into groups
3. GROUP BY can't use SUM

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Two products tie for first place. What does `dense_rank()` give the next product?

1. 3
2. 2
3. 1

<details markdown="1"><summary>Show answer</summary>
**B.** `rank()` would give 3.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which function returns the previous row's value?

1. `lead()`
2. `lag()`
3. `first_value()`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- `function() OVER (PARTITION BY … ORDER BY … frame)` calculates across related rows and **keeps every row**.
- `sum() OVER (ORDER BY …)` = running total; `ROWS BETWEEN n PRECEDING AND CURRENT ROW` = moving window.
- `row_number` (unique, needs a tie-breaker), `rank` (gaps), `dense_rank` (no gaps); filter ranks in an outer query for **top N per group**.
- `lag`/`lead` compare with previous/next rows: growth rates, gaps between events.

!!! job "Job-ready check"
    **Interview question:** *"Return each customer's most recent order."*

    **Strong answer:** "A CTE with `row_number() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn`, then select where `rn = 1`. I add order_id as a tie-breaker so customers with two orders on the same day get a deterministic answer. `rank()` would return both tied rows if that's what the business wants instead."

    **Mini project:** Build a "customer health" query: for each customer, last order date, days since last order (as of 31 Dec 2025), average gap and longest gap, and a status of Active, At risk or Lapsed based on rules you define.
