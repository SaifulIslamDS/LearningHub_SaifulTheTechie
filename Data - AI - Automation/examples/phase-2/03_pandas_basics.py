"""Phase 2 · pandas · DataFrame basics."""

# %% 1. Load and look
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)

orders = pd.read_csv("data/orders_2025.csv")
print(orders.shape)
print(orders.head(3))

# %% 2. Column types
print(orders.dtypes)

# %% 3. Summary statistics
print(orders[["quantity", "revenue", "delivery_days"]].describe().round(2))

# %% 4. Select columns and rows
print(orders[["order_id", "region", "revenue"]].head(3))
print(orders.loc[0, "product"], "|", orders.iloc[0, 7])

# %% 5. Filter rows (like SQL WHERE)
dhaka_big = orders[(orders["region"] == "Dhaka") & (orders["revenue"] > 10000)]
print(len(dhaka_big))
print(dhaka_big[["order_id", "customer_id", "product", "revenue"]])

# %% 6. Sort, count and add a column
print(orders.sort_values("revenue", ascending=False)[["order_id", "segment", "revenue"]].head(3))
print(orders["status"].value_counts())
orders["is_net"] = orders["status"] != "Cancelled"
print(orders.loc[orders["is_net"], "revenue"].sum().round(2))

# %% 7. query(): the same filter, written like SQL
print(orders.query("region == 'Khulna' and status == 'Cancelled'").shape)

# %% Try it yourself — solution
portal = orders["channel"] == "Portal"
cancelled = orders["status"] == "Cancelled"
print((portal & cancelled).sum())
print(orders.loc[portal & ~cancelled, "revenue"].mean().round(2))
