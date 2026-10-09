---
title: "Excel Conditional Formatting: Make Important Data Stand Out"
order: 5
summary: "Highlight cancelled orders, big values and whole rows automatically — with built-in rules, data bars and your own formulas."
level: Beginner
time: "30 min"
topics: ["Conditional formatting"]
prerequisites: ["phase-1/excel-analysis/01-if-logical"]
keywords: [conditional formatting, highlight, data bars, color scales, icon sets, formula rule, highlight row, above average, manage rules]
reviewed: 2026-10-09
resources:
  - title: "Use conditional formatting to highlight information in Excel"
    url: "https://support.microsoft.com/en-us/excel/use-conditional-formatting-to-highlight-information-in-excel"
    source: "Microsoft Support"
    note: "All rule types, step by step."
  - title: "Use data bars, color scales, and icon sets to highlight data"
    url: "https://support.microsoft.com/en-us/excel/use-data-bars-color-scales-and-icon-sets-to-highlight-data"
    source: "Microsoft Support"
    note: "Visual rules inside cells."
  - title: "Excel Formulas: Over-Budget Items"
    url: "https://edu.gcfglobal.org/en/excelformulas/overbudget-items/full"
    source: "GCFGlobal (free)"
    note: "A short tutorial on formula-based highlighting."
files: [orders.xlsx, excel-solutions.xlsx]
---

## What is it?

Conditional formatting changes a cell's look, such as its fill colour, font or a small bar, **based on its value**. When the data changes, the colours update by themselves. Readers see what matters without reading every number.

!!! job "Why it matters at work"
    Managers scan reports; they don't read them. Highlighting cancelled orders, overdue items or the biggest deals in red or green is expected in every operations and sales report. Formula-based rules show that you go beyond the basic menu.

## Where to find it

Select the cells → **Home** tab → **Conditional Formatting**. The main options:

| Option | Use it for |
|---|---|
| **Highlight Cells Rules** | Equal to, greater than, text contains, dates |
| **Top/Bottom Rules** | Top 10, above average, below average |
| **Data Bars / Color Scales / Icon Sets** | Show size inside the cell |
| **New Rule → Use a formula** | Any rule you can write as a TRUE/FALSE formula |
| **Manage Rules** | See, edit, reorder and delete rules |

## Example 1: highlight big values (built-in rule)

*Goal: make every order worth 1,000 or more green.*

1. Select **J2:J13**.
2. Choose **Conditional Formatting → Highlight Cells Rules → Greater Than…**
3. "Greater than" is strictly greater, so for "1,000 or more" type **999.99**. Or use **New Rule → Format only cells that contain → greater than or equal to → 1000**.
4. Pick a green fill and click **OK**.

Highlighted: orders **3, 5, 8 and 12**.

## Example 2: data bars

Select **J2:J13** → **Conditional Formatting → Data Bars** → choose a colour. Each cell gets a bar sized by its value, a mini bar chart inside the table. Order 3 (1,560) has the longest bar and order 2 (200) the shortest.

## Example 3: highlight the whole row with a formula

*Goal: shade the full row of every cancelled order.*

1. Select the **whole data area A2:J13**, starting from row 2.
2. Choose **Conditional Formatting → New Rule → Use a formula to determine which cells to format**.
3. Enter:

```excel
=$I2="Cancelled"
```

4. Choose a light red fill and click **OK**.

Row **5** of the sheet (order 4, Rahim Traders, Zippers) turns red across all columns.

!!! tip "The $ sign is the trick"
    `$I2` locks the **column** (I = status), but leaves the **row** free. Excel checks the formula from the top-left cell of your selection (row 2). For each cell, it looks at column I **in that cell's own row**, so the whole row gets the colour. Without the `$`, only the cells in column I would change.

## Example 4: "above average" — and a hidden trap

Select **J2:J13** → **Top/Bottom Rules → Above Average**. Highlighted: orders **3, 5, 8, 9, 10 and 12**.

The rule uses the average of **all 12 cells: 776.25**, including the cancelled order. The business average you calculated earlier (non-cancelled) was **825**. With 825, order 9 (810) would **not** be highlighted. Built-in rules can't exclude rows. For a business definition, use a formula rule:

```excel
=AND($I2<>"Cancelled",$J2>AVERAGEIFS($J$2:$J$13,$I$2:$I$13,"<>Cancelled"))
```

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Formula rule without `$` before the column | Only one column is coloured, or the wrong cells are | `=$I2=...` |
| Selection starts at row 1, formula refers to row 2 | Colours are shifted one row | Start the selection at the formula's row |
| Too many colours | The report looks like a rainbow, and nothing stands out | 1–2 rules per table, with consistent meaning |
| Rules pile up after copy-pasting | A slow file, conflicting colours | Clean them up in **Manage Rules** |
| Built-in average/top rules on data with excluded rows | Misleading highlights | Use a formula rule with the business filter |

## Try it yourself

**Task:** Shade the **whole row** of every order that needs follow-up: status **Shipped** or **Pending**. Which rows change colour?

<details markdown="1">
<summary>Show a hint</summary>

Select A2:J13 and use a formula rule with `OR(...)`. Lock column I with `$`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```excel
=OR($I2="Shipped",$I2="Pending")
```

Orders **7, 9 and 12** (sheet rows 8, 10 and 13) are highlighted. Combined with the red cancelled rule, the sheet now shows at a glance: one cancelled order and three that need follow-up.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. You select A2:J13 and use `=I2="Cancelled"` (no `$`). What happens?

1. Whole rows are highlighted correctly
2. The wrong cells are highlighted, because the column reference moves too
3. Excel shows an error

<details markdown="1"><summary>Show answer</summary>
**B.** Without `$`, each column checks a different column (I, J, K…). Lock the column: `=$I2=...`.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which option shows a small bar inside each cell, sized by the value?

1. Color Scales
2. Data Bars
3. Icon Sets

<details markdown="1"><summary>Show answer</summary>
**B — Data Bars.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. The built-in "Above Average" rule on J2:J13 uses which average?

1. All 12 values (776.25)
2. Only non-cancelled values (825)
3. The median

<details markdown="1"><summary>Show answer</summary>
**A.** Built-in rules use every selected cell. For a filtered business average, write a formula rule.
</details>
</div>

## Summary

- Conditional formatting colours cells by value, and updates automatically.
- Built-in rules cover common needs. Data bars show size in the cell.
- **Formula rules** (`=$I2="Cancelled"`) can highlight whole rows. The `$` locks the column.
- Keep it to 1–2 meaningful rules per table, and check what "average" or "top" really includes.

!!! job "Job-ready check"
    **Interview question:** *"How would you highlight every overdue order row in a large sheet?"*

    **Strong answer:** "Select the full data range from the first data row and add a formula rule like `=AND($I2<>"Delivered",$K2<TODAY())`, with the column locked by `$`. It colours entire rows and updates every day. I'd use one colour per meaning and document the rule for the team."

    **Mini project:** In your workbook, add three rules: red rows for Cancelled, amber rows for Shipped/Pending, and data bars on value. Take a screenshot for your portfolio README.
