---
title: "Excel PivotTables & Grouping: Summaries in Seconds"
order: 1
summary: "Turn 12 — or 120,000 — rows into a region-by-category revenue table, show shares of total, and group dates into months and values into bands."
level: Beginner
time: "40 min"
topics: ["PivotTables", "Grouping"]
prerequisites: ["phase-1/excel-analysis/02-sumifs-countifs"]
keywords: [pivottable, pivot table, rows, columns, values, filters, field list, group, months, bands, show values as, percent of total, refresh]
reviewed: 2026-10-09
resources:
  - title: "Create a PivotTable to analyze worksheet data"
    url: "https://support.microsoft.com/en-us/office/create-a-pivottable-to-analyze-worksheet-data-a9a84538-bfe9-40a9-a8e9-f99134456576"
    source: "Microsoft Support"
    note: "The official step-by-step guide."
  - title: "Group or ungroup data in a PivotTable"
    url: "https://support.microsoft.com/en-us/office/group-or-ungroup-data-in-a-pivottable-c9d1ddd0-6580-47d1-82bc-c84a5a340725"
    source: "Microsoft Support"
    note: "Grouping dates, numbers and items."
  - title: "Excel 2016: Intro to PivotTables"
    url: "https://edu.gcfglobal.org/en/excel2016/intro-to-pivottables/full"
    source: "GCFGlobal (free)"
    note: "A beginner-friendly walk-through with pictures."
files: [orders.xlsx]
---

## What is it?

A **PivotTable** is an interactive summary. You drag fields (columns) into four areas, and Excel groups and totals the data for you. Drag a different field and the summary reshapes instantly. It is the drag-and-drop version of SQL's `GROUP BY`, or of a SUMIFS summary table.

**Grouping** combines items inside a PivotTable: dates into months or quarters, numbers into bands (0–499, 500–999 …), or chosen items into a custom group.

!!! job "Why it matters at work"
    PivotTables are the fastest way to explore a new dataset and answer ad-hoc manager questions in a meeting. Nearly every analyst job description lists them, and Excel tests almost always include "build a PivotTable that shows…".

## The four areas

| Area | Does what | SQL equivalent |
|---|---|---|
| **Rows** | One row per item | `GROUP BY` |
| **Columns** | One column per item | conditional aggregation (CASE) |
| **Values** | The number to calculate (Sum, Count, Average…) | `SUM()`, `COUNT()` |
| **Filters** | Limit the whole table | `WHERE` |

## Example 1: revenue by region and category

1. Click any cell in the Orders data → **Insert → PivotTable** → **New Worksheet** → **OK**.
2. In the field list, drag **region** to **Rows**, **category** to **Columns** and **value** to **Values** (it shows "Sum of value").
3. Drag **status** to **Filters**. In the filter drop-down above the table, tick **Select Multiple Items** and untick **Cancelled**.

| Sum of value | Fabric | Trims | Yarn | Grand Total |
|---|---|---|---|---|
| Chattogram | 1,955 | 200 | | 2,155 |
| Dhaka | 1,980 | 320 | 870 | 3,170 |
| Gazipur | | | 2,520 | 2,520 |
| Narayanganj | 810 | 420 | | 1,230 |
| **Grand Total** | **4,745** | **940** | **3,390** | **9,075** |

The totals match both the SQL and the SUMIFS lessons. Empty cells mean "no orders": Gazipur only buys yarn.

!!! mistake "Forgetting the status filter"
    Without the filter, Dhaka shows **3,410** instead of 3,170, because the cancelled 240 order is included. Always check what the PivotTable includes before you share it.

## Example 2: show shares instead of amounts

Right-click any number → **Show Values As → % of Grand Total**. With only **region** in Rows (remove category from Columns):

| region | % of total revenue |
|---|---|
| Dhaka | 34.93% |
| Gazipur | 27.77% |
| Chattogram | 23.75% |
| Narayanganj | 13.55% |

Dhaka brings in about a third of revenue. Shares are often more useful to managers than raw amounts.

## Example 3: group dates into months

1. Remove region. Drag **order_date** to **Rows**.
2. Recent Excel versions group dates automatically. If not, right-click a date → **Group** → select **Months** (and **Years** if the data spans several years) → **OK**.

| Month | Sum of value |
|---|---|
| Jan | 3,440 |
| Feb | 3,940 |
| Mar | 1,695 |
| **Grand Total** | **9,075** |

*(Cancelled orders are still filtered out.)* February was the strongest month. March looks weak, but it only has two orders so far, so check how far into the month the data goes before drawing conclusions.

## Example 4: group values into bands

*Question: how many orders fall into each value band?*

1. Remove the date. Drag **value** to **Rows**, and drag **order_id** to **Values**. Click it → **Value Field Settings → Count**.
2. Right-click a value in the Rows area → **Group** → Starting at **0**, Ending at **1999**, By **500** → **OK**.

| value band | Count of order_id |
|---|---|
| 0–499 | 4 |
| 500–999 | 3 |
| 1000–1499 | 3 |
| 1500–1999 | 1 |
| **Grand Total** | **11** |

Most orders are under 1,000, but the four orders of 1,000 or more bring in 5,355 of the 9,075 revenue.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Not refreshing after the data changes | The PivotTable shows old numbers | **Data → Refresh All** (Ctrl + Alt + F5) |
| Source is a fixed range, then new rows are added | New rows are missing from the pivot | Build the pivot on an Excel **Table** |
| Value field shows "Count of value" | The numbers are counts, not sums | Value Field Settings → **Sum** |
| Dates stored as text | Can't group by month | Convert the column to real dates first |
| Grouping fails with "Cannot group that selection" | Blanks or text in a date/number column | Clean the source column |

## Try it yourself

**Task:** Build a PivotTable with **customer** in Rows and **status** in Columns, summing value. *No status filter this time.* Which customer has the most value that is not yet delivered (Shipped + Pending)?

<details markdown="1">
<summary>Show a hint</summary>

Look at each customer's Shipped and Pending columns and add them up.
</details>

<details markdown="1">
<summary>Show the solution</summary>

**Karim Garments**, with 1,275 Shipped (order 12). Sun Fashion has 810 Pending, and Nova Apparel 320 Shipped. This matches the SQL CASE lesson's "in progress" column, built here with no formulas.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which PivotTable area works like SQL's `WHERE`?

1. Rows
2. Values
3. Filters

<details markdown="1"><summary>Show answer</summary>
**C — Filters.** Rows works like `GROUP BY`, and Values like the aggregate.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. You added 50 new orders to the data, but the PivotTable totals didn't change. What's the first thing to do?

1. Rebuild the PivotTable
2. Refresh it
3. Restart Excel

<details markdown="1"><summary>Show answer</summary>
**B — Refresh.** PivotTables don't recalculate automatically. If the new rows are still missing, the source is a fixed range: use an Excel Table.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. How do you show each region's revenue as a share of the total?

1. Value Field Settings → Average
2. Show Values As → % of Grand Total
3. Group → By 100

<details markdown="1"><summary>Show answer</summary>
**B.** "Show Values As" changes how a number is displayed without changing the source data.
</details>
</div>

## Summary

- A PivotTable summarises data by dragging fields into **Rows, Columns, Values and Filters**.
- Use the **Filters** area for exclusions such as Cancelled, and check what is included.
- **Show Values As** turns amounts into shares, running totals and more.
- **Group** turns dates into months and quarters, and numbers into bands.
- Build on an Excel Table, and **refresh** after the data changes.

!!! job "Job-ready check"
    **Interview question:** *"A manager asks for revenue by region and month in a meeting. What do you do?"*

    **Strong answer:** "Build a PivotTable on the sales table: region in Rows, order date grouped by month in Columns, sum of revenue in Values, with cancelled orders filtered out. It takes under a minute, and I'd cross-check the grand total against the source before sharing."

    **Mini project:** Build a **Pivot** sheet with two PivotTables: region × category revenue, and revenue by month. Add a note under each with one insight.
