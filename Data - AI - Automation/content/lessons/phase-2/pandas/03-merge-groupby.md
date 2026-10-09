---
title: "pandas Merge & groupby: Join Tables and Summarise Like SQL"
order: 3
summary: "Join orders with customers and products safely using merge, find unmatched rows, and summarise with groupby, named aggregations and transform."
level: Beginner
time: "50 min"
topics: ["Merge", "groupby"]
prerequisites: ["phase-2/pandas/02-cleaning", "phase-1/analytical-sql/04-joins"]
keywords: [merge, join, left join, anti join, validate, indicator, many_to_one, groupby, agg, named aggregation, nunique, transform, share of total, margin, top customers]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, phase-2/customers_2025.csv, phase-2/products_2025.csv]
resources:
  - title: "Merge, join, concatenate and compare"
    url: "https://pandas.pydata.org/docs/user_guide/merging.html"
    source: "pandas official docs"
    note: "All join types, with diagrams, plus validate and indicator."
  - title: "Group by: split-apply-combine"
    url: "https://pandas.pydata.org/docs/user_guide/groupby.html"
    source: "pandas official docs"
    note: "Aggregation, transformation and filtration."
  - title: "Comparison with SQL"
    url: "https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html"
    source: "pandas official docs"
    note: "JOIN and GROUP BY side by side with pandas."
---

## What is it?

- **`merge`** joins two DataFrames on matching key columns, exactly like SQL `JOIN` (and Power Query *Merge*).
- **`groupby`** splits rows into groups, applies a calculation, and combines the results: SQL's `GROUP BY`.

| SQL | pandas |
|---|---|
| `orders LEFT JOIN customers USING (customer_id)` | `orders.merge(customers, on="customer_id", how="left")` |
| `SUM(revenue) … GROUP BY region` | `df.groupby("region")["revenue"].sum()` |
| `COUNT(DISTINCT customer_id)` | `("customer_id", "nunique")` inside `agg` |
| Window function `SUM(...) OVER (PARTITION BY …)` | `groupby(...)["col"].transform("sum")` |

!!! job "Why it matters at work"
    Real questions need several tables: "margin by category" needs costs, "revenue by customer name" needs the customer table. Joining safely (no duplicated rows, no lost rows) and summarising cleanly is everyday analyst and data-science work, and a standard interview task.

The script is `05_pandas_merge_groupby.py`. Tables: `orders_2025.csv` (4,246 rows), `customers_2025.csv` (63) and `products_2025.csv` (12).

## Example 1: merge safely

```python
import pandas as pd

orders = pd.read_csv("data/orders_2025.csv")
customers = pd.read_csv("data/customers_2025.csv")
products = pd.read_csv("data/products_2025.csv")

df = orders.merge(customers[["customer_id", "customer_name", "credit_days"]],
                  on="customer_id", how="left", validate="many_to_one", indicator=True)
print(df.shape)
print(df["_merge"].value_counts())
df = df.drop(columns="_merge")
```

```text
(4246, 19)
_merge
both          4246
left_only        0
right_only       0
Name: count, dtype: int64
```

Two safety switches:

- **`validate="many_to_one"`** raises an error if a customer ID appears twice in `customers`. Without it, a duplicate customer would silently **duplicate orders** and inflate revenue.
- **`indicator=True`** adds `_merge`, showing whether each row matched. All 4,246 orders found their customer, and the row count didn't change.

| `how=` | Keeps |
|---|---|
| `"inner"` | Only matching rows |
| `"left"` | Every row of the left table (most common for facts + dimension) |
| `"right"` / `"outer"` | Every right row / every row from both |

## Example 2: who never ordered? (anti-join)

```python
ids = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
print(ids.loc[ids["_merge"] == "left_only", ["customer_id", "customer_name", "segment"]])
```

```text
   customer_id   customer_name        segment
60        C061  Lotus Knitwear  Knitting Mill
61        C062  Padma Boutique       Retailer
62        C063  Harbor Trading         Trader
```

Three December sign-ups haven't ordered yet: a list for the sales team. (`drop_duplicates()` first, so the merge doesn't repeat each customer once per order.)

## Example 3: groupby with one aggregate

```python
net = df[df["status"] != "Cancelled"]
print(net.groupby("region")["revenue"].sum().sort_values(ascending=False).round(0))
```

```text
region
Chattogram     2057404.0
Dhaka          1835497.0
Narayanganj     583516.0
Gazipur         571973.0
Khulna          429968.0
Name: revenue, dtype: float64
```

## Example 4: named aggregations

```python
seg = net.groupby("segment").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    avg_order=("revenue", "mean"),
    customers=("customer_id", "nunique"),
).sort_values("revenue", ascending=False)
seg["share"] = seg["revenue"] / seg["revenue"].sum()
print(seg.round({"revenue": 0, "avg_order": 0, "share": 3}))
```

```text
                 orders    revenue  avg_order  customers  share
segment
Garment Factory    2594  4234667.0     1632.0         25  0.773
Knitting Mill       643   806868.0     1255.0         11  0.147
Trader              470   353757.0      753.0         11  0.065
Retailer            256    83065.0      324.0         13  0.015
```

`new_name=("column", "function")` gives readable output columns. Garment factories bring **77%** of net revenue from 25 customers: a concentration risk worth mentioning to management.

## Example 5: margin by category (merge-free, with an extra column)

```python
net = net.assign(cost=net["quantity"] * net["unit_cost"])
cat = net.groupby("category")[["revenue", "cost"]].sum()
cat["margin_pct"] = (1 - cat["cost"] / cat["revenue"]) * 100
print(cat.round(1))
```

```text
            revenue       cost  margin_pct
category
Fabric    2362740.6  1823788.6        22.8
Trims      867538.8   559883.4        35.5
Yarn      2248078.5  1696594.6        24.5
```

Trims are the smallest category by revenue but the most profitable for every unit of revenue. (`unit_cost` is already in the orders file; in a real model you'd merge it from `products`.)

## Example 6: top customers and transform

```python
top = (net.groupby(["customer_id", "customer_name"])["revenue"].sum()
          .sort_values(ascending=False).head(5).round(0))
print(top)
```

```text
customer_id  customer_name
C010         Ocean Apparel     295414.0
C044         Prime Garments    255781.0
C037         Silver Fashion    225647.0
C014         Prime Apparel     223498.0
C017         Delta Garments    223207.0
Name: revenue, dtype: float64
```

`transform` returns a value for **every row**, like a SQL window function. Here: each order's share of its customer's total.

```python
net = net.assign(cust_total=net.groupby("customer_id")["revenue"].transform("sum"))
net = net.assign(share_of_customer=net["revenue"] / net["cust_total"])
print(net.loc[net["share_of_customer"].idxmax(), ["order_id", "customer_name", "revenue", "cust_total", "share_of_customer"]])
```

```text
order_id                      11121
customer_name        Asian Boutique
revenue                     4705.65
cust_total                 10116.63
share_of_customer           0.46514
Name: 1120, dtype: object
```

One order is 47% of Asian Boutique's whole year: a single-order dependency.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Merging on a key that isn't unique on the "one" side | Rows multiply, totals inflate | `validate="many_to_one"`, and check `shape` before and after |
| Different key types (`"C010"` vs `10`, or int vs str) | Nothing matches | Check `dtypes` on both sides |
| Using `inner` by accident | Unmatched rows silently vanish | `how="left"` + `indicator=True` |
| `groupby(...).sum()` on every column | Nonsense sums (IDs, prices) | Select columns, or use named `agg` |
| Forgetting to exclude cancelled orders | Revenue overstated | Filter **before** grouping |

## Try it yourself

**Task:** Using the merged `df` (with `credit_days`), calculate the **cancellation rate** for each credit-terms group (0, 15, 30, 60 days). What pattern do you see?

<details markdown="1">
<summary>Show a hint</summary>

Group by `credit_days`, count orders, and count rows where `status == "Cancelled"` with a small `lambda`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
rate = df.groupby("credit_days").agg(orders=("order_id", "count"),
                                     cancelled=("status", lambda s: (s == "Cancelled").sum()))
rate["cancel_rate_pct"] = (rate["cancelled"] / rate["orders"] * 100).round(1)
print(rate)
```

```text
             orders  cancelled  cancel_rate_pct
credit_days
0              1353         44              3.3
15              880         38              4.3
30             1366        111              8.1
60              647         90             13.9
```

The longer the credit terms, the more orders are cancelled: 3.3% at cash terms, 13.9% at 60 days. That's a **pattern**, not yet proof of cause (EDA and A/B testing modules), but a strong lead for the credit team.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. After a left merge, your 4,246 orders became 4,300 rows. What's the most likely cause?

1. The left table had missing values
2. The right table has duplicate keys
3. `how="left"` always adds rows

<details markdown="1"><summary>Show answer</summary>
**B.** Each duplicate key on the "one" side repeats the matching orders. `validate="many_to_one"` catches it.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which pandas tool behaves like `SUM(revenue) OVER (PARTITION BY customer_id)`?

1. `groupby("customer_id")["revenue"].sum()`
2. `groupby("customer_id")["revenue"].transform("sum")`
3. `merge(...)`

<details markdown="1"><summary>Show answer</summary>
**B.** `transform` keeps every row; `sum()` returns one row per group.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. How do you count distinct customers per segment in `agg`?

1. `customers=("customer_id", "count")`
2. `customers=("customer_id", "nunique")`
3. `customers=("customer_id", "sum")`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- `merge(on=..., how="left", validate=..., indicator=True)` joins safely; check row counts before and after.
- Anti-join = left merge + `_merge == "left_only"`.
- `groupby(...).agg(name=("col", "func"))` gives clear summaries; filter first, then group.
- `transform` returns group results on every row, for shares and comparisons with the group.

!!! job "Job-ready check"
    **Interview question:** *"How do you make sure a join hasn't duplicated or dropped rows?"*

    **Strong answer:** "I check the key is unique on the 'one' side, use `validate='many_to_one'`, compare row counts and a known total before and after, and use an indicator column to count unmatched rows on each side. Then I decide deliberately whether unmatched rows should be kept, fixed or reported."

    **Mini project:** Build a customer summary table: name, segment, credit days, net revenue, orders, average order, cancellation rate and share of company revenue. Sort it and write three bullet points of findings for the sales manager.
