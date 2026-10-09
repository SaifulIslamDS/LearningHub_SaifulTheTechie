"""Shared data preparation for the ML Foundations scripts (17–19).

Question: at the moment an order is placed, how likely is it to be CANCELLED?
Only information known at order time may be used as a feature.
"""

import pandas as pd

ORDER_TIME_FEATURES = ["segment", "region", "channel", "category", "quantity", "unit_price", "discount",
                       "revenue", "promised_days", "credit_days", "month"]
CATEGORICAL = ["segment", "region", "channel", "category"]
NUMERIC = ["quantity", "unit_price", "discount", "revenue", "promised_days", "credit_days", "month"]


def load() -> pd.DataFrame:
    orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
    customers = pd.read_csv("data/customers_2025.csv")
    df = orders.merge(customers[["customer_id", "credit_days"]], on="customer_id", how="left", validate="many_to_one")
    df = df[df["status"] != "Pending"].copy()                 # outcome not known yet for open orders
    df["cancelled"] = (df["status"] == "Cancelled").astype(int)
    df["month"] = df["order_date"].dt.month
    return df.sort_values("order_date").reset_index(drop=True)
