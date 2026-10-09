---
title: "Reproducibility, Evaluation & Reporting: Results Others Can Trust"
order: 2
summary: "Make an analysis reproducible (environment, data fingerprints, seeds, one-command runs), evaluate results against a baseline with honest uncertainty, and write a report a decision-maker can act on."
level: Intermediate
time: "45 min"
topics: ["Reproducibility", "Evaluation & reporting"]
prerequisites: ["phase-2/research-thinking/01-research-question-design", "phase-2/ml-foundations/01-sklearn-train-test-split"]
keywords: [reproducibility, reproducible analysis, random seed, environment, uv.lock, data versioning, sha-256, hash, provenance, notebook vs script, evaluation, baseline, bootstrap confidence interval, sensitivity analysis, robustness, reporting, analysis report, limitations, threats to validity]
reviewed: 2026-10-09
files: [phase-2/data-science-scripts.zip, phase-2/orders_2025.csv, templates/analysis_report_template.md]
resources:
  - title: "The Turing Way: Guide for Reproducible Research"
    url: "https://book.the-turing-way.org/reproducible-research/reproducible-research"
    source: "The Turing Way (open community handbook)"
    note: "Version control, environments, data and code sharing, step by step."
  - title: "Working on projects (uv)"
    url: "https://docs.astral.sh/uv/guides/projects/"
    source: "Astral (official)"
    note: "Lock files and reproducible environments."
  - title: "Controlling randomness (scikit-learn)"
    url: "https://scikit-learn.org/stable/common_pitfalls.html#controlling-randomness"
    source: "scikit-learn official docs"
    note: "How random_state works and how to use it correctly."
---

## What is it?

| Idea | Question it answers |
|---|---|
| **Reproducibility** | Can someone else (or you in six months) get exactly the same numbers from the same data and code? |
| **Evaluation** | Is the result better than a sensible baseline, by how much, and how certain are we? |
| **Reporting** | Does the reader get the answer, its uncertainty, its limits and what to do, in that order? |

!!! job "Why it matters at work"
    "I can't get your numbers" is how analyses lose credibility. Reproducible work survives audits, handovers and reviews, and it's increasingly expected for models that affect money or people. Interviewers for data roles often ask how you'd make a project reproducible, and portfolio reviewers notice when a repo "just runs".

The script is `21_reproducibility_reporting.py`.

## Part 1: the four ingredients of reproducibility

### 1. Record the environment

```python
env = {"python": platform.python_version(), **{p: version(p) for p in ["numpy", "pandas", "scikit-learn"]}}
```

```text
environment: {'python': '3.13.16', 'numpy': '2.5.3', 'pandas': '3.0.6', 'scikit-learn': '1.9.1'}
```

*(Your versions will differ.)* In a project, the **`uv.lock`** file (Phase 0) does this properly: anyone can recreate the exact environment with `uv sync`.

### 2. Fingerprint the data

```python
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]
```

```text
data fingerprints: {'customers_2025.csv': '87f5066eee5b', 'orders_2025.csv': '706b3e132a43', 'products_2025.csv': 'd22bd2e1fdff'}
```

A **hash** changes if even one character of the file changes. Store it with your results: if someone gets different numbers, the first check is "same data hash?". Your hashes should match these exactly, since the practice files are generated deterministically.

### 3. Control randomness with seeds

Put the whole analysis in **one function** whose randomness depends only on a seed:

```python
r1, r2, r3 = analysis(SEED), analysis(SEED), analysis(SEED + 1)
print("run 1 == run 2:", r1 == r2)
print("seed 2025 CI:", r1["auc_ci95"], "| seed 2026 CI:", r3["auc_ci95"])
```

```text
run 1 == run 2: True
seed 2025 CI: [0.573, 0.702] | seed 2026 CI: [0.569, 0.707]
```

- Same seed → **identical** results.
- A different seed changes the bootstrap interval only slightly. If a conclusion changes with the seed, it wasn't a robust conclusion.

### 4. One command from data to results, with provenance

```python
report = {"results": r1, "data_sha256": data_files, "environment": env, "script": Path(__file__).name}
(RESULTS / "cancellation_model.json").write_text(json.dumps(report, indent=2))
```

Results are saved **with** the data fingerprints, versions and script that produced them. A reviewer can rerun `uv run 21_reproducibility_reporting.py` and compare.

| Habit | Why |
|---|---|
| Scripts (or notebooks run top-to-bottom) | Hidden notebook state (cells run out of order) is the #1 cause of irreproducible results |
| Raw data never edited by hand | Every change is in code, so it can be re-run and reviewed |
| Git for code, hashes or versions for data | You know exactly which code and data made which result |
| Relative paths and a config | Works on any machine |
| A README "how to reproduce" section | Others can rerun without asking you |

## Part 2: evaluate against a baseline, with uncertainty

```json
{
  "question": "Can order-time data rank orders by cancellation risk (Oct-Dec 2025)?",
  "n_train": 2899,
  "n_test": 1302,
  "test_cancel_rate": 0.0568,
  "baseline_auc": 0.5,
  "model_auc": 0.639,
  "auc_ci95": [0.573, 0.702],
  "seed": 2025
}
```

How to evaluate this honestly:

- **Against a baseline:** random ranking is 0.5. The model's 0.639 is better, and the whole 95% CI (0.573–0.702) is above 0.5, so the improvement is real.
- **With uncertainty:** the interval is wide (±0.065) because the test period has only about 74 cancellations (5.7% of 1,302). Don't promise "0.64": promise "clearly better than random, modest".
- **Time-honest:** trained on January–September, tested on October–December.

### Sensitivity: does the conclusion depend on a choice you made?

```python
for cut in ["2025-09-01", "2025-10-01", "2025-11-01"]:
```

```text
2025-09-01 1767 0.664
2025-10-01 1302 0.639
2025-11-01 804 0.701
```

With different split dates, the AUC moves between 0.64 and 0.70, always clearly above 0.5. **The conclusion ("modest, real signal") is robust; the exact number is not.** Report it that way.

## Part 3: write the report

Use `analysis_report_template.md`. The order matters: **answer first**, details later.

> **Order details can flag cancellation risk, but only modestly.**
>
> **Bottom line:** A simple model using segment, channel and credit terms ranks October–December orders by cancellation risk better than chance (ROC AUC 0.64, 95% CI 0.57–0.70; 0.64–0.70 across split dates). Flagging the riskiest 10% of orders would roughly double the cancellation rate among checked orders compared with random checks. We recommend a light-touch credit check on flagged orders, and adding payment-history data before investing in a more complex model.
>
> **Limitations:** one year of data; few cancellations in the test period (≈74); the model shows association, not cause (see the experiment plan for the confirmation-call test).
>
> **Reproduce:** `uv sync && uv run 21_reproducibility_reporting.py` · data `orders_2025.csv` SHA-256 `706b3e132a43…`

| Report element | Why |
|---|---|
| Title = the finding | Many readers stop at the title |
| Estimate + interval + baseline | Size and certainty, not just "significant" |
| Robustness check | Shows the conclusion doesn't hinge on one choice |
| Limitations | Builds trust; prevents over-use |
| Recommendation + next step | Turns analysis into action |
| How to reproduce | Lets anyone verify |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Notebook cells run out of order | Results nobody (including you) can recreate | Restart and run all before sharing; or scripts |
| No seed, or a different seed every run | Numbers change on every run | Fix seeds; report sensitivity to them |
| Data edited by hand in Excel | Changes are invisible and unrepeatable | All changes in code |
| A metric with no baseline or interval | "0.64" means nothing to the reader | Baseline, CI and n, always |
| Burying the answer on page 5 | Decision-makers miss it | Bottom line first |

## Try it yourself

**Task:** Run the "sensitivity to split date" loop yourself. Then answer: if a stakeholder asks "what's the model's accuracy?", what one sentence would you give?

<details markdown="1">
<summary>Show a model answer</summary>

```text
2025-09-01 1767 0.664
2025-10-01 1302 0.639
2025-11-01 804 0.701
```

"It ranks orders by cancellation risk clearly better than chance, with a ROC AUC of about 0.64 to 0.70 depending on the test period, so it's useful for prioritising credit checks but not for confidently predicting individual cancellations." One sentence: what it can and can't do, a range rather than a falsely precise number, and the metric that fits the use.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Two runs of your analysis give different numbers. What's the first thing to check?

1. Buy a faster computer
2. Same data (hash), same environment, same seed?
3. Use a different model

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. A model's ROC AUC is 0.64 with a 95% CI of 0.57–0.70. What can you say?

1. It's no better than random
2. It's better than random (0.5), but the exact performance is uncertain
3. It's an excellent model

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What should come first in an analysis report?

1. The data description
2. The bottom line: the answer, its uncertainty and the recommendation
3. The code

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Reproducible** = recorded environment (`uv.lock`), fingerprinted data (hashes), fixed seeds, and one command from raw data to saved results with provenance.
- **Evaluate** against a baseline, with a confidence interval, on a time-honest test, and check **sensitivity** to your choices.
- **Report** bottom line first: estimate + interval + recommendation, then method, limitations and how to reproduce.

!!! job "Job-ready check"
    **Interview question:** *"How do you make sure someone else can reproduce your analysis?"*

    **Strong answer:** "The project is in Git with a lock file for the environment, the raw data is never edited by hand and its hash is recorded, all randomness uses fixed seeds, and a single command runs the analysis from raw data to results, saving the outputs with the data hash and versions. The README explains how to rerun it and what numbers to expect. Before sharing, I rerun it from a clean environment."

    **Mini project:** Take one of your Phase 2 analyses and make it reproducible: one script, fixed seeds, a `results/` JSON with data hashes and versions, and a README "Reproduce" section. Then fill in `analysis_report_template.md` for it.
