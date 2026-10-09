---
title: "Delta Lake & the Medallion Architecture: Bronze, Silver, Gold"
order: 1
summary: "Build a mini lakehouse on your laptop: land raw data in bronze, clean it into a partitioned silver Delta table, aggregate a gold table for BI, and use schema enforcement, MERGE and time travel."
level: Intermediate
time: "55 min"
topics: ["Delta Lake / Apache Iceberg", "Medallion layers"]
prerequisites: ["phase-3/data-ingestion/02-scraping-file-formats", "phase-2/pandas/02-cleaning"]
keywords: [lakehouse, data lake, delta lake, delta-rs, deltalake, open table format, transaction log, _delta_log, acid, time travel, versioning, schema enforcement, merge, upsert, partitioning, medallion architecture, bronze, silver, gold, raw layer, curated layer, parquet]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Delta Lake documentation"
    url: "https://docs.delta.io/latest/index.html"
    source: "Delta Lake (Linux Foundation)"
    note: "Concepts: transaction log, time travel, MERGE, schema enforcement."
  - title: "delta-rs Python documentation"
    url: "https://delta-io.github.io/delta-rs/"
    source: "delta-rs (official)"
    note: "The `deltalake` package used in this lesson (no Spark needed)."
  - title: "What is the medallion lakehouse architecture?"
    url: "https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion"
    source: "Microsoft Learn (Azure Databricks)"
    note: "Bronze, silver and gold layers explained."
---

## What is it?

- **Delta Lake** is an open **table format**: a folder of Parquet data files plus a `_delta_log/` folder recording every change as a numbered **commit**. That log adds **ACID transactions, versions (time travel), schema enforcement and MERGE** to plain files.
- The **medallion architecture** organises a lakehouse into three quality layers:

| Layer | Contents | Rules |
|---|---|---|
| 🥉 **Bronze** | Raw data exactly as received, plus load metadata | Append-only; never "fix" here; keep everything |
| 🥈 **Silver** | Cleaned, typed, de-duplicated, conformed | One row per business entity; tests and constraints |
| 🥇 **Gold** | Business-ready aggregates and models | Built for BI and ML (star schemas, KPI tables) |

!!! job "Why it matters at work"
    Databricks, Microsoft Fabric and many Spark-based platforms store their tables as Delta, and "bronze/silver/gold" is the vocabulary of most lakehouse projects. Being able to explain what the transaction log gives you, and to design the layers, is expected in data engineering interviews, and you can practise it all locally.

The script is `12_delta_medallion.py`. It uses `deltalake` (delta-rs), a Rust implementation with a Python API, so **no Spark or cluster** is needed.

## Step 1: bronze — land it raw

```python
raw = pd.read_csv("data/orders_2025_raw.csv", dtype=str)
raw["_source_file"] = "orders_2025_raw.csv"
raw["_loaded_at"] = "2026-01-02T06:00:00"            # fixed here so the example is reproducible
write_deltalake(BRONZE, raw, mode="overwrite")
```

```text
bronze version 0 | 4264 rows | 1 data file(s)
```

- Everything is read as **text** (`dtype=str`): bronze never guesses or converts.
- All 4,264 lines are kept, **duplicates and typos included** (the messy export from Phase 2).
- Load metadata (`_source_file`, `_loaded_at`) tells you where each row came from. In production `_loaded_at` is the real load time.

On disk, a Delta table is just files:

```text
lake/bronze/orders/
├── _delta_log/00000000000000000000.json    ← commit 0: "added this file, with this schema"
└── part-00000-…-c000.snappy.parquet       ← the data (Parquet, snappy-compressed)
```

## Step 2: silver — clean, typed, one row per order

The cleaning rules are the ones from the Phase 2 pandas Cleaning lesson:

```python
df = bronze.to_pandas().drop(columns=["_source_file", "_loaded_at"]).drop_duplicates()
df.columns = [c.lower().replace(" ", "_") for c in df.columns]
df = df.rename(columns={"qty": "quantity"})
df["region"] = df["region"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.title()
df["quantity"] = pd.to_numeric(df["quantity"].str.replace(",", "")).abs()      # negative = typing error (Cleaning lesson)
df["unit_price"] = pd.to_numeric(df["unit_price"])
median_price = df.groupby("product")["unit_price"].transform("median")
df.loc[df["unit_price"] / median_price > 10, "unit_price"] /= 100             # 350 -> 3.50 decimal slip
...
write_deltalake(SILVER, silver, mode="overwrite", partition_by=["region"])
```

```text
silver: 4246 rows, partitioned by region -> ['region=Chattogram', 'region=Dhaka', 'region=Gazipur', 'region=Khulna', 'region=Narayanganj']
```

- 4,264 bronze lines → **4,246 orders**, the known answer.
- `partition_by=["region"]` writes one sub-folder per region. Queries that filter on region read only that folder. Partition by a column you **filter on often** that has **few distinct values** (region, date by month); never by order ID.

## Step 3: gold — ready for BI

```python
gold = (s.assign(month=pd.to_datetime(s["order_date"]).dt.to_period("M").astype(str))
          .groupby(["month", "segment"], as_index=False)["revenue"].sum().round(2))
write_deltalake(GOLD, gold, mode="overwrite")
```

```text
gold: 48 rows | net revenue 5478357.79
```

12 months × 4 segments = 48 rows that a dashboard can read instantly, reconciling exactly to Phase 2's net revenue. Gold tables are shaped for one purpose: a BI model, a KPI table or ML features.

## Step 4: schema enforcement

Someone tries to append a row with revenue as text:

```python
bad = pd.DataFrame({"month": ["2026-01"], "segment": ["Trader"], "revenue": ["a lot"]})
write_deltalake(GOLD, bad, mode="append")
```

```text
rejected append: Cast error: Cannot cast string 'a lot' to value of Float64 type
gold still has 48 rows
```

The table's schema is stored in the log, and writes that don't fit are **rejected**, with nothing half-written. Plain Parquet folders accept any file you drop in, which is how data lakes became "data swamps".

## Step 5: MERGE — update rows in files

A correction arrives: order 10001 was actually cancelled. Parquet files can't be edited in place, but Delta's `MERGE` rewrites only the affected files and records a new version:

```python
fix = pa.table({"order_id": pa.array([10001], pa.int64()), "status": ["Cancelled"]})
dt = DeltaTable(SILVER)
(dt.merge(fix, predicate="t.order_id = s.order_id", source_alias="s", target_alias="t")
   .when_matched_update(updates={"status": "s.status"})
   .execute())
```

```text
silver version 1 | order 10001 now: Cancelled
```

`MERGE` (an "upsert") is how incremental loads and late corrections reach silver: update matching rows, insert new ones (`when_not_matched_insert`), even delete.

## Step 6: time travel

```python
v0 = DeltaTable(SILVER, version=0).to_pandas().query("order_id == 10001")["status"].item()
for h in DeltaTable(SILVER).history():
    print(" ", h["version"], h["operation"])
```

```text
version 0 said: Delivered
  1 MERGE
  0 WRITE
```

Every commit is a version you can read back: audit what changed, reproduce last month's report exactly, or restore after a bad load (`DeltaTable.restore`). Old files are kept until you `vacuum` them, which is a cost and retention decision.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Cleaning in bronze | The original data is lost; you can't reprocess | Bronze = raw + metadata, append-only |
| Partitioning by a high-cardinality column | Millions of tiny files, slow reads | Partition by low-cardinality filter columns (or not at all for small tables) |
| Gold tables nobody owns | Conflicting KPI versions | Each gold table has an owner and a definition |
| Never vacuuming | Storage grows forever | Set a retention period, then vacuum |
| Treating a lake folder as a table | No schema checks, partial writes visible | Use a table format (Delta/Iceberg) |

## Try it yourself

**Task:** Read the gold table and show Q4 (October–December) revenue by segment, largest first.

<details markdown="1">
<summary>Show the solution</summary>

```python
g = DeltaTable(GOLD).to_pandas()
print(g[g["month"] >= "2025-10"].groupby("segment")["revenue"].sum().round(0).sort_values(ascending=False))
```

```text
segment
Garment Factory    1365651.0
Knitting Mill       220870.0
Trader              110905.0
Retailer             31627.0
Name: revenue, dtype: float64
```

Reading 48 pre-aggregated rows instead of 4,246 orders: that's the point of gold. Garment factories bring 79% of Q4 revenue.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does the `_delta_log` folder add to a folder of Parquet files?

1. Compression
2. Transactions, versions (time travel), the schema and the list of valid files
3. Indexes

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. In which layer do you keep the raw export with its duplicates and typos?

1. Bronze
2. Silver
3. Gold

<details markdown="1"><summary>Show answer</summary>
**A.** Silver is where it gets cleaned.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A bad append with the wrong column types is attempted on a Delta table. What happens?

1. The bad rows are added
2. The write is rejected and the table is unchanged
3. The whole table is deleted

<details markdown="1"><summary>Show answer</summary>
**B.** Schema enforcement.
</details>
</div>

## Summary

- **Delta Lake** = Parquet files + a transaction log: ACID writes, schema enforcement, MERGE, versions and time travel.
- **Medallion**: bronze (raw + metadata, append-only) → silver (clean, typed, one row per entity) → gold (business-ready).
- Partition by low-cardinality filter columns; reconcile every layer to known answers (4,246 orders; 5,478,357.79).
- You can practise all of it locally with `deltalake`; the same concepts run at scale on Databricks and Fabric.

!!! job "Job-ready check"
    **Interview question:** *"Explain the medallion architecture and why you'd use it."*

    **Strong answer:** "Bronze stores raw data exactly as received, with load metadata, so we can always reprocess and audit. Silver holds cleaned, de-duplicated, typed data with one row per entity, built with idempotent MERGEs and tested. Gold holds business-level models and aggregates for BI and ML. Separating them makes failures recoverable, keeps cleaning logic in one place, and lets each layer have its own quality checks and owners. With a table format like Delta, every layer gets transactions and time travel."

    **Mini project:** Add a second bronze load (the December orders again with five changed statuses), then MERGE it into silver so statuses update and nothing duplicates, and rebuild gold. Show the table history.
