---
title: "Research Questions & Experiment Design: Ask Something You Can Answer"
order: 1
summary: "Turn a business worry into a precise research question and hypothesis, choose the unit of randomisation, and use a power analysis to pick a design that can actually deliver an answer — or to say early that it can't."
level: Intermediate
time: "45 min"
topics: ["Research question", "Experiment design"]
prerequisites: ["phase-2/ab-testing/02-sample-size-causal-pitfalls"]
keywords: [research question, hypothesis, experiment design, study design, unit of randomisation, randomisation, eligibility, primary metric, guardrail metric, power analysis, feasibility, observational study, randomised controlled trial, quasi-experiment, pre-registration, experiment plan]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, phase-2/customers_2025.csv, templates/experiment_plan_template.md]
resources:
  - title: "Trustworthy Online Controlled Experiments — resources"
    url: "https://experimentguide.com/"
    source: "Kohavi, Tang & Xu (book site)"
    note: "Designing experiments: metrics, randomisation units and pitfalls."
  - title: "Causal Inference for the Brave and True (free online book)"
    url: "https://matheusfacure.github.io/python-causality-handbook/landing-page.html"
    source: "Matheus Facure"
    note: "Randomised experiments and what to do when you can't randomise."
  - title: "OpenIntro Statistics (free textbook)"
    url: "https://www.openintro.org/book/os/"
    source: "OpenIntro"
    note: "Chapter 1: observational studies vs experiments, sampling and design."
---

## What is it?

- A **research question** is a precise, answerable question tied to a decision: *who*, *what change*, *which outcome*, *how much*, *by when*.
- **Experiment design** is the plan for answering it: what's compared, how units are assigned, what's measured, how much data is needed, and how it will be analysed.

| Vague worry | Research question |
|---|---|
| "Credit customers cancel too much." | For orders from customers on 30+ day credit, does a pre-dispatch confirmation call reduce the cancellation rate by at least 30% (relative) over the next quarter? |

!!! job "Why it matters at work"
    Teams waste months on analyses that can't answer the question they were meant to: too little data, the wrong unit, no comparison group. An analyst who spots this at the planning stage, and proposes a design that works, saves real money. Senior interviews often include "design a study to find out whether X works".

The script is `20_research_question_design.py`.

## Step 1: from worry to question

The EDA found that cancellations rise with credit terms:

```text
             rate  orders  customers
credit_days
0             3.3    1336         18
15            4.4     872         11
30            8.2    1353         24
60           14.1     640          7
```

The tempting conclusion, "shorten credit terms to cut cancellations", is a **causal** claim from **observational** data. Customers on 60-day terms may simply be different businesses. So the question needs a design that can isolate cause.

A good research question is:

| Criterion | Check |
|---|---|
| **Decision-linked** | We'll act differently depending on the answer |
| **Specific** | Population, intervention, outcome and time frame are named |
| **Measurable** | The outcome has an exact definition in the data |
| **Feasible** | Enough units and time to detect the effect that matters |
| **Comparative** | There's a comparison (control) that answers "compared with what?" |

Then write a **hypothesis** with a direction and a size: *"A confirmation call before dispatch will reduce cancellations from about 10% to 7%, because it catches orders customers have already changed their minds about."*

## Step 2: choose the unit of randomisation

**Design A: randomise credit terms by customer.** Credit terms are part of each customer's contract, so the unit has to be the customer.

```text
customers per credit band: {0: 19, 15: 12, 30: 25, 60: 7}
customers on 60-day credit who ordered in 2025: 7
their cancellation rates range from 10.7% to 26.3%
```

Only **7 customers** on 60-day terms, and they differ a lot from each other (10.7% to 26.3%). Randomising 3 vs 4 customers can't separate the effect of credit terms from differences between those few businesses, however many orders they place. **Design A is not feasible.** It's far better to discover that now than after a quarter of waiting.

**Design B: randomise a confirmation call per order.** The intervention happens per order, so each eligible order can be randomly assigned "call" or "no call". Many more units, and the same customer appears in both groups, which balances customer differences.

| | Design A (credit terms) | Design B (confirmation call) |
|---|---|---|
| Unit | Customer | Order |
| Units available | 7 (60-day) to 32 (30+ day) | About 166 eligible orders a month |
| Main risk | Too few units; customers differ | Contamination (same customer, both arms); staff compliance |
| Answers | "Do shorter terms reduce cancellations?" | "Does a call reduce cancellations?" (a different, but actionable, question) |

## Step 3: size it before you commit

```python
eligible = df[df["credit_days"] >= 30]
base = eligible["cancelled"].mean()
target = base * 0.70                                   # the call is worth it if it cuts cancellations by 30%
h = proportion_effectsize(base, target)
n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.80)
```

```text
eligible orders: 1993 in 2025 (166/month), baseline cancellation 10.1%
detect 10.1% -> 7.1%: 1335 orders per arm, about 17 months of eligible orders
```

Even Design B needs about **17 months** to detect a 30% reduction. Options to make it feasible, each a trade-off to agree with the business:

```text
cut 40%, 30+ day credit                baseline 10.1%: 705 per arm, ~9 months
cut 30%, all credit customers (15+)    baseline 8.3%: 1639 per arm, ~14 months
```

- **Aim for a larger effect** (40%): about 9 months, but you'll miss a smaller real effect.
- **Widen eligibility** to all credit customers: more orders, but a lower baseline, so the gain is small.
- Other levers: run it across a full year of seasonality anyway; accept 70% power; use a more sensitive metric.

There's no free lunch. The right answer is a **conversation**: "with our volume, this experiment answers 'does the call cut cancellations by 40% or more?' in about 9 months. Is that useful?"

## Step 4: write the plan down

Use `experiment_plan_template.md`. The key fields:

| Field | Design B |
|---|---|
| Decision | Roll out confirmation calls to all credit orders, or not |
| Population | Orders from customers on 30+ day credit, from 1 January |
| Unit | Order (random 50/50 by order ID) |
| Primary metric | Cancellation within 14 days of order |
| Guardrails | Delivery time; sales-team hours; customer complaints |
| MDE / power | −40% relative, 80% power, α = 0.05 → 705 orders per arm |
| Duration | About 9 months; no early stopping |
| Analysis | Two-proportion test with 95% CI; segments (30 vs 60 days) pre-specified |

Writing this **before** the data arrives (sometimes called *pre-registration*) protects against choosing the metric, segment or end date that happens to look good.

## When you can't randomise

| Situation | Option | Main caveat |
|---|---|---|
| Change rolls out to everyone at once | **Before/after with a comparison group** (difference-in-differences) | Groups must have followed similar trends before |
| Rollout region by region | **Staggered rollout** | Other changes may coincide |
| Only historical data | Compare within groups, adjust for confounders | Never as strong as randomisation; state it |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Starting with data, not a decision | Interesting results nobody uses | Write the decision first |
| Causal language from observational data | Wrong interventions | Design for cause, or say "associated with" |
| Ignoring the unit of randomisation | Hundreds of "orders" but only 7 real units | Count the units you randomise, not the rows |
| No power analysis | Months of inconclusive results | Size before starting; adjust the design or the goal |
| Changing the plan mid-way silently | Untrustworthy results | Document every change with a reason |

## Try it yourself

**Task:** The operations director wants **90% power** for Design B (30% reduction, 30+ day credit customers). How many orders per arm, and how long would it take?

<details markdown="1">
<summary>Show the solution</summary>

```python
n90 = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.90)
print(f"90% power: {np.ceil(n90):.0f} per arm, ~{np.ceil(2 * n90 / per_month):.0f} months")
```

```text
90% power: 1786 per arm, ~22 months
```

Almost two years: not realistic for a process change. A sensible recommendation is the 40% / 80% design (about 9 months), stated clearly as "able to detect a large effect only".
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Credit terms are set per customer, and only 7 customers have 60-day terms. What's the problem with randomising credit terms?

1. None: they place 640 orders
2. The unit of randomisation is the customer, so there are only 7 units
3. Credit terms can't be measured

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which makes a research question feasible?

1. Using as many metrics as possible
2. Enough units and time to detect the smallest effect worth acting on
3. A large dataset of any kind

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why write the experiment plan before collecting data?

1. It's required by law
2. It prevents choosing metrics, segments or stopping points after seeing the results
3. It makes the experiment faster

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- Start from the **decision**; write a specific, measurable, comparative **research question** and a directional **hypothesis**.
- Choose the **unit of randomisation** from where the intervention happens, and count the units, not the rows.
- Run a **power analysis** before committing; trade off effect size, eligibility and duration with the business.
- Write the plan down first; when you can't randomise, use the strongest available design and state its limits.

!!! job "Job-ready check"
    **Interview question:** *"Design a study to find out whether shorter credit terms reduce cancellations."*

    **Strong answer:** "Credit terms are set per customer, so customers are the unit, and we only have a handful on long terms, which is too few for a fair randomised test. I'd say so up front, and propose either a staggered change of terms with a comparison group, or a related, testable intervention such as a confirmation call randomised per order, sized with a power analysis. I'd agree the primary metric, guardrails and duration in a written plan before starting."

    **Mini project:** Fill in `experiment_plan_template.md` for one decision you'd like to test (in this dataset or at work), including the power calculation.
