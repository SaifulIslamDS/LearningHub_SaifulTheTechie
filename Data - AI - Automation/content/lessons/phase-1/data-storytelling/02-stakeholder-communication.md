---
title: "Stakeholder Communication: The Right Message, Chart and Channel"
order: 2
summary: "Match each audience with the right level of detail, choose charts that make one point, write action titles, and handle questions and bad news with confidence."
level: Beginner
time: "35 min"
topics: ["Stakeholder communication"]
prerequisites: ["phase-1/data-storytelling/01-executive-summaries-memos"]
keywords: [stakeholder, audience, communication, chart choice, action title, presentation, email update, bad news, data caveat, requirements, feedback, meeting]
reviewed: 2026-10-09
resources:
  - title: "Create page and bookmark navigators"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/button-navigators"
    source: "Microsoft Learn"
    note: "Guide different audiences through one report."
  - title: "Get started with Microsoft data analytics"
    url: "https://learn.microsoft.com/en-us/training/paths/data-analytics-microsoft/"
    source: "Microsoft Learn (free training path)"
    note: "Covers the analyst's role with stakeholders."
files: [templates/executive_summary_template.md, known_answers.csv]
---

## What is it?

**Stakeholders** are the people who use, fund or are affected by your analysis: executives, managers, finance, operations and IT. **Stakeholder communication** means giving each of them the **right message, at the right level of detail, through the right channel**, and listening to what they actually need.

!!! job "Why it matters at work"
    The same Q1 numbers must convince a CEO, guide a sales manager and satisfy a finance controller. Analysts who adapt their message get their work used and get invited back. Behavioural interviews almost always include *"Tell me about a time you explained data to a non-technical audience."*

## Part 1: map your audience

| Stakeholder | Cares about | Give them | Channel |
|---|---|---|---|
| **CEO / director** | Are we on track? What do you need from me? | 3 numbers + 1 recommendation | 1 slide or a 5-line summary |
| **Sales manager** | Which regions and customers need action? | Region gaps, open orders by customer | Dashboard + weekly email |
| **Finance** | Are the numbers right and reconcilable? | Definitions, totals, cut-off dates | KPI dictionary + reconciliation sheet |
| **Operations** | What must be delivered, and when? | Open orders (2,405), by status and date | Filtered list / bookmark view |
| **IT / data owners** | Data quality and access | Issues found, refresh and RLS needs | Ticket or short technical note |

**Before you build anything, ask:** *What decision will you make with this? How often? What would make you trust it?*

## Part 2: one chart, one message

Choose the chart by the **point** you want to make:

| Message | Best chart | Example from our data |
|---|---|---|
| Compare items | Bar chart (sorted) | Revenue by region |
| Change over time | Line or column chart | Revenue vs target by month |
| Actual vs target | Bar + target marker, or a matrix with status colours | Achievement % by region |
| Part of a whole (few parts) | Stacked bar, or a simple % table | Share of revenue by segment |
| Single headline number | Card / big number | Net revenue 9,075 (94.5% of target) |

**Use action titles.** The title states the conclusion, not the contents:

| Descriptive title (weak) | Action title (strong) |
|---|---|
| Net Revenue by Month | March is at 47% of target and drives the Q1 gap |
| Revenue by Region | Dhaka and Narayanganj are 700 below target combined |
| Open Orders | 2,405 still to deliver. Karim Garments is half of it |

Then remove anything that doesn't support the title: extra gridlines, 3D effects, legends you can replace with direct labels, and every colour that isn't highlighting something.

## Part 3: a weekly email update

!!! example "Email — Sales update, week 41"
    **Subject:** Q1 sales: 94.5% of target. Action needed in Dhaka and Narayanganj

    Hi team,

    **Bottom line:** Q1 closed at 9,075 against a target of 9,600 (94.5%).

    - **Dhaka** −430 and **Narayanganj** −270 vs target. Account managers, please share pipeline updates by Thursday.
    - **2,405 is not yet delivered**: Karim Garments 1,275 (shipped), Sun Fashion 810 (pending), Nova Apparel 320 (shipped).
    - **Data note:** March may be incomplete. We'll confirm with the ERP team by Wednesday.

    Dashboard: [link] · Definitions: KPI dictionary [link]

Subject = the bottom line. One screen. Owners and deadlines. Caveats stated, not hidden.

## Part 4: questions, pushback and bad news

| Situation | What to do |
|---|---|
| "These numbers look wrong" | Don't argue. Reconcile together: show the definition (KPI dictionary) and the total trail (9,315 → minus the cancelled 240 → 9,075) |
| You don't know the answer | "I'll check and come back by [time]". Then do it |
| Bad news (missed target) | Say it plainly, early and with context. Bring the cause **and** a next step |
| Stakeholder wants a "quick" extra chart | Ask what decision it supports. Add it to the backlog if it doesn't change the current decision |
| Conflicting requests | Bring both owners together around the KPI definition. Don't build two versions |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| The same deck for every audience | Executives get lost, managers lack detail | Tailor depth by audience |
| Descriptive chart titles | Readers miss the point | Action titles |
| Jargon ("filter context", "LEFT JOIN") with business users | Confusion and lost trust | Plain business language |
| Hiding data caveats | Decisions on bad data, credibility damaged later | State caveats briefly and up front |
| Never asking for feedback | Reports nobody uses | Ask "what decision will this support?" and follow up |

## Try it yourself

**Task:** Rewrite these two chart titles as **action titles**, using numbers from the course:

1. "Revenue by Segment"
2. "Delivered % by Region"

<details markdown="1">
<summary>Show model answers</summary>

1. "Garment factories bring in 58% of revenue (5,265 of 9,075)"
2. "Narayanganj and Chattogram have delivered less than half of their sales"

(Narayanganj 34.1%, Chattogram 40.8%, from the CALCULATE lesson.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What should you usually give a CEO?

1. The full dashboard with every filter
2. A few headline numbers, with a recommendation and the decision needed
3. The SQL and DAX code

<details markdown="1"><summary>Show answer</summary>
**B.** Executives need the answer and the decision, not the mechanics.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which is an action title?

1. "Monthly Revenue 2026"
2. "March is at 47% of target and drives the Q1 gap"
3. "Chart 3"

<details markdown="1"><summary>Show answer</summary>
**B.** It states the conclusion the reader should take away.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A manager says your revenue number is wrong. What's the best first response?

1. Insist that it's right
2. Walk through the definition and reconcile the totals together
3. Change the number to match theirs

<details markdown="1"><summary>Show answer</summary>
**B.** Shared definitions and a transparent trail resolve most disagreements, and build trust.
</details>
</div>

## Summary

- **Map stakeholders:** what they care about, the detail level and the channel.
- **One chart, one message**, with an **action title**. Remove the clutter.
- Email updates: bottom line in the subject, owners and deadlines, caveats stated.
- Handle pushback by reconciling with definitions. Deliver bad news early, with a cause and a next step.

!!! job "Job-ready check"
    **Interview question:** *"Tell me about a time you explained data to a non-technical audience."*

    **Strong answer (STAR):** "**Situation:** quarterly sales were 5.5% below target, and managers disagreed on the numbers. **Task:** align everyone and focus action. **Action:** I shared one KPI definition, reconciled gross to net revenue live, and showed one chart with an action title, *'March drives the gap'*. **Result:** we agreed the numbers in ten minutes and spent the meeting on the pipeline plan for two regions."

    **Mini project:** For your Phase 1 project, write a one-page **stakeholder map** and one weekly update email. Add action titles to every chart in your dashboard.
