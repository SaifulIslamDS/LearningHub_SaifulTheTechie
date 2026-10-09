pandas is the standard, but two newer tools have become very popular for speed and bigger-than-comfortable data on a single laptop:

- **Polars**: a fast DataFrame library written in Rust, with a clean expression syntax and a *lazy* mode that optimises your whole query before running it.
- **DuckDB**: an in-process SQL database. No server to install: it runs inside Python and queries CSV, Parquet and DataFrames directly with SQL.

These lessons use **Polars 2.0** and **DuckDB 1.5** (October 2026). Both change quickly, so check the version you install with `pl.__version__` and `duckdb.__version__`.

**By the end of this module you can:** write Polars expressions and lazy queries, run SQL on files and DataFrames with DuckDB, and choose file formats and tools for data that is too slow for plain pandas.
