---
title: "Power Query Cleaning: From Messy Export to Tidy Table"
order: 1
summary: "Remove blanks and duplicates, fix spaces and capitals, read dates in the right format, and get the same clean table every time you refresh."
level: Beginner
time: "45 min"
topics: ["Cleaning"]
keywords: [power query, clean data, trim, capitalize each word, remove duplicates, remove blank rows, data types, locale, date format, applied steps, m language, refresh]
reviewed: 2026-10-09
resources:
  - title: "What is Power Query?"
    url: "https://learn.microsoft.com/en-us/power-query/power-query-what-is-power-query"
    source: "Microsoft Learn"
    note: "The big picture: connect, transform, load, refresh."
  - title: "Data types in Power Query"
    url: "https://learn.microsoft.com/en-us/power-query/data-types"
    source: "Microsoft Learn"
    note: "Includes 'Change type using locale', which this lesson's date fix uses."
  - title: "Text.Trim"
    url: "https://learn.microsoft.com/en-us/powerquery-m/text-trim"
    source: "Microsoft Learn — M reference"
    note: "The M function behind Format → Trim."
files: [orders_raw.csv, orders.csv]
---

## What is it?

**Power Query** is a data-cleaning tool built into Excel and Power BI. You click through cleaning actions such as *trim spaces*, *remove duplicates* or *change type*, and Power Query **records each one as a step**. Next month, you drop in the new file and click **Refresh**: every step runs again automatically.

Behind the clicks, each step is written in a language called **M**. You don't have to write M, but reading it helps you check and fix queries.

!!! job "Why it matters at work"
    Analysts often say most of their time goes on cleaning data. Power Query turns that into a repeatable, auditable process instead of a monthly copy-paste routine. "Clean and transform data" is the first skill area of the PL-300 Power BI exam, and a standard interview topic.

## The messy file

Open [orders_raw.csv](../../../downloads/orders_raw.csv). It has the same 12 orders as before, exported badly:

| Problem | Example |
|---|---|
| Extra spaces | `"  Rahim Traders"`, `"Dhaka "` |
| Mixed capitals | `chattogram`, `DHAKA`, `delivered`, `CANCELLED` |
| Dates written day/month/year as text | `05/01/2026` means **5 January**, not 1 May |
| Numbers with thousand separators, stored as text | `"5,000"` |
| A blank row | `,,,,,,,,` |
| A duplicated order | order 6 appears twice |

That gives **14 data rows**, which should become **12 clean orders**.

## Step by step in the editor

1. Choose **Data → From Text/CSV** (Excel) or **Get data → Text/CSV** (Power BI), pick the file, and click **Transform Data**.
2. **Delete the automatic "Changed Type" step** in the *Applied Steps* list (click the ✕). Power Query guessed the types using your computer's settings, and on a US-style computer it would read `05/01/2026` as 1 May. You'll set the types correctly yourself.
3. **Remove the blank row:** **Home → Remove Rows → Remove Blank Rows**. 13 rows remain.
4. **Trim spaces:** select *Customer*, *Region* and *Status* → **Transform → Format → Trim**.
5. **Fix capitals:** select *Region* and *Status* → **Transform → Format → Capitalize Each Word**. Now `DHAKA` becomes `Dhaka` and `CANCELLED` becomes `Cancelled`.
6. **Remove the thousand separators:** select *Qty* → **Transform → Replace Values** → replace `,` with nothing.
7. **Set the types with a locale:** select *Order Date*, *Qty* and *Unit Price* → right-click → **Change Type → Using Locale…**. Choose Date (for Order Date), Whole Number (Qty) or Decimal Number (Unit Price), with locale **English (United Kingdom)**. Set *Order ID* to **Whole Number**.
8. **Remove the duplicate:** **Home → Remove Rows → Remove Duplicates** (with all columns selected, or none). **12 rows** remain.
9. **Rename** the columns to `order_id, order_date, customer, region, category, product, quantity, unit_price, status`.
10. **Add the value column:** **Add Column → Custom Column**, name `value`, formula `[quantity] * [unit_price]`.
11. **Home → Close & Load** (Excel) or **Close & Apply** (Power BI).

**Result:** 12 orders, regions exactly `Chattogram / Dhaka / Gazipur / Narayanganj`, statuses `Cancelled / Delivered / Pending / Shipped`, and a total value of **9,315** (9,075 without the cancelled order). That is identical to the clean `orders.csv` used in earlier lessons.

## The same steps in M

Open **Home → Advanced Editor** to see the recorded steps. Your version will look similar to this, apart from the file path and some step names:

```m
let
    Source = Csv.Document(File.Contents("C:\Practice\orders_raw.csv"),
                 [Delimiter = ",", Columns = 9, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    #"Removed Blank Rows" = Table.SelectRows(#"Promoted Headers",
                 each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Trimmed Text" = Table.TransformColumns(#"Removed Blank Rows",
                 {{"Customer", Text.Trim, type text}, {"Region", Text.Trim, type text}, {"Status", Text.Trim, type text}}),
    #"Capitalized Each Word" = Table.TransformColumns(#"Trimmed Text",
                 {{"Region", Text.Proper, type text}, {"Status", Text.Proper, type text}}),
    #"Replaced Value" = Table.ReplaceValue(#"Capitalized Each Word", ",", "", Replacer.ReplaceText, {"Qty"}),
    #"Changed Type with Locale" = Table.TransformColumnTypes(#"Replaced Value",
                 {{"Order Date", type date}, {"Qty", Int64.Type}, {"Unit Price", type number}}, "en-GB"),
    #"Changed Type" = Table.TransformColumnTypes(#"Changed Type with Locale", {{"Order ID", Int64.Type}}),
    #"Removed Duplicates" = Table.Distinct(#"Changed Type"),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Duplicates", {
                 {"Order ID", "order_id"}, {"Order Date", "order_date"}, {"Customer", "customer"},
                 {"Region", "region"}, {"Category", "category"}, {"Product", "product"},
                 {"Qty", "quantity"}, {"Unit Price", "unit_price"}, {"Status", "status"}}),
    #"Added Value" = Table.AddColumn(#"Renamed Columns", "value", each [quantity] * [unit_price], type number)
in
    #"Added Value"
```

Each line is one Applied Step, and each step uses the result of the step before it.

!!! tip "Order of steps matters"
    Remove duplicates **after** trimming and fixing capitals. Before cleaning, `"Rahim Traders "` and `"Rahim Traders"` count as different values, so true duplicates can slip through.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Keeping the automatic "Changed Type" step | Day/month dates are read as month/day: 5 Jan becomes 1 May, and 15/01 gives an error | Delete it, then use **Change Type → Using Locale** |
| Changing type before removing the `,` in numbers | Errors in the Qty column | Replace `,` first, or use the right locale |
| Removing duplicates before cleaning text | Real duplicates survive | Trim and fix capitals first |
| Editing the loaded table in the sheet | Your changes disappear on refresh | Make every change inside Power Query |
| Hard-coded file path on your own PC | A colleague's refresh fails | Use a shared folder, or a parameter for the path |

## Try it yourself

**Task:** In your cleaned query, add one more step that keeps only **non-cancelled** orders. How many rows remain, and what is their total value?

<details markdown="1">
<summary>Show a hint</summary>

Click the filter arrow on *status* and untick **Cancelled**. Power Query adds a "Filtered Rows" step.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```m
#"Filtered Rows" = Table.SelectRows(#"Added Value", each [status] <> "Cancelled")
```

**11 rows** with a total value of **9,075**. These match the SQL and Excel results from earlier lessons, so you know the cleaning worked.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. A date column shows `05/01/2026` and you know it means 5 January. What is the safest way to convert it?

1. Change Type → Date
2. Change Type → Using Locale → English (United Kingdom)
3. Replace `/` with `-`

<details markdown="1"><summary>Show answer</summary>
**B.** "Using Locale" tells Power Query the format is day/month/year, whatever your computer's settings are.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Where should you fix a typo that appears in every monthly export?

1. In the loaded Excel table, after each refresh
2. As a step in Power Query
3. In the source system only

<details markdown="1"><summary>Show answer</summary>
**B** (and report it to the source owner, too). A Power Query step fixes it automatically on every refresh. Edits to the loaded table are overwritten.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why trim spaces before removing duplicates?

1. Trimming makes the query faster
2. `"Dhaka "` and `"Dhaka"` are different values until trimmed
3. Remove Duplicates trims automatically

<details markdown="1"><summary>Show answer</summary>
**B.** Clean the text first, so that true duplicates actually match.
</details>
</div>

## Summary

- Power Query records every cleaning action as an **Applied Step** (written in M) that runs again on **Refresh**.
- Typical cleaning: remove blank rows, Trim, Capitalize Each Word, Replace Values, Change Type **Using Locale**, Remove Duplicates, rename, add columns.
- Delete or check the automatic type step. Dates and numbers depend on the locale.
- Check the result against a known total (here 9,315, or 9,075 non-cancelled).

!!! job "Job-ready check"
    **Interview question:** *"You receive the same messy sales export every month. How do you handle it?"*

    **Strong answer:** "I build a Power Query once: remove blanks, trim and standardise text, set types with the correct locale, de-duplicate, and add calculated columns. Then each month I replace the file and refresh. I check row counts and totals against the source, and report recurring data-quality issues to the system owner."

    **Mini project:** Build the cleaning query, load it to a sheet, and add a small **Checks** table: rows loaded (12), total value (9,315), and distinct regions (4). Save it as `clean-orders.xlsx`.
