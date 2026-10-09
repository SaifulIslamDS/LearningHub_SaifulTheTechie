"""Phase 2 · Polars DataFrames."""

# %% 1. Read and inspect
import polars as pl

orders = pl.read_csv("data/orders_2025.csv", try_parse_dates=True)
print(orders.shape)
print(orders.select("order_id", "order_date", "region", "status", "revenue").head(3))

# %% 2. Expressions: select, filter, with_columns
net = (
    orders
    .filter(pl.col("status") != "Cancelled")
    .with_columns(
        (pl.col("quantity") * pl.col("unit_cost")).alias("cost"),
        pl.col("order_date").dt.month().alias("month"),
    )
)
print(net.select("order_id", "revenue", "cost", "month").head(3))

# %% 3. group_by + agg
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

# %% 4. Join with customers
customers = pl.read_csv("data/customers_2025.csv")
joined = net.join(customers.select("customer_id", "customer_name", "credit_days"), on="customer_id",
                  how="left", validate="m:1")
print(joined.select("order_id", "customer_name", "credit_days").head(3))

# %% 5. Lazy mode: describe the query, let Polars optimise it, then collect
lazy = (
    pl.scan_csv("data/orders_2025.csv", try_parse_dates=True)
    .filter(pl.col("status") == "Delivered")
    .group_by(pl.col("order_date").dt.month().alias("month"))
    .agg(pl.col("delivery_days").mean().round(2).alias("avg_days"))
    .sort("month")
)
print(lazy.explain())
print(lazy.collect().head(4))

# %% 6. Same answer as pandas?
import pandas as pd

pd_total = pd.read_csv("data/orders_2025.csv").query("status != 'Cancelled'")["revenue"].sum()
pl_total = net["revenue"].sum()
print(round(pd_total, 2), round(pl_total, 2))

# %% Try it yourself — solution: cancellation rate by channel, in Polars
rate = (
    orders.group_by("channel")
    .agg((pl.col("status") == "Cancelled").mean().mul(100).round(1).alias("cancel_pct"), pl.len().alias("orders"))
    .sort("cancel_pct", descending=True)
)
print(rate)
