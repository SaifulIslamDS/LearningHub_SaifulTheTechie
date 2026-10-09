---
title: "Python Basics: Variables, Conditions, Loops & Functions"
order: 1
summary: "Store values in variables, make decisions with if/elif/else, repeat work with for and while loops, and package logic into reusable functions — using real order data."
level: Beginner
time: "45 min"
topics: ["Variables & conditions", "Loops & functions"]
prerequisites: ["phase-0/dev-environment/01-vscode-python"]
keywords: [python, variable, int, float, str, bool, f-string, if, elif, else, comparison, and, or, not, for loop, while loop, range, break, continue, function, def, return, parameter, argument, default argument]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip]
resources:
  - title: "The Python Tutorial — An Informal Introduction & More Control Flow Tools"
    url: "https://docs.python.org/3/tutorial/"
    source: "Python official docs"
    note: "Sections 3 and 4 cover everything in this lesson."
  - title: "Quick Start Guide for Python in VS Code"
    url: "https://code.visualstudio.com/docs/python/python-quick-start"
    source: "VS Code docs"
    note: "Run and debug the practice scripts."
---

## What is it?

| Building block | What it does | Example |
|---|---|---|
| **Variable** | A name pointing at a value | `region = "Dhaka"` |
| **Condition** | Choose what to do | `if value >= 1000:` |
| **Loop** | Repeat for each item | `for v in values:` |
| **Function** | Named, reusable logic | `def size_band(value):` |

These four ideas are behind every data pipeline, API and AI agent you'll write.

!!! job "Why it matters at work"
    Business rules ("cancelled orders don't count", "orders over 1,000 are Large") become conditions and functions. Interviews for data and AI roles almost always include a short coding task built from exactly these pieces, and you need them to review AI-written code confidently.

Open `01_basics.py` from [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip).

## Example 1: variables and types

```python
region = "Dhaka"          # str  (text)
quantity = 300            # int  (whole number)
unit_price = 5.20         # float (decimal)
value = quantity * unit_price
print(f"{region}: {quantity} x {unit_price:.2f} = {value:.2f}")
```

```text
Dhaka: 300 x 5.20 = 1560.00
```

| Type | Examples | Convert with |
|---|---|---|
| `int` | `300`, `-5` | `int("300")` |
| `float` | `5.2`, `0.04` | `float("5.20")` |
| `str` | `"Dhaka"` | `str(300)` |
| `bool` | `True`, `False` | `bool(...)` |

!!! tip "f-strings format numbers"
    `{value:.2f}` → 2 decimals; `{n:,}` → thousands separator (9,075); `{share:.1%}` → percentage (94.5%); `{v:>6}` → right-align in 6 characters.

## Example 2: conditions inside a function

The same rule as the SQL `CASE` lesson:

```python
def size_band(order_value: float) -> str:
    if order_value >= 1000:
        return "Large"
    elif order_value >= 500:
        return "Medium"
    else:
        return "Small"


print(size_band(value), size_band(680), size_band(200))
```

```text
Large Medium Small
```

- Conditions are checked **top to bottom**, and the first true one wins. That's why `>= 1000` comes before `>= 500`.
- **Indentation** (4 spaces) defines the block. There are no braces in Python.
- Combine tests with `and`, `or` and `not`: `if region == "Dhaka" and status != "Cancelled":`.
- `return` sends the result back to the caller.

## Example 3: loops

```python
values = [420, 200, 1560, 240, 1260]
total = 0
for v in values:
    total += v                      # same as total = total + v
    print(f"{v:>6} -> {size_band(v)}")
print("Total:", total)
```

```text
   420 -> Small
   200 -> Small
  1560 -> Large
   240 -> Small
  1260 -> Large
Total: 3680
```

A loop with a condition counts items:

```python
large = 0
for v in values:
    if v >= 1000:
        large += 1
print("Large orders:", large)
```

```text
Large orders: 2
```

| Tool | Use |
|---|---|
| `for x in items:` | Each item in a list, file, dict… (most common) |
| `for i in range(3):` | 0, 1, 2 |
| `while condition:` | Repeat until something changes (e.g. retry a download) |
| `break` / `continue` | Leave the loop / skip to the next item |

## Functions with default arguments

```python
def net_value(quantity: int, unit_price: float, discount: float = 0.0) -> float:
    return quantity * unit_price * (1 - discount)

net_value(300, 5.20)          # 1560.0
net_value(300, 5.20, 0.10)    # 1404.0  (10% discount)
```

One function, one job, a clear name. If you copy-paste code a third time, make it a function.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `=` instead of `==` in a condition | `SyntaxError` | `=` assigns, `==` compares |
| Wrong condition order (`>= 500` first) | 1560 becomes "Medium" | Most specific/biggest first |
| Mixed or wrong indentation | `IndentationError`, or code in the wrong block | 4 spaces; let VS Code format |
| `print` instead of `return` in a function | The caller gets `None` | Return values, print outside |
| Comparing text to numbers (`"300" > 200`) | `TypeError` | Convert with `int()` / `float()` first |

## Try it yourself

**Task:** Write `status_group(status)` that returns `"Closed"` for Delivered or Cancelled and `"Open"` otherwise. Then loop over the 12 statuses below and count the open orders.

```python
statuses = ["Delivered", "Delivered", "Delivered", "Cancelled", "Delivered", "Delivered",
            "Shipped", "Delivered", "Pending", "Delivered", "Delivered", "Shipped"]
```

<details markdown="1">
<summary>Show a hint</summary>

`if status in ("Delivered", "Cancelled"):` checks against several values at once.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
def status_group(status: str) -> str:
    if status in ("Delivered", "Cancelled"):
        return "Closed"
    return "Open"


open_count = 0
for s in statuses:
    if status_group(s) == "Open":
        open_count += 1
print("Open orders:", open_count)
```

```text
Open orders: 3
```

Orders 7, 9 and 12, the same open orders as in the Power BI bookmark lesson. (File: `solutions/ex01_status_group.py`.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `size_band(1000)` return?

1. "Medium"
2. "Large"
3. "Small"

<details markdown="1"><summary>Show answer</summary>
**B.** `1000 >= 1000` is true, so the first branch wins.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `f"{0.945:.1%}"` produce?

1. `0.9%`
2. `94.5%`
3. `0.945%`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A function prints its result but has no `return`. What does `x = f()` store?

1. The printed value
2. `None`
3. An error

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Variables** hold values of a **type** (`int`, `float`, `str`, `bool`); convert with `int()`, `float()`, `str()`.
- **Conditions** (`if/elif/else`) run top to bottom: put the most specific test first.
- **Loops** (`for`, `while`) repeat work; combine them with conditions to count and total.
- **Functions** (`def … return`) name your business rules so you can reuse and test them.

!!! job "Job-ready check"
    **Interview question:** *"Write a function that classifies an order value into Small, Medium or Large, and count how many are Large in a list."*

    **Strong answer:** Write `size_band()` as in Example 2 with the biggest threshold first, then a loop or `sum(1 for v in values if size_band(v) == "Large")`. Mention the edge case (exactly 1000) and how you'd test it.

    **Mini project:** Extend `01_basics.py` with `net_value()` (with an optional discount), and print every order's value, band and discounted value in an aligned table.
