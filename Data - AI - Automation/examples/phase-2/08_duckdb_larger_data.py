"""Phase 2 · DuckDB in-process SQL & working with larger local data.
Run make_big_data.py first to create data/orders_big.csv and data/orders_big.parquet (2 million rows)."""

# %% 1. SQL directly on a CSV file
import time

import duckdb

print(duckdb.__version__)
print(duckdb.sql("""
    SELECT region, COUNT(*) AS orders, ROUND(SUM(revenue), 0) AS revenue
    FROM 'data/orders_2025.csv'
    WHERE status <> 'Cancelled'
    GROUP BY region
    ORDER BY revenue DESC
"""))

# %% 2. SQL on a pandas DataFrame, result back to pandas
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

# %% 3. Window functions: each month's revenue and running total
print(duckdb.sql("""
    SELECT month(order_date) AS m,
           ROUND(SUM(revenue), 0) AS revenue,
           ROUND(SUM(SUM(revenue)) OVER (ORDER BY month(order_date)), 0) AS running_total
    FROM 'data/orders_2025.csv'
    WHERE status <> 'Cancelled'
    GROUP BY m ORDER BY m LIMIT 4
"""))

# %% 4. Larger data: file formats
from pathlib import Path

for f in ["data/orders_big.csv", "data/orders_big.parquet"]:
    print(f, f"{Path(f).stat().st_size / 1e6:.0f} MB")


def timed(label, fn):
    t = time.perf_counter()
    out = fn()
    print(f"{label:<34}{time.perf_counter() - t:6.2f} s")
    return out


# %% 5. pandas: read everything, then summarise
big = timed("pandas read_csv (all columns)", lambda: pd.read_csv("data/orders_big.csv"))
print(f"pandas memory: {big.memory_usage(deep=True).sum() / 1e6:.0f} MB, rows: {len(big):,}")
timed("pandas read_parquet (2 columns)", lambda: pd.read_parquet("data/orders_big.parquet", columns=["region", "quantity"]))
del big

# %% 6. The same question three ways on 2 million rows
QUERY = """
    SELECT region, COUNT(*) AS orders, ROUND(SUM(quantity * unit_price), 0) AS revenue
    FROM 'data/orders_big.parquet'
    WHERE status <> 'Cancelled' AND year(order_date) = 2025
    GROUP BY region ORDER BY revenue DESC
"""
res_duck = timed("DuckDB SQL on Parquet", lambda: duckdb.sql(QUERY).df())

import polars as pl

res_pl = timed("Polars lazy scan_parquet", lambda: (
    pl.scan_parquet("data/orders_big.parquet")
    .filter((pl.col("status") != "Cancelled") & (pl.col("order_date").dt.year() == 2025))
    .group_by("region")
    .agg(pl.len().alias("orders"), (pl.col("quantity") * pl.col("unit_price")).sum().round(0).alias("revenue"))
    .sort("revenue", descending=True)
    .collect()))


def with_pandas():
    d = pd.read_parquet("data/orders_big.parquet", columns=["order_date", "region", "quantity", "unit_price", "status"])
    d = d[(d["status"] != "Cancelled") & (d["order_date"].dt.year == 2025)]
    return (d.assign(revenue=d["quantity"] * d["unit_price"]).groupby("region")
             .agg(orders=("region", "size"), revenue=("revenue", "sum")).round(0)
             .sort_values("revenue", ascending=False))


res_pd = timed("pandas read_parquet + groupby", with_pandas)
print(res_duck)
print(res_pl["orders"].to_list() == res_duck["orders"].to_list(), res_pd["orders"].to_list() == res_duck["orders"].to_list())

# %% Try it yourself — solution: export a summary to Parquet with DuckDB, read it back with Polars
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
