---
title: "Executive Summaries & Decision Memos: Turn Numbers into Decisions"
order: 1
summary: "Write a 5-line executive summary and a one-page decision memo that lead with the answer, back it with numbers, and ask for a clear decision."
level: Beginner
time: "40 min"
topics: ["Executive summaries", "Decision memos"]
prerequisites: ["phase-1/power-pivot-dax/02-measures-kpi"]
keywords: [executive summary, bluf, bottom line up front, pyramid principle, scqa, decision memo, recommendation, options, so what, insight, management report, writing]
reviewed: 2026-10-09
resources:
  - title: "Get started with Microsoft data analytics"
    url: "https://learn.microsoft.com/en-us/training/paths/data-analytics-microsoft/"
    source: "Microsoft Learn (free training path)"
    note: "Includes the analyst's role in communicating insights."
  - title: "Use report page drillthrough (guidance)"
    url: "https://learn.microsoft.com/en-us/power-bi/guidance/report-drillthrough"
    source: "Microsoft Learn"
    note: "Report design that supports the summary → detail flow."
files: [templates/executive_summary_template.md, templates/decision_memo_template.md, known_answers.csv]
---

## What is it?

- An **executive summary** is the few lines a busy leader reads instead of your whole report. It answers: *What's happening? Why does it matter? What should we do?*
- A **decision memo** is a one-page document that asks a decision-maker to **choose between options**, with the evidence and your recommendation.

Both follow one rule: **answer first, details after.** It's often called **BLUF**: *Bottom Line Up Front*.

!!! job "Why it matters at work"
    Analysts are judged on decisions improved, not on dashboards built. A clear summary gets your work read and acted on. Hiring managers regularly ask candidates to "present your findings in five minutes", and the ability to write a crisp recommendation separates senior analysts from report builders.

## Part 1: the structure that works

**Situation → Complication → Resolution (SCR)**, written answer-first:

| Part | Question it answers | Our Q1 example |
|---|---|---|
| **Bottom line** | What's the one thing to know? | Q1 sales reached 94.5% of target, 525 short |
| **Situation** | What's the context? | Jan and Feb beat targets (≈123%) |
| **Complication** | What's the problem? | March is at 47.1% of target; Dhaka and Narayanganj are below target |
| **Resolution** | What should we do? | Confirm March data is complete; focus follow-up on Dhaka and Narayanganj |

## Part 2: write the executive summary (5 lines)

Using only numbers you've already calculated:

!!! example "Executive summary — Q1 2026 sales"
    **Q1 net revenue was 9,075, which is 94.5% of the 9,600 target (525 short).**

    - January (122.9%) and February (123.1%) beat their targets. **March is at 47.1%**, the main reason for the gap.
    - By region, **Dhaka (−430)** and **Narayanganj (−270)** are below target. Gazipur (+120) and Chattogram (+55) are above.
    - 26.5% of net revenue (2,405) is not yet delivered, mostly Karim Garments (1,275, shipped) and Sun Fashion (810, pending).
    - **Recommended:** (1) confirm that March data is complete before acting; (2) review the Dhaka and Narayanganj pipelines this week; (3) chase the two open orders to delivery.

**Checklist for each line:** Is there a number? Is there a comparison (vs target, vs last month)? Is there a "so what"?

!!! tip "Insight vs observation"
    *Observation:* "March revenue was 1,695."
    *Insight:* "March is at 47% of target and drives the whole quarterly gap. Check the data is complete before reacting."
    An insight adds **comparison, cause or consequence**.

## Part 3: the decision memo (one page)

A decision memo has a fixed shape:

```text
TO / FROM / DATE
DECISION NEEDED:   one sentence, with a deadline
RECOMMENDATION:    your option, in one sentence
BACKGROUND:        3–4 lines with the key numbers
OPTIONS:           2–3 options with pros, cons and impact
RISKS & ASSUMPTIONS
NEXT STEPS if approved
```

!!! example "Decision memo — Metal Buttons pricing"
    **Decision needed:** Approve a revised discount limit for Metal Buttons by 20 October.

    **Recommendation:** Cap discounts at 10% for new Metal Buttons orders (currently 20%).

    **Background:** Metal Buttons sell at 0.04 against a list price of 0.05, a **20% discount**, compared with 2–13% for other products. Two orders (13,000 units) were sold this way in Q1.

    **Options:**

    | Option | Pro | Con |
    |---|---|---|
    | A. Keep 20% | No customer friction | Margin stays low. Sets a precedent |
    | B. Cap at 10% (recommended) | Recovers margin. Still competitive | Some volume risk with two garment customers |
    | C. List price only | Full margin | High risk of losing the orders |

    **Assumption:** The 0.05 list price reflects the market. Sales should confirm this with two customers before rollout.

    **Next steps if approved:** Update the price list, brief the account managers (Anika, Tanvir), and review volume after one month.

The numbers come from the XLOOKUP lesson: Metal Buttons orders 2 and 7, 5,000 + 8,000 units at 0.04 vs a list price of 0.05.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Starting with method ("I loaded the data…") | Readers stop before the answer | Bottom line first |
| Numbers with no comparison | "Is 9,075 good?" | Compare with target, last period or peers |
| Ten findings with equal weight | Nothing stands out | 3 findings maximum, ranked |
| A recommendation without options | Looks one-sided | Show 2–3 options with trade-offs |
| Hiding uncertainty (incomplete March data) | Wrong decisions, lost trust | State assumptions and data caveats clearly |

## Try it yourself

**Task:** Write a **3-sentence** executive summary of the **regional** results only, using BLUF.

<details markdown="1">
<summary>Show a model answer</summary>

**Two of four regions missed their Q1 target, leaving the company 525 short (94.5%).** Dhaka is the largest gap in absolute terms (−430, 88.1%) and Narayanganj the weakest in percentage terms (82.0%), while Gazipur (105.0%) and Chattogram (102.6%) beat their targets. We recommend a pipeline review with the Dhaka and Narayanganj account managers this week.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does BLUF mean in practice?

1. Put the method first
2. Put the main conclusion first
3. Put all the charts first

<details markdown="1"><summary>Show answer</summary>
**B.** Bottom Line Up Front: the answer comes first, and the evidence follows.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which sentence is an insight rather than an observation?

1. "Dhaka revenue was 3,170."
2. "Dhaka is 430 below target, the biggest gap of any region."
3. "We have four regions."

<details markdown="1"><summary>Show answer</summary>
**B.** It adds a comparison and a ranking that matter for action.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What must a decision memo always contain?

1. Every chart from the dashboard
2. The decision needed, the options, and a recommendation
3. The full SQL code

<details markdown="1"><summary>Show answer</summary>
**B.** A memo exists to get a decision. Make the choice and your view explicit.
</details>
</div>

## Summary

- **BLUF**: the answer first, then the support.
- An executive summary is a bottom line plus about 3 findings plus a recommendation, each with numbers **and** comparisons.
- A decision memo states the decision, recommendation, background, options with trade-offs, risks and next steps, on one page.
- Turn observations into insights with comparison, cause or consequence, and state caveats honestly.

!!! job "Job-ready check"
    **Interview question:** *"You have five minutes with the CEO to present quarterly results. How do you structure it?"*

    **Strong answer:** "Bottom line first: 94.5% of target, 525 short. Then the two or three findings that explain it: March, and two regions below target. Then one recommendation and the decision I need from them. Details stay in the appendix and the dashboard. I'd mention any data caveat, like March being incomplete, up front so the decision is made on the right basis."

    **Mini project:** Write a one-page **Q1 Sales Summary** (Markdown or PDF) with the executive summary and one decision memo. Add it to your Phase 1 project repository.
