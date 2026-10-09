"""Phase 2 · Research thinking · From a question to an experiment design."""

# %% 0. Setup
import numpy as np
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

from ml_data import load

pd.set_option("display.width", 120)
df = load()
customers = pd.read_csv("data/customers_2025.csv")

# %% 1. The observational starting point (from EDA): cancellation by credit terms
obs = df.groupby("credit_days")["cancelled"].agg(rate="mean", orders="size")
obs["customers"] = df.groupby("credit_days")["customer_id"].nunique()
obs["rate"] = (obs["rate"] * 100).round(1)
print(obs)

# %% 2. Design A: randomise CREDIT TERMS by customer. How many units would we have?
print("customers per credit band:", customers["credit_days"].value_counts().sort_index().to_dict())
print("customers on 60-day credit who ordered in 2025:", df.loc[df["credit_days"] == 60, "customer_id"].nunique())
by_cust = df[df["credit_days"] == 60].groupby("customer_id")["cancelled"].agg(["mean", "size"])
print("their cancellation rates range from", f"{by_cust['mean'].min():.1%} to {by_cust['mean'].max():.1%}")

# %% 3. Design B: randomise a pre-dispatch CONFIRMATION CALL per order (customers on 30+ day credit)
eligible = df[df["credit_days"] >= 30]
base = eligible["cancelled"].mean()
per_month = len(eligible) / 12
target = base * 0.70                                   # the call is worth it if it cuts cancellations by 30%
h = proportion_effectsize(base, target)
n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.80)
print(f"eligible orders: {len(eligible)} in 2025 ({per_month:.0f}/month), baseline cancellation {base:.1%}")
print(f"detect {base:.1%} -> {target:.1%}: {np.ceil(n):.0f} orders per arm, "
      f"about {np.ceil(2 * n / per_month):.0f} months of eligible orders")

# %% 4. Relax the goal or widen eligibility? Two alternatives
for label, rate_cut, pool in [("cut 40%, 30+ day credit", 0.60, eligible),
                              ("cut 30%, all credit customers (15+)", 0.70, df[df["credit_days"] >= 15])]:
    b = pool["cancelled"].mean()
    nn = NormalIndPower().solve_power(effect_size=proportion_effectsize(b, b * rate_cut), alpha=0.05, power=0.80)
    print(f"{label:38s} baseline {b:.1%}: {np.ceil(nn):.0f} per arm, ~{np.ceil(2 * nn / (len(pool) / 12)):.0f} months")

# %% Try it yourself — solution: how many orders per arm at 90% power for the 30% cut?
n90 = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.90)
print(f"90% power: {np.ceil(n90):.0f} per arm, ~{np.ceil(2 * n90 / per_month):.0f} months")
