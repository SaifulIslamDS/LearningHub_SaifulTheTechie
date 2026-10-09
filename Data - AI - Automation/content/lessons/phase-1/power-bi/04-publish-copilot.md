---
title: "Publish & Share in the Power BI Service, and Use Copilot Wisely"
order: 4
summary: "Publish to a workspace, understand licences and refresh, share safely — and know what Copilot in Power BI needs and how to check its answers."
level: Intermediate
time: "45 min"
topics: ["Service publishing", "Copilot in Power BI"]
prerequisites: ["phase-1/power-bi/03-row-level-security"]
keywords: [publish, power bi service, workspace, my workspace, app, share, license, pro, premium per user, fabric capacity, f64, scheduled refresh, gateway, onedrive, copilot, prep data for ai, verified answers]
reviewed: 2026-10-09
resources:
  - title: "Power BI service features by license type"
    url: "https://learn.microsoft.com/en-us/power-bi/fundamentals/service-features-license-type"
    source: "Microsoft Learn"
    note: "What Free, Pro and PPU users can do."
  - title: "Refresh a Power BI Desktop file from OneDrive or SharePoint Online"
    url: "https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-desktop-file-onedrive"
    source: "Microsoft Learn"
    note: "Keeping published reports up to date without a gateway."
  - title: "Copilot for Power BI overview"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction"
    source: "Microsoft Learn"
    note: "What Copilot can do in reports and models."
  - title: "Enable Fabric Copilot for Power BI"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi"
    source: "Microsoft Learn"
    note: "Capacity, region and tenant requirements."
files: [sales_model.xlsx, known_answers.csv]
---

## What is it?

- **Publishing** sends your `.pbix` file from Power BI Desktop to the **Power BI service** (app.powerbi.com). There it becomes a **report** plus a **semantic model** inside a **workspace**, ready to share, secure and refresh.
- **Copilot in Power BI** is an AI assistant that can draft report pages, summarise reports and answer questions about your data, built on your semantic model.

!!! job "Why it matters at work"
    A report on your laptop helps no one. Knowing how publishing, licences, refresh and sharing work is what lets you deliver BI to a team. And as companies roll out Copilot, analysts are expected to prepare models for AI **and** to check AI answers. That's a new, valuable skill.

## Part 1: publish

1. In Power BI Desktop, **save** the file, then **Home → Publish**.
2. Sign in with a **work or school account**, and choose a workspace: **My workspace** (personal) or a shared team workspace.
3. Open the link to the report in the service.

In the workspace you'll see two items: the **report** (pages and visuals) and the **semantic model** (tables, relationships, measures, RLS roles).

## Part 2: licences — who can share with whom

| Licence | What you can do |
|---|---|
| **Free** | Create content for your own use. You can view others' content only if it's in a Premium or Fabric **F64+** capacity workspace |
| **Pro** | Publish to shared workspaces, and share with or collaborate with other Pro users |
| **Premium Per User (PPU)** | Pro features plus most Premium features. On its own, it shares only with other PPU users |
| **Premium / Fabric F64+ capacity** (organisation) | Pro or PPU authors can distribute content to Free users |

For a portfolio, publish to **My workspace** and share **screenshots or a video**. For a team, your organisation decides the licensing.

!!! warning "Publish to web is public"
    **File → Embed report → Publish to web** creates a link **anyone on the internet** can open, with no sign-in. Never use it with company or customer data. Many organisations switch it off.

## Part 3: share safely and keep data fresh

**Share with consumers** by giving them the workspace **Viewer** role, or better, by publishing an **app** (Workspace → **Create app**). Viewers and app users are restricted by RLS. Members are not.

**Keep data fresh:**

- **Cloud sources** (SharePoint, OneDrive, cloud databases): set up **scheduled refresh** on the semantic model's settings page.
- **Files on your PC or company network**: the service can't see them. Either store the file in **OneDrive / SharePoint** and connect to it there, or install an **on-premises data gateway**.

## Part 4: Copilot in Power BI — what it needs

Copilot isn't available everywhere. According to Microsoft's documentation (checked October 2026):

- The workspace must be on a **paid Fabric capacity (F2 or higher)** or **Power BI Premium (P1 or higher)**, or use a Fabric Copilot capacity. **Trial capacities aren't supported.**
- Your admin must allow Copilot in the **tenant settings**, and the capacity must be in a supported region.
- To use Copilot **in Desktop**, you need Admin, Member or Contributor access to at least one such workspace.

If you're learning on a personal setup, you probably won't have Copilot. That's fine: the skills below still apply to any AI assistant.

## Part 5: make Copilot answers better and safer

Copilot reads your **semantic model**: names, measures, relationships and descriptions. Good modelling equals better AI answers. Power BI also has **Prep data for AI** (a preview feature, on the Home ribbon) with three tools:

| Tool | Use it to… |
|---|---|
| **AI data schema** | choose which tables, columns and measures Copilot should focus on |
| **Verified answers** | link common questions to a visual you've checked |
| **AI instructions** | explain business rules, e.g. *"Revenue means Net Revenue: all orders except Cancelled"* |

Microsoft notes that these tools **can't guarantee** a specific answer, because AI output isn't fully predictable.

**Check every Copilot answer against your measures.** For example:

| You ask | Correct answer (from your measures) | What to watch for |
|---|---|---|
| "What was revenue in Q1?" | **9,075** (Net Revenue) | An AI that sums `Orders[value]` gives **9,315**, which includes the cancelled order |
| "Which region is furthest below target?" | **Dhaka (−430)** | The *percentage* view would say Narayanganj (82.0%), so be clear whether you mean amount or % |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Publishing a file connected to `C:\` | Scheduled refresh fails | OneDrive/SharePoint source, or a gateway |
| Making consumers workspace Members | They can edit, and bypass RLS | Viewer role, or an app |
| Using Publish to web with business data | A public data leak | Never. Share inside the organisation |
| Trusting a Copilot number without checking | Wrong figures in management decks | Compare with a verified measure, and add AI instructions |
| Ambiguous measure names (`Revenue` vs `Net Revenue`) | Copilot and humans pick the wrong one | Clear names, descriptions, hide raw columns |

## Try it yourself

**Task:** Write the **AI instructions** you would give Copilot for this model. Write three or four short rules that would stop the most likely wrong answers.

<details markdown="1">
<summary>Show a hint</summary>

Think about cancelled orders, which revenue measure is "official", the grain of the targets, and what "below target" means.
</details>

<details markdown="1">
<summary>Show a model answer</summary>

- "Revenue" always means the **Net Revenue** measure (all orders except status Cancelled).
- Targets exist only by **region and month**. Don't compare targets by product, category or customer.
- "Below target" means **Achievement %** below 100%. Show both the gap amount and the %.
- Months are calendar months of 2026. March data may be incomplete. Mention this when discussing March.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which workspace role should report consumers usually get, so RLS applies?

1. Member
2. Contributor
3. Viewer

<details markdown="1"><summary>Show answer</summary>
**C — Viewer** (or access through an app).
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Your published report uses a CSV on your laptop. How can scheduled refresh work?

1. It works automatically
2. Move the file to OneDrive/SharePoint, or use an on-premises data gateway
3. Use Publish to web

<details markdown="1"><summary>Show answer</summary>
**B.** The cloud service can't reach your local files without a gateway.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Copilot says Q1 revenue was 9,315. Your Net Revenue measure says 9,075. What's the most likely reason?

1. Copilot included the cancelled order
2. The measure is wrong
3. Rounding

<details markdown="1"><summary>Show answer</summary>
**A.** 9,315 − 9,075 = 240, which is exactly the cancelled order. Add an AI instruction and check names and descriptions.
</details>
</div>

## Summary

- **Publish** from Desktop to a workspace: you get a report plus a semantic model.
- **Licences:** Pro (or PPU) to share. Free users can view only content in Premium or F64+ capacity.
- Share with **Viewer** access or **apps**. Refresh needs cloud sources or a **gateway**. Never use Publish to web for business data.
- **Copilot** needs paid F2+/P1+ capacity (not trials) and admin enablement. Prepare the model (Prep data for AI) and **verify every answer**.

!!! job "Job-ready check"
    **Interview question:** *"Your company is enabling Copilot in Power BI. What would you do to the models first?"*

    **Strong answer:** "Make the semantic model AI-ready: a clean star schema, clear measure names with descriptions, technical columns hidden, and Prep data for AI to set the schema, verified answers for common questions, and instructions such as 'revenue means net revenue'. Then test typical questions against known measure values before rolling it out, and keep reminding users to check AI answers."

    **Mini project:** Publish your report to My workspace (if you have access), or document the publishing plan: workspace, roles, refresh method and app audience. Add your Copilot AI-instruction rules to the README.
