"""Phase 3 · Lakehouse · Delta Lake tables and the medallion layers (bronze, silver, gold).

Runs locally with the `deltalake` package (delta-rs, no Spark needed):
    uv add deltalake pandas pyarrow
"""
import shutil
from pathlib import Path

import pandas as pd
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

LAKE = Path("lake")
shutil.rmtree(LAKE, ignore_errors=True)
BRONZE, SILVER, GOLD = LAKE / "bronze/orders", LAKE / "silver/orders", LAKE / "gold/monthly_revenue"

# %% 1. BRONZE: land the raw export exactly as received (all text), plus load metadata
raw = pd.read_csv("data/orders_2025_raw.csv", dtype=str)
raw["_source_file"] = "orders_2025_raw.csv"
raw["_loaded_at"] = "2026-01-02T06:00:00"            # fixed here so the example is reproducible
write_deltalake(BRONZE, raw, mode="overwrite")
bronze = DeltaTable(BRONZE)
print("bronze version", bronze.version(), "|", len(bronze.to_pandas()), "rows |", len(bronze.file_uris()), "data file(s)")

# %% 2. SILVER: clean, typed, de-duplicated, one row per order
df = bronze.to_pandas().drop(columns=["_source_file", "_loaded_at"]).drop_duplicates()
df.columns = [c.lower().replace(" ", "_") for c in df.columns]
df = df.rename(columns={"qty": "quantity"})
df["region"] = df["region"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.title()
df["quantity"] = pd.to_numeric(df["quantity"].str.replace(",", "")).abs()      # negative = typing error (Cleaning lesson)
df["unit_price"] = pd.to_numeric(df["unit_price"])
median_price = df.groupby("product")["unit_price"].transform("median")
df.loc[df["unit_price"] / median_price > 10, "unit_price"] /= 100             # 350 -> 3.50 decimal slip
df["order_id"] = df["order_id"].astype("int64")
df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
df["discount"] = pd.to_numeric(df["discount"])
df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
silver = df[["order_id", "order_date", "customer_id", "region", "segment", "channel", "product", "category",
             "quantity", "unit_price", "discount", "status", "revenue"]]
write_deltalake(SILVER, silver, mode="overwrite", partition_by=["region"])
print("silver:", len(silver), "rows, partitioned by region ->",
      sorted(p.name for p in SILVER.iterdir() if p.is_dir() and p.name.startswith("region=")))

# %% 3. GOLD: a business-ready aggregate for BI tools
s = DeltaTable(SILVER).to_pandas()
s = s[s["status"] != "Cancelled"]
gold = (s.assign(month=pd.to_datetime(s["order_date"]).dt.to_period("M").astype(str))
          .groupby(["month", "segment"], as_index=False)["revenue"].sum().round(2))
write_deltalake(GOLD, gold, mode="overwrite")
print("gold:", len(gold), "rows | net revenue", round(gold["revenue"].sum(), 2))

# %% 4. Schema enforcement: a bad append is rejected, the table is unchanged
bad = pd.DataFrame({"month": ["2026-01"], "segment": ["Trader"], "revenue": ["a lot"]})
try:
    write_deltalake(GOLD, bad, mode="append")
except Exception as exc:                                    # deltalake raises a schema-mismatch error
    print("rejected append:", str(exc).splitlines()[0][:110])
print("gold still has", len(DeltaTable(GOLD).to_pandas()), "rows")

# %% 5. MERGE (upsert): a late correction for one order arrives in silver
fix = pa.table({"order_id": pa.array([10001], pa.int64()), "status": ["Cancelled"]})
dt = DeltaTable(SILVER)
(dt.merge(fix, predicate="t.order_id = s.order_id", source_alias="s", target_alias="t")
   .when_matched_update(updates={"status": "s.status"})
   .execute())
print("silver version", DeltaTable(SILVER).version(), "| order 10001 now:",
      DeltaTable(SILVER).to_pandas().query("order_id == 10001")["status"].item())

# %% 6. Time travel: every write is a version in the transaction log (_delta_log)
v0 = DeltaTable(SILVER, version=0).to_pandas().query("order_id == 10001")["status"].item()
print("version 0 said:", v0)
for h in DeltaTable(SILVER).history():
    print(" ", h["version"], h["operation"])

# %% Try it yourself — solution: gold revenue for Q4 by segment, read straight from the Delta table
g = DeltaTable(GOLD).to_pandas()
print(g[g["month"] >= "2025-10"].groupby("segment")["revenue"].sum().round(0).sort_values(ascending=False))
