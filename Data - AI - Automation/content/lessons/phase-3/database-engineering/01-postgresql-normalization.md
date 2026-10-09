---
title: "PostgreSQL & Normalisation: One Fact in One Place"
order: 1
summary: "Load data into PostgreSQL with COPY, see why a flat export causes update anomalies, normalise it into customers, products and orders with keys and constraints, and store money as NUMERIC — not floats."
level: Intermediate
time: "55 min"
topics: ["PostgreSQL", "Normalization"]
prerequisites: ["phase-3/advanced-sql/01-ctes-recursive"]
keywords: [postgresql, postgres, psql, psycopg, copy, schema, staging, create table, data types, numeric, float, primary key, foreign key, check constraint, not null, unique, normalisation, normalization, normal form, 1nf, 2nf, 3nf, update anomaly, denormalised, view]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "PostgreSQL Tutorial"
    url: "https://www.postgresql.org/docs/current/tutorial.html"
    source: "PostgreSQL official docs"
    note: "Creating tables, querying, joins and the basics of psql."
  - title: "Constraints"
    url: "https://www.postgresql.org/docs/current/ddl-constraints.html"
    source: "PostgreSQL official docs"
    note: "Primary keys, foreign keys, CHECK, NOT NULL and UNIQUE."
  - title: "COPY"
    url: "https://www.postgresql.org/docs/current/sql-copy.html"
    source: "PostgreSQL official docs"
    note: "The fast way to load files into tables."
---

## What is it?

- **PostgreSQL** ("Postgres") is a free, open-source relational database: reliable, standards-based and extensible. `psql` is its command-line client; `psycopg` is the Python driver.
- **Normalisation** is designing tables so that **each fact is stored once**: customers in one table, products in another, orders referencing both by **keys**.

| Normal form (simplified) | Rule | Our example |
|---|---|---|
| **1NF** | One value per cell, no repeating groups | No "products: Twill, Denim" in one cell |
| **2NF** | Every column depends on the whole key | Product category depends on the product, not on the order |
| **3NF** | No column depends on another non-key column | A customer's region depends on the customer, not on the order |

!!! job "Why it matters at work"
    Application databases (OLTP) are normalised so that updates stay consistent; warehouses (next module) deliberately denormalise for fast reading. Data engineers move data between the two every day, so they must understand both, and Postgres is one of the most requested database skills in data job adverts.

## Step 1: load files with COPY (staging first)

`03_load_postgres.py` creates two schemas (**schemas** are folders for tables):

- `staging`: the files loaded **as they are**, with loose types.
- `shop`: the clean, normalised model.

```python
def copy_csv(cur, table: str, path: Path):
    with path.open("rb") as f, cur.copy(f"COPY {table} FROM STDIN WITH (FORMAT csv, HEADER true)") as cp:
        while chunk := f.read(65536):
            cp.write(chunk)
```

```text
staging.orders_flat      4246 rows
shop.customers             63 rows
shop.products              12 rows
shop.orders              4246 rows
loaded into postgres on PostgreSQL 16
```

`COPY` streams a whole file in one command: far faster than thousands of `INSERT`s. The first run failed on `invalid input syntax for type integer: "3.0"`: the export writes delivery days as `3.0`. That's why staging accepts any number (`delivery_days numeric`) and the move into `shop` casts it (`::integer`). **Land loosely, then tighten.**

## Step 2: the problem with one wide table

```sql
SELECT customer_id, count(*) AS order_rows, count(DISTINCT region) AS regions, count(DISTINCT segment) AS segments
FROM staging.orders_flat GROUP BY customer_id ORDER BY order_rows DESC LIMIT 3;
```

```text
 customer_id | order_rows | regions | segments
-------------+------------+---------+----------
 C010        |        208 |       1 |        1
 C044        |        191 |       1 |        1
 C014        |        165 |       1 |        1
```

C010's region is written **208 times**. Now the customer moves, and someone updates only the recent rows:

```sql
BEGIN;
UPDATE staging.orders_flat SET region = 'Gazipur'
WHERE customer_id = 'C010' AND order_date >= '2025-07-01';          -- someone fixed "recent" rows only
SELECT region, count(*) FROM staging.orders_flat WHERE customer_id = 'C010' GROUP BY region;
ROLLBACK;                                                              -- undo the experiment
```

```text
 region  | count
---------+-------
 Dhaka   |    82
 Gazipur |   126
```

The same customer now "lives" in two regions. That's an **update anomaly**, and every report built on this table is now inconsistent. (`BEGIN … ROLLBACK` let us try it safely; more in the Transactions lesson.)

## Step 3: the normalised model

```sql
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
```

| Element | Purpose |
|---|---|
| `PRIMARY KEY` | Uniquely identifies each row (and is automatically indexed) |
| `REFERENCES` (foreign key) | Every order must point at a real customer and product |
| `CHECK` | Business rules the database enforces itself |
| `NOT NULL`, `UNIQUE` | Required values; no duplicate product names |
| `serial` | An auto-incrementing **surrogate key** (`product_id`) |

Now a region change is **one** update:

```text
 region  | count
---------+-------
 Gazipur |   208
```

### The database rejects bad data

```text
ERROR:  insert or update on table "orders" violates foreign key constraint "orders_customer_id_fkey"
DETAIL:  Key (customer_id)=(C999) is not present in table "customers".
ERROR:  new row for relation "orders" violates check constraint "orders_quantity_check"
ERROR:  new row for relation "orders" violates check constraint "orders_status_check"
```

An unknown customer, a negative quantity and a status of `'Lost'` are all refused, no matter which application or script tries to insert them. Constraints are the last line of defence for data quality.

### Need the wide table? Make a view

```sql
CREATE OR REPLACE VIEW shop.orders_wide AS
SELECT o.order_id, o.order_date, o.customer_id, c.customer_name, c.region, c.segment, c.credit_days,
       p.product, p.category, o.channel, o.quantity, o.unit_price, o.discount, o.status,
       round(o.quantity * o.unit_price * (1 - o.discount), 2) AS revenue
FROM shop.orders o JOIN shop.customers c USING (customer_id) JOIN shop.products p USING (product_id);
```

A **view** is a saved query: analysts get one convenient wide table, while the data is stored once.

## Step 4: store money as NUMERIC

```text
 net_revenue
-------------
  5478359.10
```

1.31 **more** than Phase 2's known answer (5,478,357.79). Why?

```text
 python_float_total | numeric_total | rows_rounded_differently
--------------------+---------------+--------------------------
         5478357.79 |    5478359.10 |                      131

      float_sum      | numeric_sum
---------------------+-------------
 0.30000000000000004 |         0.3
```

Python computed revenue with **floating-point** numbers, which can't store most decimals exactly: an amount like 189.255 is really 189.2549999…, so it rounds **down**. PostgreSQL's `NUMERIC` is exact and rounds 131 such half-cent amounts **up**. Neither is a bug, but for money use exact decimals (`NUMERIC` in SQL, `decimal.Decimal` in Python), agree one rounding rule, and document which total is official.

| PostgreSQL type | Use for |
|---|---|
| `integer`, `bigint` | Counts, IDs |
| `numeric(p, s)` | **Money**, quantities that must be exact |
| `double precision` | Measurements, scientific values |
| `text` | Strings (no length limit needed) |
| `date`, `timestamptz` | Dates; timestamps **with time zone** |
| `boolean`, `jsonb` | Flags; semi-structured data |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| One wide table for everything | Update anomalies, inconsistent reports | Normalise the source of truth; views for convenience |
| No foreign keys "for speed" | Orphan orders, broken joins | Keep FKs; they're cheap at this scale |
| Strict types in staging | Loads fail on messy exports | Loose staging, strict model |
| Floats for money | Cent differences that never reconcile | `numeric` / `Decimal`; one rounding rule |
| Row-by-row INSERTs for big files | Very slow loads | `COPY` (or batched inserts) |

## Try it yourself

**Task:** Before you trusted the normalised model, did the flat export ever disagree with the customer table (a different region or segment for the same customer on some order)? Write the check.

<details markdown="1">
<summary>Show the solution</summary>

```sql
SELECT count(*) AS mismatched_rows
FROM staging.orders_flat f JOIN shop.customers c USING (customer_id)
WHERE f.region <> c.region OR f.segment <> c.segment;
```

```text
 mismatched_rows
-----------------
               0
```

Zero, so the export is consistent today and normalising loses nothing. Run checks like this **before** dropping columns from a flat source: if they disagree, you have to decide which source is right first.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. A customer's region is repeated on 208 order rows. What problem can that cause?

1. Slower inserts only
2. Update anomalies: some rows changed, others not, so the data contradicts itself
3. None

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does a foreign key on `orders.customer_id` guarantee?

1. Every order refers to a customer that exists
2. Customers can't have more than one order
3. Orders are sorted by customer

<details markdown="1"><summary>Show answer</summary>
**A.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which type should store order revenue?

1. `double precision`
2. `numeric(12,2)`
3. `text`

<details markdown="1"><summary>Show answer</summary>
**B.** Exact decimal arithmetic.
</details>
</div>

## Summary

- Load with **COPY** into a loosely typed **staging** schema, then move into a strict model.
- **Normalise** the source of truth: each fact once, linked by primary and foreign keys.
- Let **constraints** (PK, FK, CHECK, NOT NULL, UNIQUE) reject bad data at the database.
- Use **views** for convenient wide tables, and **NUMERIC** for money.

!!! job "Job-ready check"
    **Interview question:** *"What is normalisation, and when would you denormalise?"*

    **Strong answer:** "Normalisation organises tables so each fact is stored once and linked by keys, which avoids update anomalies, so it's right for transactional systems. For analytics I denormalise into star schemas or wide tables, because reads vastly outnumber writes and fewer joins make queries simpler and faster. The normalised system stays the source of truth, and the denormalised copy is rebuilt from it."

    **Mini project:** Add a `shop.order_lines` table so one order can contain several products. Write the CREATE statements with keys and constraints, and a view that rebuilds the wide table.
