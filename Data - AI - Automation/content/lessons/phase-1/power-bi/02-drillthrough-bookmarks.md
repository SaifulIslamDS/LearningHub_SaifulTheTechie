---
title: "Power BI Drill-through & Bookmarks: Guided Detail and Saved Views"
order: 2
summary: "Let users right-click a customer to open a detail page, and give them one-click saved views with bookmarks and buttons."
level: Intermediate
time: "40 min"
topics: ["Drill-through", "Bookmarks"]
prerequisites: ["phase-1/power-bi/01-model-kpis"]
keywords: [drillthrough, drill-through, drill through filters, back button, detail page, bookmark, bookmarks pane, selection pane, button, bookmark navigator, saved view, storytelling]
reviewed: 2026-10-09
resources:
  - title: "Drillthrough in Power BI reports"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough"
    source: "Microsoft Learn"
    note: "Setting up drill-through pages step by step."
  - title: "Create report bookmarks in Power BI"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks"
    source: "Microsoft Learn"
    note: "Bookmark options, the Selection pane and buttons."
  - title: "Use report page drillthrough (guidance)"
    url: "https://learn.microsoft.com/en-us/power-bi/guidance/report-drillthrough"
    source: "Microsoft Learn"
    note: "When drill-through is the right design choice."
files: [sales_model.xlsx]
---

## What is it?

- **Drill-through:** from a summary visual, a user right-clicks an item (e.g. a customer) and jumps to a **detail page filtered to that item**. A **Back** button returns them to where they were.
- **Bookmarks:** saved **views** of a report page: filters, slicer selections, visible visuals and the current page. Attached to buttons, they give users one-click views like *"All orders"* and *"Open orders only"*.

!!! job "Why it matters at work"
    Overview pages should stay simple, but managers always ask *"What's behind that number?"*. Drill-through answers that without cluttering the overview. Bookmarks turn a report into a guided story for monthly reviews. Both are standard PL-300 topics and a sign of a polished report.

## Example 1: a customer drill-through page

**Build the target page:**

1. Add a new page (the **+** at the bottom) and rename it **Customer details**.
2. In the **Visualizations** pane, find **Drill through**, and drag `Customers[customer_name]` into **Add drill-through fields here**.
3. Power BI **adds a Back button automatically**.
4. Add a **table** visual: `Orders[order_id]`, `Date[Date]`, `Products[product]`, `Orders[status]` and `Revenue`. Add a **card** with `Revenue`.

**Use it:** on the overview page, add a table with `Customers[customer_name]` and `Net Revenue`. Right-click **Karim Garments** → **Drill through → Customer details**:

| order_id | Date | product | status | Revenue |
|---|---|---|---|---|
| 2 | 2026-01-08 | Metal Buttons | Delivered | 200 |
| 6 | 2026-02-02 | Cotton Twill | Delivered | 680 |
| 12 | 2026-03-09 | Denim 12oz | Shipped | 1,275 |
| **Total** | | | | **2,155** |

The page shows only Karim Garments. Click **Back** to return.

!!! tip "If Drill through doesn't appear when you right-click"
    The visual you right-click must contain the **same field** as the drill-through well, here `Customers[customer_name]`. A visual built on `Orders[customer]` won't offer it. That's one more reason to use dimension columns.

## Example 2: bookmarks for saved views

*Goal: two buttons on the overview page, "All orders" and "Open orders only".*

1. Add a **status** slicer (`Orders[status]`).
2. Open the pane: **View → Bookmarks**.
3. Clear the status slicer → in the Bookmarks pane click **Add** → rename it **All orders** (… → Rename).
4. Select **Shipped** and **Pending** in the slicer → **Add** → rename it **Open orders only**.
5. Click each bookmark to test it. With *Open orders only*, a region table shows **Chattogram 1,275 · Dhaka 320 · Narayanganj 810** (total **2,405**).

**Add buttons:** **Insert → Buttons → Blank**. In the Format pane, set **Action → On**, **Type → Bookmark**, **Bookmark → All orders**. Do the same for *Open orders only*. In Desktop, **Ctrl + click** a button to test it. In the published report, a normal click works.

Shortcut: **Insert → Buttons → Navigator → Bookmark navigator** creates one button per bookmark automatically.

### What a bookmark saves (and how to control it)

| Option (… menu on the bookmark) | Restores | Turn it off when… |
|---|---|---|
| **Data** | filters and slicer selections | the bookmark should only change what's shown, not reset filters |
| **Display** | which visuals are visible (Selection pane), spotlight | you only want to change filters |
| **Current page** | jumps to the page where it was saved | the bookmark should work on whichever page the user is on |
| **All visuals / Selected visuals** | applies to all, or only chosen, visuals | different bookmarks control different parts of the page |

The **Selection pane** (**View → Selection**) shows or hides visuals. Combined with Display bookmarks, it can switch between a chart and a table in the same spot.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Source visual uses a different field than the drill-through well | No *Drill through* option | Use the same dimension field in both |
| Deleting the automatic Back button | Users get stuck on the detail page | Keep it, or add a page-navigation button |
| Bookmarks made, then visuals changed | The bookmark restores an old state | Select the bookmark → … → **Update** |
| Leaving **Data** on for display-only bookmarks | Clicking resets the user's filters | Turn off **Data** for that bookmark |
| Testing buttons in Desktop with a normal click | Nothing happens | **Ctrl + click** in Desktop |

## Try it yourself

**Task:** Create a **Region details** drill-through page (drill-through field `Regions[region]`) with a card for `Net Revenue` and `Achievement %`. Drill into **Narayanganj**. What do the cards show?

<details markdown="1">
<summary>Show a hint</summary>

Put `Regions[region]` into the drill-through well. Then right-click Narayanganj in the overview matrix, which uses `Regions[region]` on rows.
</details>

<details markdown="1">
<summary>Show the solution</summary>

Net Revenue **1,230** and Achievement % **82.0%** (target 1,500). Adding a table of that region's orders (9: Pending 810, and 11: Delivered 420) shows *why*: one order is still pending.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Where do you put the field that defines a drill-through page?

1. The Filters on all pages well
2. The Drill through well on the target page
3. A slicer on the source page

<details markdown="1"><summary>Show answer</summary>
**B.** Add it to **Drill through** on the detail page. The Back button is created automatically.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. You want a bookmark that only switches a chart to a table, without resetting the user's slicers. Which option do you turn off?

1. Display
2. Data
3. Current page

<details markdown="1"><summary>Show answer</summary>
**B — Data.** Keep Display on so the visibility changes.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. How do you test a bookmark button in Power BI Desktop?

1. Double-click
2. Ctrl + click
3. Right-click → Run

<details markdown="1"><summary>Show answer</summary>
**B — Ctrl + click** while editing. Readers of the published report just click.
</details>
</div>

## Summary

- **Drill-through:** a detail page with a field in the *Drill through* well, an automatic Back button, and right-click on a source visual with the same field.
- **Bookmarks:** saved states (Data, Display, Current page) added in the Bookmarks pane, triggered by buttons or a bookmark navigator.
- Use the **Selection pane** to show and hide visuals for bookmark views.
- Update bookmarks after changing visuals, and choose Data/Display options deliberately.

!!! job "Job-ready check"
    **Interview question:** *"A manager wants to see the orders behind a customer's total without leaving the dashboard. How?"*

    **Strong answer:** "A customer drill-through page: the customer dimension field in the drill-through well, a table of that customer's orders and a few KPI cards. From any visual showing customers, they right-click and drill through, then use Back to return. For common views, like open orders only, I'd add bookmark buttons."

    **Mini project:** Add **Customer details** and **Region details** drill-through pages, and two bookmark buttons on the overview page. Record a short screen video or GIF of using them for your portfolio.
