"""Phase 2 · pandas · Merge & groupby."""

# %% 1. Load three tables
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 12)
orders = pd.read_csv("data/orders_2025.csv")
customers = pd.read_csv("data/customers_2025.csv")
products = pd.read_csv("data/products_2025.csv")
print(customers.head(3))
print(products.head(3))

# %% 2. Merge orders with customers (many orders -> one customer)
df = orders.merge(customers[["customer_id", "customer_name", "credit_days"]],
                  on="customer_id", how="left", validate="many_to_one", indicator=True)
print(df.shape)
print(df["_merge"].value_counts())
df = df.drop(columns="_merge")

# %% 3. Which customers never ordered? (anti-join)
ids = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
print(ids.loc[ids["_merge"] == "left_only", ["customer_id", "customer_name", "segment"]])

# %% 4. groupby: one aggregate
net = df[df["status"] != "Cancelled"]
print(net.groupby("region")["revenue"].sum().sort_values(ascending=False).round(0))

# %% 5. groupby with named aggregations
seg = net.groupby("segment").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    avg_order=("revenue", "mean"),
    customers=("customer_id", "nunique"),
).sort_values("revenue", ascending=False)
seg["share"] = seg["revenue"] / seg["revenue"].sum()
print(seg.round({"revenue": 0, "avg_order": 0, "share": 3}))

# %% 6. Gross margin by category (needs a cost per unit)
net = net.assign(cost=net["quantity"] * net["unit_cost"])
cat = net.groupby("category")[["revenue", "cost"]].sum()
cat["margin_pct"] = (1 - cat["cost"] / cat["revenue"]) * 100
print(cat.round(1))

# %% 7. Top 5 customers
top = (net.groupby(["customer_id", "customer_name"])["revenue"].sum()
          .sort_values(ascending=False).head(5).round(0))
print(top)

# %% 8. transform: each order's share of its customer's revenue
net = net.assign(cust_total=net.groupby("customer_id")["revenue"].transform("sum"))
net = net.assign(share_of_customer=net["revenue"] / net["cust_total"])
print(net.loc[net["share_of_customer"].idxmax(), ["order_id", "customer_name", "revenue", "cust_total", "share_of_customer"]])

# %% Try it yourself — solution: cancellation rate by credit terms
rate = df.groupby("credit_days").agg(orders=("order_id", "count"),
                                     cancelled=("status", lambda s: (s == "Cancelled").sum()))
rate["cancel_rate_pct"] = (rate["cancelled"] / rate["orders"] * 100).round(1)
print(rate)
