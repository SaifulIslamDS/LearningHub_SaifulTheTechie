"""Phase 2 · Experimentation & A/B testing · Sample size and causal pitfalls."""

# %% 0. Setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize, proportions_ztest

from chart_style import INK_2, PALETTE, apply_style, save

apply_style()
pd.set_option("display.width", 120)

# %% 1. Sample size BEFORE the test: baseline 6.7%, smallest lift worth detecting +1.0 point
baseline, mde = 0.067, 0.010
effect = proportion_effectsize(baseline + mde, baseline)          # Cohen's h
n_per_group = NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.80, ratio=1.0)
print(f"Cohen's h = {effect:.4f} -> {np.ceil(n_per_group):.0f} sessions per variant (80% power, alpha 0.05)")

# %% 2. How the required sample changes with the lift you want to detect
for lift in [0.005, 0.010, 0.015, 0.020]:
    h = proportion_effectsize(baseline + lift, baseline)
    n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.80)
    print(f"detect +{lift * 100:.1f} pt: {np.ceil(n):>7,.0f} per variant, ~{np.ceil(2 * n / 387):.0f} days at 387 sessions/day")

# %% 3. Power of the test we actually ran (5,489 vs 5,347 sessions) for a +1.0 point lift
achieved = NormalIndPower().power(effect_size=effect, nobs1=5489, alpha=0.05, ratio=5347 / 5489)
print(f"power of our test for +1.0 pt: {achieved:.0%}")

# %% 4. Peeking: an A/A test (no real difference) checked every day vs checked once at the end
rng = np.random.default_rng(42)
n_sims, days, per_day, p = 2000, 28, 194, 0.067        # 194 sessions per variant per day
fp_end, fp_peek = 0, 0
for _ in range(n_sims):
    a = rng.binomial(1, p, (days, per_day)).sum(axis=1).cumsum()
    b = rng.binomial(1, p, (days, per_day)).sum(axis=1).cumsum()
    n = per_day * np.arange(1, days + 1)
    pvals = [proportions_ztest([b[d], a[d]], [n[d], n[d]])[1] if a[d] + b[d] > 0 else 1 for d in range(days)]
    fp_end += pvals[-1] < 0.05
    fp_peek += min(pvals) < 0.05
print(f"A/A tests with no real effect: 'significant' at the end {fp_end / n_sims:.1%}, "
      f"'significant' on ANY day if you peek daily {fp_peek / n_sims:.1%}")

# %% 5. Causal pitfall: does ordering on the portal reduce cancellations? (observational data)
orders = pd.read_csv("data/orders_2025.csv")
orders["cancelled"] = (orders["status"] == "Cancelled").astype(int)
overall = orders.groupby("channel")["cancelled"].mean().mul(100).round(1)
print("cancellation rate by channel (%):", overall.to_dict())
within = orders.pivot_table(index="segment", columns="channel", values="cancelled", aggfunc="mean").mul(100).round(1)
print(within)
print(orders.pivot_table(index="segment", columns="channel", values="cancelled", aggfunc="size"))
mix = pd.crosstab(orders["channel"], orders["segment"], normalize="index").mul(100).round(0)
print(mix)

# %% 6. Chart: sample size needed vs lift
lifts = np.linspace(0.004, 0.025, 40)
ns = [NormalIndPower().solve_power(effect_size=proportion_effectsize(baseline + x, baseline), alpha=0.05, power=0.8)
      for x in lifts]
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(lifts * 100, np.array(ns) / 1000, color=PALETTE[0])
ax.axvline(1.0, color=INK_2, linestyle="--", linewidth=1)
ax.annotate(f"+1.0 pt: {np.ceil(n_per_group):,.0f} per variant", (1.0, n_per_group / 1000), xytext=(1.3, 24),
            arrowprops={"arrowstyle": "->", "color": INK_2}, color=INK_2)
ax.set_title("Halving the lift you want to detect quadruples the sample")
ax.set_xlabel("Smallest lift worth detecting (percentage points, baseline 6.7%)")
ax.set_ylabel("Sessions per variant (thousands)")
ax.set_ylim(0, 60)
save(fig, "ab_sample_size.png")

# %% Try it yourself — solution: sample size for a 95% power test of +1.0 pt
n95 = NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.95)
print(f"95% power: {np.ceil(n95):,.0f} per variant ({np.ceil(n95) / np.ceil(n_per_group):.2f}x the 80% design)")
