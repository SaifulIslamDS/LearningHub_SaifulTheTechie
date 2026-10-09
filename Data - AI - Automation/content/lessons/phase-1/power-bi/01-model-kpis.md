---
title: "Power BI Report Basics: Model Hygiene and a KPI Page"
order: 1
summary: "Tidy the model so it's easy to use, then build a one-page sales overview with KPI cards, a target matrix, a monthly chart and slicers."
level: Beginner
time: "50 min"
topics: ["Data modeling", "KPIs"]
prerequisites: ["phase-1/power-pivot-dax/02-measures-kpi"]
keywords: [power bi desktop, report view, model view, card, kpi visual, matrix, column chart, slicer, conditional formatting, hide columns, display folder, sort by column, format, layout]
reviewed: 2026-10-09
resources:
  - title: "Download Power BI Desktop"
    url: "https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop"
    source: "Microsoft Learn"
    note: "System requirements and install options."
  - title: "Understand star schema and the importance for Power BI"
    url: "https://learn.microsoft.com/en-us/power-bi/guidance/star-schema"
    source: "Microsoft Learn"
    note: "Model design guidance that this lesson applies."
  - title: "Get started with Microsoft data analytics"
    url: "https://learn.microsoft.com/en-us/training/paths/data-analytics-microsoft/"
    source: "Microsoft Learn (free training path)"
    note: "The first path of the PL-300 learning journey."
files: [sales_model.xlsx]
---

## What is it?

A Power BI report has two layers:

1. **The model:** tables, relationships and measures (built in the DAX module). **Data modelling** here also means making it *easy to use*: clear names, hidden technical columns, formats and sort orders.
2. **The report pages:** visuals that show the **KPIs**, the few numbers that tell a manager whether the business is on track.

!!! job "Why it matters at work"
    Managers judge a dashboard in a few seconds: *Are we on target? Where is the problem?* A clean model with clear KPIs answers that, and also makes the report easy for the next analyst to maintain. "Build a sales dashboard" is the classic Power BI take-home assignment.

## Part 1: model hygiene (10 minutes that save hours)

In **Model view**:

| Task | How | Why |
|---|---|---|
| Hide key and duplicate columns in facts | Right-click → **Hide in report view** (`Orders[customer]`, `Orders[region]`, `Orders[product]`, `Targets[month]` …) | Users pick dimension columns, so filters work across facts |
| Hide `Orders[value]` | It's covered by explicit measures | Stops implicit "Sum of value" |
| Format every measure | Select measure → **Measure tools → Format** | Whole number for money, % with 1 decimal for ratios |
| Group measures in **display folders** | Properties pane → *Display folder*: `Sales`, `Targets` | Easy to find as the model grows |
| Sort month names | `Date[Month]` → **Sort by column → Month Number** | Jan, Feb, Mar, not alphabetical |
| Add descriptions | Properties → *Description* (e.g. "Net Revenue = all orders except Cancelled") | Shows as a tooltip, and documents the KPI |

## Part 2: build the Sales Overview page

**1. KPI cards (top row).** Add four **Card** visuals: `Net Revenue` **9,075** · `Target` **9,600** · `Achievement %` **94.5%** · `Avg Order Value` **825**.

**2. Target matrix (middle left).** **Matrix** with `Regions[region]` on rows and `Net Revenue`, `Target`, `Achievement %` and `Gap to Target` as values:

| region | Net Revenue | Target | Achievement % | Gap to Target |
|---|---|---|---|---|
| Chattogram | 2,155 | 2,100 | 102.6% | 55 |
| Dhaka | 3,170 | 3,600 | 88.1% | −430 |
| Gazipur | 2,520 | 2,400 | 105.0% | 120 |
| Narayanganj | 1,230 | 1,500 | 82.0% | −270 |
| **Total** | **9,075** | **9,600** | **94.5%** | **−525** |

Then add **conditional formatting** to *Achievement %*: Format pane → **Cell elements → Font color → Rules**: ≥ 1 → green, < 1 → red. Dhaka and Narayanganj turn red.

**3. Monthly chart (middle right).** **Clustered column chart**: X-axis `Date[Month]`, Y-axis `Net Revenue` and `Target`. Jan 3,440 vs 2,800 · Feb 3,940 vs 3,200 · Mar 1,695 vs 3,600. March stands out immediately.

**4. Slicers (top or left).** Add slicers for `Products[category]` and `Customers[segment]`. Click **Fabric**: the cards change to Net Revenue **4,745**.

!!! warning "Watch what slicers do to targets"
    Targets exist only by **region and month**. They are not related to products or customers. When you slice by category, `Target` stays at 9,600 and Achievement % becomes meaningless (4,745 ÷ 9,600). Either hide the target visuals when a category is selected, or add a note: *"Targets are set by region and month only."* Knowing the **grain** of each fact table is part of KPI design.

## Layout rules that make KPIs readable

- **Top-left first:** the most important numbers go where the eye starts.
- **One page, one question:** this page answers *"Are we on target, and where aren't we?"*
- **Few colours:** use one neutral colour, and red or green only for status.
- **Titles that say something:** "March is 53% below target", not "Net Revenue by Month".

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Building visuals on fact-table columns | Targets don't filter, comparisons break | Use dimension columns, and hide the fact keys |
| Raw numbers like 0.9453125 | Hard to read | Set formats on the measures |
| Ten visuals on one page | Nobody finds the message | 4–6 visuals that answer one question |
| A category slicer next to target KPIs | Meaningless achievement % | Explain the grain, or keep target pages separate |
| Months in alphabetical order (Feb, Jan, Mar) | A confusing chart | Sort Month by Month Number |

## Try it yourself

**Task:** Add a **Customers[segment]** slicer and select **Garment Factory**. What does the Net Revenue card show, and why does the Target card *not* change?

<details markdown="1">
<summary>Show a hint</summary>

Think about which tables the Customers dimension is related to.
</details>

<details markdown="1">
<summary>Show the solution</summary>

Net Revenue shows **5,265**. The Target card stays at **9,600**, because Customers is related only to Orders, not to Targets, so the segment filter never reaches the targets. That's correct model behaviour. The report design must make the grain clear, for example with a note under the target visuals.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Why hide `Orders[region]` in report view?

1. To save memory
2. So users pick `Regions[region]`, which filters both Orders and Targets
3. Hidden columns are faster

<details markdown="1"><summary>Show answer</summary>
**B.** Hiding fact keys guides users to the shared dimension columns.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Where should the most important KPI usually go on a report page?

1. Bottom right
2. Top left
3. In a tooltip

<details markdown="1"><summary>Show answer</summary>
**B — top left.** That's where readers look first.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Months appear as Feb, Jan, Mar. How do you fix this?

1. Rename them 1-Jan, 2-Feb…
2. Sort the Month column by Month Number
3. Use a different chart

<details markdown="1"><summary>Show answer</summary>
**B.** "Sort by column" keeps the readable labels and fixes the order.
</details>
</div>

## Summary

- **Model hygiene:** hide fact keys and raw columns, format measures, use display folders and descriptions, and sort months properly.
- **KPI page:** cards for headline numbers, a target matrix with status colours, a monthly chart and a few slicers.
- Know each fact's **grain**: targets by region and month don't respond to product or customer slicers.
- Use clear, message-driven titles and few colours.

!!! job "Job-ready check"
    **Interview question:** *"Walk me through how you'd build a sales-vs-target dashboard."*

    **Strong answer:** "First the model: a star schema with Orders and Targets facts, shared Region and Date dimensions, explicit measures for net revenue, target and achievement, formatted and documented. Then one overview page: KPI cards top left, a region matrix with conditional formatting, revenue vs target by month, and slicers that respect the target grain. I'd check the totals against the source before sharing."

    **Mini project:** Build the **Sales Overview** page and take a screenshot. In your README, write 3 sentences: on target? where not? what next?
