"""Phase 2 · EDA · Relationships & anomalies."""

# %% 0. Setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from chart_style import INK_2, PALETTE, apply_style, save

apply_style()
pd.set_option("display.width", 120)
orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
customers = pd.read_csv("data/customers_2025.csv")
df = orders.merge(customers[["customer_id", "credit_days"]], on="customer_id", how="left", validate="many_to_one")
df["cancelled"] = (df["status"] == "Cancelled").astype(int)
net = df[df["cancelled"] == 0].copy()

# %% 1. Two categories: crosstab with row percentages
ct = pd.crosstab(df["segment"], df["channel"], normalize="index").mul(100).round(1)
print(ct)

# %% 2. Category vs number: cancellation rate by credit terms (with counts)
rate = df.groupby("credit_days")["cancelled"].agg(["mean", "size"])
rate["mean"] = (rate["mean"] * 100).round(1)
print(rate)
fig, ax = plt.subplots(figsize=(7, 3.4))
bars = ax.bar(rate.index.astype(str), rate["mean"], color=PALETTE[0], width=0.6)
ax.bar_label(bars, labels=[f"{v}%" for v in rate["mean"]], padding=3, color=INK_2)
ax.set_title("Longer credit terms, more cancellations")
ax.set_xlabel("Customer credit terms (days)")
ax.set_ylabel("Cancelled orders (%)")
ax.set_ylim(0, 16)
save(fig, "eda_cancel_by_credit.png")

# %% 3. Number vs number: correlation
num = net[["quantity", "unit_price", "discount", "revenue", "delivery_days", "promised_days", "credit_days"]]
corr = num.corr(method="spearman").round(2)
print(corr.loc[["revenue", "delivery_days"], ["quantity", "discount", "promised_days", "credit_days"]])

fig, ax = plt.subplots(figsize=(6.4, 5.2))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr)), corr.columns, rotation=40, ha="right")
ax.set_yticks(range(len(corr)), corr.index)
ax.grid(False)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8,
                color="white" if abs(corr.iloc[i, j]) > 0.6 else "#0b0b0b")
fig.colorbar(im, ax=ax, shrink=0.8, label="Spearman correlation")
ax.set_title("Which numbers move together?")
save(fig, "eda_correlation_heatmap.png")

# %% 4. Scatter: discount vs order revenue (log scale)
fig, ax = plt.subplots(figsize=(7, 3.8))
jitter = np.random.default_rng(1).uniform(-0.004, 0.004, len(net))
ax.scatter(net["discount"] * 100 + jitter * 100, net["revenue"], s=8, alpha=0.35, color=PALETTE[0], edgecolors="none")
ax.set_yscale("log")
ax.set_title("Bigger orders get bigger discounts (the 5% rule above 1,500)")
ax.set_xlabel("Discount (%)")
ax.set_ylabel("Order revenue (log scale)")
save(fig, "eda_discount_vs_revenue.png")
print(net.groupby("discount")["revenue"].median().round(0))

# %% 5. Anomalies over time: days far below their recent "normal" (rolling median)
daily = net.set_index("order_date").resample("D")["order_id"].count()
daily = daily[daily.index.dayofweek != 4]                          # skip Fridays (weekend)
is_saturday = daily.index.dayofweek == 5                           # Saturdays are half days: compare like with like
normal = daily.groupby(is_saturday).transform(lambda s: s.rolling(15, center=True, min_periods=5).median())
ratio = daily / normal
low_days = ratio[ratio < 0.35]
print(f"{len(low_days)} unusually quiet days (below 35% of the rolling median for that kind of day):")
print([d.strftime("%d %b") for d in low_days.index])

# %% 6. Anomalies in order size: IQR rule within each segment
def iqr_flags(s: pd.Series) -> pd.Series:
    q1, q3 = s.quantile([0.25, 0.75])
    return s > q3 + 3 * (q3 - q1)


net["unusual"] = net.groupby("segment")["revenue"].transform(iqr_flags)
print(net["unusual"].sum(), "unusually large orders")
print(net.loc[net["unusual"]].nlargest(5, "revenue")[["order_id", "segment", "product", "quantity", "revenue"]])

# %% Try it yourself — solution: delivery days by region (relationship) and the slowest outliers
by_region = net.groupby("region")["delivery_days"].agg(["median", "mean", "max"]).round(2)
print(by_region.sort_values("mean"))
print(net.nlargest(3, "delivery_days")[["order_id", "order_date", "region", "delivery_days", "promised_days"]])
