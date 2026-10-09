---
title: "OOP & Type Hints: Classes, Dataclasses and Clear Contracts"
order: 4
summary: "Model business objects with classes and dataclasses, add methods and properties, and use type hints so editors, checkers and reviewers catch mistakes before they run."
level: Beginner
time: "45 min"
topics: ["OOP", "Type hints"]
prerequisites: ["phase-0/programming-refresher/03-files-exceptions"]
keywords: [oop, object-oriented, class, object, instance, self, __init__, method, attribute, property, dataclass, type hints, annotations, mypy, pylance, "list[str]", "dict[str, float]", optional, None, "X | None"]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip]
resources:
  - title: "Classes (Python tutorial)"
    url: "https://docs.python.org/3/tutorial/"
    source: "Python official docs"
    note: "Section 9: classes, instances and methods."
  - title: "Python debugging in VS Code"
    url: "https://code.visualstudio.com/docs/python/debugging"
    source: "VS Code docs"
    note: "Step into methods to see objects in the Variables panel."
---

## What is it?

- **OOP (object-oriented programming)** groups **data** and the **behaviour** that belongs to it into a **class**. An `Order` knows its quantity and price, and how to calculate its value.
- A **dataclass** writes the boring parts of a class for you (`__init__`, a readable print-out, comparison).
- **Type hints** (`quantity: int`, `-> float`) document what goes in and out. Python doesn't enforce them at run time, but **Pylance** and **mypy** check them before you run anything.

!!! job "Why it matters at work"
    Frameworks you'll use later are built on classes: Pydantic models for APIs and LLM outputs, scikit-learn estimators, LangChain/agent tools. Type hints are now standard in professional Python, because they make code self-documenting and let tools (and AI assistants) catch errors early.

Open `04_classes.py` from [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip).

## Example 1: a dataclass with a property and a method

```python
from dataclasses import dataclass


@dataclass
class Order:
    order_id: int
    customer: str
    region: str
    quantity: int
    unit_price: float
    status: str

    @property
    def value(self) -> float:
        return self.quantity * self.unit_price

    def is_open(self) -> bool:
        return self.status in {"Shipped", "Pending"}
```

- `Order` is the **class** (the blueprint). `Order(1, "Rahim Traders", ...)` creates an **instance** (an object).
- `self` is "this particular order".
- `@property` lets you write `order.value` (no brackets) for a calculated field.

## Example 2: a class that works with many objects

```python
class OrderBook:
    """A collection of orders with business calculations."""

    def __init__(self, orders: list[Order]) -> None:
        self.orders = orders

    def net(self) -> list[Order]:
        return [o for o in self.orders if o.status != "Cancelled"]

    def net_revenue(self) -> float:
        return sum(o.value for o in self.net())

    def open_value(self) -> float:
        return sum(o.value for o in self.orders if o.is_open())

    def revenue_by(self, attr: str) -> dict[str, float]:
        result: dict[str, float] = {}
        for o in self.net():
            key = getattr(o, attr)
            result[key] = result.get(key, 0) + o.value
        return result
```

With the five Dhaka orders:

```python
first = book.orders[0]
print(first)
print(f"Order {first.order_id} value: {first.value:.2f}")
print(f"Net revenue: {book.net_revenue():.2f}")
print(f"Open value: {book.open_value():.2f}")
print(book.revenue_by("customer"))
```

```text
Order(order_id=1, customer='Rahim Traders', region='Dhaka', quantity=120, unit_price=3.5, status='Delivered')
Order 1 value: 420.00
Net revenue: 3170.00
Open value: 320.00
{'Rahim Traders': 1290.0, 'Nova Apparel': 1880.0}
```

Dhaka net revenue = **3,170**, matching SQL, Excel and Power BI. The business rules now live in **one** place.

## Example 3: type hints catch a bug before it runs

```python
def achievement(revenue: float, target: float) -> float:
    return revenue / target


print(f"{achievement(3170, 3600):.1%}")
print(achievement("3170", 3600))     # oops: text from a CSV
```

Running it crashes on the second call:

```text
88.1%
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for /: 'str' and 'int'
```

A type checker finds it **without running** the code (`uvx mypy hints.py`, or the red underline from Pylance in VS Code):

```text
hints.py:6: error: Argument 1 to "achievement" has incompatible type "str"; expected "float"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

| Hint | Means |
|---|---|
| `x: int`, `y: float`, `s: str`, `ok: bool` | Simple types (an `int` is accepted where `float` is expected) |
| `list[Order]` | A list of Order objects |
| `dict[str, float]` | Keys are text, values are numbers |
| `str | None` | Text, or nothing (an optional value) |
| `-> None` | The function returns nothing |

## When to use a class

| Use a class when… | Stay with functions when… |
|---|---|
| Data and the rules about it belong together (`Order.value`) | It's a single transformation (`clean_row(row)`) |
| You create many similar objects | A script runs once, top to bottom |
| A framework expects one (Pydantic, scikit-learn) | A dict or tuple is enough |

Good Python mixes both: dataclasses for records, plain functions for steps.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Forgetting `self` in a method | `TypeError: takes 0 positional arguments but 1 was given` | `def net(self):` |
| `order.value()` on a property | `TypeError: 'float' object is not callable` | No brackets for properties |
| Mutable default: `def __init__(self, orders=[])` | Every instance shares one list | Use `None`, or `field(default_factory=list)` in dataclasses |
| Believing hints are enforced at run time | Wrong types still crash later | Run Pylance/mypy, and validate input (Pydantic later) |
| Giant "God classes" doing everything | Hard to test or change | Small classes with one responsibility |

## Try it yourself

**Task:** Add a method `largest(self) -> Order` to `OrderBook` that returns the biggest **non-cancelled** order. Print its ID, customer and value.

<details markdown="1">
<summary>Show a hint</summary>

`max(items, key=lambda o: o.value)` returns the item with the largest value.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
    def largest(self) -> Order:
        """The biggest non-cancelled order."""
        return max(self.net(), key=lambda o: o.value)


big = book.largest()
print(f"Largest order: {big.order_id} ({big.customer}) = {big.value:.2f}")
```

```text
Largest order: 3 (Nova Apparel) = 1560.00
```

(File: `solutions/ex04_largest_order.py`.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `@dataclass` generate for you?

1. A database table
2. `__init__`, a readable print-out and comparison methods
3. Type checking at run time

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Does Python stop `achievement("3170", 3600)` because of the type hint?

1. Yes, immediately
2. No; hints are checked by tools like Pylance and mypy, not at run time
3. Only in Python 3.14

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does `dict[str, float]` describe?

1. A dict with text keys and number values
2. A list of strings and floats
3. A string that looks like a dict

<details markdown="1"><summary>Show answer</summary>
**A.**
</details>
</div>

## Summary

- A **class** bundles data and behaviour; **instances** are the objects; `self` is the current one.
- `@dataclass` removes boilerplate; `@property` exposes calculated fields like `order.value`.
- Keep business rules in one place (`OrderBook.net_revenue`) so every report agrees.
- **Type hints** document contracts; **Pylance/mypy** catch mismatches before run time.

!!! job "Job-ready check"
    **Interview question:** *"Why use type hints if Python doesn't enforce them?"*

    **Strong answer:** "They make function contracts explicit for readers, give the editor accurate autocomplete, and let a type checker like mypy catch mistakes, such as passing CSV text where a number is expected, before the code runs, often in CI. Libraries like Pydantic also use them to validate data at run time."

    **Mini project:** Load all 12 orders from `data/orders.csv` into `Order` objects (convert the types), build an `OrderBook`, and print `revenue_by("region")`. It must match the region totals from the Collections lesson.
