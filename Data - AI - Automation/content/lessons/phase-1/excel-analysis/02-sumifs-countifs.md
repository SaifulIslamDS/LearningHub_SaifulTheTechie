---
title: "Excel SUMIFS & COUNTIFS: Build KPI Summaries"
order: 2
summary: "Add up and count only the rows that match your conditions — the formulas behind most Excel reports."
level: Beginner
time: "35 min"
topics: ["SUMIFS & COUNTIFS"]
prerequisites: ["phase-1/excel-analysis/01-if-logical"]
keywords: [sumifs, countifs, averageifs, sumif, countif, criteria, wildcard, date range, absolute reference, dollar sign, kpi, summary table]
reviewed: 2026-10-09
resources:
  - title: "SUMIFS function"
    url: "https://support.microsoft.com/en-us/excel/functions/sumifs-function"
    source: "Microsoft Support"
    note: "The official reference, with examples of multiple criteria."
  - title: "COUNTIFS function"
    url: "https://support.microsoft.com/en-us/excel/functions/countifs-function"
    source: "Microsoft Support"
    note: "Counting with several conditions."
  - title: "Excel SUMIFS function"
    url: "https://exceljet.net/functions/sumifs-function"
    source: "Exceljet (free)"
    note: "Date, wildcard and not-equal criteria explained clearly."
files: [orders.xlsx, excel-solutions.xlsx]
---

## What is it?

- `SUMIFS` adds up numbers, but **only in rows that meet all your conditions**.
- `COUNTIFS` counts those rows.
- `AVERAGEIFS` averages them.

Together they do in a sheet what `WHERE` + `GROUP BY` do in SQL.

!!! job "Why it matters at work"
    Monthly sales packs, regional summaries and KPI tables in Excel are mostly SUMIFS and COUNTIFS. Unlike a PivotTable, they live in fixed cells, so you can format them, reference them in charts and update them automatically. Interviewers often ask candidates to rebuild a summary table with them.

## The syntax

```text
=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...)
=COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2], ...)
```

- **SUMIFS starts with the range to add.** COUNTIFS has no sum range.
- All ranges must be the **same size** (here, rows 2–13).
- Criteria can be text (`"Dhaka"`), comparisons (`"<>Cancelled"`, `">=1000"`) or a cell reference (`L2`).

## Example 1: one total with two conditions

*Question: what is Dhaka's revenue, excluding cancelled orders?*

```excel
=SUMIFS($J$2:$J$13,$D$2:$D$13,"Dhaka",$I$2:$I$13,"<>Cancelled")
```

Result: **3,170**, the same as the SQL `GROUP BY` lesson. Order 4 (cancelled, 240) is left out.

## Example 2: a full summary table

Type the four regions in **L2:L5**. Then put this in **M2** and copy it down:

```excel
=SUMIFS($J$2:$J$13,$D$2:$D$13,L2,$I$2:$I$13,"<>Cancelled")
```

Put this in **N2** and copy it down:

```excel
=COUNTIFS($D$2:$D$13,L2,$I$2:$I$13,"<>Cancelled")
```

| L: region | M: revenue | N: orders |
|---|---|---|
| Dhaka | 3,170 | 4 |
| Gazipur | 2,520 | 2 |
| Chattogram | 2,155 | 3 |
| Narayanganj | 1,230 | 2 |

!!! tip "Why the $ signs?"
    `$J$2:$J$13` is an **absolute** reference, so it doesn't move when you copy the formula down. `L2` has no `$`, so it changes to L3, L4, L5. Mixing absolute data ranges with relative criteria cells is the core SUMIFS skill. Press **F4** to add the `$` signs quickly.

## Example 3: date ranges, averages and wildcards

**Revenue in February 2026** (non-cancelled):

```excel
=SUMIFS($J$2:$J$13,
        $B$2:$B$13,">="&DATE(2026,2,1),
        $B$2:$B$13,"<"&DATE(2026,3,1),
        $I$2:$I$13,"<>Cancelled")
```

Result: **3,940** (orders 6–10). Notice the `&`: it joins the operator `">="` to the date. Using `"<"` with the first day of the *next* month catches every day of February, including the last one.

**Average Fabric order value** (non-cancelled):

```excel
=AVERAGEIFS($J$2:$J$13,$E$2:$E$13,"Fabric",$I$2:$I$13,"<>Cancelled")
```

Result: **949** (4,745 ÷ 5 orders).

**How many orders are for a "Cotton…" product?** `*` means "any characters":

```excel
=COUNTIFS($F$2:$F$13,"Cotton*")
```

Result: **4** (Cotton Twill × 2, Cotton Yarn 30s × 2).

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Sum range last (SUMIF habit) | Wrong result or error | In SUMIFS, the sum range comes **first** |
| Ranges of different sizes | `#VALUE!` error | Make every range cover the same rows |
| No `$` signs, then copying down | Ranges slide down, so totals are wrong | Absolute ranges: `$J$2:$J$13` |
| `">=DATE(2026,2,1)"` all inside quotes | Matches nothing (counts as text) | `">="&DATE(2026,2,1)` |
| Totals don't match the source | Some criteria text has spaces or typos | Check with `=COUNTIFS(...)` and clean the data |

## Try it yourself

**Task:** Build a **category summary**. Put Fabric, Yarn and Trims in a column, then show non-cancelled revenue and order count for each.

<details markdown="1">
<summary>Show a hint</summary>

It's the same as Example 2, but the criteria range is column **E** (category) instead of D.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```excel
=SUMIFS($J$2:$J$13,$E$2:$E$13,L2,$I$2:$I$13,"<>Cancelled")
=COUNTIFS($E$2:$E$13,L2,$I$2:$I$13,"<>Cancelled")
```

| category | revenue | orders |
|---|---|---|
| Fabric | 4,745 | 5 |
| Yarn | 3,390 | 3 |
| Trims | 940 | 3 |

Check: 4,745 + 3,390 + 940 = **9,075**, the same non-cancelled total as in SQL.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. In `=SUMIFS(A:A, B:B, "X")`, which column is added up?

1. A
2. B
3. Both

<details markdown="1"><summary>Show answer</summary>
**A.** In SUMIFS, the first argument is always the range to add.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which criterion correctly means "on or after the date in cell P1"?

1. `">=P1"`
2. `">="&P1`
3. `>=P1`

<details markdown="1"><summary>Show answer</summary>
**B.** Put the operator in quotes and join it to the cell with `&`. Option A compares with the text "P1".
</details>
</div>

<div class="quiz-q" markdown="1">
3\. You copy a SUMIFS formula down and the totals get smaller in each row. What's the likely cause?

1. Missing `$` signs on the data ranges
2. Wrong criteria text
3. SUMIFS can't be copied

<details markdown="1"><summary>Show answer</summary>
**A.** Without `$`, the data ranges slide down as you copy, so each row covers fewer orders.
</details>
</div>

## Summary

- `SUMIFS(sum_range, range1, crit1, ...)`, `COUNTIFS(range1, crit1, ...)` and `AVERAGEIFS(...)` calculate with conditions.
- Every condition must be true (AND logic).
- Lock data ranges with `$`, and point the criteria at cells, so one formula fills a whole summary table.
- For dates and comparisons, join the operator and the value with `&`. `*` is a wildcard.

!!! job "Job-ready check"
    **Interview question:** *"Build a revenue-by-region table that updates automatically when new orders are added."*

    **Strong answer:** "I'd convert the data to an Excel Table, so the ranges grow automatically, then use SUMIFS with the region names in a criteria column. I'd always check that the summary's grand total matches the raw total."

    **Mini project:** Add a **Summary** sheet to your workbook with three blocks: by region, by category and by month. Add a check cell that compares the grand total with `SUM` of the non-cancelled data.
