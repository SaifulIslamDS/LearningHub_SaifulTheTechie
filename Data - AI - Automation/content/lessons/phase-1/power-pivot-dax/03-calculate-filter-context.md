---
title: "DAX CALCULATE & Filter Context: Control What Each Number Includes"
order: 3
summary: "Understand the filters behind every number, then use CALCULATE to add, replace or remove them — for status splits, shares of total and month-on-month growth."
level: Intermediate
time: "50 min"
topics: ["CALCULATE", "Filter context"]
prerequisites: ["phase-1/power-pivot-dax/02-measures-kpi"]
keywords: [calculate, filter context, removefilters, all, percent of total, share, dateadd, previous month, month over month, mom growth, time intelligence, context, keepfilters]
reviewed: 2026-10-09
resources:
  - title: "CALCULATE function (DAX)"
    url: "https://learn.microsoft.com/en-us/dax/calculate-function-dax"
    source: "Microsoft Learn"
    note: "The official reference."
  - title: "Filter context in DAX"
    url: "https://www.sqlbi.com/articles/filter-context-in-dax/"
    source: "SQLBI (free article)"
    note: "The clearest explanation of filter context, from the authors of the standard DAX book."
  - title: "Introducing CALCULATE in DAX"
    url: "https://www.sqlbi.com/articles/introducing-calculate-in-dax/"
    source: "SQLBI (free article)"
    note: "How CALCULATE adds and replaces filters."
  - title: "REMOVEFILTERS function (DAX)"
    url: "https://learn.microsoft.com/en-us/dax/removefilters-function-dax"
    source: "Microsoft Learn"
    note: "Used for % of total."
files: [sales_model.xlsx, known_answers.csv]
---

## What is it?

**Filter context** is the set of filters active when a measure is calculated. In a matrix, the cell for *Dhaka* is calculated with the filter *region = Dhaka*. A slicer set to *February* adds *month = Feb*. Same measure, different filters, different number.

**CALCULATE** changes that filter context. It evaluates a measure with filters that you **add**, **replace** or **remove**:

```dax
CALCULATE ( <measure>, <filter1>, <filter2>, ... )
```

!!! job "Why it matters at work"
    "Delivered revenue", "share of total", "same period last month": nearly every useful KPI is a measure inside CALCULATE. Understanding filter context is what separates people who drag fields into visuals from people who can build any metric a manager asks for. It's the most tested DAX topic in interviews and on the PL-300 exam.

## Example 1: see filter context

A matrix with `Products[category]` on rows and `[Net Revenue]`:

| category | Net Revenue |
|---|---|
| Fabric | 4,745 |
| Trims | 940 |
| Yarn | 3,390 |
| **Total** | **9,075** |

Nothing in the measure mentions categories. Each row is different because the **row filters the Products table**, and the relationship passes that filter to Orders. The Total row has no category filter.

## Example 2: CALCULATE adds a filter

```dax
Delivered Revenue =
CALCULATE ( [Revenue], Orders[status] = "Delivered" )
```

With regions on rows:

| region | Net Revenue | Delivered Revenue |
|---|---|---|
| Chattogram | 2,155 | 880 |
| Dhaka | 3,170 | 2,850 |
| Gazipur | 2,520 | 2,520 |
| Narayanganj | 1,230 | 420 |
| **Total** | **9,075** | **6,670** |

The row filter (region) **stays**, and CALCULATE **adds** status = Delivered on top. This is the DAX version of the SQL CASE lesson's conditional aggregation.

## Example 3: CALCULATE replaces a filter on the same column

```dax
Fabric Revenue =
CALCULATE ( [Net Revenue], Products[category] = "Fabric" )
```

Put it in the **category** matrix and every row shows **4,745**, even the Trims and Yarn rows. When CALCULATE filters a column that is **already** filtered (category), it **replaces** that filter. That's surprising at first, but useful, as the next example shows.

## Example 4: remove filters for % of total

```dax
Net Revenue All Regions =
CALCULATE ( [Net Revenue], REMOVEFILTERS ( Regions ) )

Share of Total = DIVIDE ( [Net Revenue], [Net Revenue All Regions] )
```

| region | Net Revenue | All Regions | Share of Total |
|---|---|---|---|
| Chattogram | 2,155 | 9,075 | 23.7% |
| Dhaka | 3,170 | 9,075 | 34.9% |
| Gazipur | 2,520 | 9,075 | 27.8% |
| Narayanganj | 1,230 | 9,075 | 13.6% |
| **Total** | **9,075** | **9,075** | **100.0%** |

`REMOVEFILTERS ( Regions )` (or the older `ALL ( Regions )`) removes the region filter, so the denominator is always the company total. Other filters, such as a month slicer, **still apply**, so the shares stay correct for whatever period is selected.

## Example 5: time comparison (previous month)

This needs the marked **Date** table from the relationships lesson.

```dax
Prev Month Revenue =
CALCULATE ( [Net Revenue], DATEADD ( 'Date'[Date], -1, MONTH ) )

MoM Growth % =
DIVIDE ( [Net Revenue] - [Prev Month Revenue], [Prev Month Revenue] )
```

| Month | Net Revenue | Prev Month Revenue | MoM Growth % |
|---|---|---|---|
| Jan 2026 | 3,440 | *(blank)* | *(blank)* |
| Feb 2026 | 3,940 | 3,440 | 14.5% |
| Mar 2026 | 1,695 | 3,940 | −57.0% |

`DATEADD` shifts the dates in the current filter back one month, and CALCULATE evaluates Net Revenue for those dates. January has no previous month in the data, so it shows blank: DIVIDE handles that safely.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Expecting CALCULATE to keep an existing filter on the same column | Every row shows the same number | That's replacement. Use `KEEPFILTERS ( ... )` if you need to keep it |
| `REMOVEFILTERS ( Orders )` for % of region | Removes **all** order filters, including status | Remove only the dimension you mean: `REMOVEFILTERS ( Regions )` |
| Time intelligence without a marked date table | Wrong or blank results | Create a full calendar, mark it, and relate it |
| Filtering with the fact table's copy (`Orders[region]`) while visuals use `Regions[region]` | Filters don't line up | Filter and display the same dimension columns |
| Building a long measure in one go | Hard to debug | Build small measures and test each one in a table visual |

## Try it yourself

**Task:** Create **Delivered %**, the share of net revenue that is already delivered. What is it for the company, and which region has the **lowest** delivered share?

<details markdown="1">
<summary>Show a hint</summary>

`DIVIDE ( [Delivered Revenue], [Net Revenue] )`. Both measures already exist.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```dax
Delivered % = DIVIDE ( [Delivered Revenue], [Net Revenue] )
```

| region | Delivered % |
|---|---|
| Chattogram | 40.8% |
| Dhaka | 89.9% |
| Gazipur | 100.0% |
| Narayanganj | 34.1% |
| **Total** | **73.5%** |

**Narayanganj** (34.1%) has the lowest share, with order 9 still pending. Chattogram (40.8%) is close behind, with order 12 shipped but not yet delivered. These two regions are the follow-up priorities.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. In a region matrix, `CALCULATE ( [Revenue], Orders[status] = "Delivered" )` — what happens to the region filter?

1. It is removed
2. It stays, and status is added
3. It is replaced by status

<details markdown="1"><summary>Show answer</summary>
**B.** Filters on **different** columns are combined. Only filters on the same column are replaced.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which expression gives each region's share of the company total?

1. `DIVIDE ( [Net Revenue], [Net Revenue] )`
2. `DIVIDE ( [Net Revenue], CALCULATE ( [Net Revenue], REMOVEFILTERS ( Regions ) ) )`
3. `[Net Revenue] / 4`

<details markdown="1"><summary>Show answer</summary>
**B.** The denominator removes the region filter, so it is always the total.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does a measure need to use `DATEADD ( 'Date'[Date], -1, MONTH )` reliably?

1. A marked date table with continuous dates, related to the facts
2. A text column with month names
3. Nothing extra

<details markdown="1"><summary>Show answer</summary>
**A.** Time-intelligence functions rely on a proper date table.
</details>
</div>

## Summary

- **Filter context** = the filters active for a calculation: rows, columns, slicers, filters.
- **CALCULATE** evaluates a measure with modified filters. It **adds** filters on new columns and **replaces** filters on the same column.
- `REMOVEFILTERS ( dimension )` gives totals for **% of total** measures.
- `DATEADD` + CALCULATE gives previous-period comparisons, using a marked date table.

!!! job "Job-ready check"
    **Interview question:** *"Explain filter context and how CALCULATE changes it."*

    **Strong answer:** "Filter context is everything filtering the model when a measure is evaluated: visual rows, slicers, page filters. CALCULATE re-evaluates a measure with changed filters. It adds conditions on new columns, overrides existing filters on the same column, and can remove filters with REMOVEFILTERS. For example, a share-of-total measure divides region revenue by revenue with the region filter removed."

    **Mini project:** Add Delivered Revenue, Share of Total, Prev Month Revenue and MoM Growth % to your model. Build one matrix (regions × measures) and one by month. Add each measure to your KPI dictionary with a one-line business meaning.
