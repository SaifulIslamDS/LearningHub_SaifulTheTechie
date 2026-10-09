-- Phase 3 · Data warehousing · Slowly changing dimensions (SCD type 1 and type 2)   (run after 09_star_schema.sql)
\pset footer off
SET client_min_messages = warning;

-- A type 2 customer dimension: a new ROW for every change, with validity dates
DROP TABLE IF EXISTS dw.dim_customer_scd2;
CREATE TABLE dw.dim_customer_scd2 (
    customer_key  serial PRIMARY KEY,                 -- surrogate key: one per VERSION
    customer_id   text NOT NULL,                      -- business key: one per customer
    customer_name text, segment text, region text, credit_days int,
    valid_from    date NOT NULL,
    valid_to      date NOT NULL DEFAULT '9999-12-31',
    is_current    boolean NOT NULL DEFAULT true
);
INSERT INTO dw.dim_customer_scd2 (customer_id, customer_name, segment, region, credit_days, valid_from)
SELECT customer_id, customer_name, segment, region, credit_days, date '2025-01-01' FROM shop.customers;

\echo '== 1. A change arrives: on 1 July, C010 moves to Gazipur and gets 60-day credit'
DROP TABLE IF EXISTS staging.customer_changes;
CREATE TABLE staging.customer_changes AS
SELECT customer_id, customer_name, segment, 'Gazipur'::text AS region, 60 AS credit_days, date '2025-07-01' AS changed_on
FROM shop.customers WHERE customer_id = 'C010';

\echo '== 2. Apply type 2: close the old version, insert the new one (one transaction)'
BEGIN;
UPDATE dw.dim_customer_scd2 d
SET valid_to = c.changed_on - 1, is_current = false
FROM staging.customer_changes c
WHERE d.customer_id = c.customer_id AND d.is_current
  AND (d.region, d.credit_days) IS DISTINCT FROM (c.region, c.credit_days);
INSERT INTO dw.dim_customer_scd2 (customer_id, customer_name, segment, region, credit_days, valid_from)
SELECT c.customer_id, c.customer_name, c.segment, c.region, c.credit_days, c.changed_on
FROM staging.customer_changes c
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_customer_scd2 d
                  WHERE d.customer_id = c.customer_id AND d.is_current
                    AND (d.region, d.credit_days) = (c.region, c.credit_days));
COMMIT;
SELECT customer_key, customer_id, region, credit_days, valid_from, valid_to, is_current
FROM dw.dim_customer_scd2 WHERE customer_id = 'C010' ORDER BY valid_from;

\echo '== 3. Run exactly the same two statements again: nothing changes (the load is idempotent)'
BEGIN;
UPDATE dw.dim_customer_scd2 d SET valid_to = c.changed_on - 1, is_current = false
FROM staging.customer_changes c
WHERE d.customer_id = c.customer_id AND d.is_current
  AND (d.region, d.credit_days) IS DISTINCT FROM (c.region, c.credit_days);
INSERT INTO dw.dim_customer_scd2 (customer_id, customer_name, segment, region, credit_days, valid_from)
SELECT c.customer_id, c.customer_name, c.segment, c.region, c.credit_days, c.changed_on
FROM staging.customer_changes c
WHERE NOT EXISTS (SELECT 1 FROM dw.dim_customer_scd2 d
                  WHERE d.customer_id = c.customer_id AND d.is_current
                    AND (d.region, d.credit_days) = (c.region, c.credit_days));
COMMIT;
SELECT count(*) AS versions_of_C010 FROM dw.dim_customer_scd2 WHERE customer_id = 'C010';

\echo '== 4. "As it was": join each order to the version valid on its order date'
SELECT d.region AS region_at_order_time, count(*) AS orders, round(sum(o.quantity * o.unit_price * (1 - o.discount)), 0) AS revenue
FROM shop.orders o
JOIN dw.dim_customer_scd2 d
  ON d.customer_id = o.customer_id AND o.order_date BETWEEN d.valid_from AND d.valid_to
WHERE o.customer_id = 'C010' AND o.status <> 'Cancelled'
GROUP BY d.region ORDER BY d.region;

\echo '== 5. "As it is now": join on the current version only (type 1 behaviour)'
SELECT d.region AS current_region, count(*) AS orders
FROM shop.orders o JOIN dw.dim_customer_scd2 d ON d.customer_id = o.customer_id AND d.is_current
WHERE o.customer_id = 'C010' AND o.status <> 'Cancelled'
GROUP BY d.region;

\echo '== Try it yourself: how many customers have more than one version, and which is current?'
SELECT customer_id, count(*) AS versions, max(region) FILTER (WHERE is_current) AS current_region
FROM dw.dim_customer_scd2 GROUP BY customer_id HAVING count(*) > 1;
