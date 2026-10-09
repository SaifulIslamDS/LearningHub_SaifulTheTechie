-- Phase 3 · Advanced SQL · CTEs and recursive CTEs   (PostgreSQL; run: psql -f 04_ctes.sql)
\pset footer off
SET client_min_messages = warning;

\echo '== 1. A CTE: customers whose revenue beats their segment average'
WITH net_orders AS (                      -- step 1: only orders that count
    SELECT o.*, o.quantity * o.unit_price * (1 - o.discount) AS revenue
    FROM shop.orders o
    WHERE o.status <> 'Cancelled'
),
customer_revenue AS (                     -- step 2: one row per customer
    SELECT c.customer_id, c.customer_name, c.segment, round(sum(n.revenue), 0) AS revenue
    FROM net_orders n JOIN shop.customers c USING (customer_id)
    GROUP BY c.customer_id, c.customer_name, c.segment
),
segment_avg AS (                          -- step 3: one row per segment
    SELECT segment, round(avg(revenue), 0) AS avg_revenue
    FROM customer_revenue GROUP BY segment
)
SELECT cr.segment, count(*) AS customers_above_avg, max(sa.avg_revenue) AS segment_avg
FROM customer_revenue cr JOIN segment_avg sa USING (segment)
WHERE cr.revenue > sa.avg_revenue
GROUP BY cr.segment
ORDER BY cr.segment;

\echo '== 2. Chained CTEs: in which month did each customer first order? (a cohort count)'
WITH first_order AS (
    SELECT customer_id, min(order_date) AS first_date FROM shop.orders GROUP BY customer_id
)
SELECT to_char(date_trunc('quarter', first_date), 'YYYY-"Q"Q') AS first_quarter, count(*) AS customers
FROM first_order GROUP BY 1 ORDER BY 1;

\echo '== 3. Recursive CTE: a calendar of all 12 months, so months with no orders still show up'
WITH RECURSIVE months(m) AS (
    SELECT date '2025-01-01'                        -- anchor: where to start
    UNION ALL
    SELECT (m + interval '1 month')::date FROM months
    WHERE m < date '2025-12-01'                     -- stop condition
)
SELECT to_char(m, 'Mon') AS month, count(o.order_id) AS orders     -- count(column) gives 0 for no match
FROM months
LEFT JOIN shop.orders o ON date_trunc('month', o.order_date) = months.m AND o.customer_id = 'C053'
GROUP BY m ORDER BY m;

\echo '== 4. Recursive CTE: walk the sales organisation (a hierarchy)'
DROP TABLE IF EXISTS shop.staff;
CREATE TABLE shop.staff (staff_id int PRIMARY KEY, name text, title text, manager_id int REFERENCES shop.staff);
INSERT INTO shop.staff VALUES
  (1, 'Farhana', 'Head of Sales', NULL),
  (2, 'Anika',   'Regional Manager, Dhaka & Gazipur', 1),
  (3, 'Tanvir',  'Regional Manager, Chattogram & Khulna', 1),
  (4, 'Rafi',    'Sales Rep', 2), (5, 'Mitu', 'Sales Rep', 2),
  (6, 'Sohel',   'Sales Rep', 3), (7, 'Nadia', 'Key Account Lead', 3), (8, 'Imran', 'Sales Rep', 7);

WITH RECURSIVE org AS (
    SELECT staff_id, name, title, 1 AS level, name::text AS path
    FROM shop.staff WHERE manager_id IS NULL                       -- anchor: the top of the tree
    UNION ALL
    SELECT s.staff_id, s.name, s.title, org.level + 1, org.path || ' > ' || s.name
    FROM shop.staff s JOIN org ON s.manager_id = org.staff_id     -- recursive step: their reports
)
SELECT level, repeat('    ', level - 1) || name AS person, title, path FROM org ORDER BY path;

\echo '== Try it yourself: everyone who reports (directly or indirectly) to Tanvir'
WITH RECURSIVE team AS (
    SELECT staff_id, name FROM shop.staff WHERE name = 'Tanvir'
    UNION ALL
    SELECT s.staff_id, s.name FROM shop.staff s JOIN team t ON s.manager_id = t.staff_id
)
SELECT name FROM team WHERE name <> 'Tanvir' ORDER BY name;
