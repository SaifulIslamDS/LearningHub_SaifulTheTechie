"""Phase 2 · Statistics · Correlation and confidence intervals."""

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

# %% 1. Pearson vs Spearman, within one product (no mix effect)
twill = net[net["product"] == "Cotton Twill"]
r, p_r = stats.pearsonr(twill["quantity"], twill["revenue"])
rho, p_rho = stats.spearmanr(twill["quantity"], twill["revenue"])
print(f"Cotton Twill orders: {len(twill)} | Pearson r = {r:.3f} (p = {p_r:.1e}) | Spearman rho = {rho:.3f}")
print(f"r squared = {r**2:.3f}: quantity explains {r**2:.1%} of the variation in revenue")

# %% 2. One outlier can create (or hide) a Pearson correlation
rng = np.random.default_rng(7)
x = rng.normal(0, 1, 30)
y = rng.normal(0, 1, 30)
print(f"30 random points:      Pearson {stats.pearsonr(x, y)[0]:.2f} | Spearman {stats.spearmanr(x, y)[0]:.2f}")
x2, y2 = np.append(x, 8), np.append(y, 8)
print(f"plus one extreme point: Pearson {stats.pearsonr(x2, y2)[0]:.2f} | Spearman {stats.spearmanr(x2, y2)[0]:.2f}")

# %% 3. Confidence interval for a mean: t-interval
delivered = net[net["status"] == "Delivered"]
khulna = delivered.loc[delivered["region"] == "Khulna", "delivery_days"]
m, se = khulna.mean(), stats.sem(khulna)
lo, hi = stats.t.interval(0.95, df=len(khulna) - 1, loc=m, scale=se)
print(f"Khulna delivery days: n = {len(khulna)}, mean {m:.2f}, 95% CI {lo:.2f} to {hi:.2f}")

# %% 4. A smaller sample gives a wider interval
sample = khulna.sample(30, random_state=1)
lo30, hi30 = stats.t.interval(0.95, df=29, loc=sample.mean(), scale=stats.sem(sample))
print(f"Only 30 orders:       mean {sample.mean():.2f}, 95% CI {lo30:.2f} to {hi30:.2f}")

# %% 5. Confidence interval for a proportion: late deliveries (Wilson interval)
late = delivered["delivery_days"] > delivered["promised_days"]
res = stats.binomtest(int(late.sum()), len(late))
ci = res.proportion_ci(confidence_level=0.95, method="wilson")
print(f"Late deliveries: {late.sum()} of {len(late)} = {late.mean():.2%}, 95% CI {ci.low:.2%} to {ci.high:.2%}")

# %% 6. Bootstrap: a CI for the MEDIAN order value (no formula needed)
rev = net["revenue"].to_numpy()
boot = np.array([np.median(rng.choice(rev, size=len(rev), replace=True)) for _ in range(5000)])
print(f"median order value {np.median(rev):.0f}, bootstrap 95% CI {np.percentile(boot, 2.5):.0f} "
      f"to {np.percentile(boot, 97.5):.0f}")

# %% 7. Chart: late-delivery rate by region with 95% CIs
rows = []
for region, g in delivered.groupby("region"):
    k = int((g["delivery_days"] > g["promised_days"]).sum())
    ci_r = stats.binomtest(k, len(g)).proportion_ci(method="wilson")
    rows.append({"region": region, "n": len(g), "late_pct": 100 * k / len(g),
                 "lo": 100 * ci_r.low, "hi": 100 * ci_r.high})
by_region = pd.DataFrame(rows).sort_values("late_pct")
print(by_region.round(1).to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 3.4))
yy = np.arange(len(by_region))
ax.errorbar(by_region["late_pct"], yy, xerr=[by_region["late_pct"] - by_region["lo"], by_region["hi"] - by_region["late_pct"]],
            fmt="o", color=PALETTE[0], ecolor=PALETTE[0], elinewidth=2, capsize=4)
ax.set_yticks(yy, [f"{r} (n={n})" for r, n in zip(by_region["region"], by_region["n"])])
ax.set_xlabel("Deliveries later than promised (%), with 95% confidence interval")
ax.set_title("Dhaka is clearly faster; the other four regions overlap")
ax.grid(axis="y", visible=False)
save(fig, "stats_late_ci.png")

# %% Try it yourself — solution: CI for mean revenue, Garment Factory vs Retailer
for seg in ["Garment Factory", "Retailer"]:
    s = net.loc[net["segment"] == seg, "revenue"]
    lo_s, hi_s = stats.t.interval(0.95, df=len(s) - 1, loc=s.mean(), scale=stats.sem(s))
    print(f"{seg:16s} n={len(s):4d} mean {s.mean():7.0f}  95% CI {lo_s:7.0f} to {hi_s:7.0f}")
