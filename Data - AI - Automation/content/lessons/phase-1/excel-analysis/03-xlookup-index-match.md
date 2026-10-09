---
title: "Excel XLOOKUP & INDEX/MATCH: Bring Data Together from Other Sheets"
order: 3
summary: "Look up prices, segments and suppliers from other sheets — with modern XLOOKUP and the classic INDEX/MATCH that works everywhere."
level: Beginner
time: "40 min"
topics: ["XLOOKUP & INDEX/MATCH"]
prerequisites: ["phase-1/excel-analysis/02-sumifs-countifs"]
keywords: [xlookup, index match, vlookup, lookup, match, iferror, not found, n/a, list price, discount, join, combine sheets]
reviewed: 2026-10-09
resources:
  - title: "XLOOKUP function"
    url: "https://support.microsoft.com/en-us/excel/functions/xlookup-function"
    source: "Microsoft Support"
    note: "The full syntax, including match and search modes."
  - title: "Look up values with VLOOKUP, INDEX, or MATCH"
    url: "https://support.microsoft.com/en-us/office/look-up-values-with-vlookup-index-or-match-68297403-7c3c-4150-9e3c-4d348188976b"
    source: "Microsoft Support"
    note: "The classic lookup functions side by side."
  - title: "Excel XLOOKUP function"
    url: "https://exceljet.net/functions/xlookup-function"
    source: "Exceljet (free)"
    note: "Many practical XLOOKUP patterns."
files: [orders.xlsx, excel-solutions.xlsx]
---

## What is it?

A lookup finds a value in one table and brings back related information from another column. Our **Orders** sheet has the product name. The **Products** sheet has each product's list price and supplier. A lookup connects them, the same way a SQL `JOIN` does.

- **XLOOKUP**: the modern, simple lookup (Microsoft 365, Excel 2021 or newer).
- **INDEX/MATCH**: the classic combination that works in **every** Excel version, and still appears in many company files.

!!! job "Why it matters at work"
    Combining data from different sheets or exports is a daily task: price lists, customer details, targets. "Can you do a lookup?" is the most common Excel interview question. Knowing both XLOOKUP and INDEX/MATCH means you can work in any company's files.

## The syntax

```text
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])

=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
```

- `lookup_value`: what you're searching for (e.g. the product in F2).
- `lookup_array`: where to search (the product names on the Products sheet).
- `return_array`: what to bring back (the list price column).
- `MATCH(..., 0)`: the `0` means **exact match**. Always use it for names and IDs.

## Example 1: bring in the list price

The **Products** sheet: names in A2:A7, list prices in C2:C7, suppliers in D2:D7. In **Orders!K2**:

```excel
=XLOOKUP(F2,Products!$A$2:$A$7,Products!$C$2:$C$7,"Not found")
```

The same with INDEX/MATCH (works in every version):

```excel
=INDEX(Products!$C$2:$C$7,MATCH(F2,Products!$A$2:$A$7,0))
```

Now calculate the **discount** given on each order in **L2**: `=1-H2/K2`, formatted as a percentage.

| order_id | product | unit_price | K: list_price | L: discount |
|---|---|---|---|---|
| 1 | Cotton Twill | 3.50 | 3.60 | 2.8% |
| 2 | Metal Buttons | 0.04 | 0.05 | 20.0% |
| 3 | Denim 12oz | 5.20 | 5.50 | 5.5% |
| 4 | Zippers | 0.30 | 0.32 | 6.3% |
| 5 | Cotton Yarn 30s | 2.80 | 3.00 | 6.7% |
| 6 | Cotton Twill | 3.40 | 3.60 | 5.6% |
| 7 | Metal Buttons | 0.04 | 0.05 | 20.0% |
| 8 | Polyester Yarn | 2.10 | 2.20 | 4.5% |
| 9 | Denim 12oz | 5.40 | 5.50 | 1.8% |
| 10 | Cotton Yarn 30s | 2.90 | 3.00 | 3.3% |
| 11 | Zippers | 0.28 | 0.32 | 12.5% |
| 12 | Denim 12oz | 5.10 | 5.50 | 7.3% |

**Insight:** Metal Buttons are sold at 20% below the list price, far more than any other product. That's a question for the sales team.

## Example 2: look up from a different sheet and column

*Question: what segment is each customer?* The **Customers** sheet has names in B2:B7 and segments in C2:C7. In **M2**:

```excel
=XLOOKUP(C2,Customers!$B$2:$B$7,Customers!$C$2:$C$7,"Not found")
```

Order 1 → **Trader**. Order 3 → **Garment Factory**. Order 5 → **Knitting Mill**.

With this column in place, you can use SUMIFS by segment, just like the SQL JOIN lesson.

## Example 3: handle values that aren't found

If you look up a product that isn't in the list, for example `"Velcro"`:

- XLOOKUP with `"Not found"` as the 4th argument shows **Not found**.
- INDEX/MATCH shows **#N/A**. Wrap it in `IFERROR` for a friendly message:

```excel
=IFERROR(INDEX(Products!$C$2:$C$7,MATCH("Velcro",Products!$A$2:$A$7,0)),"Not found")
```

!!! warning "Don't hide real problems"
    `#N/A` often means the data has a typo or a trailing space (`"Zippers "` is not `"Zippers"`). Before hiding errors with IFERROR, count them, then fix the source data where you can.

## Why not VLOOKUP?

You'll still see `VLOOKUP` in older files. It only searches the **first** column and returns by column **number**, so inserting a column silently breaks it. It also defaults to an *approximate* match unless you add `FALSE`. Prefer XLOOKUP, or INDEX/MATCH on older Excel.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `MATCH(F2, range)` without `0` | Approximate match: wrong prices with no error | Always `MATCH(..., 0)` |
| No `$` on the lookup ranges | Ranges shift when copied, causing `#N/A` lower down | `Products!$A$2:$A$7` |
| Lookup and return ranges of different sizes | `#VALUE!` / wrong row | Same start and end rows |
| Extra spaces in names | `#N/A` | Clean with `TRIM`, or fix the source |
| Duplicate keys in the lookup table | Only the first match is returned | Make the keys unique |

## Try it yourself

**Task:** Add a **Supplier** column using a lookup on the Products sheet (column D). How many orders are for products supplied by **Star Trims**?

<details markdown="1">
<summary>Show a hint</summary>

Use XLOOKUP (or INDEX/MATCH) returning `Products!$D$2:$D$7`, then count the result with `COUNTIF`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```excel
=XLOOKUP(F2,Products!$A$2:$A$7,Products!$D$2:$D$7,"Not found")
=COUNTIF(N2:N13,"Star Trims")
```

**4 orders** (2, 4, 7 and 11): all the Metal Buttons and Zippers orders.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does the `0` in `MATCH(F2, A2:A7, 0)` mean?

1. Start at row 0
2. Exact match
3. Return 0 if not found

<details markdown="1"><summary>Show answer</summary>
**B — exact match.** Without it, MATCH may return a nearby, wrong row.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does XLOOKUP return when nothing matches and no `if_not_found` is given?

1. 0
2. A blank
3. `#N/A`

<details markdown="1"><summary>Show answer</summary>
**C — `#N/A`.** Add a 4th argument such as `"Not found"` to show a message instead.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why does inserting a column often break VLOOKUP but not XLOOKUP?

1. VLOOKUP returns by column number
2. XLOOKUP is faster
3. VLOOKUP can't look across sheets

<details markdown="1"><summary>Show answer</summary>
**A.** VLOOKUP's column number doesn't update when columns move. XLOOKUP points at the return range directly.
</details>
</div>

## Summary

- Lookups combine data from different tables, like a SQL JOIN for one column.
- `XLOOKUP(value, lookup_array, return_array, "Not found")` is the modern way.
- `INDEX(return, MATCH(value, lookup, 0))` works in every Excel version. Always use `0`.
- Lock ranges with `$`, keep the keys unique and clean, and treat `#N/A` as a data-quality signal.

!!! job "Job-ready check"
    **Interview question:** *"You have a sales export and a separate price list. How do you find orders sold below list price?"*

    **Strong answer:** "Look up the list price for each order with XLOOKUP, or INDEX/MATCH on older Excel, using exact match. Then calculate the discount as `1 - price/list_price` and filter or conditionally format the big ones. First I'd check for `#N/A` results, because they usually mean mismatched product names."

    **Mini project:** Add a list price, discount % and supplier to every order. Then build a small table: average discount by product with `AVERAGEIFS`. Write one sentence of insight.
