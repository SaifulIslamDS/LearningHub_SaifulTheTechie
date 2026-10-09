"""Phase 2 · Statistics · Central tendency, variance and distributions."""

# %% 0. Setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from chart_style import PALETTE, apply_style, save

apply_style()
pd.set_option("display.width", 120)
orders = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
net = orders[orders["status"] != "Cancelled"].copy()
rev = net["revenue"]

# %% 1. Central tendency: mean, median, mode, trimmed mean
print("mean   ", round(rev.mean(), 2))
print("median ", round(rev.median(), 2))
print("trimmed mean (5% each end)", round(stats.trim_mean(rev, 0.05), 2))
print("mode of discount:", net["discount"].mode().tolist())

# %% 2. Spread: range, IQR, variance, standard deviation, coefficient of variation
q1, q3 = rev.quantile([0.25, 0.75])
spread = pd.Series({
    "range": rev.max() - rev.min(),
    "IQR": q3 - q1,
    "variance": rev.var(),          # sample variance (divides by n - 1)
    "std": rev.std(),
    "CV": rev.std() / rev.mean(),
}).round(2)
print(spread)

# %% 3. Different centre AND spread: delivery days in two regions
dd = net[net["status"] == "Delivered"]
two = dd[dd["region"].isin(["Dhaka", "Khulna"])].groupby("region")["delivery_days"].agg(["mean", "std", "min", "max"])
print(two.round(2))

# %% 4. Distributions: a count per day (Poisson) and a yes/no outcome (binomial)
weekday = net[net["order_date"].dt.dayofweek.isin([0, 1, 2, 3, 6])]           # Sun–Thu working days
per_day = weekday.groupby("order_date").size()
per_day = per_day[per_day.index.month.isin([5, 7])]                          # two steady months, no Eid: May, July
lam = per_day.mean()
print(f"May + July working days: {len(per_day)}, mean orders/day {lam:.2f}, variance {per_day.var():.2f}")
print("P(a working day has 20+ orders), Poisson model:", round(1 - stats.poisson.cdf(19, lam), 3),
      "| observed:", round((per_day >= 20).mean(), 3))

p_cancel = (orders["status"] == "Cancelled").mean()
print(f"cancellation rate {p_cancel:.3f}; in a batch of 50 orders, P(5 or more cancelled) =",
      round(1 - stats.binom.cdf(4, 50, p_cancel), 3))

# %% 5. Normal or not? Order revenue vs log revenue
for name, x in [("revenue", rev), ("log revenue", np.log(rev))]:
    within_1sd = ((x - x.mean()).abs() <= x.std()).mean()
    print(f"{name:12s} skew {stats.skew(x):5.2f} | share within 1 std of mean: {within_1sd:.1%} (normal: 68.3%)")

fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
axes[0].hist(np.log10(rev), bins=50, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=0.5, density=True)
xs = np.linspace(np.log10(rev).min(), np.log10(rev).max(), 200)
axes[0].plot(xs, stats.norm.pdf(xs, np.log10(rev).mean(), np.log10(rev).std()), color=PALETTE[1])
axes[0].set_title("Log revenue is close to a normal curve")
axes[0].set_xlabel("Order revenue (log10: 2 = 100, 3 = 1,000, 4 = 10,000)")
axes[0].set_ylabel("Density")
ks = np.arange(0, 31)
axes[1].bar(ks, [(per_day == k).mean() for k in ks], color=PALETTE[0], width=0.8, label="Observed (May, July)")
axes[1].plot(ks, stats.poisson.pmf(ks, lam), "o-", color=PALETTE[1], markersize=3, label=f"Poisson, mean {lam:.1f}")
axes[1].set_title("Orders per working day vs a Poisson model")
axes[1].set_xlabel("Orders in a day")
axes[1].set_ylabel("Share of days")
axes[1].legend()
save(fig, "stats_distributions.png")

# %% Try it yourself — solution: how unusual is the 44,127 order? z-scores on two scales
big = 44127.55
z_raw = (big - rev.mean()) / rev.std()
z_log = (np.log10(big) - np.log10(rev).mean()) / np.log10(rev).std()
print(f"z on the raw scale: {z_raw:.1f} | z on the log scale: {z_log:.1f}")
