-- Phase 3 · Database engineering · PostgreSQL basics and normalisation   (run: psql -f 06_normalization.sql)
\pset footer off
SET client_min_messages = warning;

\echo '== 1. psql basics: which tables exist, and how big are they?'
SELECT table_schema, table_name,
       (xpath('/row/c/text()', query_to_xml(format('select count(*) as c from %I.%I', table_schema, table_name), false, true, '')))[1]::text::int AS rows
FROM information_schema.tables
WHERE table_schema IN ('staging', 'shop') AND table_type = 'BASE TABLE'
ORDER BY 1, 2;

\echo '== 2. The flat export repeats customer facts on every order'
SELECT customer_id, count(*) AS order_rows, count(DISTINCT region) AS regions, count(DISTINCT segment) AS segments
FROM staging.orders_flat GROUP BY customer_id ORDER BY order_rows DESC LIMIT 3;

\echo '== 3. Update anomaly: a customer moves region, but only some rows get changed'
BEGIN;
UPDATE staging.orders_flat SET region = 'Gazipur'
WHERE customer_id = 'C010' AND order_date >= '2025-07-01';          -- someone fixed "recent" rows only
SELECT region, count(*) FROM staging.orders_flat WHERE customer_id = 'C010' GROUP BY region;
ROLLBACK;                                                              -- undo the experiment

\echo '== 4. In the normalised model the fact lives in ONE place'
BEGIN;
UPDATE shop.customers SET region = 'Gazipur' WHERE customer_id = 'C010';
SELECT c.region, count(*) FROM shop.orders o JOIN shop.customers c USING (customer_id)
WHERE customer_id = 'C010' GROUP BY c.region;
ROLLBACK;

\echo '== 5. Constraints let the database reject bad data'
\set ON_ERROR_STOP off
INSERT INTO shop.orders VALUES (99999, '2025-12-31', 'C999', 1, 'Portal', 10, 3.5, 0, 'Delivered', 3, 2);
INSERT INTO shop.orders VALUES (99999, '2025-12-31', 'C010', 1, 'Portal', -5, 3.5, 0, 'Delivered', 3, 2);
INSERT INTO shop.orders VALUES (99999, '2025-12-31', 'C010', 1, 'Portal', 10, 3.5, 0, 'Lost', 3, 2);
\set ON_ERROR_STOP on

\echo '== 6. Rebuild the flat view whenever you need it: one JOIN away'
CREATE OR REPLACE VIEW shop.orders_wide AS
SELECT o.order_id, o.order_date, o.customer_id, c.customer_name, c.region, c.segment, c.credit_days,
       p.product, p.category, o.channel, o.quantity, o.unit_price, o.discount, o.status,
       round(o.quantity * o.unit_price * (1 - o.discount), 2) AS revenue
FROM shop.orders o JOIN shop.customers c USING (customer_id) JOIN shop.products p USING (product_id);
SELECT round(sum(revenue), 2) AS net_revenue FROM shop.orders_wide WHERE status <> 'Cancelled';

\echo '== 7. Why 1.31 more than the Python total? Exact NUMERIC vs floating-point rounding'
SELECT sum(revenue) AS python_float_total,
       sum(round(quantity * unit_price * (1 - discount), 2)) AS numeric_total,
       count(*) FILTER (WHERE revenue <> round(quantity * unit_price * (1 - discount), 2)) AS rows_rounded_differently
FROM staging.orders_flat WHERE status <> 'Cancelled';
SELECT 0.1::float8 + 0.2::float8 AS float_sum, 0.1::numeric + 0.2::numeric AS numeric_sum;

\echo '== Try it yourself: does the flat file agree with the customer table everywhere?'
SELECT count(*) AS mismatched_rows
FROM staging.orders_flat f JOIN shop.customers c USING (customer_id)
WHERE f.region <> c.region OR f.segment <> c.segment;
