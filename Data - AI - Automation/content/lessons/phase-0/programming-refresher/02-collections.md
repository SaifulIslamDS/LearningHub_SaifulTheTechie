---
title: "Python Collections: Lists, Dictionaries, Sets & Tuples"
order: 2
summary: "Hold many values with lists, tuples, dictionaries and sets; filter with comprehensions; and group and sort data the way SQL GROUP BY does."
level: Beginner
time: "45 min"
topics: ["Collections"]
prerequisites: ["phase-0/programming-refresher/01-basics"]
keywords: [list, tuple, dict, dictionary, set, comprehension, list comprehension, dict comprehension, unpacking, sorted, lambda, key, get, append, len, in]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip]
resources:
  - title: "Data Structures (Python tutorial)"
    url: "https://docs.python.org/3/tutorial/"
    source: "Python official docs"
    note: "Section 5: lists, tuples, sets, dictionaries and comprehensions."
---

## What is it?

| Collection | Looks like | Ordered? | Change it? | Use it for |
|---|---|---|---|---|
| **list** | `[420, 200, 1560]` | ✅ | ✅ | A sequence of items: rows, values |
| **tuple** | `(1, "Rahim Traders", 420.0)` | ✅ | ❌ | A fixed record |
| **dict** | `{"Dhaka": 3170.0}` | ✅ (insertion) | ✅ | Look-ups by key; totals per group |
| **set** | `{"Dhaka", "Gazipur"}` | ❌ | ✅ | Unique values, fast membership tests |

!!! job "Why it matters at work"
    JSON from APIs is dictionaries and lists. Rows from a CSV are dictionaries. LLM API messages are a list of dictionaries. Grouping, de-duplicating and sorting with these collections is daily work, and a classic interview task ("revenue per customer, sorted").

Open `02_collections.py` from [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip). It holds the 12 practice orders as tuples: `(order_id, customer, region, value, status)`.

## Example 1: filter a list with a comprehension

```python
net = [o for o in orders if o[4] != "Cancelled"]
print("Net orders:", len(net))
```

```text
Net orders: 11
```

A **list comprehension** reads: *"a list of `o`, for each `o` in `orders`, if the status isn't Cancelled"*. It's the Python version of `SELECT … WHERE`.

## Example 2: tuple unpacking

```python
order_id, customer, region, value, status = orders[0]
print(order_id, customer, value)
```

```text
1 Rahim Traders 420.0
```

Use `_` for values you don't need: `for _, _, region, value, _ in net:`.

## Example 3: a dictionary as GROUP BY

```python
revenue_by_region: dict[str, float] = {}
for _, _, region, value, _ in net:
    revenue_by_region[region] = revenue_by_region.get(region, 0) + value
print(revenue_by_region)
```

```text
{'Dhaka': 3170.0, 'Chattogram': 2155.0, 'Gazipur': 2520.0, 'Narayanganj': 1230.0}
```

`.get(region, 0)` returns the current total, or 0 the first time a region appears. These are the same totals as `SUM(...) GROUP BY region` in SQL.

## Example 4: sort by value

```python
for region, rev in sorted(revenue_by_region.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{region:<12}{rev:>8.2f}")
```

```text
Dhaka        3170.00
Gazipur      2520.00
Chattogram   2155.00
Narayanganj  1230.00
```

- `.items()` gives `(key, value)` pairs.
- `key=lambda kv: kv[1]` says "sort by the value". `reverse=True` = descending (`ORDER BY … DESC`).

## Example 5: sets and dict comprehensions

```python
customers = {o[1] for o in orders}                       # set comprehension
print(len(customers), "customers:", sorted(customers))

counts = {c: sum(1 for o in orders if o[1] == c) for c in sorted(customers)}
print(counts)
```

```text
5 customers: ['Delta Knit', 'Karim Garments', 'Nova Apparel', 'Rahim Traders', 'Sun Fashion']
{'Delta Knit': 2, 'Karim Garments': 3, 'Nova Apparel': 2, 'Rahim Traders': 3, 'Sun Fashion': 2}
```

A set removes duplicates automatically (12 orders → 5 customers), just like `COUNT(DISTINCT customer)`.

## Handy operations

| Task | Code |
|---|---|
| Add to a list | `values.append(810)` |
| Is it in there? | `"Dhaka" in regions` (fast for sets and dict keys) |
| Count items | `len(orders)` |
| Sum, min, max | `sum(values)`, `min(values)`, `max(values, key=...)` |
| Loop with a position | `for i, row in enumerate(rows, start=1):` |
| Missing key safely | `d.get("key", default)` |
| Set maths | `a | b` (union), `a & b` (in both), `a - b` (in a, not b) |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `d[key] += v` for a new key | `KeyError` | `d[key] = d.get(key, 0) + v` |
| Changing a list while looping over it | Skipped items | Build a new list with a comprehension |
| `sorted(d)` expecting values | Sorted **keys** only | `sorted(d.items(), key=lambda kv: kv[1])` |
| Using a list for membership checks on big data | Slow | Use a set |
| Positional tuples everywhere (`o[4]`) | Hard to read | Dicts or dataclasses (lesson 4) |

## Try it yourself

**Task:** Using `orders`, print **net revenue per customer** (excluding Cancelled), biggest first, aligned in two columns.

<details markdown="1">
<summary>Show a hint</summary>

The same pattern as Example 3, keyed on `customer` with an `if status != "Cancelled"` check, then sort as in Example 4.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
revenue: dict[str, float] = {}
for _, customer, _, value, status in orders:
    if status != "Cancelled":
        revenue[customer] = revenue.get(customer, 0) + value

for customer, total in sorted(revenue.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{customer:<16}{total:>8.2f}")
```

```text
Delta Knit       2520.00
Karim Garments   2155.00
Nova Apparel     1880.00
Rahim Traders    1290.00
Sun Fashion      1230.00
```

The total is 9,075, as everywhere else. (File: `solutions/ex02_revenue_by_customer.py`.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which collection removes duplicates automatically?

1. list
2. set
3. tuple

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `{"a": 1}.get("b", 0)` return?

1. `KeyError`
2. `0`
3. `None`

<details markdown="1"><summary>Show answer</summary>
**B.** The default you passed.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which SQL idea matches `[o for o in orders if o[4] != "Cancelled"]`?

1. `WHERE`
2. `JOIN`
3. `ORDER BY`

<details markdown="1"><summary>Show answer</summary>
**A.**
</details>
</div>

## Summary

- **list** = ordered items; **tuple** = fixed record; **dict** = key → value; **set** = unique values.
- Comprehensions filter and transform in one readable line (`WHERE`).
- A dict with `.get(key, 0) + value` is a GROUP BY; `sorted(..., key=..., reverse=True)` is ORDER BY.
- Sets give unique counts (`COUNT DISTINCT`) and fast membership checks.

!!! job "Job-ready check"
    **Interview question:** *"Given a list of order records, return the top 3 customers by revenue."*

    **Strong answer:** Accumulate totals in a dict with `.get()` (or `collections.Counter` / `defaultdict`), then `sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:3]`. Mention ties and excluded statuses, and that for large data you'd use SQL or pandas.

    **Mini project:** Add revenue **per region and status** to `02_collections.py`, using tuple keys like `("Dhaka", "Delivered")`, and print it sorted.
