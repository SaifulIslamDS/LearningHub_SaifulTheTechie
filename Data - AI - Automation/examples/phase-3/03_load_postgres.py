"""Phase 3 · Database engineering · Load the 2025 data into PostgreSQL.

Needs a running PostgreSQL (see the PostgreSQL lesson; with Docker:
    docker run --name pg -e POSTGRES_PASSWORD=practice -p 5432:5432 -d postgres:18
) and the driver:  uv add "psycopg[binary]"

Creates two schemas:
    staging.orders_flat  the 2025 orders exactly as exported (one wide table)
    shop.*               the same data normalised: customers, products, orders
"""
import os
from pathlib import Path

import psycopg

DSN = os.environ.get("DATABASE_URL", "postgresql://postgres:practice@localhost:5432/postgres")
DATA = Path(__file__).parent / "data"

SCHEMA = """
DROP SCHEMA IF EXISTS staging CASCADE;
DROP SCHEMA IF EXISTS shop CASCADE;
CREATE SCHEMA staging;
CREATE SCHEMA shop;

CREATE TABLE staging.orders_flat (
    order_id integer, order_date date, customer_id text, region text, segment text, channel text,
    category text, product text, quantity integer, unit_price numeric(10,3), discount numeric(4,2),
    unit_cost numeric(10,3), status text, promised_days integer,
    delivery_days numeric,           -- the export writes "3.0", so staging accepts any number
    revenue numeric(12,2)
);
CREATE TABLE staging.customers (
    customer_id text, customer_name text, segment text, region text, signup_date date, credit_days integer
);
CREATE TABLE staging.products (product text, category text, list_price numeric(10,3), unit_cost numeric(10,3));

-- normalised model: every fact stored once
CREATE TABLE shop.customers (
    customer_id   text PRIMARY KEY,
    customer_name text NOT NULL,
    segment       text NOT NULL,
    region        text NOT NULL,
    signup_date   date NOT NULL,
    credit_days   integer NOT NULL CHECK (credit_days IN (0, 15, 30, 60))
);
CREATE TABLE shop.products (
    product_id  serial PRIMARY KEY,
    product     text UNIQUE NOT NULL,
    category    text NOT NULL,
    list_price  numeric(10,3) NOT NULL CHECK (list_price > 0),
    unit_cost   numeric(10,3) NOT NULL
);
CREATE TABLE shop.orders (
    order_id      integer PRIMARY KEY,
    order_date    date NOT NULL,
    customer_id   text NOT NULL REFERENCES shop.customers,
    product_id    integer NOT NULL REFERENCES shop.products,
    channel       text NOT NULL,
    quantity      integer NOT NULL CHECK (quantity > 0),
    unit_price    numeric(10,3) NOT NULL,
    discount      numeric(4,2) NOT NULL DEFAULT 0,
    status        text NOT NULL CHECK (status IN ('Delivered', 'Shipped', 'Pending', 'Cancelled')),
    promised_days integer NOT NULL,
    delivery_days integer
);
"""

NORMALISE = """
INSERT INTO shop.customers SELECT * FROM staging.customers;
INSERT INTO shop.products (product, category, list_price, unit_cost)
    SELECT product, category, list_price, unit_cost FROM staging.products ORDER BY product;
INSERT INTO shop.orders
    SELECT f.order_id, f.order_date, f.customer_id, p.product_id, f.channel, f.quantity, f.unit_price,
           f.discount, f.status, f.promised_days, f.delivery_days::integer
    FROM staging.orders_flat f JOIN shop.products p USING (product);
"""


def copy_csv(cur, table: str, path: Path):
    with path.open("rb") as f, cur.copy(f"COPY {table} FROM STDIN WITH (FORMAT csv, HEADER true)") as cp:
        while chunk := f.read(65536):
            cp.write(chunk)


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute(SCHEMA)
    copy_csv(cur, "staging.orders_flat", DATA / "orders_2025.csv")
    copy_csv(cur, "staging.customers", DATA / "customers_2025.csv")
    copy_csv(cur, "staging.products", DATA / "products_2025.csv")
    cur.execute(NORMALISE)
    for t in ["staging.orders_flat", "shop.customers", "shop.products", "shop.orders"]:
        cur.execute(f"SELECT count(*) FROM {t}")
        print(f"{t:22s} {cur.fetchone()[0]:>6} rows")
    print("loaded into", conn.info.dbname, "on PostgreSQL", conn.info.server_version // 10000)
