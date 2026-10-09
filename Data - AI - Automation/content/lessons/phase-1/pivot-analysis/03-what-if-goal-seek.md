---
title: "Excel What-If Analysis & Goal Seek: Plan with Numbers"
order: 3
summary: "Test business scenarios with a Data Table, compare plans with Scenario Manager, and work backwards from a target with Goal Seek."
level: Beginner–Intermediate
time: "35 min"
topics: ["What-If Analysis", "Goal Seek"]
prerequisites: ["phase-1/excel-analysis/02-sumifs-countifs"]
keywords: [what-if analysis, data table, goal seek, scenario manager, sensitivity, forecast, target, price change, volume change, model, input cells]
reviewed: 2026-10-09
resources:
  - title: "Introduction to What-If Analysis"
    url: "https://support.microsoft.com/en-us/office/introduction-to-what-if-analysis-22bffa5f-e891-4acc-bf7a-e4645c446fb4"
    source: "Microsoft Support"
    note: "An overview of scenarios, Goal Seek and data tables."
  - title: "Use Goal Seek to find the result you want by adjusting an input value"
    url: "https://support.microsoft.com/en-us/excel/use-goal-seek-to-find-the-result-you-want-by-adjusting-an-input-value"
    source: "Microsoft Support"
    note: "Step-by-step Goal Seek."
  - title: "Calculate multiple results by using a data table"
    url: "https://support.microsoft.com/en-us/excel/calculate-multiple-results-by-using-a-data-table"
    source: "Microsoft Support"
    note: "One- and two-variable data tables."
  - title: "Excel 2016: What-If Analysis"
    url: "https://edu.gcfglobal.org/en/excel2016/whatif-analysis/full"
    source: "GCFGlobal (free)"
    note: "A beginner tutorial with screenshots."
files: [orders.xlsx, excel-solutions.xlsx]
---

## What is it?

**What-If Analysis** answers planning questions by changing inputs and watching the result. Excel has three tools, under **Data → What-If Analysis**:

| Tool | Question it answers |
|---|---|
| **Data Table** | "What is the result for *many* different inputs?" |
| **Scenario Manager** | "How do my *named plans* (best / base / worst) compare?" |
| **Goal Seek** | "What input do I need to *hit a target*?" |

!!! job "Why it matters at work"
    Price changes, targets and budgets: managers constantly ask *"what happens if…?"* and *"what do we need to reach…?"*. Answering with a clean model instead of guesses is what turns a report-builder into an analyst. This is also the foundation for forecasting in Phase 4.

## Step 1: build a small model

A good model separates **inputs** (cells you change) from **calculations**. In a new sheet, **Model**:

| Cell | Label | Value / formula |
|---|---|---|
| B1 | Base revenue (non-cancelled) | `=SUMIFS(Orders!J2:J13,Orders!I2:I13,"<>Cancelled")` → **9,075** |
| B2 | Price change | **0%** *(input)* |
| B3 | Volume change | **0%** *(input)* |
| B4 | Projected revenue | `=B1*(1+B2)*(1+B3)` |

With both inputs at 0%, B4 shows **9,075**. Try a 5% price increase in B2 and B4 becomes **9,528.75**.

!!! tip "Colour your inputs"
    Give input cells a light fill (e.g. light yellow) so everyone knows which cells may be changed. It's a common convention in financial modelling.

## Example 1: a two-variable Data Table

*Question: what is projected revenue for price changes of 0%, +5% and +10%, combined with volume changes of 0%, −5% and −10%?* Customers may buy less if prices rise.

1. In **D2** type `=B4`. This corner cell links to the result.
2. In **E2:G2** type the price changes **0%, 5%, 10%**. In **D3:D5** type the volume changes **0%, −5%, −10%**.
3. Select **D2:G5** → **Data → What-If Analysis → Data Table**.
4. **Row input cell: B2** (price). **Column input cell: B3** (volume). Click **OK**.

| volume ↓ / price → | 0% | 5% | 10% |
|---|---|---|---|
| **0%** | 9,075.00 | 9,528.75 | 9,982.50 |
| **−5%** | 8,621.25 | 9,052.31 | 9,483.38 |
| **−10%** | 8,167.50 | 8,575.88 | 8,984.25 |

**Insight:** a 10% price rise that loses 10% of volume (8,984.25) ends up **below** today's revenue (9,075). The price rise only pays off if volume drops by less than about 9%.

!!! note "Data Tables recalculate constantly"
    A Data Table is a live formula grid. Large ones can slow down a workbook. You can set **Formulas → Calculation Options → Automatic except for Data Tables**.

## Example 2: Scenario Manager (named plans)

Choose **Data → What-If Analysis → Scenario Manager → Add**, and create three scenarios that change **B2:B3**:

| Scenario | Price change | Volume change | Projected revenue |
|---|---|---|---|
| Base | 0% | 0% | 9,075.00 |
| Price push | 10% | −5% | 9,483.38 |
| Discount drive | 0% | −10% | 8,167.50 |

Click **Show** to apply a scenario, or **Summary** to create a comparison sheet automatically. Scenarios are useful when you present two or three named options to management.

## Example 3: Goal Seek (work backwards)

*Question: with volume expected to fall 5%, what price increase do we need to reach 10,000 revenue?*

1. Set **B3** to **−5%**.
2. Choose **Data → What-If Analysis → Goal Seek**.
3. **Set cell: B4**. **To value: 10000**. **By changing cell: B2**. Click **OK**.

Excel finds **B2 ≈ 15.99%**. In other words, a price rise of about 16% is needed, which is a lot. The model has turned a vague target into a concrete, debatable number.

**A second Goal Seek, on one order:** Sun Fashion's Denim order is priced at 5.40 per unit. How many units for a 1,000 order? Set up `=quantity*5.40`, then Goal Seek it to 1000 by changing the quantity. The result is **185.19**. In practice you'd round **up to 186 units**: Goal Seek gives the exact maths, and you apply the business rule.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Typing numbers into formulas (`=9075*1.05`) | Nothing can vary | Put inputs in their own cells |
| Data Table input cells on another sheet | Excel refuses | Keep the input cells on the same sheet as the Data Table |
| Swapping row and column input cells | Labels and results don't match | Row input = the values across the top |
| Goal Seek "by changing" a formula cell | Error | It must be a plain input value |
| Treating Goal Seek's decimal result as final | 185.19 units isn't orderable | Apply rounding or business rules afterwards |

## Try it yourself

**Task:** Using the same model, find the **volume change** that keeps revenue at exactly **9,075** if the price rises **10%**.

<details markdown="1">
<summary>Show a hint</summary>

Set B2 to 10%. Then Goal Seek: set cell **B4**, to value **9075**, by changing **B3**.
</details>

<details markdown="1">
<summary>Show the solution</summary>

Goal Seek returns **B3 ≈ −9.09%**. You can lose up to about 9.1% of volume after a 10% price rise and still keep today's revenue. That's the break-even point behind the insight in Example 1. (Check: 1 ÷ 1.10 − 1 = −0.0909.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. You need the input value that produces a target result. Which tool do you use?

1. Data Table
2. Goal Seek
3. Scenario Manager

<details markdown="1"><summary>Show answer</summary>
**B — Goal Seek.** It works backwards from the target to one input.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. In a two-variable Data Table, what goes in the top-left corner cell?

1. The first input value
2. A link to the result formula (e.g. `=B4`)
3. Nothing

<details markdown="1"><summary>Show answer</summary>
**B.** The corner cell links to the result. Excel fills the grid by substituting the row and column inputs.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why keep inputs in separate cells instead of typing them into formulas?

1. Excel requires it
2. So What-If tools and colleagues can change them safely
3. It makes the file smaller

<details markdown="1"><summary>Show answer</summary>
**B.** Separate input cells make a model testable, transparent and reusable.
</details>
</div>

## Summary

- Build models with clear **input cells** and **formula cells**.
- **Data Table**: results for many input combinations in one grid.
- **Scenario Manager**: named plans you can show and summarise.
- **Goal Seek**: the input needed to reach a target. Apply business rounding afterwards.

!!! job "Job-ready check"
    **Interview question:** *"Management wants 10,000 in revenue next quarter. How would you show what it takes?"*

    **Strong answer:** "I'd build a simple model, base revenue × (1 + price change) × (1 + volume change), with separate input cells. Then a Data Table to show the range of outcomes, and Goal Seek to find the required price change for a given volume assumption, about 16% if volume drops 5%. Finally I'd present it as two or three named scenarios, so the discussion is about assumptions, not arithmetic."

    **Mini project:** Add a **Model** sheet to your workbook with the inputs, a 3×3 Data Table and the Goal Seek answer, written as a one-paragraph recommendation. This completes your Excel portfolio piece for Phase 1A.
