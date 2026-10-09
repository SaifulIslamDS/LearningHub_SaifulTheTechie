---
title: "Excel FILTER & LET: Live Filtered Lists and Readable Formulas"
order: 4
summary: "Pull a live list of matching rows with FILTER, sort it, and make long formulas readable by naming their parts with LET."
level: Intermediate
time: "35 min"
topics: ["FILTER", "LET"]
prerequisites: ["phase-1/excel-analysis/02-sumifs-countifs"]
keywords: [filter, let, dynamic array, spill, sort, calc error, spill error, named variables, readable formula, microsoft 365, excel 2021]
reviewed: 2026-10-09
resources:
  - title: "FILTER function"
    url: "https://support.microsoft.com/en-us/excel/functions/filter-function"
    source: "Microsoft Support"
    note: "Official syntax, including how to combine AND / OR conditions."
  - title: "LET function"
    url: "https://support.microsoft.com/en-us/office/let-function-34842dd8-b92b-4d3f-b325-b8b8f9908999"
    source: "Microsoft Support"
    note: "Naming parts of a formula."
  - title: "How to correct a #SPILL! error"
    url: "https://support.microsoft.com/en-us/excel/how-to-correct-a-spill-error?ui=en-us&rs=en-ie&ad=ie"
    source: "Microsoft Support"
    note: "The most common error with dynamic arrays."
  - title: "Excel FILTER function"
    url: "https://exceljet.net/functions/filter-function"
    source: "Exceljet (free)"
    note: "Many FILTER patterns with clear examples."
files: [orders.xlsx, excel-solutions.xlsx]
---

## What is it?

- **FILTER** returns every row that matches your conditions, as a **live list**. When the data changes, the list updates by itself. It works like a SQL `SELECT ... WHERE` inside a cell.
- **LET** lets you give names to parts of a formula, like variables. Long formulas become shorter, easier to read, and calculate each part only once.

Both are **dynamic array** functions: one formula fills ("spills" into) as many cells as it needs. They need **Microsoft 365 or Excel 2021 or newer**.

!!! job "Why it matters at work"
    FILTER replaces copy-pasting filtered data into report sheets, which is a common source of stale numbers. LET makes complex business formulas easy for colleagues to review. Modern Excel job descriptions mention "dynamic arrays" more and more.

## The syntax

```text
=FILTER(array, include, [if_empty])
=LET(name1, value1, [name2, value2, ...], calculation)
```

- `include` is a TRUE/FALSE test for each row, e.g. `D2:D13="Dhaka"`.
- **AND:** multiply the tests: `(test1)*(test2)`. **OR:** add them: `(test1)+(test2)`.
- In LET, the **last** argument is the result. Everything before it is name/value pairs.

## Example 1: a live list of matching rows

*Question: list all non-cancelled Dhaka orders.* In an empty cell, e.g. **L2** (with room below and to the right):

```excel
=FILTER(A2:J13,(D2:D13="Dhaka")*(I2:I13<>"Cancelled"),"No orders")
```

The result spills into 4 rows × 10 columns:

| order_id | customer | product | status | value |
|---|---|---|---|---|
| 1 | Rahim Traders | Cotton Twill | Delivered | 420.00 |
| 3 | Nova Apparel | Denim 12oz | Delivered | 1,560.00 |
| 7 | Nova Apparel | Metal Buttons | Shipped | 320.00 |
| 10 | Rahim Traders | Cotton Yarn 30s | Delivered | 870.00 |

*(5 of the 10 columns shown.)* Change order 7's status to "Cancelled" and it disappears from the list immediately.

**OR conditions** (Shipped or Pending):

```excel
=FILTER(A2:J13,(I2:I13="Shipped")+(I2:I13="Pending"),"None")
```

This returns orders **7, 9 and 12**.

## Example 2: filter and sort in one formula

Wrap FILTER in **SORT** to sort the result by column 10 (value), largest first (`-1`):

```excel
=SORT(FILTER(A2:J13,(D2:D13="Dhaka")*(I2:I13<>"Cancelled"),"No orders"),10,-1)
```

Order of the result: **3** (1,560), **10** (870), **1** (420), **7** (320).

## Example 3: LET for readable calculations

*Question: what is the average order value, excluding cancelled orders?*

Without LET, the meaning gets lost in the ranges:

```excel
=SUMIFS(J2:J13,I2:I13,"<>Cancelled")/COUNTIFS(I2:I13,"<>Cancelled")
```

With LET, each part has a name:

```excel
=LET(
    revenue, SUMIFS(J2:J13, I2:I13, "<>Cancelled"),
    orders,  COUNTIFS(I2:I13, "<>Cancelled"),
    revenue / orders
)
```

Both give **825**, the same as SQL's `AVG`. You can type line breaks inside a formula with **Alt + Enter** (Windows) or **Option + Return** (Mac).

!!! tip "When to reach for LET"
    Use LET when a formula repeats the same piece more than once, or is longer than one line. Reviewers can read `revenue / orders` at a glance. They can't easily read three nested SUMIFS.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Cells below or right of the formula aren't empty | `#SPILL!` | Clear the space the result needs |
| No `if_empty` and nothing matches | `#CALC!` | Add a 3rd argument like `"No orders"` |
| `AND(D2:D13="Dhaka", ...)` inside FILTER | Returns one TRUE/FALSE, not one per row | Multiply the tests: `(...)*(...)` |
| `include` range a different size from `array` | `#VALUE!` | Use the same rows (2–13) |
| Using FILTER in Excel 2019 or older | `#NAME?` | Use AutoFilter, or upgrade |

## Try it yourself

**Task:** Use FILTER to list every **Fabric** order worth **more than 700** that is **not cancelled**. Sort it by value, highest first.

<details markdown="1">
<summary>Show a hint</summary>

Multiply three tests: category, value and status. Then wrap the FILTER in `SORT(..., 10, -1)`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```excel
=SORT(FILTER(A2:J13,(E2:E13="Fabric")*(J2:J13>700)*(I2:I13<>"Cancelled"),"None"),10,-1)
```

| order_id | customer | product | value |
|---|---|---|---|
| 3 | Nova Apparel | Denim 12oz | 1,560.00 |
| 12 | Karim Garments | Denim 12oz | 1,275.00 |
| 9 | Sun Fashion | Denim 12oz | 810.00 |

All three are Denim: the high-value fabric line.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. In FILTER, how do you require **both** conditions to be true?

1. `(test1)+(test2)`
2. `(test1)*(test2)`
3. `AND(test1,test2)`

<details markdown="1"><summary>Show answer</summary>
**B — multiply.** TRUE×TRUE = 1. Any FALSE gives 0. Adding the tests gives OR logic.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Your FILTER formula shows `#SPILL!`. What is the most likely cause?

1. No rows match
2. Something is in the cells where the result needs to go
3. The ranges are absolute

<details markdown="1"><summary>Show answer</summary>
**B.** Clear the cells below and to the right. (No matches without `if_empty` gives `#CALC!`.)
</details>
</div>

<div class="quiz-q" markdown="1">
3\. In `=LET(a, 10, b, 5, a*b)`, which part is the result?

1. `a, 10`
2. `b, 5`
3. `a*b`

<details markdown="1"><summary>Show answer</summary>
**C.** The last argument of LET is always the calculation that is returned. Here it gives 50.
</details>
</div>

## Summary

- `FILTER(array, include, if_empty)` returns a live list of matching rows that updates by itself.
- Multiply tests for AND, add them for OR, and always give an `if_empty` value.
- Wrap FILTER in `SORT(..., column, -1)` for a sorted list.
- `LET(name, value, ..., result)` names the parts of a formula: clearer, and each part is calculated only once.
- Both need Microsoft 365 or Excel 2021 or newer, and enough empty space to spill.

!!! job "Job-ready check"
    **Interview question:** *"How would you give a manager a list of open orders that is always up to date?"*

    **Strong answer:** "A FILTER formula on the order table: status is Shipped or Pending, sorted by value with SORT. It updates as soon as the data changes, so nobody copies and pastes stale data. On older Excel I'd use a PivotTable or an AutoFilter view instead."

    **Mini project:** Create a sheet **Open Orders** with one sorted FILTER formula. Above it, show the total open value using a LET formula. Change a status in the data and watch both update.
