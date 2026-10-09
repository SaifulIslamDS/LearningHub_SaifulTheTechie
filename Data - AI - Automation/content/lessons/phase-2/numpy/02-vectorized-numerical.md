---
title: "Vectorized Operations & Numerical Computation in NumPy"
order: 2
summary: "Replace slow loops with whole-array maths, use broadcasting and axis aggregations, handle missing values and floating-point traps, and make random numbers reproducible."
level: Beginner
time: "45 min"
topics: ["Vectorized operations", "Numerical computation"]
prerequisites: ["phase-2/numpy/01-arrays-indexing"]
keywords: [vectorization, vectorized, broadcasting, axis, aggregation, cumsum, percentile, nan, nanmean, isnan, floating point, isclose, rounding, random generator, default_rng, seed, reproducible, performance]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv]
resources:
  - title: "Broadcasting"
    url: "https://numpy.org/doc/stable/user/basics.broadcasting.html"
    source: "NumPy official docs"
    note: "The rules for combining arrays of different shapes, with diagrams."
  - title: "Random sampling (numpy.random)"
    url: "https://numpy.org/doc/stable/reference/random/index.html"
    source: "NumPy official docs"
    note: "Why default_rng is the recommended way to make random numbers."
  - title: "Floating-point arithmetic: issues and limitations"
    url: "https://docs.python.org/3/tutorial/floatingpoint.html"
    source: "Python official docs"
    note: "Why 0.1 + 0.2 isn't exactly 0.3."
---

## What is it?

- **Vectorized operation:** one expression that works on whole arrays (`qty * price`) instead of a Python loop over each element.
- **Broadcasting:** NumPy's rule for combining arrays of different shapes, such as a column of prices with a row of discounts.
- **Numerical computation:** aggregating (sum, mean, percentiles) along an axis, handling missing values (`nan`), and knowing the limits of floating-point numbers.

!!! job "Why it matters at work"
    Vectorized code is shorter, has fewer bugs and runs tens to hundreds of times faster, which matters once data reaches millions of rows. pandas, scikit-learn and every ML library expect you to think this way. Knowing about `nan` and floating-point rounding prevents "the totals are off by 0.01" arguments.

The script is `02_numpy_vectorized.py` in [data-science-scripts.zip](../../../downloads/phase-2/data-science-scripts.zip).

## Example 1: loop vs vectorized

One million random orders, total value two ways:

```python
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
```

```text
loop:       0.316 s
vectorized: 0.0053 s  (60x faster)
True
```

Same answer, about 60 times faster on our build machine. Your timings will differ, but the gap is always large.

## Example 2: broadcasting

Net price for 4 products × 4 discount levels, without a loop:

```python
prices = np.array([3.50, 5.20, 2.90, 0.30])          # 4 products
discounts = np.array([0, 0.02, 0.05, 0.08])           # 4 discount levels
table = prices[:, None] * (1 - discounts)             # (4, 1) x (4,) -> (4, 4)
print(table.round(3))
```

```text
[[3.5   3.43  3.325 3.22 ]
 [5.2   5.096 4.94  4.784]
 [2.9   2.842 2.755 2.668]
 [0.3   0.294 0.285 0.276]]
```

`prices[:, None]` turns the prices into a **column** (shape `(4, 1)`). NumPy then "stretches" the column and the discount row to a 4 × 4 grid. **Rule:** shapes are compared from the right, and each dimension must be equal or 1.

## Example 3: aggregate along an axis

```python
week_orders = np.array([[8, 15, 14, 16, 13, 15], [7, 14, 15, 12, 16, 14], [9, 16, 13, 15, 14, 17]])
print(week_orders.mean(axis=0).round(1))   # average per weekday
print(week_orders.max(axis=1))             # busiest day per week
print(week_orders.cumsum(axis=1)[0])       # running total, week 1
```

```text
[ 8.  15.  14.  14.3 14.3 15.3]
[16 16 17]
[ 8 23 37 53 66 81]
```

| `axis=` | Collapses | One result per |
|---|---|---|
| `0` | rows (goes down) | column |
| `1` | columns (goes across) | row |
| none | everything | whole array |

## Example 4: real data, percentiles and missing values

```python
data = np.genfromtxt("data/orders_2025.csv", delimiter=",", skip_header=1, usecols=(14, 15))
delivery_days, revenue = data[:, 0], data[:, 1]
print(np.percentile(revenue, [25, 50, 75, 95]).round(2))
print(np.isnan(delivery_days).sum(), "orders without delivery days")
print(np.mean(delivery_days), np.nanmean(delivery_days).round(2))
```

```text
[ 554.21 1062.3  1794.22 3510.48]
374 orders without delivery days
nan 3.44
```

- Half of the orders are below 1,062; only 5% are above 3,510. A few very large orders pull the **mean** up (you'll see why that matters in Statistics).
- 374 orders (cancelled, shipped or pending) have no delivery days, stored as `nan` ("not a number").
- **One `nan` makes `mean` return `nan`.** Use `np.nanmean`, `np.nansum` and so on, and report how many values were missing.

## Example 5: floating-point care

```python
print(0.1 + 0.2 == 0.3, np.isclose(0.1 + 0.2, 0.3))
print(np.round(2.675, 2), round(2.675, 2))
print(np.array([1, 2, 3]) / np.array([1, 0, 3]))
```

```text
False True
2.68 2.67
[ 1. inf  1.]
```

(plus `RuntimeWarning: divide by zero encountered in divide`)

- Decimals like 0.1 can't be stored exactly in binary, so compare with `np.isclose`, never `==`.
- `2.675` is really stored as 2.67499999…, and NumPy and Python round it differently. For money, round **once, at the end**, with an agreed rule (or use Python's `decimal` module).
- Dividing by zero gives `inf` and a **warning, not an error**. Check for it.

## Example 6: reproducible random numbers

```python
rng = np.random.default_rng(7)
print(rng.normal(loc=1000, scale=150, size=3).round(1))
rng = np.random.default_rng(7)
print(rng.normal(loc=1000, scale=150, size=3).round(1))
```

```text
[1000.2 1044.8  958.9]
[1000.2 1044.8  958.9]
```

The same **seed** gives the same numbers, so simulations, train/test splits and the practice data itself can be reproduced exactly. (The Phase 2 data was generated with seed 2025.)

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Looping over rows "to be safe" | Slow code, more bugs | Write the maths for the whole array |
| Wrong `axis` | Totals per row when you wanted per column | `axis=0` = per column, `axis=1` = per row |
| `np.mean` on data with `nan` | Result is `nan` | `np.nanmean`, and report the missing count |
| `==` on floats | Equal numbers look different | `np.isclose` |
| Shapes `(4,)` and `(3,)` combined | `ValueError: operands could not be broadcast` | Check `.shape`; add an axis with `[:, None]` |
| `np.random.seed(…)` everywhere | Hidden global state | `rng = np.random.default_rng(seed)` and pass `rng` around |

## Try it yourself

**Task:** Margin per unit is `price − cost`. With `prices = [3.50, 5.20, 2.90, 0.30]`, `costs = [2.60, 3.90, 2.10, 0.19]` and the same 4 discount levels, build the 4 × 4 table of **margin % after discount** (`(net price − cost) / net price`). Which product–discount combinations fall below 20%?

<details markdown="1">
<summary>Show a hint</summary>

Compute `net = prices[:, None] * (1 - discounts)`, then `(net - costs[:, None]) / net`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
costs = np.array([2.60, 3.90, 2.10, 0.19])
net = prices[:, None] * (1 - discounts)
margin = (net - costs[:, None]) / net
print((margin * 100).round(1))
print(margin < 0.20)
```

```text
[[25.7 24.2 21.8 19.3]
 [25.  23.5 21.1 18.5]
 [27.6 26.1 23.8 21.3]
 [36.7 35.4 33.3 31.2]]
[[False False False  True]
 [False False False  True]
 [False False False False]
 [False False False False]]
```

Cotton Twill and Denim drop below 20% margin at the 8% discount: a useful rule for the sales team.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. `m` has shape `(3, 6)`. What shape is `m.sum(axis=0)`?

1. `(3,)`
2. `(6,)`
3. `(3, 6)`

<details markdown="1"><summary>Show answer</summary>
**B.** `axis=0` collapses the rows, leaving one value per column.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. `np.mean([2, np.nan, 4])` returns:

1. `3.0`
2. `nan`
3. An error

<details markdown="1"><summary>Show answer</summary>
**B.** Use `np.nanmean` to ignore missing values.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why use `np.random.default_rng(42)`?

1. It's faster than any other method
2. The same seed gives the same random numbers, so results are reproducible
3. It makes numbers truly random

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Vectorize:** whole-array expressions replace loops and run much faster.
- **Broadcasting** combines shapes like `(4, 1)` and `(4,)` into a grid; check shapes when it fails.
- Aggregate with `axis=0` (per column) or `axis=1` (per row); use `nan`-aware functions for missing data.
- Compare floats with `isclose`, round once at the end, and watch for `inf`.
- Use a seeded `default_rng` for reproducible randomness.

!!! job "Job-ready check"
    **Interview question:** *"What is broadcasting in NumPy?"*

    **Strong answer:** "It's how NumPy applies an operation to arrays of different shapes without copying data. It compares shapes from the right; a dimension of size 1 is stretched to match. For example, a `(4, 1)` column of prices times a `(4,)` row of discounts gives a `(4, 4)` table of net prices."

    **Mini project:** Using `orders_2025.csv`, calculate the 50th, 90th and 99th percentiles of revenue, and the mean delivery days with `nanmean`. Write two sentences on what the gap between the median and the mean tells a manager.
