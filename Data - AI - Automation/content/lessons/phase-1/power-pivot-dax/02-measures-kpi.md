---
title: "DAX Measures & KPI Logic: Revenue, AOV and Target Achievement"
order: 2
summary: "Write reusable measures with SUM, COUNTROWS and DIVIDE, then build KPIs such as average order value, target achievement and status labels."
level: Beginner
time: "45 min"
topics: ["Measures", "KPI logic"]
prerequisites: ["phase-1/power-pivot-dax/01-relationships"]
keywords: [dax, measure, calculated column, sum, countrows, divide, kpi, achievement, target, gap, average order value, aov, format string, implicit measure, explicit measure]
reviewed: 2026-10-09
resources:
  - title: "Learn DAX basics in Power BI Desktop"
    url: "https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-quickstart-learn-dax-basics"
    source: "Microsoft Learn"
    note: "The official first steps with DAX measures."
  - title: "DIVIDE function vs the divide operator (/)"
    url: "https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator"
    source: "Microsoft Learn"
    note: "Why KPI ratios use DIVIDE."
  - title: "DAX overview"
    url: "https://learn.microsoft.com/en-us/dax/dax-overview"
    source: "Microsoft Learn"
    note: "Syntax, functions and context, in one place."
files: [sales_model.xlsx, known_answers.csv]
---

## What is it?

A **measure** is a named DAX formula that calculates a number **for whatever is on the screen**: the whole company, one region, one month, or one region in one month. You write it once and reuse it in every visual.

| | **Measure** | **Calculated column** |
|---|---|---|
| Calculates | at query time, for the current filters | once per row, stored in the table |
| Use for | KPIs: totals, ratios, % | row labels, categories to slice by |
| Example | `Revenue = SUM(Orders[value])` | `Size = IF(Orders[value] >= 1000, "Large", "Small")` |

**KPI logic** means turning business definitions into measures. For example: *achievement = net revenue ÷ target*, and *"on target" when achievement ≥ 100%*.

!!! job "Why it matters at work"
    Every number on a dashboard should come from a **named, reviewed measure**, never a quick "Sum of value" dragged into a visual. That is how a company gets one agreed definition of revenue. Measures and KPI design are the heart of BI analyst and analytics engineer roles.

## Where to write measures

- **Power BI:** select the **Orders** table → **Home → New measure** → type the formula → set the format (e.g. *Whole number*, *Percentage*).
- **Excel Power Pivot:** **Power Pivot → Measures → New Measure**, or type `Name := formula` in the measure grid.

!!! tip "Keep measures in one place"
    Many teams create an empty table called **_Measures** (Home → Enter data, one column, no rows) and store every measure there. It is easier to find than spreading measures across fact tables.

## Example 1: the base measures

```dax
Revenue = SUM ( Orders[value] )

Orders Count = COUNTROWS ( Orders )

Net Revenue =
CALCULATE ( [Revenue], Orders[status] <> "Cancelled" )

Net Orders =
CALCULATE ( [Orders Count], Orders[status] <> "Cancelled" )

Avg Order Value = DIVIDE ( [Net Revenue], [Net Orders] )
```

In a card visual, with no filters:

| Measure | Result |
|---|---|
| Revenue | 9,315 |
| Orders Count | 12 |
| Net Revenue | 9,075 |
| Net Orders | 11 |
| Avg Order Value | 825 |

`CALCULATE` adds a filter: "Revenue, but only rows that are not cancelled". The next lesson explains it in depth. Notice how measures **reuse** other measures: change the definition of *Net Revenue* once, and every KPI built on it updates.

## Example 2: target and achievement KPIs

```dax
Target = SUM ( Targets[target] )

Achievement % = DIVIDE ( [Net Revenue], [Target] )

Gap to Target = [Net Revenue] - [Target]

KPI Status =
IF ( [Achievement %] >= 1, "On target", "Below target" )
```

Put them in a **matrix** with `Regions[region]` on rows (format Achievement % as a percentage with 1 decimal):

| region | Net Revenue | Target | Achievement % | Gap to Target | KPI Status |
|---|---|---|---|---|---|
| Chattogram | 2,155 | 2,100 | 102.6% | 55 | On target |
| Dhaka | 3,170 | 3,600 | 88.1% | −430 | Below target |
| Gazipur | 2,520 | 2,400 | 105.0% | 120 | On target |
| Narayanganj | 1,230 | 1,500 | 82.0% | −270 | Below target |
| **Total** | **9,075** | **9,600** | **94.5%** | **−525** | **Below target** |

Swap the rows to `Date[Month]` and the **same measures** give monthly KPIs:

| Month | Net Revenue | Target | Achievement % |
|---|---|---|---|
| Jan 2026 | 3,440 | 2,800 | 122.9% |
| Feb 2026 | 3,940 | 3,200 | 123.1% |
| Mar 2026 | 1,695 | 3,600 | 47.1% |

**Insight:** the quarter is 525 short. January and February beat their targets, but March is far behind. Before raising an alarm, check whether March's data is complete.

!!! warning "Why the total row isn't a sum of percentages"
    The total Achievement % is **94.5%**, calculated as 9,075 ÷ 9,600. It is **not** the average of the four regional percentages (that would be 94.4%). Measures always recalculate at each level. That's exactly what you want for ratios.

## Example 3: why DIVIDE, not `/`

`[Net Revenue] / [Target]` returns an **error (∞ or NaN)** when the target is 0 or blank, for example for a region with no target yet. `DIVIDE ( [Net Revenue], [Target] )` returns **blank** instead, and you can choose your own alternative: `DIVIDE ( x, y, 0 )`. Use DIVIDE for every KPI ratio.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Dragging columns into visuals ("implicit" Sum of value) | Inconsistent definitions, includes cancelled orders | Use explicit measures only |
| Calculated column for a ratio (`value / target` per row) | Wrong totals | Ratios are **measures** (sum first, divide after) |
| `/` instead of `DIVIDE` | Errors on zero or blank | `DIVIDE ( numerator, denominator )` |
| Averaging percentages in the total row | A misleading KPI | Let the measure recalculate: total ÷ total |
| No format strings | 0.9453125 instead of 94.5% | Set the measure format once in the model |

## Try it yourself

**Task:** Put `Avg Order Value` in the region matrix. Which region has the **highest** average order value, and why might that be?

<details markdown="1">
<summary>Show a hint</summary>

No new measure is needed. AOV already uses Net Revenue ÷ Net Orders, and the region rows filter both.
</details>

<details markdown="1">
<summary>Show the solution</summary>

| region | Net Revenue | Net Orders | Avg Order Value |
|---|---|---|---|
| Chattogram | 2,155 | 3 | 718.33 |
| Dhaka | 3,170 | 4 | 792.50 |
| Gazipur | 2,520 | 2 | 1,260.00 |
| Narayanganj | 1,230 | 2 | 615.00 |
| **Total** | **9,075** | **11** | **825.00** |

**Gazipur** has the highest AOV: only two orders, both large yarn orders from one knitting mill. Small samples swing averages a lot, so mention the order count next to any average.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. You need "achievement = revenue ÷ target" that is correct at every level. Measure or calculated column?

1. Calculated column
2. Measure
3. Either

<details markdown="1"><summary>Show answer</summary>
**B — measure.** It sums revenue and target for the current filter, then divides, so the totals stay correct.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `DIVIDE ( [Net Revenue], [Target] )` return when Target is blank?

1. An error
2. Blank (or the optional alternative result)
3. Zero always

<details markdown="1"><summary>Show answer</summary>
**B.** DIVIDE handles division by zero or blank safely.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why is the total Achievement % 94.5% and not the average of the region percentages?

1. Rounding
2. The measure recalculates on the totals: 9,075 ÷ 9,600
3. Power BI ignores some regions

<details markdown="1"><summary>Show answer</summary>
**B.** Measures are re-evaluated at every level, including the total.
</details>
</div>

## Summary

- A **measure** is a reusable formula evaluated for the current filters. A **calculated column** is evaluated row by row and stored.
- Build from base measures (Revenue, Orders Count) to business measures (Net Revenue, AOV, Achievement %).
- Use `DIVIDE` for ratios, and set number formats on the measure.
- One set of measures answers by region, by month, or both. No new formulas are needed.

!!! job "Job-ready check"
    **Interview question:** *"When would you use a measure instead of a calculated column?"*

    **Strong answer:** "Measures for anything aggregated or ratio-based, like revenue, AOV and achievement %, because they respond to filters and total correctly. Calculated columns only for row-level attributes I want to slice or filter by, like an order-size band. I also avoid implicit measures, so every KPI has one reviewed definition."

    **Mini project:** Add the nine measures above to your model, plus a **KPI Status** column in the region matrix. Write a definitions table (measure name · formula · business meaning). That's the start of your KPI dictionary for the Phase 1 project.
