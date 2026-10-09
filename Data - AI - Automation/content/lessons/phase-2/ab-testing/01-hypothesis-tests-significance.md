---
title: "A/B Testing Part 1: Hypothesis Tests and Significance"
order: 1
summary: "Analyse a real-shaped A/B test end to end: check the split, test conversion with a two-proportion z-test and confidence interval, check guardrail metrics, and explain p-values and significance in plain business language."
level: Intermediate
time: "55 min"
topics: ["Hypothesis tests", "Significance"]
prerequisites: ["phase-2/statistics/02-correlation-confidence-intervals"]
keywords: [a/b test, ab test, experiment, hypothesis test, null hypothesis, alternative hypothesis, p-value, significance, statistical significance, practical significance, two-proportion z-test, chi-square test, welch t-test, mann-whitney, conversion rate, lift, sample ratio mismatch, srm, guardrail metric, statsmodels]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/ab_test_checkout.csv]
resources:
  - title: "proportions_ztest (statsmodels)"
    url: "https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html"
    source: "statsmodels official docs"
    note: "The two-proportion test used in this lesson."
  - title: "OpenIntro Statistics (free textbook)"
    url: "https://www.openintro.org/book/os/"
    source: "OpenIntro"
    note: "Chapter 5–6: hypothesis testing and inference for proportions."
  - title: "Trustworthy Online Controlled Experiments — resources"
    url: "https://experimentguide.com/"
    source: "Kohavi, Tang & Xu (book site)"
    note: "The standard practitioner book on A/B testing; the site has free chapters and slides."
---

## What is it?

A **hypothesis test** asks: *if there were really no difference, how surprising would our result be?*

| Term | Meaning in this test |
|---|---|
| **Null hypothesis (H₀)** | The new checkout (B) converts the same as the old one (A) |
| **Alternative (H₁)** | B converts differently from A |
| **p-value** | If H₀ were true, the probability of seeing a difference at least this large by chance |
| **Significance level (α)** | The threshold we chose in advance, usually 0.05 |
| **Statistically significant** | p < α: the result is unlikely to be chance alone |
| **Practically significant** | The difference is big enough to matter for the business |

!!! job "Why it matters at work"
    Product, growth and analytics teams decide what to launch with A/B tests. Analysts who can run the test correctly, and explain "significant" without misleading anyone, are trusted with these decisions. Expect an A/B case question in most product data science interviews.

The script is `13_ab_hypothesis_tests.py`.

## Step 0: decide before you look

Before the data comes in, the team wrote down:

- **Primary metric:** conversion rate (sessions that place an order).
- **Guardrail metrics:** order value among buyers; revenue per session. They must not get worse.
- **α = 0.05**, two-sided test, run for **4 full weeks**, analysed **once** at the end.

Writing this first stops you from choosing the metric or the end date that happens to look good (see Part 2).

## Step 1: health check — is the split intact?

```python
counts = ab["variant"].value_counts().sort_index()
srm = stats.binomtest(int(counts["A"]), int(counts.sum()), 0.5)
print(counts.to_dict(), f"| SRM p-value = {srm.pvalue:.3f}")
```

```text
{'A': 5489, 'B': 5347} | SRM p-value = 0.176
```

A **sample ratio mismatch (SRM)** means the split isn't what was designed, often a bug (e.g. B crashes on some browsers, so those users vanish). 5,489 vs 5,347 is within normal random variation for a 50/50 split (p = 0.18). If this p-value were tiny (say < 0.001), you'd **stop and fix the experiment**, not analyse it.

## Step 2: the primary metric

```python
summary = ab.groupby("variant").agg(sessions=("converted", "size"), orders=("converted", "sum"),
                                    conversion=("converted", "mean"))
summary["conversion"] = (summary["conversion"] * 100).round(2)
print(summary)
```

```text
         sessions  orders  conversion
variant
A            5489     368        6.70
B            5347     423        7.91
```

B converts at 7.91% vs 6.70%. Is that more than chance?

## Step 3: the two-proportion z-test, with a confidence interval

```python
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest

orders_ = summary["orders"].to_numpy()[::-1]          # [B, A]
sessions = summary["sessions"].to_numpy()[::-1]
z, p = proportions_ztest(orders_, sessions)
low, high = confint_proportions_2indep(orders_[0], sessions[0], orders_[1], sessions[1], compare="diff")
diff = orders_[0] / sessions[0] - orders_[1] / sessions[1]
print(f"difference B - A = {diff * 100:.2f} percentage points, 95% CI {low * 100:.2f} to {high * 100:.2f}")
print(f"z = {z:.2f}, p-value = {p:.4f}")
print(f"relative lift = {diff / (orders_[1] / sessions[1]):.1%}")
```

```text
difference B - A = 1.21 percentage points, 95% CI 0.23 to 2.19
z = 2.41, p-value = 0.0158
relative lift = 18.0%
```

How to read it:

- **p = 0.016 < 0.05**: if B were truly no better, a gap this large would happen only about 1.6% of the time. **Statistically significant.**
- The **CI (0.23 to 2.19 points)** excludes 0, which tells the same story, and also shows the **size**: the true lift could be as small as +0.2 points or as large as +2.2. Report the interval, not just "significant".
- **Percentage points vs percent:** +1.21 *points* (6.70% → 7.91%) is an **18% relative** lift. Say which one you mean.

The same test as a **chi-square test** on the 2×2 table gives an identical p-value (χ² = z²):

```text
chi-square = 5.83 (= z squared 5.83), p = 0.0158
```

## Step 4: guardrails — did anything get worse?

Order value among buyers is skewed, so use **Welch's t-test** (means, unequal variances) and check it with the **Mann-Whitney** test (ranks):

```text
mean order value A 754, B 711 | median A 606, B 603
Welch t-test p = 0.221 | Mann-Whitney p = 0.446
```

No evidence that buyers spend less with B: the medians are almost identical and both p-values are large. Now the metric the business really cares about:

```text
revenue per session A 50.53, B 56.27 (+11.4%), p = 0.195
```

Revenue per session is up 11.4%, but **not significant** (p = 0.20). Revenue per session is very noisy (most sessions are 0, a few are large orders), so this test can't confirm the revenue gain on its own. Honest summary: *conversion is clearly up; revenue is probably up, but the test can't confirm it.*

## Step 5: segments — consistent, or one group only?

```text
         mean        size
variant     A     B     A     B
device
desktop  7.49  9.73  2323  2272
mobile   6.13  6.57  3166  3075
```

The lift is large on **desktop** (+2.2 points) and small on **mobile** (+0.4). Treat this as a **hypothesis for the next test** (maybe the one-page form is long on small screens), not a conclusion: slicing results many ways will always find *some* difference by chance.

## Putting it together: the decision

> **Ship B.** Conversion rose from 6.70% to 7.91% (+1.21 points, 95% CI +0.23 to +2.19; p = 0.016). Order value per buyer was unchanged. Revenue per session rose 11% but this test is too small to confirm it, so we'll track it after launch. The lift is concentrated on desktop; we'll test a mobile-optimised layout next.

## p-value: what it is and isn't

| ✅ It is | ❌ It is not |
|---|---|
| How surprising the data would be if there were no effect | The probability that B is better |
| One input to a decision | Proof, or the size of the effect |
| Valid only for the test you planned | Valid after you've tried many metrics or stop dates |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Skipping the SRM check | Analysing a broken experiment | Check the split first |
| Reporting only "significant / not significant" | Hides the size and uncertainty | Difference + 95% CI + p |
| Confusing points and percent | "18% better" vs "1.2 points better" mix-ups | State both explicitly |
| Calling p = 0.20 "no effect" | Missing real but under-measured gains | "Not enough evidence", and say how much data would be needed |
| Celebrating the best segment | False discoveries | Pre-register segments, or treat them as new hypotheses |

## Try it yourself

**Task:** Run the conversion test for **new customers only** (`new_customer == 1`). What are the rates, z and p? What do you conclude?

<details markdown="1">
<summary>Show the solution</summary>

```python
new = ab[ab["new_customer"] == 1]
s_new = new.groupby("variant")["converted"].agg(["sum", "size"])
z_n, p_n = proportions_ztest(s_new["sum"].to_numpy()[::-1], s_new["size"].to_numpy()[::-1])
print(s_new.assign(rate=(s_new["sum"] / s_new["size"] * 100).round(2)))
print(f"new customers: z = {z_n:.2f}, p = {p_n:.3f}")
```

```text
         sum  size  rate
variant
A         91  1648  5.52
B        118  1673  7.05
new customers: z = 1.82, p = 0.069
```

B is ahead for new customers too (+1.5 points), but p = 0.069 > 0.05: with only about 3,300 new-customer sessions, the test can't confirm it. It's consistent with the overall result, not evidence against it. "Not significant" in a subgroup usually means **too little data**, not "no effect".
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. p = 0.016. Which statement is correct?

1. There's a 98.4% chance that B is better
2. If there were no real difference, a gap this large would occur about 1.6% of the time
3. B is 1.6% better than A

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. A test shows 5,489 vs 5,347 sessions for a 50/50 split. What does the SRM check tell you?

1. The difference is within normal random variation, so the split looks healthy
2. The test is invalid
3. B is better

<details markdown="1"><summary>Show answer</summary>
**A.** p = 0.18; a tiny p-value would signal a broken split.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Conversion went from 6.70% to 7.91%. How do you describe the change?

1. +1.21 percentage points, an 18% relative lift
2. +18 percentage points
3. +1.21%, an 18-point lift

<details markdown="1"><summary>Show answer</summary>
**A.**
</details>
</div>

## Summary

- Decide metrics, α and duration **before** the test; check the **split (SRM)** first.
- Conversion: **two-proportion z-test** (= chi-square on a 2×2 table); report the **difference with a 95% CI** and the p-value.
- Check **guardrails** (Welch t-test, Mann-Whitney for skewed values) and the business metric.
- "Significant" = unlikely to be chance; whether it *matters* depends on the size of the effect.

!!! job "Job-ready check"
    **Interview question:** *"Your A/B test gives p = 0.03 for conversion. Do you launch?"*

    **Strong answer:** "First I'd check the experiment is healthy (sample ratio, tracking, full weeks), and that this was the pre-registered primary metric analysed at the planned end. Then I'd look at the size: the difference and its confidence interval, against the cost of the change. And I'd check guardrails like order value and errors. If those hold, yes, and I'd keep monitoring after launch."

    **Mini project:** Write a one-page experiment report for the checkout test: hypothesis, design, health check, results table with CIs, guardrails, decision and next test.
