-- Phase 3 · Database engineering · Indexing and EXPLAIN ANALYZE   (run: psql -f 07_indexing_explain.sql)
\pset footer off
SET client_min_messages = warning;
SET TimeZone = 'UTC';

\echo '== 0. A bigger table: 2 million synthetic orders (takes a few seconds)'
DROP TABLE IF EXISTS shop.orders_big;
SELECT setseed(0.42);
CREATE TABLE shop.orders_big AS
SELECT g AS order_id,
       date '2021-01-01' + (random() * 1825)::int AS order_date,
       'C' || lpad((1 + (random() * 1999)::int)::text, 4, '0') AS customer_id,
       (ARRAY['Dhaka','Chattogram','Gazipur','Narayanganj','Khulna'])[1 + (random() * 4)::int] AS region,
       CASE WHEN random() < 0.90 THEN 'Delivered' WHEN random() < 0.6 THEN 'Cancelled' ELSE 'Shipped' END AS status,
       round((50 + random() * 3000)::numeric, 2) AS revenue
FROM generate_series(1, 2000000) AS g;
ANALYZE shop.orders_big;
SELECT pg_size_pretty(pg_total_relation_size('shop.orders_big')) AS table_size, count(*) FROM shop.orders_big;

\echo '== 1. Find one customer''s orders WITHOUT an index: a sequential scan reads every row'
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT * FROM shop.orders_big WHERE customer_id = 'C0042';

\echo '== 2. Add an index and run the same query'
CREATE INDEX idx_orders_big_customer ON shop.orders_big (customer_id);
EXPLAIN (ANALYZE, COSTS OFF, TIMING ON, SUMMARY ON)
SELECT * FROM shop.orders_big WHERE customer_id = 'C0042';
SELECT pg_size_pretty(pg_relation_size('shop.idx_orders_big_customer')) AS index_size;

\echo '== 3. A composite index for "one customer, one date range"'
CREATE INDEX idx_orders_big_cust_date ON shop.orders_big (customer_id, order_date);
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT order_date, revenue FROM shop.orders_big
WHERE customer_id = 'C0042' AND order_date >= '2025-01-01' AND order_date < '2025-04-01';

\echo '== 4. Low selectivity: 90% of rows are Delivered, so the planner ignores the index'
CREATE INDEX idx_orders_big_status ON shop.orders_big (status);
ANALYZE shop.orders_big;
EXPLAIN (COSTS OFF) SELECT count(*) FROM shop.orders_big WHERE status = 'Delivered';
EXPLAIN (COSTS OFF) SELECT count(*) FROM shop.orders_big WHERE status = 'Shipped';

\echo '== 5. A function on the column hides the index; rewrite as a range'
CREATE INDEX idx_orders_big_date ON shop.orders_big (order_date);
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT count(*) FROM shop.orders_big WHERE date_trunc('month', order_date) = '2025-03-01';
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT count(*) FROM shop.orders_big WHERE order_date >= '2025-03-01' AND order_date < '2025-04-01';

\echo '== 6. Indexes are not free: total size now'
SELECT pg_size_pretty(pg_relation_size('shop.orders_big')) AS table_only,
       pg_size_pretty(pg_indexes_size('shop.orders_big')) AS all_indexes;

\echo '== Try it yourself: total revenue per region for 2024 — does any index help?'
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT region, round(sum(revenue), 0) FROM shop.orders_big
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01' GROUP BY region;
