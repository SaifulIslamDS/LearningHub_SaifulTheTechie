---
title: "Data Model Relationships: Build a Star Schema"
order: 1
summary: "Load fact and dimension tables, connect them with one-to-many relationships, and add a date table, so every visual filters correctly."
level: Beginner
time: "40 min"
topics: ["Relationships"]
prerequisites: ["phase-1/power-query/02-merge-append"]
keywords: [data model, relationship, star schema, fact table, dimension table, one-to-many, cardinality, filter direction, date table, calendar, mark as date table, power pivot, model view]
reviewed: 2026-10-09
resources:
  - title: "Understand star schema and the importance for Power BI"
    url: "https://learn.microsoft.com/en-us/power-bi/guidance/star-schema"
    source: "Microsoft Learn"
    note: "The standard guide to facts, dimensions and relationships."
  - title: "Set and use date tables in Power BI Desktop"
    url: "https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables"
    source: "Microsoft Learn"
    note: "Why you need a date table, and how to mark it."
  - title: "Get started with Power Pivot in Microsoft Excel"
    url: "https://support.microsoft.com/en-us/office/get-started-with-power-pivot-in-microsoft-excel-fdfcf944-7876-424a-8437-1a6c1043a80b"
    source: "Microsoft Support"
    note: "The Excel version: the data model, diagram view and relationships."
files: [sales_model.xlsx, regions.csv]
---

## What is it?

A **relationship** links two tables through a shared column, for example `Orders[customer]` → `Customers[customer_name]`. Once linked, choosing a customer *segment* in a visual automatically filters the related orders. You don't need XLOOKUP or a merge.

The recommended shape is a **star schema**:

- **Fact tables** hold events and numbers (Orders, Targets). They have many rows.
- **Dimension tables** describe things (Customers, Products, Regions, Date). They have one row per item.
- Each dimension connects to the facts with a **one-to-many (1 → \*)** relationship.

```text
              Customers      Products
                  1 \          / 1
                     *        *
     Regions 1 ──* ORDERS *── 1 Date
          1 \                  / 1
             *               *
               ── TARGETS ──
```

!!! job "Why it matters at work"
    A clean star schema makes every report faster, simpler and correct. Wrong or missing relationships are the number-one cause of "the totals don't add up" in Power BI. Interviewers ask "What's a star schema?" and "Why do we need a date table?" in almost every BI role.

## Step 1: load the tables

**Power BI Desktop:** **Home → Get data → Excel workbook** → `sales_model.xlsx` → tick **Orders, Customers, Products, Regions, Targets** → **Load**.

**Excel:** open `sales_model.xlsx` → for each table, choose **Power Pivot → Add to Data Model**.

## Step 2: add a date table

Time analysis (months, previous month, year-to-date) needs a table with **one row for every day**.

**Power BI:** **Modeling → New table**:

```dax
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2026, 1, 1 ), DATE ( 2026, 3, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "mmm yyyy" )
)
```

Then **Table tools → Mark as date table** (date column: `Date`). Select the `Month` column → **Sort by column → Month Number**, so months sort Jan, Feb, Mar instead of alphabetically.

**Excel Power Pivot:** **Power Pivot → Manage → Design → Date Table → New**. Excel creates a *Calendar* table for you.

The result is **90 rows** (1 January to 31 March 2026).

## Step 3: create the relationships

Go to **Model view** (Power BI) or **Diagram View** (Power Pivot), and drag each key from the dimension onto the fact table:

| From (one side, dimension) | To (many side, fact) |
|---|---|
| `Customers[customer_name]` | `Orders[customer]` |
| `Products[product]` | `Orders[product]` |
| `Regions[region]` | `Orders[region]` |
| `Date[Date]` | `Orders[order_date]` |
| `Regions[region]` | `Targets[region]` |
| `Date[Date]` | `Targets[month]` |

Check each one: **Cardinality: Many to one (\*:1)** and **Cross-filter direction: Single**. Power BI often detects some of these automatically. Always check them.

!!! tip "Use dimension columns in visuals"
    Build visuals with `Regions[region]`, `Products[category]`, `Customers[segment]` and `Date[Month]`, **not** the copies inside Orders. Dimension columns filter **both** Orders and Targets. Then hide the duplicate key columns in the fact tables (right-click → **Hide in report view**) so nobody picks them by mistake.

## Example: see the relationship work

Create a table visual with `Customers[segment]` and `Orders[value]` (Sum), and filter `Orders[status]` to exclude **Cancelled**:

| segment | Sum of value |
|---|---|
| Garment Factory | 5,265 |
| Knitting Mill | 2,520 |
| Trader | 1,290 |
| **Total** | **9,075** |

These are the same numbers as the SQL JOIN and Power Query merge lessons, now with **no** join or merge step.

**What a missing relationship looks like:** delete the Customers–Orders relationship and the table shows **9,075 on every row**. Each segment shows the grand total, because nothing tells the model how segments relate to orders. When you see the same number repeated down a visual, check the relationships first.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Using fact-table columns (e.g. `Orders[region]`) in visuals | Targets aren't filtered, so comparisons are wrong | Use dimension columns (`Regions[region]`) |
| Missing relationship | The same total repeats on every row | Create the relationship in Model view |
| Many-to-many caused by duplicate keys in a "dimension" | Ambiguous or slow model, wrong totals | Make dimension keys unique |
| Both-direction filters everywhere | Ambiguity and unexpected results | Keep **Single** direction unless you have a specific need |
| No date table, or not marked as one | Time-intelligence functions fail or give wrong results | Create a full calendar and mark it as the date table |

## Try it yourself

**Task:** Using the model, build a visual showing non-cancelled revenue by **division** (from the Regions table). Which division is larger?

<details markdown="1">
<summary>Show a hint</summary>

Use `Regions[division]` with Sum of `Orders[value]`, with the status filter excluding Cancelled. It works because Regions → Orders is related.
</details>

<details markdown="1">
<summary>Show the solution</summary>

| division | revenue |
|---|---|
| Dhaka Division | 6,920 |
| Chattogram Division | 2,155 |
| **Total** | **9,075** |

Dhaka Division (Dhaka, Gazipur and Narayanganj) brings in about three-quarters of revenue. `division` isn't in the Orders table at all: the relationship brings it in.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. In a star schema, which tables have one row per item (customer, product, day)?

1. Fact tables
2. Dimension tables
3. Bridge tables

<details markdown="1"><summary>Show answer</summary>
**B — dimension tables.** Fact tables store the events and numbers.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. A visual shows **9,075** on every segment row. What is the most likely cause?

1. Wrong number format
2. Missing relationship between Customers and Orders
3. Too many rows in Orders

<details markdown="1"><summary>Show answer</summary>
**B.** Without the relationship, the segment can't filter the orders, so every row shows the grand total.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why use `Regions[region]` instead of `Orders[region]` in a sales-vs-target visual?

1. It is faster to type
2. The dimension filters both Orders and Targets
3. Orders[region] can't be displayed

<details markdown="1"><summary>Show answer</summary>
**B.** Only the shared dimension filters both fact tables, so actuals and targets line up.
</details>
</div>

## Summary

- A **star schema** has facts (Orders, Targets) in the middle and dimensions (Customers, Products, Regions, Date) around them.
- Relationships are **one-to-many** from dimension to fact, with **single** filter direction.
- Add a full **date table**, mark it, and sort month names by month number.
- Put **dimension** columns in visuals, and hide the duplicate keys in the facts.
- A repeated grand total on every row means a relationship is missing.

!!! job "Job-ready check"
    **Interview question:** *"What is a star schema, and why does Power BI recommend it?"*

    **Strong answer:** "Fact tables with events and numbers, surrounded by dimension tables that describe them, linked one-to-many. It keeps the model simple and fast, and filters flow predictably from dimensions to facts. One shared dimension, like Region or Date, can filter several facts at once. That's how I compare actual sales with targets."

    **Mini project:** Build the six-table model in Power BI Desktop (or Power Pivot), and take a screenshot of Model view for your portfolio README. Save the file as `sales-model.pbix` (or `.xlsx`). You'll add measures to it in the next lesson.
