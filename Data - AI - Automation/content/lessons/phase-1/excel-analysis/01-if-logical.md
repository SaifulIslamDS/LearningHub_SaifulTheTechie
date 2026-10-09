---
title: "Excel IF, AND & OR: Let Your Sheet Make Decisions"
order: 1
summary: "Label rows, build categories and flag the orders that need attention with IF, IFS, AND and OR."
level: Beginner
time: "30 min"
topics: ["IF & logical functions"]
keywords: [if, ifs, nested if, and, or, not, logical test, "true", "false", flag, label, excel formula]
reviewed: 2026-10-09
resources:
  - title: "IF function — nested formulas and avoiding pitfalls"
    url: "https://support.microsoft.com/en-us/excel/if-function-nested-formulas-and-avoiding-pitfalls"
    source: "Microsoft Support"
    note: "The official guide, including when nested IFs become a problem."
  - title: "Using IF with AND, OR and NOT functions"
    url: "https://support.microsoft.com/en-us/excel/using-if-with-and-or-and-not-functions-in-excel"
    source: "Microsoft Support"
    note: "Combining several conditions, with examples."
  - title: "IFS function"
    url: "https://support.microsoft.com/en-us/excel/functions/ifs-function"
    source: "Microsoft Support"
    note: "A cleaner alternative to nested IFs (Excel 2019 and newer)."
  - title: "Excel IF function"
    url: "https://exceljet.net/functions/if-function"
    source: "Exceljet (free)"
    note: "Many short worked examples."
files: [orders.xlsx, excel-solutions.xlsx]
---

## What is it?

`IF` checks a condition and returns one value when it is true and another when it is false. It is the Excel version of SQL's `CASE`. With `AND` and `OR` you can check several conditions at once.

!!! job "Why it matters at work"
    Raw data rarely says "needs follow-up" or "large order". Analysts add those labels with IF formulas, then filter, count and chart them. IF is the most used logical function in Excel, and it appears in nearly every Excel skills test.

## The syntax

```text
=IF(logical_test, value_if_true, value_if_false)
=AND(condition1, condition2, ...)   → TRUE only if ALL are true
=OR(condition1, condition2, ...)    → TRUE if ANY is true
```

- Text results go in double quotes: `"Yes"`. Numbers don't: `0`.
- A logical test compares something: `I2="Cancelled"`, `J2>=1000`, `G2<>0`.

## Example 1: a simple yes/no label

*Question: does each order count as a sale (anything except Cancelled)?* In **K2**:

```excel
=IF(I2="Cancelled","No","Yes")
```

Copy it down to K13. Order 4 shows **No**, and the other 11 show **Yes**. Check: `=COUNTIF(K2:K13,"Yes")` returns **11**.

## Example 2: three categories with a nested IF

*Question: label each order Large (1,000 or more), Medium (500 or more) or Small.* In **L2**:

```excel
=IF(J2>=1000,"Large",IF(J2>=500,"Medium","Small"))
```

| order_id | value | L: size |
|---|---|---|
| 1 | 420.00 | Small |
| 3 | 1,560.00 | Large |
| 6 | 680.00 | Medium |
| 9 | 810.00 | Medium |
| 12 | 1,275.00 | Large |

*(5 of 12 rows shown.)* The labels match the SQL CASE lesson exactly.

**Cleaner option: IFS** (Excel 2019 and newer). It lists the conditions in order. `TRUE` at the end means "otherwise":

```excel
=IFS(J2>=1000,"Large",J2>=500,"Medium",TRUE,"Small")
```

!!! mistake "Order matters, just like in SQL"
    Excel checks from left to right and stops at the first true condition. If `J2>=500` came first, a 1,560 order would be labelled "Medium".

## Example 3: several conditions with AND / OR

*Question: flag "Priority" orders: from Dhaka **and** worth 1,000 or more.* In **N2**:

```excel
=IF(AND(D2="Dhaka",J2>=1000),"Priority","Normal")
```

Only **order 3** (Nova Apparel, 1,560) is Priority.

*Question: flag orders that need a follow-up: Shipped **or** Pending.* In **O2**:

```excel
=IF(OR(I2="Shipped",I2="Pending"),"Follow up","")
```

Orders **7, 9 and 12** show "Follow up". The others stay blank (`""` means an empty text).

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `=IF(I2=Cancelled,...)` (no quotes) | `#NAME?` error | `"Cancelled"` in double quotes |
| `=IF(J2>=1000 AND D2="Dhaka",...)` | Error: Excel has no AND operator | `AND(J2>=1000,D2="Dhaka")` |
| Looser condition first in a nested IF | Wrong labels | Strictest condition first |
| Typing numbers as text: `"1000"` | The comparison doesn't behave as expected | Numbers without quotes |
| Seven or more nested IFs | Unreadable and easy to break | `IFS`, or a lookup table (next lessons) |

## Try it yourself

**Task:** In column **P**, label an order **"Key delivery"** if it is *Delivered* **and** worth 1,000 or more. Otherwise show **"-"**. Which orders are key deliveries?

<details markdown="1">
<summary>Show a hint</summary>

Use `IF` with `AND(...)` inside, combining a status check and a value check.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```excel
=IF(AND(I2="Delivered",J2>=1000),"Key delivery","-")
```

Orders **3, 5 and 8** are key deliveries. Order 12 is worth 1,275 but is only *Shipped*, so it shows "-".
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `=IF(J2>=500,"Medium",IF(J2>=1000,"Large","Small"))` return for a value of 1,560?

1. Large
2. Medium
3. Small

<details markdown="1"><summary>Show answer</summary>
**B — Medium.** The first test (`>=500`) is already true, so Excel never reaches the Large check. That's why the strictest test goes first.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which formula is TRUE only when **both** conditions are true?

1. `=OR(A1>5,B1>5)`
2. `=AND(A1>5,B1>5)`
3. `=IF(A1>5,B1>5)`

<details markdown="1"><summary>Show answer</summary>
**B — AND.** OR is true when at least one condition is true.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. In `IFS`, how do you give a default result when nothing else matches?

1. Leave the last argument empty
2. Use `TRUE` as the final condition
3. Use `ELSE`

<details markdown="1"><summary>Show answer</summary>
**B.** `...,TRUE,"Small")`. Without it, IFS returns `#N/A` when nothing matches.
</details>
</div>

## Summary

- `=IF(test, if_true, if_false)` adds decisions to a sheet. Text goes in double quotes.
- Nest IFs, or use `IFS`, for several categories. Put the strictest test first.
- `AND(...)` needs all conditions to be true, and `OR(...)` needs any one. Use them inside IF.
- The labels you create become filters, counts and chart categories.

!!! job "Job-ready check"
    **Interview question:** *"How would you flag orders that need attention in a sheet with thousands of rows?"*

    **Strong answer:** "I'd add a helper column with IF plus AND/OR for the business rule, for example Shipped or Pending and older than 7 days. Then I'd filter or count that column. If the rules get complex, I'd keep them in a small rules table and look them up, so they're easy to change."

    **Mini project:** In `orders.xlsx`, add three label columns (Counts as sale, Size, Follow up). Below the data, count each label with `COUNTIF`. Save it as `orders-labelled.xlsx`.
