-- =====================================================================
-- Analytical SQL — solutions to every "Try it yourself" exercise
-- Run orders.sql first (it creates the orders and customers tables).
-- Try each exercise yourself before reading the answer!
-- Tested in SQLite. Works in PostgreSQL and MySQL unless noted.
-- =====================================================================

-- Lesson 1 — SELECT & WHERE
-- Which Trims orders were not cancelled? Show customer, product and order value.
-- Expected: 3 rows (Karim Garments 200, Nova Apparel 320, Sun Fashion 420)
SELECT customer,
       product,
       quantity * unit_price AS order_value
FROM orders
WHERE category = 'Trims'
  AND status <> 'Cancelled';

-- Lesson 2 — ORDER BY, GROUP BY & HAVING
-- Delivered orders only: orders and revenue per region, regions above 2,000.
-- Expected: Dhaka 3 / 2850.00, Gazipur 2 / 2520.00
SELECT region,
       COUNT(*)                             AS orders,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY region
HAVING SUM(quantity * unit_price) > 2000
ORDER BY revenue DESC;

-- Lesson 3 — CASE expressions
-- Delivered vs in-progress (Shipped or Pending) revenue per customer.
-- Expected: Delta Knit 2520/0, Nova Apparel 1560/320, Rahim Traders 1290/0,
--           Karim Garments 880/1275, Sun Fashion 420/810
SELECT customer,
       SUM(CASE WHEN status = 'Delivered'
                THEN quantity * unit_price ELSE 0 END)   AS delivered,
       SUM(CASE WHEN status IN ('Shipped', 'Pending')
                THEN quantity * unit_price ELSE 0 END)   AS in_progress
FROM orders
GROUP BY customer
ORDER BY delivered DESC;

-- Lesson 4 — JOINs
-- Non-cancelled revenue and order count per account manager.
-- Expected: Tanvir 5 / 4675.00, Anika 6 / 4400.00
SELECT c.account_manager,
       COUNT(*)                       AS orders,
       SUM(o.quantity * o.unit_price) AS revenue
FROM orders AS o
JOIN customers AS c
  ON o.customer = c.customer_name
WHERE o.status <> 'Cancelled'
GROUP BY c.account_manager
ORDER BY revenue DESC;

-- Bonus (lesson 4): customers who have never ordered (anti-join).
-- Expected: Blue Thread Ltd | Tanvir
SELECT c.customer_name, c.account_manager
FROM customers AS c
LEFT JOIN orders AS o ON o.customer = c.customer_name
WHERE o.order_id IS NULL;

-- Lesson 5 — Subqueries
-- Customers whose non-cancelled revenue is above the average customer revenue (1,815).
-- Expected: Delta Knit 2520, Karim Garments 2155, Nova Apparel 1880
SELECT customer,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status <> 'Cancelled'
GROUP BY customer
HAVING SUM(quantity * unit_price) > (
        SELECT AVG(revenue)
        FROM (
               SELECT customer, SUM(quantity * unit_price) AS revenue
               FROM orders
               WHERE status <> 'Cancelled'
               GROUP BY customer
             ) AS t
      )
ORDER BY revenue DESC;

-- Same answer, written as a CTE (easier to read).
WITH customer_totals AS (
    SELECT customer,
           SUM(quantity * unit_price) AS revenue
    FROM orders
    WHERE status <> 'Cancelled'
    GROUP BY customer
)
SELECT customer, revenue
FROM customer_totals
WHERE revenue > (SELECT AVG(revenue) FROM customer_totals)
ORDER BY revenue DESC;
