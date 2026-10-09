---
title: "Power Query Reshape & Folder Workflows: Unpivot and Combine Files"
order: 3
summary: "Turn wide month-by-column tables into analysis-ready long tables, and load every file in a folder with one refresh."
level: Intermediate
time: "40 min"
topics: ["Reshape", "Multiple-file workflows"]
prerequisites: ["phase-1/power-query/02-merge-append"]
keywords: [unpivot, unpivot other columns, pivot column, wide to long, tidy data, folder, combine files, source.name, sample file, refresh, monthly files]
reviewed: 2026-10-09
resources:
  - title: "Unpivot columns"
    url: "https://learn.microsoft.com/en-us/power-query/unpivot-column"
    source: "Microsoft Learn"
    note: "Unpivot, Unpivot Other Columns and Unpivot Only Selected Columns explained."
  - title: "Combine files overview"
    url: "https://learn.microsoft.com/en-us/power-query/combine-files-overview"
    source: "Microsoft Learn"
    note: "How Combine Files builds the sample file and helper queries."
  - title: "Folder connector"
    url: "https://learn.microsoft.com/en-us/power-query/connectors/folder"
    source: "Microsoft Learn"
    note: "Connect to a folder and filter its files."
files: [targets_wide.csv, targets_long.csv, monthly/orders_2026-01.csv, monthly/orders_2026-02.csv, monthly/orders_2026-03.csv]
---

## What is it?

**Reshape (unpivot).** Budgets and targets often come **wide**, with one column per month. Analysis tools work best with **long** (tidy) tables: one row per region per month. **Unpivot** turns the month columns into rows.

| Wide (hard to analyse) | → | Long (tidy) |
|---|---|---|
| region · Jan · Feb · Mar | | region · month · target |
| 4 rows × 4 columns | | 12 rows × 3 columns |

**Multiple-file workflow (folder).** Instead of appending files one by one, point Power Query at a **folder**. It combines every file inside, and next month you just drop the new file in and click **Refresh**.

!!! job "Why it matters at work"
    "Every month I copy 30 branch files into one sheet" is one of the most common automation wins. Folder queries remove that work. Unpivoting is how budget and target sheets get compared with actual sales. Both are everyday tasks for BI analysts.

## Example 1: unpivot the targets

Open [targets_wide.csv](../../../downloads/targets_wide.csv):

| region | 2026-01-01 | 2026-02-01 | 2026-03-01 |
|---|---|---|---|
| Dhaka | 1100 | 1200 | 1300 |
| Gazipur | 700 | 800 | 900 |
| Chattogram | 600 | 700 | 800 |
| Narayanganj | 400 | 500 | 600 |

1. Load it into Power Query (**From Text/CSV → Transform Data**).
2. Select the **region** column only → **Transform → Unpivot Columns ▾ → Unpivot Other Columns**.
3. Rename **Attribute** → `month` and **Value** → `target`.
4. Set `month` to **Date** and `target` to **Whole Number**.

```m
Unpivoted = Table.UnpivotOtherColumns(#"Promoted Headers", {"region"}, "Attribute", "Value"),
Renamed   = Table.RenameColumns(Unpivoted, {{"Attribute", "month"}, {"Value", "target"}}),
Typed     = Table.TransformColumnTypes(Renamed, {{"month", type date}, {"target", Int64.Type}})
```

Result: **12 rows** (4 regions × 3 months), summing to **9,600**. The first rows:

| region | month | target |
|---|---|---|
| Dhaka | 2026-01-01 | 1100 |
| Dhaka | 2026-02-01 | 1200 |
| Dhaka | 2026-03-01 | 1300 |
| Gazipur | 2026-01-01 | 700 |

!!! tip "Why Unpivot Other Columns?"
    You select the column that should **stay** (region), and everything else is unpivoted. When April's column appears next month, it is unpivoted automatically. "Unpivot Columns" on the three month columns would hard-code their names, and April would be ignored.

Long tables like this connect directly to a data model. In the DAX lessons, you'll compare these targets with actual revenue.

## Example 2: combine every file in a folder

Put the three monthly files in one folder, e.g. `C:\Practice\monthly\`.

1. **Data → Get Data → From File → From Folder** (Power BI: **Get data → Folder**). Pick the folder.
2. In the preview, click **Combine → Combine & Transform Data**.
3. Choose the **first file** as the sample → **OK**.

Power Query creates helper queries (a *Sample File*, a *Transform File* function and parameters) and a final query with:

- **12 rows**: all orders from all three files.
- A **Source.Name** column showing which file each row came from (`orders_2026-01.csv` …). Keep it: it's useful for checking the load.

**Next month:** save `orders_2026-04.csv` in the folder → **Refresh All**. The new rows appear, with no editing.

!!! warning "Any cleaning goes on the sample file"
    The steps you add to **Transform Sample File** run on *every* file. Put cleaning steps (types, trimming) there, so each file is cleaned the same way before combining.

## Make folder queries robust

| Risk | Fix |
|---|---|
| Other files in the folder (notes, temporary Excel `~$` files) | Filter the `Extension` column to `.csv` and exclude names starting with `~$` |
| A file with different column names | Fix the file, or rename the columns in Transform Sample File |
| The folder path is on your laptop | Use a shared or synced folder (OneDrive, SharePoint) |
| Someone saves a file twice | Check the row count per Source.Name for duplicates |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| "Unpivot Columns" on the named month columns | New months are ignored | Select the fixed column → **Unpivot Other Columns** |
| Leaving `Attribute` / `Value` as column names | Confusing models and measures | Rename to business names |
| Month stays as text after unpivot | Can't be linked to a date table | Change type to **Date** |
| Cleaning added to the final combined query only | Some files fail before combining | Add per-file cleaning to **Transform Sample File** |
| Deleting the helper queries | The folder query breaks | Leave them. Put them in a group if they clutter the list |

## Try it yourself

**Task:** After unpivoting the targets, use **Group By** (region, Sum of target) to get each region's **quarter target**. Which region has the largest target, and what is the total?

<details markdown="1">
<summary>Show a hint</summary>

**Transform → Group By** → group by `region`, new column `q1_target` = **Sum** of `target`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

| region | q1_target |
|---|---|
| Dhaka | 3600 |
| Gazipur | 2400 |
| Chattogram | 2100 |
| Narayanganj | 1500 |

Dhaka has the largest target. The total is **9,600**. Compare it with actual non-cancelled revenue of 9,075: the business is **525 short** of the quarter target. You'll calculate that properly with DAX next.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. A table has region plus one column per month. Which action makes it long and tidy?

1. Pivot Column
2. Unpivot Other Columns (with region selected)
3. Transpose

<details markdown="1"><summary>Show answer</summary>
**B.** It keeps region and turns all the month columns into rows, including future months.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. After setting up a folder query, how do you add April's data?

1. Edit the query to add the file
2. Save the file into the folder and Refresh
3. Append it manually

<details markdown="1"><summary>Show answer</summary>
**B.** That's the whole point: drop the file in and refresh.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Where should cleaning steps go so that every file in a folder is cleaned the same way?

1. Transform Sample File
2. The final combined query only
3. In each Excel file

<details markdown="1"><summary>Show answer</summary>
**A.** Steps on the sample file are applied to every file before they are combined.
</details>
</div>

## Summary

- **Unpivot Other Columns** turns wide tables (one column per month) into long tidy tables, and handles new months automatically.
- Rename `Attribute`/`Value` and set proper types after unpivoting.
- **Folder → Combine & Transform** loads every file in a folder. New files arrive with one Refresh.
- Put per-file cleaning in **Transform Sample File**, filter out unwanted files, and keep `Source.Name` for checks.

!!! job "Job-ready check"
    **Interview question:** *"Each branch sends a monthly Excel file. How would you automate the consolidation?"*

    **Strong answer:** "A Power Query folder connection: Combine & Transform, with the cleaning steps on the sample file so each file is standardised. I'd filter to the right file type, keep Source.Name for auditing, and store the folder somewhere shared. Monthly work becomes: save the files, refresh, and check the row counts per file."

    **Mini project:** Create a folder query for the three monthly files and an unpivoted targets query. Load both to the Data Model, or as connections. You'll use them as the fact tables in the DAX lessons.
