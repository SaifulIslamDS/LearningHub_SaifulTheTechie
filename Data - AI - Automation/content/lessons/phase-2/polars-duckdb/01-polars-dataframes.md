---
title: "Polars DataFrames: Fast Expressions and Lazy Queries"
order: 1
summary: "Load data with Polars, transform it with expressions (filter, with_columns, group_by, join), and use lazy mode so Polars optimises the whole query before running it."
level: Intermediate
time: "45 min"
topics: ["Polars DataFrames"]
prerequisites: ["phase-2/pandas/03-merge-groupby"]
keywords: [polars, dataframe, expression, pl.col, filter, with_columns, group_by, agg, join, lazy, scan_csv, collect, explain, query optimization, predicate pushdown, projection pushdown, rust]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, phase-2/customers_2025.csv]
resources:
  - title: "Polars user guide — Getting started"
    url: "https://docs.pola.rs/user-guide/getting-started/"
    source: "Polars official docs"
    note: "Reading data, expressions, contexts and joins."
  - title: "Lazy API"
    url: "https://docs.pola.rs/user-guide/lazy/"
    source: "Polars official docs"
    note: "Why lazy queries are faster, and how to read a query plan."
  - title: "Coming from pandas"
    url: "https://docs.pola.rs/user-guide/migration/pandas/"
    source: "Polars official docs"
    note: "Key differences for pandas users."
---

## What is it?

**Polars** is a DataFrame library (like pandas) built for speed: it's written in Rust, uses all CPU cores, and stores data in the Apache Arrow column format.

| | pandas | Polars |
|---|---|---|
| Style | Methods and indexing (`df[df.x > 1]`) | **Expressions** (`df.filter(pl.col("x") > 1)`) |
| Row index | Yes | No: rows are just rows |
| Execution | Eager (runs each line) | Eager **or lazy** (plans first, then runs) |
| Speed on large data | Good | Usually much faster, uses all cores |
| Ecosystem | Huge (most tutorials, libraries) | Growing quickly; converts to/from pandas |

!!! job "Why it matters at work"
    Data teams increasingly use Polars for pipelines that were slow in pandas, and job adverts have started listing it next to pandas. Learning its expression style also prepares you for Spark and SQL-style thinking used in data engineering (Phase 3).

The script is `07_polars.py` (Polars 2.0).

## Example 1: read and inspect

```python
import polars as pl

orders = pl.read_csv("data/orders_2025.csv", try_parse_dates=True)
print(orders.shape)
print(orders.select("order_id", "order_date", "region", "status", "revenue").head(3))
```

```text
(4246, 16)
shape: (3, 5)
┌──────────┬────────────┬─────────────┬───────────┬─────────┐
│ order_id ┆ order_date ┆ region      ┆ status    ┆ revenue │
│ ---      ┆ ---        ┆ ---         ┆ ---       ┆ ---     │
│ i64      ┆ date       ┆ str         ┆ str       ┆ f64     │
╞══════════╪════════════╪═════════════╪═══════════╪═════════╡
│ 10001    ┆ 2025-01-01 ┆ Chattogram  ┆ Delivered ┆ 189.26  │
│ 10002    ┆ 2025-01-01 ┆ Narayanganj ┆ Cancelled ┆ 834.56  │
│ 10003    ┆ 2025-01-01 ┆ Gazipur     ┆ Delivered ┆ 248.11  │
└──────────┴────────────┴─────────────┴───────────┴─────────┘
```

Types are shown under each column name. `try_parse_dates=True` already turned `order_date` into a real `date`.

## Example 2: expressions

```python
net = (
    orders
    .filter(pl.col("status") != "Cancelled")
    .with_columns(
        (pl.col("quantity") * pl.col("unit_cost")).alias("cost"),
        pl.col("order_date").dt.month().alias("month"),
    )
)
print(net.select("order_id", "revenue", "cost", "month").head(3))
```

```text
shape: (3, 4)
┌──────────┬─────────┬────────┬───────┐
│ order_id ┆ revenue ┆ cost   ┆ month │
│ ---      ┆ ---     ┆ ---    ┆ ---   │
│ i64      ┆ f64     ┆ f64    ┆ i8    │
╞══════════╪═════════╪════════╪═══════╡
│ 10001    ┆ 189.26  ┆ 115.4  ┆ 1     │
│ 10003    ┆ 248.11  ┆ 159.25 ┆ 1     │
│ 10004    ┆ 1988.18 ┆ 1614.0 ┆ 1     │
└──────────┴─────────┴────────┴───────┘
```

An **expression** (`pl.col("quantity") * pl.col("unit_cost")`) describes a calculation on columns. Polars runs the expressions inside one `with_columns` **in parallel**. Methods chain top to bottom, so the code reads like a recipe.

| pandas | Polars |
|---|---|
| `df[df["status"] != "Cancelled"]` | `df.filter(pl.col("status") != "Cancelled")` |
| `df["cost"] = df.quantity * df.unit_cost` | `df.with_columns((pl.col("quantity") * pl.col("unit_cost")).alias("cost"))` |
| `df[["a", "b"]]` | `df.select("a", "b")` |
| `df.groupby("x").agg(...)` | `df.group_by("x").agg(...)` |
| `df.sort_values("x", ascending=False)` | `df.sort("x", descending=True)` |

## Example 3: group_by and agg

```python
by_region = (
    net.group_by("region")
    .agg(
        pl.len().alias("orders"),
        pl.col("revenue").sum().round(0).alias("revenue"),
        ((1 - pl.col("cost").sum() / pl.col("revenue").sum()) * 100).round(1).alias("margin_pct"),
    )
    .sort("revenue", descending=True)
)
print(by_region)
```

```text
shape: (5, 4)
┌─────────────┬────────┬────────────┬────────────┐
│ region      ┆ orders ┆ revenue    ┆ margin_pct │
│ ---         ┆ ---    ┆ ---        ┆ ---        │
│ str         ┆ u32    ┆ f64        ┆ f64        │
╞═════════════╪════════╪════════════╪════════════╡
│ Chattogram  ┆ 1433   ┆ 2.057404e6 ┆ 25.6       │
│ Dhaka       ┆ 1301   ┆ 1.835497e6 ┆ 25.6       │
│ Narayanganj ┆ 447    ┆ 583516.0   ┆ 24.9       │
│ Gazipur     ┆ 469    ┆ 571973.0   ┆ 25.3       │
│ Khulna      ┆ 313    ┆ 429968.0   ┆ 25.7       │
└─────────────┴────────┴────────────┴────────────┘
```

The same regional totals as pandas (2.057404e6 = 2,057,404). Polars shows big floats in scientific notation; `pl.Config(float_precision=0)` or casting to integers changes the display. **Note:** `group_by` doesn't keep a stable group order, so always `sort` when order matters.

## Example 4: join

```python
customers = pl.read_csv("data/customers_2025.csv")
joined = net.join(customers.select("customer_id", "customer_name", "credit_days"), on="customer_id",
                  how="left", validate="m:1")
print(joined.select("order_id", "customer_name", "credit_days").head(3))
```

```text
shape: (3, 3)
┌──────────┬──────────────────┬─────────────┐
│ order_id ┆ customer_name    ┆ credit_days │
│ ---      ┆ ---              ┆ ---         │
│ i64      ┆ str              ┆ i64         │
╞══════════╪══════════════════╪═════════════╡
│ 10001    ┆ Padma Knitting   ┆ 15          │
│ 10003    ┆ Ocean Enterprise ┆ 15          │
│ 10004    ┆ Jamuna Knit      ┆ 30          │
└──────────┴──────────────────┴─────────────┘
```

`validate="m:1"` is the same safety check as in pandas.

## Example 5: lazy mode and the query plan

```python
lazy = (
    pl.scan_csv("data/orders_2025.csv", try_parse_dates=True)
    .filter(pl.col("status") == "Delivered")
    .group_by(pl.col("order_date").dt.month().alias("month"))
    .agg(pl.col("delivery_days").mean().round(2).alias("avg_days"))
    .sort("month")
)
print(lazy.explain())
print(lazy.collect().head(4))
```

```text
SORT BY [col("month")]
  AGGREGATE[maintain_order: false]
    [col("delivery_days").mean().round().alias("avg_days")] BY [col("order_date").dt.month().alias("month")]
    FROM
    simple π 2/2 ["order_date", "delivery_days"]
      Csv SCAN [data/orders_2025.csv]
      PROJECT 3/16 COLUMNS
      SELECTION: col("status") == "Delivered"
      ESTIMATED ROWS: 4130
shape: (4, 2)
┌───────┬──────────┐
│ month ┆ avg_days │
│ ---   ┆ ---      │
│ i8    ┆ f64      │
╞═══════╪══════════╡
│ 1     ┆ 3.14     │
│ 2     ┆ 3.11     │
│ 3     ┆ 2.92     │
│ 4     ┆ 3.17     │
└───────┴──────────┘
```

`scan_csv` reads **nothing** yet; it builds a plan. Read the plan from the bottom up:

- **`PROJECT 3/16 COLUMNS`**: Polars will read only the 3 columns it needs (*projection pushdown*).
- **`SELECTION: col("status") == "Delivered"`**: the filter is applied **while reading** (*predicate pushdown*), so unneeded rows never enter memory.
- `.collect()` runs the optimised plan.

On a 2-million-row file this is the difference between "fits easily" and "out of memory" (next lesson).

## Example 6: same answer as pandas?

```python
import pandas as pd

pd_total = pd.read_csv("data/orders_2025.csv").query("status != 'Cancelled'")["revenue"].sum()
pl_total = net["revenue"].sum()
print(round(pd_total, 2), round(pl_total, 2))
```

```text
5478357.79 5478357.79
```

Always reconcile a new tool against a known answer. Convert between them with `pl.from_pandas(df)` and `df_pl.to_pandas()`.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Writing pandas syntax (`df[df.x > 1]`, `df["new"] = …`) | Errors or unexpected results | `filter`, `with_columns`, `select` |
| Forgetting `.alias()` | The new column overwrites or is named after the input | Name every derived column |
| Expecting group order | Groups come back in random order | `.sort(...)` after `group_by` |
| Using `read_csv` for big files | Everything loads, then you filter | `scan_csv` / `scan_parquet` + `collect()` |
| Forgetting `.collect()` | You print a plan, not data | Call `.collect()` at the end of a lazy query |

## Try it yourself

**Task:** In Polars, calculate the **cancellation rate (%) by channel**, with the number of orders, highest rate first.

<details markdown="1">
<summary>Show a hint</summary>

`(pl.col("status") == "Cancelled").mean()` gives the share of cancelled orders in each group.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
rate = (
    orders.group_by("channel")
    .agg((pl.col("status") == "Cancelled").mean().mul(100).round(1).alias("cancel_pct"), pl.len().alias("orders"))
    .sort("cancel_pct", descending=True)
)
print(rate)
```

```text
shape: (3, 3)
┌───────────┬────────────┬────────┐
│ channel   ┆ cancel_pct ┆ orders │
│ ---       ┆ ---        ┆ ---    │
│ str       ┆ f64        ┆ u32    │
╞═══════════╪════════════╪════════╡
│ Phone     ┆ 9.5        ┆ 796    │
│ Sales rep ┆ 6.3        ┆ 1244   │
│ Portal    ┆ 5.8        ┆ 2206   │
└───────────┴────────────┴────────┘
```

Phone orders are cancelled most often (9.5%). Is the channel the cause, or do certain customers prefer the phone? Hold that question for the Causal pitfalls lesson.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `pl.scan_csv(...)` return?

1. A DataFrame with all rows loaded
2. A lazy query plan that runs when you call `.collect()`
3. A list of column names

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What is "predicate pushdown"?

1. Applying the filter while reading the file, so fewer rows are loaded
2. Sorting rows before grouping
3. Pushing results to a database

<details markdown="1"><summary>Show answer</summary>
**A.** (Projection pushdown does the same for columns.)
</details>
</div>

<div class="quiz-q" markdown="1">
3\. How do you add a calculated column in Polars?

1. `df["cost"] = df["quantity"] * df["unit_cost"]`
2. `df.with_columns((pl.col("quantity") * pl.col("unit_cost")).alias("cost"))`
3. `df.add_column("cost")`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Polars uses **expressions** (`pl.col(...)`) inside `select`, `filter`, `with_columns`, `group_by().agg()` and `join`.
- No index; `group_by` order isn't guaranteed, so sort.
- **Lazy mode** (`scan_*` → plan → `collect()`) reads only the needed columns and rows; check with `explain()`.
- Reconcile with pandas or a known answer when switching tools.

!!! job "Job-ready check"
    **Interview question:** *"When would you choose Polars over pandas?"*

    **Strong answer:** "When data is large enough that pandas is slow or memory-hungry, or for a pipeline where performance matters. Polars' lazy engine pushes filters and column selection into the file scan and uses all cores. For small exploratory work or when a library expects pandas, I stay with pandas and convert at the boundary."

    **Mini project:** Rewrite the segment summary from the merge & groupby lesson (orders, revenue, average order, distinct customers, share) in Polars, and check that every number matches pandas.
