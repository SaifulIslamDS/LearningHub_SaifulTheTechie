A **lakehouse** stores data as open files (usually Parquet) in cheap object storage, like a data lake, but adds what used to need a warehouse: **tables** with schemas, transactions, updates, history and SQL. The magic is an **open table format** (Delta Lake or Apache Iceberg) that keeps a transaction log next to the data files. Microsoft Fabric, Databricks and Snowflake all build on these formats.

The scripts are `12_delta_medallion.py` and `13_iceberg_tables.py` in [data-engineering-scripts.zip](../../../downloads/phase-3/data-engineering-scripts.zip). Both run on your laptop, with no Spark and no cloud account:

```bash
uv add deltalake "pyiceberg[sql-sqlite,pyarrow]" pandas pyarrow
```

**By the end of this module you can:** explain what a table format adds to Parquet files, build bronze/silver/gold (medallion) layers with Delta Lake, use time travel, schema enforcement and MERGE, create and evolve an Iceberg table, and compare how Fabric, Databricks and Snowflake implement the lakehouse.
