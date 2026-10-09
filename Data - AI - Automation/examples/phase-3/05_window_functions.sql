-- Phase 3 · Advanced SQL · Window functions, RANK, LAG & LEAD   (PostgreSQL; run: psql -f 05_window_functions.sql)
\pset footer off
SET client_min_messages = warning;

CREATE OR REPLACE VIEW shop.net_orders AS
SELECT o.order_id, o.order_date, o.customer_id, c.segment, c.region, p.product, p.category,
       round(o.quantity * o.unit_price * (1 - o.discount), 2) AS revenue
FROM shop.orders o
JOIN shop.customers c USING (customer_id)
JOIN shop.products p USING (product_id)
WHERE o.status <> 'Cancelled';

\echo '== 1. GROUP BY collapses rows; a window keeps every row and adds a calculation'
SELECT order_id, segment, revenue,
       round(sum(revenue) OVER (PARTITION BY segment), 0)                    AS segment_total,
       round(100 * revenue / sum(revenue) OVER (PARTITION BY segment), 3)    AS pct_of_segment
FROM shop.net_orders
ORDER BY order_id
LIMIT 4;

\echo '== 2. Running total of revenue through the year (ORDER BY inside OVER)'
WITH monthly AS (
    SELECT date_trunc('month', order_date)::date AS month, round(sum(revenue), 0) AS revenue
    FROM shop.net_orders GROUP BY 1
)
SELECT to_char(month, 'Mon') AS mon, revenue,
       sum(revenue) OVER (ORDER BY month)                                         AS running_total,
       round(avg(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS moving_avg_3m
FROM monthly ORDER BY month;

\echo '== 3. ROW_NUMBER vs RANK vs DENSE_RANK when there are ties'
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

\echo '== 4. Top 2 customers by revenue in every region'
WITH customer_rev AS (
    SELECT region, customer_id, round(sum(revenue), 0) AS revenue,
           rank() OVER (PARTITION BY region ORDER BY sum(revenue) DESC) AS rnk
    FROM shop.net_orders GROUP BY region, customer_id
)
SELECT region, rnk, customer_id, revenue FROM customer_rev WHERE rnk <= 2 ORDER BY region, rnk;

\echo '== 5. LAG and LEAD: month-on-month growth'
WITH monthly AS (
    SELECT date_trunc('month', order_date)::date AS month, round(sum(revenue), 0) AS revenue
    FROM shop.net_orders GROUP BY 1
)
SELECT to_char(month, 'Mon') AS mon, revenue,
       lag(revenue)  OVER (ORDER BY month) AS prev_month,
       lead(revenue) OVER (ORDER BY month) AS next_month,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY month)) / lag(revenue) OVER (ORDER BY month), 1) AS mom_pct
FROM monthly ORDER BY month LIMIT 6;

\echo '== 6. LAG per customer: days between consecutive orders'
WITH gaps AS (
    SELECT customer_id, order_date,
           order_date - lag(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS days_since_prev
    FROM shop.net_orders
)
SELECT customer_id, count(*) AS orders, round(avg(days_since_prev), 1) AS avg_gap_days, max(days_since_prev) AS longest_gap
FROM gaps GROUP BY customer_id ORDER BY longest_gap DESC NULLS LAST LIMIT 3;

\echo '== Try it yourself: each segment''s best month, and its share of the segment''s year'
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
