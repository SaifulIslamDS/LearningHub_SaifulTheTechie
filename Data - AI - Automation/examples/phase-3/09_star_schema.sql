-- Phase 3 · Data warehousing · OLTP vs OLAP, facts & dimensions, star schema   (run: psql -f 09_star_schema.sql)
\pset footer off
SET client_min_messages = warning;

DROP SCHEMA IF EXISTS dw CASCADE;
CREATE SCHEMA dw;

-- Dimensions: the "by" columns (who, what, when, how), with a surrogate key
CREATE TABLE dw.dim_date AS
SELECT to_char(d, 'YYYYMMDD')::int AS date_key, d::date AS full_date,
       extract(year FROM d)::int AS year, extract(quarter FROM d)::int AS quarter,
       extract(month FROM d)::int AS month, to_char(d, 'Mon') AS month_name,
       to_char(d, 'Dy') AS weekday, extract(isodow FROM d) IN (5) AS is_weekend   -- Friday weekend
FROM generate_series(date '2025-01-01', date '2025-12-31', interval '1 day') AS d;
ALTER TABLE dw.dim_date ADD PRIMARY KEY (date_key);

CREATE TABLE dw.dim_customer AS
SELECT row_number() OVER (ORDER BY customer_id)::int AS customer_key, customer_id, customer_name,
       segment, region, credit_days
FROM shop.customers;
ALTER TABLE dw.dim_customer ADD PRIMARY KEY (customer_key);

CREATE TABLE dw.dim_product AS
SELECT product_id AS product_key, product, category, list_price FROM shop.products;
ALTER TABLE dw.dim_product ADD PRIMARY KEY (product_key);

CREATE TABLE dw.dim_channel AS
SELECT row_number() OVER (ORDER BY channel)::int AS channel_key, channel
FROM (SELECT DISTINCT channel FROM shop.orders) c;
ALTER TABLE dw.dim_channel ADD PRIMARY KEY (channel_key);

-- Fact: one row per order (the grain), foreign keys to every dimension + numeric measures
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
ALTER TABLE dw.fact_sales ADD PRIMARY KEY (order_id),
    ADD FOREIGN KEY (date_key) REFERENCES dw.dim_date, ADD FOREIGN KEY (customer_key) REFERENCES dw.dim_customer,
    ADD FOREIGN KEY (product_key) REFERENCES dw.dim_product, ADD FOREIGN KEY (channel_key) REFERENCES dw.dim_channel;

\echo '== 1. The star: one fact table, four dimensions'
SELECT 'fact_sales' AS table_name, count(*) AS rows FROM dw.fact_sales
UNION ALL SELECT 'dim_date', count(*) FROM dw.dim_date
UNION ALL SELECT 'dim_customer', count(*) FROM dw.dim_customer
UNION ALL SELECT 'dim_product', count(*) FROM dw.dim_product
UNION ALL SELECT 'dim_channel', count(*) FROM dw.dim_channel;

\echo '== 2. An OLTP question: one order, by its key (touches one row)'
SELECT order_id, order_date, customer_id, status FROM shop.orders WHERE order_id = 12935;

\echo '== 3. An OLAP question: revenue and margin by quarter and segment (scans many rows)'
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

\echo '== 4. Any dimension slices the same fact: weekday x channel'
SELECT d.weekday, ch.channel, count(*) AS orders
FROM dw.fact_sales f JOIN dw.dim_date d USING (date_key) JOIN dw.dim_channel ch USING (channel_key)
WHERE d.weekday IN ('Fri', 'Sat', 'Sun')
GROUP BY d.weekday, ch.channel ORDER BY d.weekday, ch.channel;

\echo '== Try it yourself: net revenue by product category and month for Q4'
SELECT p.category, d.month_name, round(sum(f.revenue), 0) AS revenue
FROM dw.fact_sales f JOIN dw.dim_date d USING (date_key) JOIN dw.dim_product p USING (product_key)
WHERE f.is_cancelled = 0 AND d.quarter = 4
GROUP BY p.category, d.month, d.month_name ORDER BY p.category, d.month;
