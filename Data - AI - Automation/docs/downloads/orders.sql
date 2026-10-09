-- Practice tables for the Analytical SQL lessons: orders and customers.
-- Works in SQLite, PostgreSQL and MySQL. Run the whole file once, then start querying.

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    order_date  DATE          NOT NULL,
    customer    VARCHAR(50)   NOT NULL,
    region      VARCHAR(30)   NOT NULL,
    category    VARCHAR(20)   NOT NULL,
    product     VARCHAR(40)   NOT NULL,
    quantity    INTEGER       NOT NULL,
    unit_price  DECIMAL(10,2) NOT NULL,
    status      VARCHAR(20)   NOT NULL
);

INSERT INTO orders (order_id, order_date, customer, region, category, product, quantity, unit_price, status) VALUES
(1,  '2026-01-05', 'Rahim Traders',  'Dhaka',       'Fabric', 'Cotton Twill',     120,  3.50, 'Delivered'),
(2,  '2026-01-08', 'Karim Garments', 'Chattogram',  'Trims',  'Metal Buttons',   5000,  0.04, 'Delivered'),
(3,  '2026-01-12', 'Nova Apparel',   'Dhaka',       'Fabric', 'Denim 12oz',       300,  5.20, 'Delivered'),
(4,  '2026-01-15', 'Rahim Traders',  'Dhaka',       'Trims',  'Zippers',          800,  0.30, 'Cancelled'),
(5,  '2026-01-20', 'Delta Knit',     'Gazipur',     'Yarn',   'Cotton Yarn 30s',  450,  2.80, 'Delivered'),
(6,  '2026-02-02', 'Karim Garments', 'Chattogram',  'Fabric', 'Cotton Twill',     200,  3.40, 'Delivered'),
(7,  '2026-02-06', 'Nova Apparel',   'Dhaka',       'Trims',  'Metal Buttons',   8000,  0.04, 'Shipped'),
(8,  '2026-02-11', 'Delta Knit',     'Gazipur',     'Yarn',   'Polyester Yarn',   600,  2.10, 'Delivered'),
(9,  '2026-02-18', 'Sun Fashion',    'Narayanganj', 'Fabric', 'Denim 12oz',       150,  5.40, 'Pending'),
(10, '2026-02-25', 'Rahim Traders',  'Dhaka',       'Yarn',   'Cotton Yarn 30s',  300,  2.90, 'Delivered'),
(11, '2026-03-03', 'Sun Fashion',    'Narayanganj', 'Trims',  'Zippers',         1500,  0.28, 'Delivered'),
(12, '2026-03-09', 'Karim Garments', 'Chattogram',  'Fabric', 'Denim 12oz',       250,  5.10, 'Shipped');

-- Customers table (used from the JOINs lesson onwards).
-- Note: orders.customer matches customers.customer_name.
-- "Blue Thread Ltd" has not ordered yet. That is on purpose, for the LEFT JOIN example.
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id      INTEGER PRIMARY KEY,
    customer_name    VARCHAR(50) NOT NULL,
    segment          VARCHAR(30) NOT NULL,
    city             VARCHAR(30) NOT NULL,
    account_manager  VARCHAR(30) NOT NULL
);

INSERT INTO customers (customer_id, customer_name, segment, city, account_manager) VALUES
(1, 'Rahim Traders',   'Trader',          'Dhaka',       'Anika'),
(2, 'Karim Garments',  'Garment Factory', 'Chattogram',  'Tanvir'),
(3, 'Nova Apparel',    'Garment Factory', 'Dhaka',       'Anika'),
(4, 'Delta Knit',      'Knitting Mill',   'Gazipur',     'Tanvir'),
(5, 'Sun Fashion',     'Garment Factory', 'Narayanganj', 'Anika'),
(6, 'Blue Thread Ltd', 'Trader',          'Dhaka',       'Tanvir');
