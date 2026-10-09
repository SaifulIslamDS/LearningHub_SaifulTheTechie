---
title: "Power Query Merge & Append: Combine Tables Without Formulas"
order: 2
summary: "Add customer details to orders with Merge (like a SQL JOIN), and stack monthly tables with Append (like UNION)."
level: Beginner
time: "35 min"
topics: ["Merge", "Append"]
prerequisites: ["phase-1/power-query/01-cleaning"]
keywords: [merge queries, append queries, join kind, left outer, left anti, inner, expand column, table.nestedjoin, table.combine, union, lookup]
reviewed: 2026-10-09
resources:
  - title: "Merge queries overview"
    url: "https://learn.microsoft.com/en-us/power-query/merge-queries-overview"
    source: "Microsoft Learn"
    note: "Every join kind, with diagrams."
  - title: "Append queries"
    url: "https://learn.microsoft.com/en-us/power-query/append-queries"
    source: "Microsoft Learn"
    note: "Append two tables, or three or more."
  - title: "Shape and combine data in Power BI Desktop"
    url: "https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-shape-and-combine-data"
    source: "Microsoft Learn"
    note: "A full tutorial that uses merge and shaping steps."
files: [orders.csv, customers.csv, products.csv, monthly/orders_2026-01.csv, monthly/orders_2026-02.csv, monthly/orders_2026-03.csv]
---

## What is it?

Power Query combines tables in two directions:

| | **Merge** | **Append** |
|---|---|---|
| Direction | Side by side: adds **columns** | On top of each other: adds **rows** |
| Like | SQL `JOIN` or XLOOKUP | SQL `UNION ALL`, or pasting one list under another |
| Example | Orders + the customer's segment | January + February + March orders |

!!! job "Why it matters at work"
    Company data lives in separate exports: sales, the customer master, price lists, one file per month. Merging and appending in Power Query replaces fragile VLOOKUP sheets and manual copy-paste. And because the steps are recorded, next month's update is one click.

## Setup

Load these as separate queries: **Data → From Text/CSV → Transform Data**, then **Close & Load To… → Only Create Connection**.

- `orders.csv` → query **Orders** (12 rows)
- `customers.csv` → query **Customers** (6 rows)
- the three monthly files → queries **Jan**, **Feb**, **Mar** (5, 5 and 2 rows)

## Example 1: Merge — add the customer segment to each order

1. Select the **Orders** query → **Home → Merge Queries → Merge Queries as New**.
2. Top table: **Orders**, click the **customer** column. Bottom table: **Customers**, click **customer_name**.
3. **Join Kind: Left Outer** (all orders, plus matching customer details). Power Query shows "The selection matches **12 of 12** rows". Click **OK**.
4. The new column contains nested tables. Click its **expand ⇄** icon, tick only **segment**, untick "Use original column name as prefix", and click **OK**.

```m
Merged = Table.NestedJoin(Orders, {"customer"}, Customers, {"customer_name"},
                          "Customers", JoinKind.LeftOuter),
Expanded = Table.ExpandTableColumn(Merged, "Customers", {"segment"}, {"segment"})
```

Every order now has a segment: order 1 is **Trader**, order 3 is **Garment Factory**, order 5 is **Knitting Mill**. Group by segment (**Transform → Group By**, Sum of value, with Cancelled filtered out) and you get **Garment Factory 5,265 · Knitting Mill 2,520 · Trader 1,290**, the same as the SQL JOIN lesson.

!!! tip "Read the match count"
    The "matches X of Y rows" message is your first data-quality check. If it says 10 of 12, two orders have customer names that don't exist in the customer list, usually because of typos or spaces.

## Example 2: Merge with an anti join — find what's missing

*Which customers have never ordered?*

**Merge Queries as New** → top **Customers** (customer_name), bottom **Orders** (customer), **Join Kind: Left Anti** (rows only in the first table).

```m
NoOrders = Table.NestedJoin(Customers, {"customer_name"}, Orders, {"customer"},
                            "Orders", JoinKind.LeftAnti)
```

Result: **1 row**, Blue Thread Ltd. This is the same anti-join you wrote in SQL, without any code.

| Join Kind | Keeps |
|---|---|
| Left Outer | all rows from the first table + matches |
| Right Outer | all rows from the second table + matches |
| Full Outer | all rows from both |
| Inner | only matching rows |
| Left Anti | rows in the first table with **no** match |
| Right Anti | rows in the second table with **no** match |

## Example 3: Append — stack the monthly files

1. Select **Jan** → **Home → Append Queries → Append Queries as New**.
2. Choose **Three or more tables**, and add **Jan, Feb, Mar** to the right-hand list → **OK**.

```m
AllOrders = Table.Combine({Jan, Feb, Mar})
```

Result: **12 rows** (5 + 5 + 2). Append matches columns **by name**, not by position.

!!! mistake "Different column names break an append"
    If March's file calls the column `Qty` instead of `quantity`, the appended table gets **two** columns, each half empty. Rename the columns to match in each query **before** appending.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Inner join when you need every order | Orders without a matching customer disappear | Left Outer, and check the match count |
| Merging on columns with different types (text vs number) | No matches | Set the same data type on both key columns |
| Duplicate keys in the lookup table | Orders multiply after the merge | Make the lookup keys unique first |
| Different column names before an append | Half-empty extra columns | Rename to identical names first |
| Loading every helper query to a sheet | A cluttered workbook | Load helpers as **Only Create Connection** |

## Try it yourself

**Task:** Merge **Orders** with **products** information: create a small *Products* query (or use the **Products** sheet of `orders.xlsx`) and bring in **supplier**. How many orders are for **Star Trims** products?

<details markdown="1">
<summary>Show a hint</summary>

Merge Orders.product with Products.product, Left Outer, expand **supplier**. Then filter, or use Group By.
</details>

<details markdown="1">
<summary>Show the solution</summary>

**4 orders** (2, 4, 7 and 11): all the Metal Buttons and Zippers orders. That's the same answer as the XLOOKUP lesson, now produced by a refreshable query.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. You want to add January's and February's orders into one list. Which tool?

1. Merge
2. Append
3. Group By

<details markdown="1"><summary>Show answer</summary>
**B — Append** adds rows. Merge adds columns.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which join kind returns customers with **no** orders?

1. Inner
2. Left Outer
3. Left Anti

<details markdown="1"><summary>Show answer</summary>
**C — Left Anti**, when Customers is the first table.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Merge says "The selection matches 10 of 12 rows". What does that tell you?

1. 2 orders have no matching customer: check for typos or missing customers
2. The merge failed
3. 2 customers have no orders

<details markdown="1"><summary>Show answer</summary>
**A.** Two rows in the first table found no match in the second. Investigate before you trust the totals.
</details>
</div>

## Summary

- **Merge** = side by side, like a JOIN. Pick the key columns and a join kind, then expand the columns you need.
- **Left Outer** keeps every row. **Left Anti** finds missing matches.
- **Append** = stack rows, like UNION ALL. Columns are matched by name.
- Use the match count and row counts as built-in data-quality checks.

!!! job "Job-ready check"
    **Interview question:** *"What's the difference between merge and append in Power Query?"*

    **Strong answer:** "Merge joins tables side by side on a key, like a SQL join: for example, adding customer segments to orders. Append stacks tables with the same columns, like UNION ALL: for example, monthly files. With a merge I check the match count and the join kind. With an append, I check that the column names line up."

    **Mini project:** Build one query that appends the three monthly files and then merges in segment (from Customers) and supplier (from Products). Load it as the single, refreshable "sales" table for the next lessons.
