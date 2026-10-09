---
title: "Apache Iceberg & Lakehouse Platforms: Fabric, Databricks, Snowflake"
order: 2
summary: "Create, evolve and time-travel an Apache Iceberg table locally with PyIceberg, then compare how Microsoft Fabric, Databricks and Snowflake implement the lakehouse — and how to choose between them."
level: Intermediate
time: "50 min"
topics: ["Fabric, Databricks or Snowflake"]
prerequisites: ["phase-3/lakehouse/01-delta-lake-medallion"]
keywords: [apache iceberg, iceberg, pyiceberg, catalog, snapshot, schema evolution, hidden partitioning, metadata, manifest, delta vs iceberg, microsoft fabric, onelake, fabric lakehouse, databricks, unity catalog, snowflake, iceberg tables, lakehouse platform, vendor lock-in, open table format]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "PyIceberg documentation"
    url: "https://py.iceberg.apache.org/"
    source: "Apache Iceberg (official)"
    note: "Catalogs, tables, scans, schema evolution in Python."
  - title: "What is a lakehouse in Microsoft Fabric?"
    url: "https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview"
    source: "Microsoft Learn"
    note: "Fabric's lakehouse on OneLake, built on Delta tables."
  - title: "Apache Iceberg tables in Snowflake"
    url: "https://docs.snowflake.com/en/user-guide/tables-iceberg"
    source: "Snowflake docs"
    note: "Snowflake-managed and externally managed Iceberg tables."
  - title: "Try Databricks"
    url: "https://www.databricks.com/try"
    source: "Databricks"
    note: "Free options for learning, including the Free Edition."
---

## What is it?

- **Apache Iceberg** is the other major open **table format**. Like Delta Lake it adds transactions, snapshots, schema evolution and time travel to Parquet files. Its **catalog** (a registry of tables) makes the same table usable from many engines: Spark, Trino, Flink, DuckDB, Snowflake, BigQuery and more.
- **Lakehouse platforms** package storage, compute, a catalog, governance and tools. The three you'll meet most in job adverts are **Microsoft Fabric**, **Databricks** and **Snowflake**.

| | Delta Lake | Apache Iceberg |
|---|---|---|
| Origin | Databricks (now Linux Foundation) | Netflix (now Apache) |
| Metadata | `_delta_log/` JSON commits | Catalog → metadata JSON → manifest files (Avro) |
| Strengths | Deep Spark/Databricks/Fabric integration | Engine-neutral; hidden partitioning; wide vendor support |
| Today | Both are converging: platforms increasingly read and write both |

!!! job "Why it matters at work"
    Choosing a platform and table format is one of the biggest (and most expensive) decisions in a data team. Even as a junior, you'll be asked "Delta or Iceberg?", "why Fabric for us?" or "how would this work on Snowflake?". Knowing the concepts, which transfer across all three, matters more than any one product's buttons.

## Part 1: an Iceberg table on your laptop

The script is `13_iceberg_tables.py`. It uses **PyIceberg** with a SQLite catalog: no server, no cloud.

```python
catalog = SqlCatalog("local", uri=f"sqlite:///{WH}/catalog.db", warehouse=f"file://{WH}")
catalog.create_namespace("sales")
table = catalog.create_table("sales.orders", schema=h1.schema)
table.append(h1)                                   # snapshot 1: January–June
table.append(h2)                                   # snapshot 2: July–December
```

```text
rows: 4246 | snapshots: 2
```

Each `append` is an atomic commit that creates a **snapshot**.

### Filtered reads

```python
dhaka_q4 = table.scan(row_filter="region == 'Dhaka' and order_date >= '2025-10-01'",
                      selected_fields=("order_id", "revenue")).to_pandas()
```

```text
Dhaka Q4 orders: 434 | revenue 606561.85
```

Iceberg keeps **min/max statistics** per file in its manifests, so a scan can skip files that can't contain matching rows, and it reads only the selected columns.

### Schema evolution without rewriting data

```python
with table.update_schema() as update:
    update.add_column("sales_rep", StringType(), doc="assigned rep, from the CRM (new in 2026)")
```

```text
['delivery_days', 'revenue', 'sales_rep']
old rows show nulls: True
```

Adding a column is a **metadata-only** change: no data file is rewritten, and old rows read the new column as NULL. Iceberg tracks columns by ID, so renaming or reordering columns is safe too.

### Time travel by snapshot

```text
rows at snapshot 1: 1653 | rows now: 4246
```

### What's on disk

```text
2 parquet data files | 4 metadata.json versions | 4 avro manifest files
```

Data in Parquet; every change writes a new `metadata.json` (schema, partitioning, snapshot list) and manifests listing the data files. The **catalog** just points to the current metadata file, which is what lets several engines share one table safely.

## Part 2: the three platforms

| | **Microsoft Fabric** | **Databricks** | **Snowflake** |
|---|---|---|---|
| What it is | All-in-one SaaS analytics: lakehouse, warehouse, pipelines, Power BI | Data and AI platform built around Spark and Delta Lake | Cloud data warehouse, extended into a lakehouse |
| Storage | **OneLake** (one lake per organisation) | Your cloud storage (AWS, Azure, GCP) | Snowflake-managed, or your storage for Iceberg tables |
| Native table format | **Delta** (OneLake can also expose tables as Iceberg) | **Delta** (Unity Catalog also supports Iceberg) | Native tables, plus **Iceberg tables** |
| Main languages | SQL, PySpark, Dataflows (Power Query), DAX | PySpark, SQL, Python | SQL, Python (Snowpark) |
| Governance | Fabric/Purview | Unity Catalog | Horizon (built-in governance) |
| Typical fit | Microsoft/Power BI organisations; business-led analytics | Heavy data engineering, ML/AI, large Spark workloads | SQL-first analytics teams; data sharing |
| Try it | Fabric trial capacity | Databricks Free Edition | Free trial with credits |

*Products and free offers change often: check the official pages in the resources before you rely on details.*

### How to choose (the questions that matter)

1. **Where is your data and your team's skill set?** Power BI + Microsoft 365 points to Fabric; strong Python/Spark and ML to Databricks; SQL-heavy analysts to Snowflake.
2. **What are the workloads?** BI dashboards, large-scale engineering, ML training, real-time data, data sharing with partners?
3. **Cost model:** capacity-based (Fabric), compute clusters and DBUs (Databricks), credits per warehouse-second (Snowflake). Run a realistic pilot before committing.
4. **Openness:** storing tables as Delta or Iceberg in your own storage keeps the option to change engines later, so lock-in is about the **catalog and tools**, not the files.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Choosing a platform from a demo | Surprises on cost and fit | Pilot with your real workloads and data volumes |
| Proprietary formats for everything | Expensive migrations later | Prefer open table formats where it fits |
| Skipping the catalog | Engines disagree about what the table is | One catalog as the source of truth |
| Rewriting tables to add a column | Slow, risky migrations | Use schema evolution |
| Learning buttons instead of concepts | Skills that don't transfer | Learn formats, layers, SQL and Spark concepts |

## Try it yourself

**Task:** Count the **cancelled orders** visible in each snapshot of the Iceberg table. What does the difference tell you?

<details markdown="1">
<summary>Show the solution</summary>

```python
for n, snap in enumerate(table.snapshots(), start=1):
    t = table.scan(snapshot_id=snap.snapshot_id, row_filter="status == 'Cancelled'").to_arrow()
    print(f"snapshot {n} ->", len(t), "cancelled orders")
```

```text
snapshot 1 -> 116 cancelled orders
snapshot 2 -> 283 cancelled orders
```

Snapshot 1 (January–June only) has 116 cancellations; the full year has 283, the Phase 2 known answer. Time travel lets you reproduce "what the data said on a given day": essential for audits, debugging and comparing model training sets.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does adding a column to an Iceberg table rewrite?

1. Every data file
2. Only metadata; old rows read the new column as NULL
3. Nothing; it's not allowed

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which native table format does a Microsoft Fabric lakehouse use?

1. Iceberg
2. Delta
3. CSV

<details markdown="1"><summary>Show answer</summary>
**B.** OneLake can also make tables readable as Iceberg.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What mainly reduces lock-in when choosing a lakehouse platform?

1. Using the vendor's proprietary format
2. Storing tables in an open format (Delta or Iceberg) in storage you control
3. Using only notebooks

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Iceberg** = Parquet + metadata + manifests + a **catalog**: snapshots, schema evolution, time travel and file skipping, usable from many engines.
- **Delta** and **Iceberg** solve the same problem; platforms increasingly support both.
- **Fabric** (OneLake, Delta, Power BI), **Databricks** (Spark, Delta, Unity Catalog), **Snowflake** (SQL-first, Iceberg tables): choose by data, skills, workloads and cost, after a pilot.
- Concepts transfer; buttons don't.

!!! job "Job-ready check"
    **Interview question:** *"Delta Lake or Iceberg? And which platform would you pick for us?"*

    **Strong answer:** "Both are open table formats that add ACID transactions, schema evolution and time travel to Parquet. Delta is deepest in Databricks and Fabric; Iceberg is the most engine-neutral and widely supported, and the platforms now read each other's formats. For the platform I'd ask where the data and skills are and what the workloads are: a Power BI-centred team often fits Fabric, Spark- and ML-heavy work fits Databricks, SQL-first analytics fits Snowflake. Then I'd run a pilot on real data to compare cost and performance."

    **Mini project:** Write a one-page platform recommendation for the textile wholesaler (Power BI users, a small data team, 4,000 orders a year growing to 400,000), comparing two platforms on fit, cost model and lock-in, with a pilot plan.
