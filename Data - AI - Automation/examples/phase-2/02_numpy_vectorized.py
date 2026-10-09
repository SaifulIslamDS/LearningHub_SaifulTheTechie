"""Phase 2 · NumPy · Vectorized operations & numerical computation."""

# %% 1. Loop vs vectorized
import time

import numpy as np

rng = np.random.default_rng(42)
qty = rng.integers(1, 5000, size=1_000_000)
price = rng.uniform(0.04, 5.5, size=1_000_000)

start = time.perf_counter()
loop_total = 0.0
for q, p in zip(qty, price):
    loop_total += q * p
loop_s = time.perf_counter() - start

start = time.perf_counter()
vec_total = (qty * price).sum()
vec_s = time.perf_counter() - start
print(f"loop:       {loop_s:.3f} s")
print(f"vectorized: {vec_s:.4f} s  ({loop_s / vec_s:.0f}x faster)")
print(np.isclose(loop_total, vec_total))

# %% 2. Broadcasting: price list x discount levels
prices = np.array([3.50, 5.20, 2.90, 0.30])          # 4 products
discounts = np.array([0, 0.02, 0.05, 0.08])           # 4 discount levels
table = prices[:, None] * (1 - discounts)             # (4, 1) x (4,) -> (4, 4)
print(table.round(3))

# %% 3. Aggregations along an axis
week_orders = np.array([[8, 15, 14, 16, 13, 15], [7, 14, 15, 12, 16, 14], [9, 16, 13, 15, 14, 17]])
print(week_orders.mean(axis=0).round(1))   # average per weekday
print(week_orders.max(axis=1))             # busiest day per week
print(week_orders.cumsum(axis=1)[0])       # running total, week 1

# %% 4. Real data: revenue statistics and missing values
data = np.genfromtxt("data/orders_2025.csv", delimiter=",", skip_header=1, usecols=(14, 15))
delivery_days, revenue = data[:, 0], data[:, 1]
print(np.percentile(revenue, [25, 50, 75, 95]).round(2))
print(np.isnan(delivery_days).sum(), "orders without delivery days")
print(np.mean(delivery_days), np.nanmean(delivery_days).round(2))

# %% 5. Floating-point care
print(0.1 + 0.2 == 0.3, np.isclose(0.1 + 0.2, 0.3))
print(np.round(2.675, 2), round(2.675, 2))
print(np.array([1, 2, 3]) / np.array([1, 0, 3]))

# %% 6. Reproducible random numbers
rng = np.random.default_rng(7)
print(rng.normal(loc=1000, scale=150, size=3).round(1))
rng = np.random.default_rng(7)
print(rng.normal(loc=1000, scale=150, size=3).round(1))

# %% Try it yourself — solution: margin % after discount
costs = np.array([2.60, 3.90, 2.10, 0.19])
net = prices[:, None] * (1 - discounts)
margin = (net - costs[:, None]) / net
print((margin * 100).round(1))
print(margin < 0.20)
