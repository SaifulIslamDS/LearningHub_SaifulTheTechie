"""Phase 3 · Data warehousing · BigQuery: the same warehouse SQL in a cloud data warehouse.

BigQuery needs a Google Cloud project, so this script does the parts that run locally:
  1. translate our PostgreSQL query into BigQuery's SQL dialect (sqlglot)
  2. run the portable version on DuckDB, a local columnar engine, against the same data
  3. estimate how many bytes a BigQuery query would scan (what you pay for on demand)
    uv add sqlglot duckdb pyarrow pandas
"""
from pathlib import Path

import duckdb
import pandas as pd
import pyarrow.parquet as pq
import sqlglot

DATA = Path(__file__).parent / "data"

# %% 1. A PostgreSQL warehouse query (from the window-functions lesson) ...
pg_sql = """
WITH monthly AS (
    SELECT date_trunc('month', order_date)::date AS month,
           sum(quantity * unit_price * (1 - discount)) AS revenue
    FROM orders
    WHERE status <> 'Cancelled'
    GROUP BY 1
)
SELECT month, round(revenue, 0) AS revenue,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY month)) / lag(revenue) OVER (ORDER BY month), 1) AS mom_pct
FROM monthly
ORDER BY month
"""
# %% ... translated to BigQuery Standard SQL
bq_sql = sqlglot.transpile(pg_sql, read="postgres", write="bigquery", pretty=True)[0]
print(bq_sql)

# %% 2. Run the query locally on DuckDB (columnar, like BigQuery) against the CSV
con = duckdb.connect()
con.execute(f"CREATE VIEW orders AS SELECT * FROM read_csv_auto('{DATA / 'orders_2025.csv'}')")
duck_sql = sqlglot.transpile(pg_sql, read="postgres", write="duckdb")[0]
print(con.execute(duck_sql).df().head(4).to_string(index=False))

# %% 3. On-demand BigQuery bills by bytes SCANNED: only the columns you select count
pd.read_csv(DATA / "orders_2025.csv").to_parquet("orders_2025.parquet", index=False)
meta = pq.ParquetFile("orders_2025.parquet").metadata
col_bytes = {}
for rg in range(meta.num_row_groups):
    for i in range(meta.num_columns):
        col = meta.row_group(rg).column(i)
        col_bytes[col.path_in_schema] = col_bytes.get(col.path_in_schema, 0) + col.total_uncompressed_size
used = ["order_date", "quantity", "unit_price", "discount", "status"]
print(f"all columns: {sum(col_bytes.values()) / 1e3:.0f} KB | columns the query uses: "
      f"{sum(col_bytes[c] for c in used) / 1e3:.0f} KB ({sum(col_bytes[c] for c in used) / sum(col_bytes.values()):.0%})")

# %% Try it yourself — solution: translate a query that uses Postgres-only syntax
print(sqlglot.transpile("SELECT customer_id, string_agg(product, ', ') FROM orders GROUP BY 1 LIMIT 5",
                        read="postgres", write="bigquery")[0])
