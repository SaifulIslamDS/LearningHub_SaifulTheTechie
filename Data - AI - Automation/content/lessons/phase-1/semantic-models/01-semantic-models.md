---
title: "Semantic Models: One Trusted Definition for Every KPI"
order: 1
summary: "Why companies need one shared definition of each metric, how to build a semantic model people can trust, and how to reuse it in Power BI, Excel and AI tools."
level: Intermediate
time: "40 min"
topics: ["Why one KPI definition", "Building a semantic model", "Reusing metrics in reports and AI tools"]
prerequisites: ["phase-1/power-pivot-dax/02-measures-kpi", "phase-1/power-bi/04-publish-copilot"]
keywords: [semantic model, dataset, metrics layer, single source of truth, kpi definition, thin report, live connection, analyze in excel, build permission, endorsement, certified, measure description, display folder, copilot, ai-ready]
reviewed: 2026-10-09
resources:
  - title: "New name for Power BI datasets"
    url: "https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-rename"
    source: "Microsoft Learn"
    note: "Why datasets were renamed semantic models."
  - title: "Connect Excel to Power BI semantic models"
    url: "https://learn.microsoft.com/en-us/power-bi/collaborate-share/office-integration/service-connect-power-bi-datasets-excel"
    source: "Microsoft Learn"
    note: "Analyze in Excel and Get Data → From Power BI, with permissions."
  - title: "Prepare your data for AI to improve Copilot results"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai"
    source: "Microsoft Learn"
    note: "AI data schemas, verified answers and AI instructions."
  - title: "Optimize your semantic model for Copilot"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-evaluate-data"
    source: "Microsoft Learn"
    note: "Naming and modelling tips that help AI."
files: [sales_model.xlsx, templates/kpi_dictionary_template.md]
---

## What is it?

A **semantic model** is the shared business layer between raw data and every report: tables, relationships, **measures**, formats, descriptions and security. In Power BI, this used to be called a **dataset**. Microsoft renamed it because "semantic model" better describes a model that carries business meaning.

The idea is simple: **define each KPI once, and use it everywhere.**

!!! job "Why it matters at work"
    The most expensive BI problem isn't a slow report. It's **two reports showing different revenue** for the same month. Then meetings turn into arguments about numbers instead of decisions. Companies hire analysts and analytics engineers specifically to build and govern trusted semantic models, and the same models now feed AI assistants.

## Part 1: why one KPI definition

Look at what "Q1 revenue" can mean with our data:

| Definition | Q1 value |
|---|---|
| All orders, including cancelled | 9,315 |
| All except cancelled (**Net Revenue**) | **9,075** |
| Delivered only | 6,670 |

Three honest analysts can report three numbers. The fix isn't "be more careful": it's **one agreed definition, written down and built once**.

A **KPI dictionary** records each definition:

| KPI | Definition | DAX measure | Owner |
|---|---|---|---|
| Net Revenue | Value of all orders except status Cancelled | `CALCULATE([Revenue], Orders[status] <> "Cancelled")` | Head of Sales |
| Achievement % | Net Revenue ÷ Target, at region/month grain | `DIVIDE([Net Revenue], [Target])` | Head of Sales |
| Avg Order Value | Net Revenue ÷ Net Orders | `DIVIDE([Net Revenue], [Net Orders])` | Sales Ops |

## Part 2: build a semantic model people can trust

Most of this you've already done in the DAX and Power BI lessons. Here is the full checklist:

| Area | Good practice |
|---|---|
| **Structure** | Star schema, single-direction one-to-many relationships, a marked date table |
| **Measures** | Explicit measures only. Raw value columns hidden. Measures built from base measures |
| **Names** | Business names (`Net Revenue`, not `SumVal2`). Consistent units |
| **Descriptions** | Every measure and important column has a description (shown as a tooltip, and read by AI) |
| **Organisation** | Display folders (`Sales`, `Targets`, `Time`), a `_Measures` table |
| **Formats** | Set on the measure: money as whole numbers, ratios as %, 1 decimal |
| **Security** | RLS roles on dimensions, tested |
| **Trust signals** | In the service, mark the model **Promoted**, or **Certified** if your organisation has a certification process |

## Part 3: reuse the model in reports, Excel and AI

Once the model is published, **don't copy it**. Connect to it.

**1. Thin reports (Power BI).** Other report authors use **Get data → Power BI semantic models** in Desktop and build new pages on the **same** measures. They create reports but don't copy the data. Change *Net Revenue* once, and every connected report updates.

**2. Excel.** Finance can stay in Excel:

- In the service, open the semantic model → **… → Analyze in Excel**. You get an Excel file with a **live connection**.
- Or, in Excel: **Data → Get Data → From Power BI**.

You can then build PivotTables using the **same measures**. Users need **Build** permission on the model (or the Contributor role or higher), and your admin must allow live connections from Excel.

**3. AI tools.** Copilot and similar assistants answer questions **from the semantic model**. The same descriptions and clear names that help people also help AI. Add **Prep data for AI** settings (from the previous lesson), such as instructions that "revenue means Net Revenue".

```text
       raw data ──► Power Query ──► SEMANTIC MODEL ──┬──► Power BI reports (thin)
                                    (measures, RLS,   ├──► Excel PivotTables (live)
                                     descriptions)    └──► Copilot / AI questions
```

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Every report imports its own copy of the data | Different numbers, many refreshes | One shared model, and thin reports connect to it |
| Measures without descriptions | Confusion for people and AI | Describe every published measure |
| Definitions agreed in a meeting but not written down | Drift over time | A KPI dictionary with owners |
| Exporting the model's data to Excel and editing it | Uncontrolled copies | Analyze in Excel (live connection) |
| Renaming or changing a measure without telling anyone | Downstream reports break or change silently | Treat measures like an API: announce changes and document versions |

## Try it yourself

**Task:** Write the KPI-dictionary row for **Delivered %** (from the CALCULATE lesson). Include its definition, measure, value for Q1, and one sentence on when to use it rather than Net Revenue.

<details markdown="1">
<summary>Show a model answer</summary>

| KPI | Definition | DAX measure | Q1 value |
|---|---|---|---|
| Delivered % | Share of Net Revenue from orders with status Delivered | `DIVIDE([Delivered Revenue], [Net Revenue])` | 73.5% |

*Use it* to track fulfilment: how much of the business won is actually delivered. Net Revenue measures sales won. Delivered % shows operational follow-through.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What was a Power BI semantic model previously called?

1. Dataflow
2. Dataset
3. Datamart

<details markdown="1"><summary>Show answer</summary>
**B — Dataset.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. A second team needs a new report with the same KPIs. What's the best approach?

1. Copy the .pbix and modify it
2. Build a thin report connected to the published semantic model
3. Export the data to Excel

<details markdown="1"><summary>Show answer</summary>
**B.** A single model with many thin reports keeps every KPI consistent.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why do measure descriptions matter for Copilot?

1. Copilot reads model metadata, such as names and descriptions, to choose the right measure
2. Descriptions make the model faster
3. They're required to publish

<details markdown="1"><summary>Show answer</summary>
**A.** Clear metadata helps both people and AI pick the correct definition.
</details>
</div>

## Summary

- A **semantic model** is the shared business layer: tables, relationships, measures, descriptions and security.
- **One KPI definition** prevents "two revenue numbers". Keep a **KPI dictionary** with owners.
- Build it as a star schema with explicit, described, formatted measures, plus RLS.
- **Reuse** it: thin Power BI reports, Analyze in Excel (live) and AI assistants. Don't copy the data.

!!! job "Job-ready check"
    **Interview question:** *"Two departments report different revenue numbers. How do you fix that permanently?"*

    **Strong answer:** "Agree one definition with the business owner and write it in a KPI dictionary. Implement it once as a measure in a shared, certified semantic model, then connect every report and Excel workbook to that model instead of keeping separate copies. Changes go through the model owner, so every consumer, including Copilot, uses the same number."

    **Mini project:** Write a KPI dictionary (8–10 measures) for your sales model as a Markdown table in your repository. This becomes a key part of the Phase 1 milestone project.
