---
title: "Cleaning Data with pandas: From Messy Export to Trusted Table"
order: 2
summary: "Fix column names, text, numbers stored as text, duplicates, impossible values, typo outliers and missing values — then prove the result is right against a known clean file."
level: Beginner
time: "55 min"
topics: ["Cleaning"]
prerequisites: ["phase-2/pandas/01-dataframe-basics"]
keywords: [data cleaning, pandas cleaning, str.strip, str.title, to_numeric, astype, duplicated, drop_duplicates, missing values, isna, fillna, outlier, transform, assert_frame_equal, validation, data quality]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025_raw.csv, phase-2/orders_2025.csv]
resources:
  - title: "Working with missing data"
    url: "https://pandas.pydata.org/docs/user_guide/missing_data.html"
    source: "pandas official docs"
    note: "NaN, NA, isna, fillna and dropna."
  - title: "Working with text data"
    url: "https://pandas.pydata.org/docs/user_guide/text.html"
    source: "pandas official docs"
    note: "The .str methods: strip, lower, replace, contains and more."
  - title: "Duplicate labels and drop_duplicates"
    url: "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html"
    source: "pandas API reference"
    note: "Options for keeping the first, last or no duplicate."
---

## What is it?

**Data cleaning** turns a raw export into a table you can trust: consistent names and text, correct types, no duplicates, no impossible values, and missing values that are **explained**. You did this with Power Query in Phase 1 and with the CSV cleaner in Phase 0; pandas does it in a few lines of repeatable code.

!!! job "Why it matters at work"
    Analysts commonly say most of their time goes on preparing data. Every wrong cleaning decision flows straight into dashboards and models. Being able to say *what* you changed, *why*, and *how you checked it* is what makes your numbers trusted.

The raw file `orders_2025_raw.csv` is the same 2025 data after a messy ERP export. The script is `04_pandas_cleaning.py`.

## Step 1: profile the raw file

```python
import pandas as pd

raw = pd.read_csv("data/orders_2025_raw.csv")
print(raw.shape)
print(raw.dtypes[["Qty", "Unit Price", "Delivery Days"]])
print(raw["Region"].unique())
print(raw["Status"].value_counts())
```

```text
(4264, 14)
Qty                  str
Unit Price       float64
Delivery Days    float64
dtype: object
<ArrowStringArray>
[  'Chattogram',  'Narayanganj',      'Gazipur',       'Khulna',        'Dhaka',       'DHAKA ',  'CHATTOGRAM ',
      'KHULNA ',     'GAZIPUR ', 'NARAYANGANJ ']
Length: 10, dtype: str
Status
Delivered     3863
Cancelled      282
Shipped         45
Pending         44
 delivered      26
 cancelled       2
 pending         1
 shipped         1
Name: count, dtype: int64
```

Problems found: **Qty is text** (it shouldn't be), 10 region spellings for 5 regions, statuses with spaces and lower case, and 4,264 rows where the ERP says 4,246 orders. (The exact look of `unique()` depends on whether `pyarrow` is installed; the values are the same.)

## Step 2: tidy column names

```python
df = raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.rename(columns={"qty": "quantity"})
print(list(df.columns))
```

```text
['order_id', 'order_date', 'customer_id', 'region', 'segment', 'channel', 'category', 'product', 'quantity', 'unit_price', 'discount', 'status', 'promised_days', 'delivery_days']
```

`snake_case` names are easy to type and match the SQL tables.

## Step 3: clean text

```python
df["region"] = df["region"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.title()
print(df["region"].value_counts())
print(df["status"].value_counts())
```

```text
region
Chattogram     1541
Dhaka          1410
Gazipur         509
Narayanganj     473
Khulna          331
Name: count, dtype: int64
status
Delivered    3889
Cancelled     284
Shipped       46
Pending       45
Name: count, dtype: int64
```

5 regions and 4 statuses. (The counts still include duplicates; Step 5 removes them.)

## Step 4: numbers stored as text

```python
bad = pd.to_numeric(df["quantity"], errors="coerce").isna()
print(df.loc[bad, "quantity"].head(3).tolist(), bad.sum())
df["quantity"] = df["quantity"].str.replace(",", "", regex=False).astype("int64")
print(df["quantity"].dtype)
```

```text
['3,052', '1,235', '15,347'] 25
int64
```

`to_numeric(errors="coerce")` turns anything that isn't a number into `NaN`, a quick way to **find** the problem values before fixing them. 25 quantities had thousands separators.

## Step 5: duplicates

```python
print(df.duplicated().sum(), "exact duplicate rows")
print(df["order_id"].duplicated().sum(), "duplicate order IDs")
df = df.drop_duplicates()
print(len(df), df["order_id"].is_unique)
```

```text
18 exact duplicate rows
18 duplicate order IDs
4246 True
```

Always check both: whole-row duplicates (safe to drop) and duplicate **keys** (two different rows with the same ID need investigating). Here they're the same 18, so dropping them leaves 4,246 unique orders.

## Step 6: impossible values

```python
print(df.loc[df["quantity"] <= 0, ["order_id", "product", "quantity"]])
df["quantity"] = df["quantity"].abs()          # assumption (confirmed with ERP owner): sign error
```

```text
      order_id         product  quantity
341      10338   Metal Buttons    -13489
2089     12080  Polyester Yarn      -698
```

A negative quantity could be a **return** or a **typing error**. You can't tell from the data: ask the data owner, then write the decision down next to the code.

## Step 7: outliers that are errors

Compare each price with the median price **of the same product**:

```python
median_price = df.groupby("product")["unit_price"].transform("median")
ratio = df["unit_price"] / median_price
print(df.loc[ratio > 10, ["order_id", "product", "unit_price"]].assign(median=median_price[ratio > 10]))
df.loc[ratio > 10, "unit_price"] = df.loc[ratio > 10, "unit_price"] / 100
```

```text
      order_id       product  unit_price  median
2035     12026  Cotton Twill       355.0    3.49
3362     13352  Cotton Twill       344.0    3.49
3642     13629  Cotton Twill       346.0    3.49
```

Prices about 100× the usual 3.49 are a decimal-point slip (3.55 typed as 355). `transform("median")` returns one value **per row** (the median of that row's product), so it lines up with the data. Real large orders, such as the 44,127 bulk order, are **not** errors and stay.

## Step 8: missing values — explain, don't just fill

```python
print(df.isna().sum()[lambda s: s > 0])
print(df.loc[df["delivery_days"].isna(), "status"].value_counts())
```

```text
delivery_days    374
dtype: int64
status
Cancelled    283
Shipped       46
Pending       45
Name: count, dtype: int64
```

All 374 missing delivery times belong to orders that **haven't been delivered**. That's correct data, so filling them with 0 or the average would be wrong. Missing values need a reason, not a reflex.

| Situation | Usual choice |
|---|---|
| Missing because it doesn't apply (not delivered) | Leave missing; filter when analysing |
| Missing at random, few rows | Drop those rows for that analysis, and say how many |
| Needed for a model | Fill (impute) with a documented rule, e.g. median per group |
| Missing key fields (ID, date) | Reject the row and report it |

## Step 9: types, derived columns and validation

```python
df["order_date"] = pd.to_datetime(df["order_date"])
df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)

clean = pd.read_csv("data/orders_2025.csv", parse_dates=["order_date"])
check = clean[list(df.columns)]
print(len(df) == len(check), df["order_id"].is_unique)
pd.testing.assert_frame_equal(df.reset_index(drop=True), check, check_dtype=False)
print("Cleaned data matches orders_2025.csv")
print(round(df.loc[df["status"] != "Cancelled", "revenue"].sum(), 2))
```

```text
True True
Cleaned data matches orders_2025.csv
5478357.79
```

`assert_frame_equal` raises an error at the first difference, so a silent mistake can't slip through. The cleaned data is identical to the official clean file, and net revenue matches the known answer.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `fillna(0)` on everything | Fake zeros distort averages | Explain each missing pattern first |
| Dropping all outliers | Real big customers disappear | Separate errors (impossible) from rare-but-real |
| `drop_duplicates()` without checking keys | Conflicting rows with the same ID survive | Also check `df["id"].duplicated()` |
| Cleaning in place on `raw` | No way to compare before/after | Work on `raw.copy()` |
| No validation step | Errors found by the CFO | Row counts, unique keys, known totals, `assert` |

## Try it yourself

**Task:** Turn Steps 2–9 into one function, `clean_orders(path)`, that ends with `assert` checks (unique IDs, positive quantities, only the 4 known statuses). Run it on the raw file and print the shape and net revenue.

<details markdown="1">
<summary>Show the solution</summary>

```python
def clean_orders(path: str) -> pd.DataFrame:
    d = pd.read_csv(path)
    d.columns = d.columns.str.strip().str.lower().str.replace(" ", "_")
    d = d.rename(columns={"qty": "quantity"})
    for col in ["region", "status"]:
        d[col] = d[col].str.strip().str.title()
    d["quantity"] = d["quantity"].str.replace(",", "", regex=False).astype("int64").abs()
    d = d.drop_duplicates()
    med = d.groupby("product")["unit_price"].transform("median")
    d.loc[d["unit_price"] / med > 10, "unit_price"] /= 100
    d["order_date"] = pd.to_datetime(d["order_date"])
    d["revenue"] = (d["quantity"] * d["unit_price"] * (1 - d["discount"])).round(2)
    assert d["order_id"].is_unique, "duplicate order IDs"
    assert (d["quantity"] > 0).all(), "non-positive quantities"
    assert d["status"].isin(["Delivered", "Shipped", "Pending", "Cancelled"]).all(), "unknown status"
    return d


result = clean_orders("data/orders_2025_raw.csv")
print(result.shape, round(result.loc[result.status != "Cancelled", "revenue"].sum(), 2))
```

```text
(4246, 15) 5478357.79
```

A function plus assertions is a small, testable pipeline: exactly the pattern of the Phase 0 CSV cleaner.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. `delivery_days` is missing for 374 orders, all cancelled, shipped or pending. What should you do?

1. Fill with 0
2. Fill with the average
3. Leave them missing, and filter to delivered orders when analysing delivery time

<details markdown="1"><summary>Show answer</summary>
**C.** The values are missing for a valid reason.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `groupby("product")["unit_price"].transform("median")` return?

1. One median per product (a short table)
2. One value per row: the median price of that row's product
3. The overall median

<details markdown="1"><summary>Show answer</summary>
**B.** `transform` keeps the original row count, so you can compare each row with its group.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which check proves your cleaned table matches a trusted version?

1. `df.head()`
2. `pd.testing.assert_frame_equal(df, trusted)`
3. `df.info()`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Profile first: types, distinct values, counts, duplicates, missing values.
- Fix names and text (`.str.strip().str.title()`), convert text numbers, drop duplicates (checking keys).
- Separate **errors** (negative quantity, ×100 price) from **rare but real** values; document assumptions.
- Explain missing values before handling them.
- Validate: row counts, unique keys, known totals and `assert_frame_equal`.

!!! job "Job-ready check"
    **Interview question:** *"How do you decide whether an outlier is an error?"*

    **Strong answer:** "I compare it with its context, such as the same product's typical price or the customer's usual order size, and check whether it's physically possible. A price 100 times the median is almost certainly a decimal slip; a bulk order from a large factory is rare but real. I confirm with the data owner, fix errors in a documented step, and keep real extremes, using robust statistics like the median when they distort averages."

    **Mini project:** Write `clean_orders()` in its own file with a pytest test that runs it on the raw file and checks 4,246 rows and net revenue 5,478,357.79, the Phase 0 testing habits applied to data.
