"""Phase 2 · EDA · Analytical questions, patterns & distributions."""

# %% 0. Setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from chart_style import BLUE_RAMP, INK_2, PALETTE, apply_style, save

apply_style()
pd.set_option("display.width", 120)
orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
net = orders[orders["status"] != "Cancelled"].copy()

# %% 1. Profile in one table
profile = pd.DataFrame({
    "dtype": orders.dtypes.astype(str),
    "missing": orders.isna().sum(),
    "distinct": orders.nunique(),
})
print(profile.loc[["order_date", "customer_id", "region", "segment", "product", "quantity", "revenue", "delivery_days"]])

# %% 2. Distribution of order revenue: shape, skew, percentiles
rev = net["revenue"]
print(rev.describe(percentiles=[0.1, 0.5, 0.9, 0.99]).round(0))
print("skewness:", round(rev.skew(), 2))

fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
axes[0].hist(rev, bins=60, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=0.6)
axes[0].set_title("Most orders are small; a long tail of big ones")
axes[0].set_xlabel("Order revenue")
axes[0].set_ylabel("Orders")
axes[1].hist(np.log10(rev), bins=40, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=0.6)
axes[1].set_title("On a log scale the shape is clear")
axes[1].set_xlabel("Order revenue (log10: 2 = 100, 3 = 1,000, 4 = 10,000)")
save(fig, "eda_revenue_distribution.png")

# %% 3. Distribution by group: segment
print(net.groupby("segment")["revenue"].describe()[["count", "25%", "50%", "75%", "max"]].round(0))
order = ["Garment Factory", "Knitting Mill", "Trader", "Retailer"]
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.boxplot([net.loc[net.segment == s, "revenue"] for s in order], tick_labels=order, orientation="horizontal", showfliers=False,
           patch_artist=True, boxprops={"facecolor": BLUE_RAMP[1], "edgecolor": INK_2},
           medianprops={"color": "#0b0b0b", "linewidth": 2}, whiskerprops={"color": INK_2}, capprops={"color": INK_2})
ax.invert_yaxis()
ax.set_title("Garment factories place the largest orders (middle 50% shown as boxes)")
ax.set_xlabel("Order revenue (outliers hidden)")
save(fig, "eda_revenue_by_segment.png")

# %% 4. Patterns over time: weekly revenue with the Eid dips marked
weekly = net.set_index("order_date")["revenue"].resample("W-SAT").sum() / 1000
print(weekly.idxmin().date(), round(weekly.min(), 0), "|", weekly.idxmax().date(), round(weekly.max(), 0))
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(weekly.index, weekly.values, color=PALETTE[0])
for d, label in [("2025-03-31", "Eid al-Fitr"), ("2025-06-07", "Eid al-Adha")]:
    ax.axvline(pd.Timestamp(d), color="#898781", linestyle="--", linewidth=1)
    ax.text(pd.Timestamp(d), weekly.max() * 0.97, f" {label}", color=INK_2, fontsize=9, va="top")
ax.set_title("Weekly revenue: Eid weeks drop sharply; Sep–Nov is the peak")
ax.set_ylabel("Revenue (thousands)")
save(fig, "eda_weekly_revenue.png")

# %% 5. Patterns in categories: product mix
mix = net.groupby("category")["revenue"].sum().div(net["revenue"].sum()).mul(100).round(1)
print(mix.sort_values(ascending=False))

# %% Try it yourself — solution: distribution of delivery days (delivered orders only)
dd = orders.loc[orders["status"] == "Delivered", "delivery_days"]
print(dd.value_counts().sort_index().to_dict())
print("median:", dd.median(), "| mean:", round(dd.mean(), 2), "| share over 7 days:", round((dd > 7).mean() * 100, 1), "%")
