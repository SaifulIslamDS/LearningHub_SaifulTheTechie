---
title: "DuckDB & Larger Local Data: SQL on Files, Parquet and Millions of Rows"
order: 2
summary: "Query CSV, Parquet and pandas DataFrames with SQL using DuckDB, then handle 2 million rows on a laptop by choosing the right file format, reading only what you need, and comparing pandas, Polars and DuckDB."
level: Intermediate
time: "50 min"
topics: ["DuckDB in-process SQL", "Working with larger local data"]
prerequisites: ["phase-2/polars-duckdb/01-polars-dataframes", "phase-1/analytical-sql/02-order-group-by"]
keywords: [duckdb, in-process sql, olap, sql on csv, sql on parquet, parquet, columnar, file format, memory, out of memory, larger than memory, group by all, window function, copy to parquet, performance, benchmark]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, phase-2/customers_2025.csv]
resources:
  - title: "DuckDB Python API — overview"
    url: "https://duckdb.org/docs/stable/clients/python/overview"
    source: "DuckDB official docs"
    note: "duckdb.sql, querying DataFrames and files, converting results."
  - title: "Reading and writing Parquet files"
    url: "https://duckdb.org/docs/stable/data/parquet/overview"
    source: "DuckDB official docs"
    note: "Querying Parquet directly and COPY ... TO for exporting."
  - title: "Scaling to large datasets"
    url: "https://pandas.pydata.org/docs/user_guide/scale.html"
    source: "pandas official docs"
    note: "Load fewer columns, use efficient types, use Parquet, chunk."
---

## What is it?

- **DuckDB** is an analytical SQL database that runs **inside your Python process**: `pip install duckdb` and you have it. No server, no accounts. It can query CSV and Parquet files and pandas/Polars DataFrames directly.
- **Parquet** is a **columnar** file format: compressed, typed, and fast to read one column at a time. CSV is plain text, row by row.
- **Working with larger local data** means getting answers from millions of rows on a laptop by reading less, using better formats and choosing the right engine.

!!! job "Why it matters at work"
    Many analyses are "too big for Excel, too small to justify a cloud warehouse". DuckDB and Parquet fill that gap and are now common in data teams for local analysis, testing pipelines and even small production jobs. Your SQL from Phase 1 transfers directly.

The script is `08_duckdb_larger_data.py`. Run `make_big_data.py` first: it creates a 2-million-row synthetic file in `data/` (as CSV and Parquet).

## Example 1: SQL directly on a CSV file

```python
import duckdb

print(duckdb.__version__)
print(duckdb.sql("""
    SELECT region, COUNT(*) AS orders, ROUND(SUM(revenue), 0) AS revenue
    FROM 'data/orders_2025.csv'
    WHERE status <> 'Cancelled'
    GROUP BY region
    ORDER BY revenue DESC
"""))
```

```text
1.5.6
┌─────────────┬────────┬───────────┐
│   region    │ orders │  revenue  │
│   varchar   │ int64  │  double   │
├─────────────┼────────┼───────────┤
│ Chattogram  │   1433 │ 2057404.0 │
│ Dhaka       │   1301 │ 1835497.0 │
│ Narayanganj │    447 │  583516.0 │
│ Gazipur     │    469 │  571973.0 │
│ Khulna      │    313 │  429968.0 │
└─────────────┴────────┴───────────┘
```

A file path in quotes works as a table name. Same numbers as pandas and Polars.

## Example 2: SQL on a pandas DataFrame

```python
import pandas as pd

customers = pd.read_csv("data/customers_2025.csv")
top = duckdb.sql("""
    SELECT c.customer_name, c.credit_days, ROUND(SUM(o.revenue), 0) AS revenue
    FROM 'data/orders_2025.csv' AS o
    JOIN customers AS c USING (customer_id)
    WHERE o.status <> 'Cancelled'
    GROUP BY ALL
    ORDER BY revenue DESC
    LIMIT 3
""").df()
print(type(top).__name__)
print(top)
```

```text
DataFrame
    customer_name  credit_days   revenue
0   Ocean Apparel           15  295414.0
1  Prime Garments           60  255781.0
2  Silver Fashion            0  225647.0
```

- DuckDB finds the Python variable `customers` by name and joins it to the CSV.
- `GROUP BY ALL` groups by every non-aggregated column (a DuckDB convenience).
- `.df()` returns pandas; `.pl()` returns Polars; `.fetchall()` returns Python tuples.

## Example 3: window functions

```python
print(duckdb.sql("""
    SELECT month(order_date) AS m,
           ROUND(SUM(revenue), 0) AS revenue,
           ROUND(SUM(SUM(revenue)) OVER (ORDER BY month(order_date)), 0) AS running_total
    FROM 'data/orders_2025.csv'
    WHERE status <> 'Cancelled'
    GROUP BY m ORDER BY m LIMIT 4
"""))
```

```text
┌───────┬──────────┬───────────────┐
│   m   │ revenue  │ running_total │
│ int64 │  double  │    double     │
├───────┼──────────┼───────────────┤
│     1 │ 330192.0 │      330192.0 │
│     2 │ 335736.0 │      665928.0 │
│     3 │ 324249.0 │      990177.0 │
│     4 │ 336682.0 │     1326859.0 │
└───────┴──────────┴───────────────┘
```

A year-to-date running total in one query. (Window functions are covered fully in Phase 3's Advanced SQL.)

## Example 4: larger data — the file format matters

The 2-million-row file:

```text
data/orders_big.csv 131 MB
data/orders_big.parquet 22 MB
```

Same data, **6× smaller** as Parquet: it's compressed column by column and stores types (no re-parsing text).

```python
big = timed("pandas read_csv (all columns)", lambda: pd.read_csv("data/orders_big.csv"))
print(f"pandas memory: {big.memory_usage(deep=True).sum() / 1e6:.0f} MB, rows: {len(big):,}")
timed("pandas read_parquet (2 columns)", lambda: pd.read_parquet("data/orders_big.parquet", columns=["region", "quantity"]))
```

```text
pandas read_csv (all columns)       1.83 s
pandas memory: 215 MB, rows: 2,000,000
pandas read_parquet (2 columns)     0.06 s
```

(`timed` is a small helper in the script that prints how long a step took. Timings are from one run on our build machine; yours will differ, but the ratios hold.) Reading **only the columns you need** from Parquet is about 30× faster than reading the whole CSV.

## Example 5: one question, three engines, 2 million rows

*"Net 2025 revenue and orders by region"*:

```python
QUERY = """
    SELECT region, COUNT(*) AS orders, ROUND(SUM(quantity * unit_price), 0) AS revenue
    FROM 'data/orders_big.parquet'
    WHERE status <> 'Cancelled' AND year(order_date) = 2025
    GROUP BY region ORDER BY revenue DESC
"""
res_duck = timed("DuckDB SQL on Parquet", lambda: duckdb.sql(QUERY).df())
```

The Polars version uses `scan_parquet(...).filter(...).group_by(...).agg(...).collect()`, and the pandas version reads 5 columns, filters, then groups (both are in the script).

```text
DuckDB SQL on Parquet               0.03 s
Polars lazy scan_parquet            0.04 s
pandas read_parquet + groupby       0.26 s
        region  orders     revenue
0        Dhaka  127781  98557119.0
1   Chattogram   82445  64583892.0
2      Gazipur   75390  58494988.0
3  Narayanganj   52444  40485666.0
4       Khulna   37357  29121935.0
True True
```

All three agree (`True True`). DuckDB and Polars are several times faster because they **push the filter and column choice into the file scan** and use all CPU cores; pandas loads the columns first and filters afterwards.

## A practical playbook for "too slow" data

| Step | Why |
|---|---|
| 1. Store data as **Parquet**, not CSV | Smaller, typed, column-selective |
| 2. Read **only the columns** you need | Less memory, faster |
| 3. **Filter early**, ideally in the scan (DuckDB, Polars lazy) | Rows never enter memory |
| 4. Use efficient types (`category` for repeated text, smaller ints) | pandas memory drops a lot |
| 5. Aggregate in DuckDB/Polars, hand the small result to pandas | Use each tool for what it's best at |
| 6. Still too big? Partition files (by year/month) or move to a warehouse (Phase 3) | Scale beyond one machine |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Loading a huge CSV "just to look" | Memory errors, long waits | `duckdb.sql("SELECT * FROM 'f.csv' LIMIT 10")` or `scan_csv(...).head().collect()` |
| Keeping big data as CSV | Re-parsing text on every run | Convert once to Parquet |
| Comparing tools on one tiny run | Misleading benchmarks | Several runs, realistic data, same question, check results match |
| Treating DuckDB as a shared server database | Concurrency surprises | It's for local/embedded analytics; use PostgreSQL etc. for many writers |
| Forgetting `.df()` | You get a DuckDB relation, not a DataFrame | `.df()` / `.pl()` at the end |

## Try it yourself

**Task:** With DuckDB, write a summary of **delivered units per year and product** from `orders_big.parquet` to a new Parquet file, `data/units_by_year.parquet`. Read it with Polars and show Zippers by year.

<details markdown="1">
<summary>Show a hint</summary>

`COPY (SELECT …) TO 'file.parquet' (FORMAT parquet)` writes any query result to a file.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
duckdb.sql("""
    COPY (
        SELECT year(order_date) AS year, product, SUM(quantity)::BIGINT AS units
        FROM 'data/orders_big.parquet' WHERE status = 'Delivered'
        GROUP BY ALL
    ) TO 'data/units_by_year.parquet' (FORMAT parquet)
""")
summary = pl.read_parquet("data/units_by_year.parquet")
print(summary.shape)
print(summary.filter(pl.col("product") == "Zippers").sort("year"))
```

```text
(60, 3)
shape: (5, 3)
┌──────┬─────────┬──────────┐
│ year ┆ product ┆ units    │
│ ---  ┆ ---     ┆ ---      │
│ i64  ┆ str     ┆ i64      │
╞══════╪═════════╪══════════╡
│ 2021 ┆ Zippers ┆ 11002774 │
│ 2022 ┆ Zippers ┆ 10961713 │
│ 2023 ┆ Zippers ┆ 11108952 │
│ 2024 ┆ Zippers ┆ 10968963 │
│ 2025 ┆ Zippers ┆ 10927947 │
└──────┴─────────┴──────────┘
```

5 years × 12 products = 60 rows. `::BIGINT` keeps the total a whole number (without it, the sum comes back as a float). A 2-million-row file became a 60-row file that any tool, including Excel or Power BI, can use.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does "in-process" mean for DuckDB?

1. It needs a separate database server
2. It runs inside your Python program, with nothing else to install or start
3. It only works in the cloud

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why is Parquet usually faster than CSV for analysis?

1. It's a text format
2. It's columnar, compressed and typed, so tools read only the needed columns without parsing text
3. It stores fewer rows

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Your pandas script runs out of memory on a 5 GB CSV. What's the best first step?

1. Buy more RAM
2. Read only needed columns, ideally from Parquet, and filter/aggregate with DuckDB or Polars
3. Split the CSV by hand in Excel

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- DuckDB = SQL inside Python: query CSV, Parquet and DataFrames directly; return results with `.df()` or `.pl()`.
- Parquet is smaller and much faster than CSV; read only the columns you need.
- For millions of rows, push filters and column selection into the scan (DuckDB, Polars lazy), then hand small results to pandas.
- Always check that different tools give the same answer.

!!! job "Job-ready check"
    **Interview question:** *"You have 50 million rows of sales history on your laptop. How do you analyse it?"*

    **Strong answer:** "I'd convert it to Parquet once, partitioned by year if it's very large, then query it with DuckDB or Polars lazy so only the needed columns and filtered rows are read. I aggregate there and bring the small result into pandas for charts or modelling. If it keeps growing or several people need it, it belongs in a warehouse."

    **Mini project:** Run `make_big_data.py` with 5,000,000 rows. Time the region summary in DuckDB, Polars and pandas, three runs each, and write a short table of median timings and file sizes with your machine's specs.
