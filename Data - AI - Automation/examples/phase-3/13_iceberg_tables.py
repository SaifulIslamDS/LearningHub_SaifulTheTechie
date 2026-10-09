"""Phase 3 · Lakehouse · Apache Iceberg tables: catalog, snapshots, schema evolution, time travel.

Runs locally with PyIceberg and a SQLite catalog (no server, no cloud):
    uv add "pyiceberg[sql-sqlite,pyarrow]" pandas
"""
import shutil
from pathlib import Path

import pandas as pd
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.types import StringType

WH = Path("iceberg_warehouse").absolute()
shutil.rmtree(WH, ignore_errors=True)
WH.mkdir()

# %% 1. A catalog keeps track of tables; the data and metadata are plain files in the warehouse folder
catalog = SqlCatalog("local", uri=f"sqlite:///{WH}/catalog.db", warehouse=f"file://{WH}")
catalog.create_namespace("sales")

orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
orders["order_date"] = orders["order_date"].dt.date
h1 = pa.Table.from_pandas(orders[orders["order_date"] < pd.Timestamp("2025-07-01").date()], preserve_index=False)
h2 = pa.Table.from_pandas(orders[orders["order_date"] >= pd.Timestamp("2025-07-01").date()], preserve_index=False)

table = catalog.create_table("sales.orders", schema=h1.schema)
table.append(h1)                                   # snapshot 1
table.append(h2)                                   # snapshot 2
print("rows:", len(table.scan().to_arrow()), "| snapshots:", len(table.snapshots()))

# %% 2. Read with a filter: Iceberg prunes files using column statistics in its metadata
dhaka_q4 = table.scan(row_filter="region == 'Dhaka' and order_date >= '2025-10-01'",
                      selected_fields=("order_id", "revenue")).to_pandas()
print("Dhaka Q4 orders:", len(dhaka_q4), "| revenue", round(dhaka_q4["revenue"].sum(), 2))

# %% 3. Schema evolution: add a column without rewriting any data
with table.update_schema() as update:
    update.add_column("sales_rep", StringType(), doc="assigned rep, from the CRM (new in 2026)")
print([f.name for f in table.schema().fields][-3:])
print("old rows show nulls:", table.scan(selected_fields=("sales_rep",)).to_pandas()["sales_rep"].isna().all())

# %% 4. Time travel: read the table as it was after the first snapshot
first = table.snapshots()[0].snapshot_id
print("rows at snapshot 1:", len(table.scan(snapshot_id=first).to_arrow()),
      "| rows now:", len(table.scan().to_arrow()))

# %% 5. What's on disk: Parquet data files + JSON/Avro metadata
files = sorted(p.relative_to(WH).as_posix() for p in WH.rglob("*") if p.is_file())
print(len([f for f in files if f.endswith(".parquet")]), "parquet data files |",
      len([f for f in files if f.endswith(".metadata.json")]), "metadata.json versions |",
      len([f for f in files if f.endswith(".avro")]), "avro manifest files")

# %% Try it yourself — solution: count cancelled orders per snapshot
for n, snap in enumerate(table.snapshots(), start=1):
    t = table.scan(snapshot_id=snap.snapshot_id, row_filter="status == 'Cancelled'").to_arrow()
    print(f"snapshot {n} ->", len(t), "cancelled orders")
