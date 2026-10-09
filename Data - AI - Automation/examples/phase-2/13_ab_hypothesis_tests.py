"""Phase 2 · Experimentation & A/B testing · Hypothesis tests and significance."""

# %% 0. Setup
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest

pd.set_option("display.width", 120)
ab = pd.read_csv("data/ab_test_checkout.csv", parse_dates=["date"])
print(ab.shape, ab["date"].min().date(), "to", ab["date"].max().date())

# %% 1. Sanity check first: is the 50/50 split intact? (sample ratio mismatch)
counts = ab["variant"].value_counts().sort_index()
srm = stats.binomtest(int(counts["A"]), int(counts.sum()), 0.5)
print(counts.to_dict(), f"| SRM p-value = {srm.pvalue:.3f}")

# %% 2. The primary metric: conversion rate per variant
summary = ab.groupby("variant").agg(sessions=("converted", "size"), orders=("converted", "sum"),
                                    conversion=("converted", "mean"))
summary["conversion"] = (summary["conversion"] * 100).round(2)
print(summary)

# %% 3. Two-proportion z-test (H0: conversion A = conversion B)
orders_ = summary["orders"].to_numpy()[::-1]          # [B, A]
sessions = summary["sessions"].to_numpy()[::-1]
z, p = proportions_ztest(orders_, sessions)
low, high = confint_proportions_2indep(orders_[0], sessions[0], orders_[1], sessions[1], compare="diff")
diff = orders_[0] / sessions[0] - orders_[1] / sessions[1]
print(f"difference B - A = {diff * 100:.2f} percentage points, 95% CI {low * 100:.2f} to {high * 100:.2f}")
print(f"z = {z:.2f}, p-value = {p:.4f}")
print(f"relative lift = {diff / (orders_[1] / sessions[1]):.1%}")

# %% 4. The same test as a chi-square test on the 2x2 table
table = pd.crosstab(ab["variant"], ab["converted"])
chi2, p_chi, dof, _ = stats.chi2_contingency(table, correction=False)
print(f"chi-square = {chi2:.2f} (= z squared {z**2:.2f}), p = {p_chi:.4f}")

# %% 5. A guardrail metric: order value among buyers (skewed -> compare carefully)
buyers = ab[ab["converted"] == 1]
a_val, b_val = buyers.loc[buyers.variant == "A", "order_value"], buyers.loc[buyers.variant == "B", "order_value"]
t = stats.ttest_ind(b_val, a_val, equal_var=False)                     # Welch's t-test
u = stats.mannwhitneyu(b_val, a_val)
print(f"mean order value A {a_val.mean():.0f}, B {b_val.mean():.0f} | median A {a_val.median():.0f}, B {b_val.median():.0f}")
print(f"Welch t-test p = {t.pvalue:.3f} | Mann-Whitney p = {u.pvalue:.3f}")

# %% 6. What the business cares about: revenue per session
rps = ab.groupby("variant")["order_value"].mean()
t_rps = stats.ttest_ind(ab.loc[ab.variant == "B", "order_value"], ab.loc[ab.variant == "A", "order_value"], equal_var=False)
print(f"revenue per session A {rps['A']:.2f}, B {rps['B']:.2f} (+{(rps['B'] / rps['A'] - 1):.1%}), p = {t_rps.pvalue:.3f}")

# %% 7. Segments: same direction on mobile and desktop?
seg = ab.groupby(["device", "variant"])["converted"].agg(["mean", "size"])
seg["mean"] = (seg["mean"] * 100).round(2)
print(seg.unstack("variant"))

# %% Try it yourself — solution: the test for new customers only
new = ab[ab["new_customer"] == 1]
s_new = new.groupby("variant")["converted"].agg(["sum", "size"])
z_n, p_n = proportions_ztest(s_new["sum"].to_numpy()[::-1], s_new["size"].to_numpy()[::-1])
print(s_new.assign(rate=(s_new["sum"] / s_new["size"] * 100).round(2)))
print(f"new customers: z = {z_n:.2f}, p = {p_n:.3f}")
