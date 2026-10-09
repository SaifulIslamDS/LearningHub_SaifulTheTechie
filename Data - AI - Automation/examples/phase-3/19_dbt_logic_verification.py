from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

orders = pd.read_csv(DATA / "orders_2025.csv", parse_dates=["order_date"])
customers = pd.read_csv(DATA / "customers_2025.csv")
products = pd.read_csv(DATA / "products_2025.csv")

allowed_statuses = {"Delivered", "Cancelled", "Shipped", "Pending"}
orders = orders.copy()
orders["net_revenue"] = orders["revenue"].where(orders["status"].ne("Cancelled"), 0.0)
orders["estimated_margin"] = (orders["revenue"] - orders["quantity"] * orders["unit_cost"]).where(
    orders["status"].ne("Cancelled"), 0.0
).round(2)
orders["discount_band"] = pd.cut(
    orders["discount"], bins=[-1e-12, 0, 0.03, float("inf")], labels=["none", "low", "high"], include_lowest=True
).astype(str)

missing_customers = orders.loc[~orders["customer_id"].isin(customers["customer_id"]), "customer_id"].nunique()
missing_products = orders.loc[~orders["product"].isin(products["product"]), "product"].nunique()
invalid_statuses = sorted(set(orders["status"]) - allowed_statuses)

monthly = (
    orders.assign(order_month=orders["order_date"].dt.to_period("M").astype(str))
    .groupby("order_month", as_index=False)
    .agg(order_count=("order_id", "size"), net_revenue=("net_revenue", "sum"), estimated_margin=("estimated_margin", "sum"))
)
monthly["net_revenue"] = monthly["net_revenue"].round(2)
monthly["estimated_margin"] = monthly["estimated_margin"].round(2)

top = monthly.loc[monthly["net_revenue"].idxmax()]

print(f"source rows: orders {len(orders)} | customers {len(customers)} | products {len(products)}")
print(f"grain/tests: duplicate order_id {orders['order_id'].duplicated().sum()} | invalid statuses {invalid_statuses or 'none'}")
print(f"relationships: missing customers {missing_customers} | missing products {missing_products}")
print(f"known answer: rows {len(orders)} | net revenue {orders['net_revenue'].sum():.2f}")
print("discount bands:", " | ".join(f"{k} {v}" for k, v in orders["discount_band"].value_counts().sort_index().items()))
print(f"monthly mart: {len(monthly)} rows | top month {top['order_month']} | net revenue {top['net_revenue']:.2f}")

baseline = customers.loc[customers["customer_id"].eq("C007"), ["customer_id", "credit_days"]].iloc[0]
changed = baseline.copy()
changed["credit_days"] = 45
print(f"snapshot demo input: {baseline['customer_id']} credit_days {int(baseline['credit_days'])} -> {int(changed['credit_days'])}")

assert len(orders) == 4246
assert orders["order_id"].nunique() == 4246
assert round(float(orders["net_revenue"].sum()), 2) == 5_478_357.79
assert missing_customers == 0
assert missing_products == 0
assert not invalid_statuses
assert len(monthly) == 12
