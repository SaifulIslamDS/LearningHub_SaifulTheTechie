"""Phase 2 · pandas · Pivot & datetime."""

# %% 1. Parse dates and extract parts
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 14)
orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
print(orders["order_date"].dtype, orders["order_date"].min().date(), orders["order_date"].max().date())
net = orders[orders["status"] != "Cancelled"].copy()
net["month"] = net["order_date"].dt.month
net["weekday"] = net["order_date"].dt.day_name()
net["quarter"] = net["order_date"].dt.quarter
print(net[["order_date", "month", "weekday", "quarter"]].head(3))

# %% 2. Orders by weekday (Friday is the weekend in Bangladesh)
days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
print(net["weekday"].value_counts().reindex(days))

# %% 3. Resample: monthly revenue and month-on-month growth
monthly = net.set_index("order_date")["revenue"].resample("ME").sum()
mom = monthly.pct_change() * 100
print(pd.DataFrame({"revenue": monthly.round(0), "mom_pct": mom.round(1)}).to_string())

# %% 4. pivot_table: region x quarter
pt = net.pivot_table(index="region", columns="quarter", values="revenue", aggfunc="sum", margins=True, margins_name="Total")
print((pt / 1000).round(0))

# %% 5. Rolling 7-day average of daily orders
daily = net.set_index("order_date").resample("D")["order_id"].count()
roll = daily.rolling(7).mean()
print(daily.loc["2025-03-27":"2025-04-09"].to_string())
print(roll.loc["2025-04-05":"2025-04-09"].round(1).to_string())

# %% 6. Date arithmetic: delivery date and late orders
delivered = net[net["status"] == "Delivered"].copy()
delivered["delivered_on"] = delivered["order_date"] + pd.to_timedelta(delivered["delivery_days"], unit="D")
delivered["late"] = delivered["delivery_days"] > delivered["promised_days"]
print(delivered[["order_date", "delivery_days", "delivered_on", "promised_days", "late"]].head(3))
print(delivered.groupby(delivered["order_date"].dt.month)["late"].mean().mul(100).round(1).to_dict())

# %% 7. melt: wide pivot back to long
wide = pt.drop(index="Total", columns="Total")
long = wide.reset_index().melt(id_vars="region", var_name="quarter", value_name="revenue")
print(long.head(4))

# %% Try it yourself — solution: late-delivery rate by region and quarter
late_pt = delivered.pivot_table(index="region", columns="quarter", values="late", aggfunc="mean") * 100
print(late_pt.round(1))
