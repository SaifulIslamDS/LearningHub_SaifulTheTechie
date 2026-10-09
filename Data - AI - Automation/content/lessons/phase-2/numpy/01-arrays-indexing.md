---
title: "NumPy Arrays & Indexing: Fast Tables of Numbers"
order: 1
summary: "Create 1-D and 2-D arrays, understand shape and dtype, and select exactly the values you need with slices, boolean masks and sorting — on real order data."
level: Beginner
time: "40 min"
topics: ["Arrays", "Indexing"]
prerequisites: ["phase-0/programming-refresher/02-collections"]
keywords: [numpy, array, ndarray, dtype, shape, ndim, reshape, indexing, slicing, boolean mask, fancy indexing, argsort, genfromtxt, vstack, set_printoptions]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv]
resources:
  - title: "NumPy: the absolute basics for beginners"
    url: "https://numpy.org/doc/stable/user/absolute_beginners.html"
    source: "NumPy official docs"
    note: "Arrays, shape, indexing and basic operations."
  - title: "Indexing on ndarrays"
    url: "https://numpy.org/doc/stable/user/basics.indexing.html"
    source: "NumPy official docs"
    note: "Slicing, boolean and integer-array indexing in depth."
  - title: "Python Data Science Handbook — Introduction to NumPy"
    url: "https://jakevdp.github.io/PythonDataScienceHandbook/02.00-introduction-to-numpy.html"
    source: "Jake VanderPlas (free online book)"
    note: "A classic, clear chapter with many examples."
---

## What is it?

A **NumPy array** (`ndarray`) is a grid of values that all have the **same type**, stored compactly in memory.

| Python list | NumPy array |
|---|---|
| Can mix types (`[1, "a", 2.5]`) | One type (`int64`, `float64` …) |
| Loops to do maths | Maths on the whole array at once |
| Slow for millions of numbers | Fast: the work runs in compiled C code |

- **shape** = size of each dimension: `(5,)` for 5 values, `(3, 6)` for 3 rows × 6 columns.
- **dtype** = the type of every element.
- **Indexing** = choosing elements by position, by slice or by a True/False **mask**.

!!! job "Why it matters at work"
    pandas columns, scikit-learn inputs, images in computer vision and embeddings in AI search are all NumPy arrays underneath. When a model says "expected 2D array, got 1D" or a calculation is mysteriously slow, array thinking is what fixes it.

Run `01_numpy_arrays.py` from [data-science-scripts.zip](../../../downloads/phase-2/data-science-scripts.zip) cell by cell.

## Example 1: create arrays

The five orders from Phase 1, as arrays:

```python
import numpy as np

qty = np.array([120, 5000, 300, 800, 450])          # quantities of 5 orders
price = np.array([3.50, 0.04, 5.20, 0.30, 2.80])     # unit prices
print(qty, qty.dtype, qty.shape)
print(price, price.dtype)
```

```text
[ 120 5000  300  800  450] int64 (5,)
[3.5  0.04 5.2  0.3  2.8 ] float64
```

## Example 2: a 2-D array

Orders per day for three weeks (rows = weeks, columns = Saturday to Thursday; Friday is the weekend):

```python
week_orders = np.array([
    [8, 15, 14, 16, 13, 15],
    [7, 14, 15, 12, 16, 14],
    [9, 16, 13, 15, 14, 17],
])
print(week_orders.shape, week_orders.ndim, week_orders.size)
```

```text
(3, 6) 2 18
```

3 rows × 6 columns, 2 dimensions, 18 values.

## Example 3: indexing and slicing

```python
print(qty[0], qty[-1])          # first, last
print(qty[1:4])                 # positions 1, 2, 3
print(week_orders[1, 2])        # week 2, Mon
print(week_orders[:, 0])        # every Saturday
print(week_orders[0])           # week 1
```

```text
120 450
[5000  300  800]
15
[8 7 9]
[ 8 15 14 16 13 15]
```

| Syntax | Means |
|---|---|
| `a[0]`, `a[-1]` | First, last element (counting starts at 0) |
| `a[1:4]` | Positions 1 up to, **not including**, 4 |
| `m[row, col]` | One cell of a 2-D array |
| `m[:, 0]` | Every row, column 0 (`:` = "all") |

## Example 4: boolean masks — filter without loops

```python
value = qty * price
print(value)
big = value >= 1000
print(big)
print(value[big])
print(qty[(price < 1) & (qty > 1000)])
```

```text
[ 420.  200. 1560.  240. 1260.]
[False False  True False  True]
[1560. 1260.]
[5000]
```

- `value >= 1000` gives a **mask**: one True/False per element.
- `value[mask]` keeps only the True positions, like SQL `WHERE`.
- Combine conditions with `&` (and), `|` (or), `~` (not), and **brackets around each condition**.

## Example 5: sort by value

```python
order = np.argsort(value)[::-1]   # positions, biggest value first
print(order, value[order])
```

```text
[2 4 0 3 1] [1560. 1260.  420.  240.  200.]
```

`argsort` returns the **positions** that would sort the array; `[::-1]` reverses them. Use those positions to reorder any related array (`qty[order]`), so rows stay aligned.

## Example 6: reshape, stack and load a file

```python
daily = np.arange(1, 13)
print(daily.reshape(3, 4))
print(np.vstack([qty, price]).shape)
```

```text
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
(2, 5)
```

Load three numeric columns (quantity, unit price, revenue) from the 2025 orders:

```python
data = np.genfromtxt("data/orders_2025.csv", delimiter=",", skip_header=1, usecols=(8, 9, 15))
print(data.shape)
np.set_printoptions(suppress=True)   # plain numbers instead of 4.6160e+03
print(data[:3])
revenue = data[:, 2]
print(f"Orders: {len(revenue)}, total revenue: {revenue.sum():,.2f}, largest: {revenue.max():,.2f}")
```

```text
(4246, 3)
[[4616.       0.041  189.26 ]
 [ 256.       3.26   834.56 ]
 [6370.       0.041  248.11 ]]
Orders: 4246, total revenue: 5,898,071.17, largest: 44,127.55
```

(This total includes cancelled orders. Text columns like status are easier with pandas, in the next module.)

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `a[mask1 and mask2]` | `ValueError: truth value of an array … is ambiguous` | `a[(mask1) & (mask2)]` |
| Forgetting brackets: `price < 1 & qty > 1000` | Wrong result: `&` binds before `<` | Bracket each condition |
| Expecting `a[1:4]` to include position 4 | One element short | The end of a slice is excluded |
| Mixing text into a numeric array | Everything becomes text (`<U32` dtype) | Keep arrays numeric; use pandas for mixed tables |
| Changing a slice and surprising the original | Slices are **views** that share memory | Use `.copy()` when you need an independent array |

## Try it yourself

**Task:** Using `week_orders`, find (a) the total orders per week, and (b) which weekday columns ever had **16 or more** orders in a day.

<details markdown="1">
<summary>Show a hint</summary>

`week_orders.sum(axis=1)` adds across each row. `(week_orders >= 16).any(axis=0)` checks each column.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
print(week_orders.sum(axis=1))
days = np.array(["Sat", "Sun", "Mon", "Tue", "Wed", "Thu"])
print(days[(week_orders >= 16).any(axis=0)])
```

```text
[81 78 84]
['Sun' 'Tue' 'Wed' 'Thu']
```

`axis=1` works across columns (one result per row); `axis=0` works down rows (one result per column).
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What is the shape of an array with 4 rows and 12 columns?

1. `(12, 4)`
2. `(4, 12)`
3. `(48,)`

<details markdown="1"><summary>Show answer</summary>
**B.** Rows first, then columns.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `value[value >= 1000]` return?

1. True/False values
2. Only the values that are 1,000 or more
3. The positions of large values

<details markdown="1"><summary>Show answer</summary>
**B.** The mask selects matching elements.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. `a = np.array([1, 2.5, 3])`. What is `a.dtype`?

1. `int64`
2. `float64`
3. `object`

<details markdown="1"><summary>Show answer</summary>
**B.** One float makes the whole array float, because every element must share one type.
</details>
</div>

## Summary

- A NumPy array holds values of **one dtype** in a given **shape**.
- Index with positions and slices (`a[1:4]`, `m[:, 0]`); the slice end is excluded.
- Filter with **boolean masks** (`a[(x > 1) & (y < 5)]`), the array version of `WHERE`.
- `argsort` gives positions for sorting related arrays together; `reshape` and `vstack` change layout.

!!! job "Job-ready check"
    **Interview question:** *"Why is NumPy faster than a Python list for numerical work?"*

    **Strong answer:** "An array stores one data type in a continuous block of memory, and operations run in compiled code over the whole block, instead of the Python interpreter looping element by element. That's also why NumPy needs a single dtype."

    **Mini project:** Load `quantity`, `unit_price` and `revenue` from `orders_2025.csv`, and use masks to count how many orders are above 5,000 in revenue and what share of total revenue they bring.
