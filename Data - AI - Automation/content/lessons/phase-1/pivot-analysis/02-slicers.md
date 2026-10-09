---
title: "Excel Slicers & Timelines: Click-to-Filter Reports"
order: 2
summary: "Add buttons that filter one or many PivotTables at once, so managers can explore the numbers themselves."
level: Beginner
time: "25 min"
topics: ["Slicers"]
prerequisites: ["phase-1/pivot-analysis/01-pivottables-grouping"]
keywords: [slicer, timeline, filter, report connections, interactive, dashboard, multi-select, clear filter, pivottable]
reviewed: 2026-10-09
resources:
  - title: "Use slicers to filter data"
    url: "https://support.microsoft.com/en-us/office/use-slicers-to-filter-data-249f966b-a9d5-4b0f-b31a-12651785d29d"
    source: "Microsoft Support"
    note: "Inserting, formatting and connecting slicers."
  - title: "Create a PivotTable timeline to filter dates"
    url: "https://support.microsoft.com/en-us/office/create-a-pivottable-timeline-to-filter-dates-d3956083-01be-408c-906d-6fc99d9fadfa"
    source: "Microsoft Support"
    note: "The date-range slider for PivotTables."
  - title: "Excel 2016: Doing More with PivotTables"
    url: "https://edu.gcfglobal.org/en/excel2016/doing-more-with-pivottables/1/"
    source: "GCFGlobal (free)"
    note: "Slicers and timelines with screenshots."
files: [orders.xlsx]
---

## What is it?

A **slicer** is a set of clickable buttons, one per item (e.g. each region), that filters a PivotTable or an Excel Table. A **timeline** is a slider for dates: click a month or drag across several. Unlike the Filters drop-down, slicers **show** what is selected, so nobody misreads a filtered report.

!!! job "Why it matters at work"
    Slicers turn a static PivotTable into a small **self-service dashboard**. Managers click "Dhaka" and "Delivered" instead of asking you for another version. One slicer can drive several PivotTables at once, which is the basic idea behind Power BI dashboards in the next modules.

## Add slicers

1. Click inside a PivotTable (e.g. **category** in Rows, **Sum of value** in Values).
2. Choose **PivotTable Analyze → Insert Slicer** → tick **region** and **status** → **OK**.
3. Two button panels appear. Click a button to filter by it.
   - Select several buttons with **Ctrl + click**, or turn on the **Multi-Select** button at the top of the slicer.
   - Clear a slicer with the **funnel ✕** icon at its top right.

## Example 1: filter with two slicers

*Question: what has Dhaka received (Delivered) by category?* Click **Dhaka** in the region slicer and **Delivered** in the status slicer:

| category | Sum of value |
|---|---|
| Fabric | 1,980 |
| Yarn | 870 |
| **Grand Total** | **2,850** |

Dhaka's delivered revenue is 2,850, matching the SQL CASE lesson. The slicers show at a glance which filters are on.

## Example 2: a timeline for dates

1. Click in the PivotTable → **PivotTable Analyze → Insert Timeline** → tick **order_date** → **OK**.
2. Set the timeline to **MONTHS** and click **FEB 2026**. Clear the region and status slicers, and change the Rows field to **region**.

| region | Sum of value |
|---|---|
| Chattogram | 680 |
| Dhaka | 1,190 |
| Gazipur | 1,260 |
| Narayanganj | 810 |
| **Grand Total** | **3,940** |

The February total, 3,940, is the same number you got with SUMIFS and a date range, now in two clicks. (February has no cancelled orders, so the status filter doesn't change it.)

## Example 3: one slicer, several PivotTables

Build a second PivotTable, e.g. **customer** in Rows and Sum of value. Then:

1. Click the **region** slicer → **Slicer → Report Connections** (on older Windows versions: **PivotTable Connections**).
2. Tick **both** PivotTables → **OK**.

Now clicking "Dhaka" filters both tables together. This is how simple Excel dashboards are built.

!!! note "Report Connections only lists pivots from the same data"
    Slicers can only connect PivotTables built on the **same source**: the same Table or data model. If a PivotTable is missing from the list, it was built from a different range.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Sharing a report with a slicer still set | Readers think they see all data | Clear slicers, or label the filter clearly |
| Slicer doesn't affect the second pivot | It isn't connected | Report Connections → tick both |
| Pivot not in Report Connections | Built from a different source | Rebuild both pivots from the same Table |
| A timeline can't be added | The date field isn't real dates | Convert to dates, refresh the pivot |
| Too many slicers | A cluttered, confusing report | 2–4 slicers on the most-asked filters |

## Try it yourself

**Task:** Using the **status** slicer, select **Shipped** and **Pending** together, with region in Rows. What is the total open value, and which region has the most?

<details markdown="1">
<summary>Show a hint</summary>

Turn on Multi-Select (or Ctrl + click), then click both statuses. Make sure the timeline and the region slicer are cleared.
</details>

<details markdown="1">
<summary>Show the solution</summary>

| region | Sum of value |
|---|---|
| Chattogram | 1,275 |
| Dhaka | 320 |
| Narayanganj | 810 |
| **Grand Total** | **2,405** |

**Chattogram** has the most open value (order 12, Karim Garments). Gazipur doesn't appear: it has no open orders.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What is the main advantage of a slicer over the PivotTable Filters drop-down?

1. It calculates faster
2. It shows the selected filters visibly, and is easy to click
3. It works without a PivotTable or Table

<details markdown="1"><summary>Show answer</summary>
**B.** Visible, clickable filters reduce misreading. Slicers do need a PivotTable or an Excel Table.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. How do you make one slicer filter two PivotTables?

1. Copy the slicer
2. Report Connections → tick both pivots
3. Group the two pivots

<details markdown="1"><summary>Show answer</summary>
**B — Report Connections.** Both pivots must use the same data source.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which control is designed for filtering by a date range, such as a month or quarter?

1. Slicer
2. Timeline
3. Data bar

<details markdown="1"><summary>Show answer</summary>
**B — Timeline.**
</details>
</div>

## Summary

- **Slicers** are clickable filter buttons for PivotTables and Tables. **Timelines** filter by date ranges.
- Ctrl + click or Multi-Select chooses several items, and the ✕ clears the slicer.
- **Report Connections** lets one slicer drive several pivots built on the same source.
- Keep slicers few and meaningful, and clear them before you share a report.

!!! job "Job-ready check"
    **Interview question:** *"How would you let a sales manager explore revenue by region and month without asking you every time?"*

    **Strong answer:** "I'd build PivotTables on one Excel Table, add region and status slicers plus a date timeline, and connect them all with Report Connections. The manager clicks to filter, and I make sure the default view shows all data with the slicers cleared."

    **Mini project:** On your **Pivot** sheet, add region and status slicers and a timeline, connected to both PivotTables. Take a screenshot of a filtered view for your portfolio.
