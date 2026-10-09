---
title: "AI-Assisted Analytics: Faster Formulas, DAX and SQL — Checked by You"
order: 1
summary: "Use AI assistants to draft Excel formulas, DAX and SQL, give them the right context, and validate every answer before it reaches a report."
level: Beginner
time: "40 min"
topics: ["AI for formulas", "AI for DAX & SQL", "Human validation"]
prerequisites: ["phase-1/excel-analysis/02-sumifs-countifs", "phase-1/power-pivot-dax/02-measures-kpi"]
keywords: [ai, copilot, chatgpt, claude, llm, prompt, formula, dax, sql, validation, reconcile, test cases, data privacy, hallucination, review, check totals]
reviewed: 2026-10-09
resources:
  - title: "Copilot for Power BI overview"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction"
    source: "Microsoft Learn"
    note: "What AI can do inside Power BI."
  - title: "Optimize your semantic model for Copilot"
    url: "https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-evaluate-data"
    source: "Microsoft Learn"
    note: "How model design affects AI answers."
  - title: "SUMIFS function"
    url: "https://support.microsoft.com/en-us/excel/functions/sumifs-function"
    source: "Microsoft Support"
    note: "Check AI-written formulas against the official syntax."
files: [known_answers.csv, orders.xlsx, sales_model.xlsx]
---

## What is it?

AI assistants (built-in tools like Copilot, or general chat assistants) can **draft** formulas, DAX measures and SQL queries in seconds, and **explain** code you don't understand. They work like a fast junior colleague: helpful, but sometimes confidently wrong.

**AI-assisted analytics** means using AI for speed while **you** stay responsible for correctness. The key skill is **validation**.

!!! job "Why it matters at work"
    AI fluency now appears in most data job postings. Employers don't want people who paste AI output into reports. They want people who can **prompt with context, review critically and prove the result is right**. That combination is faster than working alone and safer than trusting AI.

## Part 1: prompt with context

A vague prompt gets a generic answer. Give the AI the **data structure**, the **business rule** and the **output format**:

| Weak prompt | Strong prompt |
|---|---|
| "Formula for Dhaka revenue" | "Excel sheet *Orders*, rows 2–13. Column D = region, I = status, J = value. Write a formula for total value where region is Dhaka and status is **not** Cancelled. Use SUMIFS and absolute references." |
| "DAX for achievement" | "Power BI model: measures `[Net Revenue]` (excludes Cancelled) and `[Target]` (from Targets table, by region and month). Write an Achievement % measure that's safe when Target is blank." |
| "SQL for customers without orders" | "Tables `customers(customer_name, …)` and `orders(customer, status, …)`. List customers with no orders at all. SQLite. Avoid NOT IN." |

Also tell it what to **avoid** (e.g. "no VLOOKUP", "no volatile functions") and which **version** you use ("Excel 2019", "PostgreSQL").

## Part 2: validate — three real examples

Each example below shows a plausible AI answer that **looks right** and is wrong. The checks come from numbers you already know.

**1. Excel: the missing condition.** Asked for "Dhaka revenue", an assistant might return:

```excel
=SUMIF(D2:D13,"Dhaka",J2:J13)
```

It gives **3,410**. Your known value is **3,170**. The 240 difference is the cancelled order 4: the formula forgot the business rule. Fix:

```excel
=SUMIFS($J$2:$J$13,$D$2:$D$13,"Dhaka",$I$2:$I$13,"<>Cancelled")
```

**2. DAX: the inverted ratio.** A drafted measure:

```dax
Achievement % = DIVIDE ( SUM ( Targets[target] ), SUM ( Orders[value] ) )
```

It returns **103.1%** (9,600 ÷ 9,315), which suggests "we beat target". The correct value is **94.5%** (9,075 ÷ 9,600). There are two errors: the ratio is upside down, and it uses gross revenue instead of Net Revenue. Fix: `DIVIDE ( [Net Revenue], [Target] )`. Always reuse the agreed measures.

**3. SQL: the LEFT JOIN + COUNT(\*) trap.** Asked for "orders per customer, including customers with none":

```sql
SELECT c.customer_name, COUNT(*) AS orders
FROM customers c LEFT JOIN orders o ON o.customer = c.customer_name
GROUP BY c.customer_name;
```

Blue Thread Ltd shows **1** order, but it has **none**. The fix is `COUNT(o.order_id)`, as in the JOINs lesson.

## Part 3: the validation checklist

Before any AI-written formula, measure or query goes into a report:

1. **Read it.** Can you explain every part? If not, ask the AI to explain, or don't use it.
2. **Reconcile with a known total.** Net Revenue 9,075, Orders 12, etc. Keep a small "known answers" table for your data.
3. **Test edge cases.** Blanks, zero targets, cancelled orders, a customer with no orders, a new month.
4. **Check the business rule.** Does it follow the KPI dictionary definition (e.g. excludes Cancelled)?
5. **Check the version.** Does the function exist in your tool (e.g. XLOOKUP isn't in Excel 2019)?
6. **Get a second look** for anything that goes to senior management.

## Part 4: privacy and responsible use

| Do | Don't |
|---|---|
| Use your organisation's **approved** AI tools | Paste customer names, salaries or confidential data into public tools |
| Share **structure** (column names, sample fake rows) | Share real exports when structure is enough |
| Say in reports or READMEs when AI helped | Present AI output as verified when it wasn't checked |
| Keep your own judgement on conclusions | Let AI decide what the business should do |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| No context in the prompt | Generic answers that miss business rules | Give structure + rule + format |
| Accepting the first answer | Hidden errors (like the 3,410 above) | Reconcile with known totals |
| Asking AI to "fix" without understanding | Errors become harder to see | Ask it to **explain**, then decide |
| Pasting real customer data into public tools | A privacy or policy breach | Approved tools, fake sample data |
| AI writes a new measure instead of reusing one | Two definitions of the same KPI | Tell it which existing measures to use |

## Try it yourself

**Task:** An AI assistant suggests this measure for "average order value":

```dax
AOV = AVERAGE ( Orders[value] )
```

Is it correct for our business definition? What value does it return, and what should it be?

<details markdown="1">
<summary>Show a hint</summary>

Check the KPI definition: Net Revenue ÷ Net Orders, excluding Cancelled. `AVERAGE` looks at every row.
</details>

<details markdown="1">
<summary>Show the solution</summary>

It returns **776.25** (9,315 ÷ 12), because it includes the cancelled order. The agreed AOV is **825** (9,075 ÷ 11):

```dax
Avg Order Value = DIVIDE ( [Net Revenue], [Net Orders] )
```

You've seen 776.25 before: it's the same trap as Excel's built-in "Above Average" rule in the conditional-formatting lesson.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What is the most reliable first check of an AI-written revenue formula?

1. It runs without an error
2. It matches a known, agreed total
3. The AI says it's correct

<details markdown="1"><summary>Show answer</summary>
**B.** Running without errors doesn't mean the result is right. Reconcile with a known number.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which prompt is most likely to get a correct DAX measure?

1. "Write a DAX achievement measure"
2. "Using existing measures [Net Revenue] and [Target], write Achievement % that returns blank if Target is blank"
3. "Make my dashboard better"

<details markdown="1"><summary>Show answer</summary>
**B.** It gives context, reuses agreed measures and states the edge case.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. You want AI help with a query on customer data. What should you share with a public AI tool?

1. The full customer export
2. Table and column names, with a few made-up rows
3. Passwords to the database

<details markdown="1"><summary>Show answer</summary>
**B.** Share the structure, not confidential data. Use approved tools for real data.
</details>
</div>

## Summary

- AI drafts formulas, DAX and SQL fast. **You** own correctness.
- Prompt with **structure + business rule + format + version**, and ask it to reuse existing measures.
- Validate: read it, **reconcile with known totals**, test edge cases, check the rule and the version.
- Protect data: approved tools, structure instead of real records, and say when AI helped.

!!! job "Job-ready check"
    **Interview question:** *"How do you use AI tools in your analytics work?"*

    **Strong answer:** "To draft and explain formulas, DAX and SQL faster, always with context such as table structure and business rules. I never ship AI output unchecked: I reconcile it with known totals, test edge cases like cancelled orders and blank targets, and make sure it reuses our agreed KPI measures. I only share structure, not confidential data, with approved tools."

    **Mini project:** Create a **known answers** sheet for your project data (10 key numbers). Then ask an AI assistant for three formulas or measures, test each against the sheet, and document what was right or wrong in your README.
