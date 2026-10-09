---
title: "pandas DataFrame Basics: Load, Explore, Select and Filter"
order: 1
summary: "Load a CSV into a DataFrame, check its shape, types and statistics, select columns and rows with loc and iloc, filter and sort like SQL, and add calculated columns."
level: Beginner
time: "45 min"
topics: ["DataFrame basics"]
prerequisites: ["phase-2/numpy/01-arrays-indexing"]
keywords: [pandas, dataframe, series, read_csv, head, shape, dtypes, describe, info, loc, iloc, filter, boolean indexing, sort_values, value_counts, query, new column, str dtype, pandas 3]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv]
resources:
  - title: "10 minutes to pandas"
    url: "https://pandas.pydata.org/docs/user_guide/10min.html"
    source: "pandas official docs"
    note: "The official quick tour of the most-used features."
  - title: "Getting started tutorials"
    url: "https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html"
    source: "pandas official docs"
    note: "Short visual tutorials: reading, selecting, plotting, new columns."
  - title: "Comparison with SQL"
    url: "https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html"
    source: "pandas official docs"
    note: "Every common SQL query, written in pandas."
---

## What is it?

- A **DataFrame** is a table: rows, named columns, and one data type per column.
- A **Series** is one column (or one row) of a DataFrame.
- pandas sits on top of NumPy, so filters and maths are vectorized.

| You know | pandas equivalent |
|---|---|
| Excel sheet / SQL table | `DataFrame` |
| `SELECT region, revenue` | `df[["region", "revenue"]]` |
| `WHERE region = 'Dhaka'` | `df[df["region"] == "Dhaka"]` |
| `ORDER BY revenue DESC` | `df.sort_values("revenue", ascending=False)` |
| `COUNT(*) … GROUP BY status` | `df["status"].value_counts()` |

!!! job "Why it matters at work"
    pandas is the most requested Python skill in data analyst and data scientist job adverts, and it is the usual first step in machine-learning and AI data preparation. Interview coding tasks almost always start with "load this CSV and tell me…".

The script is `03_pandas_basics.py` in [data-science-scripts.zip](../../../downloads/phase-2/data-science-scripts.zip).

## Example 1: load and look

```python
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)

orders = pd.read_csv("data/orders_2025.csv")
print(orders.shape)
print(orders.head(3))
```

```text
(4246, 16)
   order_id  order_date customer_id       region        segment  ... unit_cost     status promised_days  \
0     10001  2025-01-01        C042   Chattogram  Knitting Mill  ...     0.025  Delivered             5
1     10002  2025-01-01        C007  Narayanganj  Knitting Mill  ...     2.450  Cancelled             3
2     10003  2025-01-01        C028      Gazipur         Trader  ...     0.025  Delivered             3

   delivery_days  revenue
0            3.0   189.26
1            NaN   834.56
2            2.0   248.11

[3 rows x 16 columns]
```

4,246 orders × 16 columns. `...` means columns are hidden to fit the screen. The left-most numbers (0, 1, 2) are the **index**, pandas' row labels.

## Example 2: check the column types

```python
print(orders.dtypes)
```

```text
order_id           int64
order_date           str
customer_id          str
region               str
segment              str
channel              str
category             str
product              str
quantity           int64
unit_price       float64
discount         float64
unit_cost        float64
status               str
promised_days      int64
delivery_days    float64
revenue          float64
dtype: object
```

- Text columns are `str` (new in pandas 3; older versions showed `object`).
- `order_date` is **text**, not a date yet: you'll convert it in the Datetime lesson.
- `delivery_days` is `float64` because it has missing values (`NaN`).

## Example 3: summary statistics

```python
print(orders[["quantity", "revenue", "delivery_days"]].describe().round(2))
```

```text
        quantity   revenue  delivery_days
count    4246.00   4246.00        3872.00
mean     3153.99   1389.09           3.44
std      6814.85   1461.19           2.03
min        17.00     36.04           1.00
25%       392.25    554.21           2.00
50%       823.00   1062.30           3.00
75%      3122.75   1794.22           4.00
max    250160.00  44127.55          17.00
```

Read it like a detective: `delivery_days` has 374 fewer values (not delivered yet); revenue's mean (1,389) is well above its median (1,062), so a few big orders pull it up; max quantity 250,160 deserves a look (it's a bulk trims order).

## Example 4: select columns and rows

```python
print(orders[["order_id", "region", "revenue"]].head(3))
print(orders.loc[0, "product"], "|", orders.iloc[0, 7])
```

```text
   order_id       region  revenue
0     10001   Chattogram   189.26
1     10002  Narayanganj   834.56
2     10003      Gazipur   248.11
Metal Buttons | Metal Buttons
```

| Accessor | Selects by | Example |
|---|---|---|
| `df["col"]` / `df[["a", "b"]]` | Column name(s) | `orders["revenue"]` |
| `df.loc[rows, cols]` | **Labels** (index values, column names) | `orders.loc[0, "product"]` |
| `df.iloc[rows, cols]` | **Positions** (0, 1, 2…) | `orders.iloc[0, 7]` |

## Example 5: filter rows

```python
dhaka_big = orders[(orders["region"] == "Dhaka") & (orders["revenue"] > 10000)]
print(len(dhaka_big))
print(dhaka_big[["order_id", "customer_id", "product", "revenue"]])
```

```text
5
      order_id customer_id          product   revenue
1483     11484        C035       Denim 12oz  10998.34
2202     12203        C013  Cotton Yarn 30s  11269.07
2376     12377        C046       Denim 12oz  12581.04
3269     13270        C039     Viscose Yarn  13091.76
3824     13825        C059    Sewing Thread  44127.55
```

Same rules as NumPy masks: `&`, `|`, `~` and brackets around each condition. `query()` is a readable alternative:

```python
print(orders.query("region == 'Khulna' and status == 'Cancelled'").shape)
```

```text
(16, 17)
```

(17 columns, because Example 6 added one.)

## Example 6: sort, count and add a column

```python
print(orders.sort_values("revenue", ascending=False)[["order_id", "segment", "revenue"]].head(3))
print(orders["status"].value_counts())
orders["is_net"] = orders["status"] != "Cancelled"
print(orders.loc[orders["is_net"], "revenue"].sum().round(2))
```

```text
      order_id          segment   revenue
3824     13825  Garment Factory  44127.55
2934     12935  Garment Factory  25381.04
1550     11551    Knitting Mill  13927.33
status
Delivered    3872
Cancelled     283
Shipped        46
Pending        45
Name: count, dtype: int64
5478357.79
```

**Known answer for Phase 2:** net revenue for 2025 (excluding cancelled orders) = **5,478,357.79**.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `df["region", "revenue"]` | `KeyError` | Double brackets: `df[["region", "revenue"]]` |
| `df[df.region == "Dhaka" and df.revenue > 1]` | `ValueError: truth value … ambiguous` | `&` with brackets around each condition |
| Mixing up `loc` and `iloc` | Wrong rows after sorting or filtering | `loc` = labels, `iloc` = positions |
| Chained assignment: `df[df.x > 1]["y"] = 0` | No change (pandas 3 never modifies through a chain) | `df.loc[df.x > 1, "y"] = 0` |
| Trusting a column's type | Maths on text, or dates as text | Check `df.dtypes` first |

## Try it yourself

**Task:** How many **Portal** orders were **cancelled**, and what is the average revenue of non-cancelled Portal orders?

<details markdown="1">
<summary>Show a hint</summary>

Build two masks, `orders["channel"] == "Portal"` and `orders["status"] == "Cancelled"`, and combine them.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
portal = orders["channel"] == "Portal"
cancelled = orders["status"] == "Cancelled"
print((portal & cancelled).sum())
print(orders.loc[portal & ~cancelled, "revenue"].mean().round(2))
```

```text
129
1463.7
```

129 cancelled Portal orders; the rest average 1,463.70.

`.sum()` on a True/False column counts the Trues; `~` means "not".
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which selects rows 0–4 **by position**?

1. `df.loc[0:4]`
2. `df.iloc[0:5]`
3. `df["0:5"]`

<details markdown="1"><summary>Show answer</summary>
**B.** `iloc` uses positions with an exclusive end. (`loc[0:4]` uses labels and *includes* 4, which only matches here by coincidence.)
</details>
</div>

<div class="quiz-q" markdown="1">
2\. In pandas 3, a column of text has which dtype?

1. `object`
2. `str`
3. `category`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does `df["status"].value_counts()` do?

1. Counts rows per distinct status
2. Counts all non-empty cells in the DataFrame
3. Sorts the DataFrame by status

<details markdown="1"><summary>Show answer</summary>
**A.** Like `COUNT(*) … GROUP BY status`.
</details>
</div>

## Summary

- `pd.read_csv` → check `shape`, `head()`, `dtypes` and `describe()` first.
- Select with `df[[cols]]`, `loc` (labels) and `iloc` (positions).
- Filter with masks or `query()`; sort with `sort_values`; count with `value_counts`.
- Add columns with vectorized expressions; set values with `loc`, never chained indexing.

!!! job "Job-ready check"
    **Interview question:** *"You get a new CSV. What do you check in the first five minutes?"*

    **Strong answer:** "Shape, the first rows, the column types, missing values per column and `describe()` for ranges and outliers. Then the distinct values of key categories, duplicates on the ID column, and one known total I can reconcile with the source, before any analysis."

    **Mini project:** For `orders_2025.csv`, write a short "data profile": row count, columns and types, missing values per column (`orders.isna().sum()`), the three largest orders, and net revenue. Check that you get 5,478,357.79.
