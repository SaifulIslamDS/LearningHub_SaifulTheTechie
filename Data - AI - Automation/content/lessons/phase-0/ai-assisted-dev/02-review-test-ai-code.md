---
title: "Reviewing & Testing AI-Written Code: Trust, but Verify"
order: 2
summary: "Review AI-generated code with a checklist, trace it against real data, and prove it right or wrong with known-answer tests — using a function that runs cleanly but returns 5,875 instead of 9,075."
level: Beginner
time: "50 min"
topics: ["Reviewing AI-written code", "Testing AI-written code"]
prerequisites: ["phase-0/ai-assisted-dev/01-agents-prompting", "phase-0/testing-ci/01-pytest-ruff"]
keywords: [code review, ai-generated code, review checklist, silent failure, bare except, date format, known answers, pytest, test from the spec, edge cases, hallucinated api, security, dependency, verification, regression test]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip, orders_raw.csv, known_answers.csv]
resources:
  - title: "Claude Code: best practices for agentic coding"
    url: "https://www.anthropic.com/engineering/claude-code-best-practices"
    source: "Anthropic Engineering"
    note: "Why giving an agent tests to verify against improves results."
  - title: "Get started with pytest"
    url: "https://docs.pytest.org/en/stable/getting-started.html"
    source: "pytest docs (official)"
    note: "Asserts, pytest.approx and the tmp_path fixture."
  - title: "Pull requests documentation"
    url: "https://docs.github.com/en/pull-requests/reference/pull-requests"
    source: "GitHub Docs"
    note: "Reviewing and approving changes, including agent-created PRs."
---

## What is it?

- **Reviewing AI-written code** means reading it as critically as a colleague's pull request: is it correct for *our* data and rules, safe, and maintainable?
- **Testing AI-written code** means proving it with tests written from the **specification** (business rules and known answers), not from whatever the code happens to do.

The dangerous AI bug is not the one that crashes. It's the one that **runs cleanly and gives a believable wrong number**.

!!! job "Why it matters at work"
    AI makes producing code cheap; checking it is now the valuable skill. Teams expect you to catch wrong assumptions, silent failures and security issues before merge, and reviewers will ask "how do you know it's right?". The answer must be tests and known answers, not "the AI said so".

## The code to review

`ai-review/ai_suggestion.py` in [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip) came from the weak prompt in the previous lesson: *"Write a Python function that reads orders_raw.csv and returns net revenue by month."*

```python
import csv
from collections import defaultdict
from datetime import datetime


def net_revenue_by_month(path):
    totals = defaultdict(float)
    with open(path) as f:
        for row in csv.DictReader(f):
            try:
                qty = int(row["Qty"])
                price = float(row["Unit Price"])
                month = datetime.strptime(row["Order Date"], "%m/%d/%Y").strftime("%Y-%m")
                totals[month] += qty * price
            except Exception:
                continue
    return dict(sorted(totals.items()))
```

It looks tidy, and it runs:

```text
2026-02 1360.0
2026-05 420.0
2026-09 1275.0
2026-11 1260.0
2026-12 1560.0
Total: 5875.0
```

The known answer is **9,075** for January–March. Months 05, 09, 11 and 12 don't even exist in the data.

## Part 1: review with a checklist

| Check | Question | Finding here |
|---|---|---|
| **Assumptions** | Does it match our data's real format? | ❌ Reads dates as **month-first**; the export is day-first (`05/01/2026` = 5 January) |
| **Business rules** | Does "net" mean what we mean? | ❌ Cancelled orders are **not** excluded |
| **Error handling** | Are failures visible? | ❌ `except Exception: continue` silently drops every row it can't parse |
| **Data quirks** | Blanks, `"5,000"`, duplicates, casing? | ❌ `"5,000"` fails `int()` and is dropped; the duplicate row is counted twice |
| **Security** | `eval`, SQL built from strings, secrets, shell commands? | ✅ None here |
| **Dependencies & APIs** | Do imported packages and functions really exist? | ✅ Standard library only |
| **Readability** | Type hints, names, docstring? | ⚠️ No type hints; no `encoding` or `newline=""` |

### Trace it against the data

Walking through the 14 raw rows shows exactly where 9,075 became 5,875:

| Raw row | What the AI code did |
|---|---|
| `05/01/2026` order 1 (420) | Counted, but in **May** |
| `08/01/2026` qty `"5,000"` | Dropped silently (`int("5,000")` fails) |
| `12/01/2026` order 3 (1,560) | Counted, but in **December** |
| `15/01/2026`, `20/01/2026` | Dropped silently: month 15 and 20 don't exist |
| `02/02/2026` order 6, **twice** | Counted **twice** (1,360) |
| `06/02` `"8,000"`, `03/03` `"1,500"` | Dropped silently |
| `11/02/2026` order 8 (1,260) | Counted, but in **November** |
| `18/02`, `25/02` | Dropped silently |
| `09/03/2026` order 12 (1,275) | Counted, but in **September** |
| Order 4 `CANCELLED` | Dropped only because `15/01` failed, **not** because of the rule |
| The blank row | Dropped, again by accident (`int("")` fails) |

Six of the eleven orders that should count vanished without a single message, and four of the five that survived landed in the wrong month. That's what the bare `except` hides.

## Part 2: test from the specification

Write tests from the **rules and known answers**, never by copying the code's current output. `ai-review/test_ai_suggestion.py`:

```python
from pathlib import Path

import pytest
from ai_suggestion import net_revenue_by_month

RAW = Path(__file__).parent.parent / "data" / "orders_raw.csv"
HEADER = "Order ID,Order Date,Customer,Region,Category,Product,Qty,Unit Price,Status\n"


def write_csv(tmp_path, rows):
    f = tmp_path / "orders.csv"
    f.write_text(HEADER + "".join(rows), encoding="utf-8")
    return f


def test_only_q1_months():
    assert list(net_revenue_by_month(RAW)) == ["2026-01", "2026-02", "2026-03"]


def test_known_monthly_totals():
    expected = {"2026-01": 3440.0, "2026-02": 3940.0, "2026-03": 1695.0}
    assert net_revenue_by_month(RAW) == pytest.approx(expected)


def test_total_matches_known_answer():
    assert sum(net_revenue_by_month(RAW).values()) == pytest.approx(9075.0)


def test_day_first_dates(tmp_path):
    f = write_csv(tmp_path, ["1,15/01/2026,A,Dhaka,F,P,10,1.00,Delivered\n"])
    assert net_revenue_by_month(f) == pytest.approx({"2026-01": 10.0})


def test_cancelled_excluded(tmp_path):
    f = write_csv(tmp_path, ["1,05/01/2026,A,Dhaka,F,P,10,1.00,Delivered\n",
                             "2,06/01/2026,A,Dhaka,F,P,10,1.00,CANCELLED\n"])
    assert net_revenue_by_month(f) == pytest.approx({"2026-01": 10.0})


def test_quantity_with_thousands_separator(tmp_path):
    f = write_csv(tmp_path, ['1,05/01/2026,A,Dhaka,F,P,"5,000",0.04,Delivered\n'])
    assert net_revenue_by_month(f) == pytest.approx({"2026-01": 200.0})
```

- **Known-answer tests** use the real file: 3,440 / 3,940 / 1,695 (the same months and MoM changes as the DAX lesson).
- **Rule tests** use tiny files made with pytest's `tmp_path` fixture: one rule per test, so a failure names the broken rule.

Run them in the `ai-review` folder:

```bash
python -m pytest
```

```text
FAILED test_ai_suggestion.py::test_only_q1_months - AssertionError: assert ['...
FAILED test_ai_suggestion.py::test_known_monthly_totals - AssertionError: ass...
FAILED test_ai_suggestion.py::test_total_matches_known_answer - assert 5875.0...
FAILED test_ai_suggestion.py::test_day_first_dates - AssertionError: assert {...
FAILED test_ai_suggestion.py::test_cancelled_excluded - AssertionError: asser...
FAILED test_ai_suggestion.py::test_quantity_with_thousands_separator - Assert...
============================== 6 failed in 0.07s ===============================
```

One failure in detail:

```text
>       assert sum(net_revenue_by_month(RAW).values()) == pytest.approx(9075.0)
E       assert 5875.0 == 9075.0 ± 0.009075
```

## Part 3: fix, then prove it

Give the failures back to the AI (or fix them yourself) with the rules stated precisely. The reviewed version is `solutions/ai_review_fixed.py`:

```python
def net_revenue_by_month(path: Path | str) -> dict[str, float]:
    """Net revenue (excluding Cancelled) per month from the raw export."""
    totals: dict[str, float] = defaultdict(float)
    seen: set[tuple[str, ...]] = set()
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            values = tuple((v or "").strip().lower() for v in row.values())
            if not any(values):
                continue  # blank row
            if values in seen:
                continue  # exact duplicate
            seen.add(values)
            if row["Status"].strip().lower() == "cancelled":
                continue
            try:
                qty = int(row["Qty"].replace(",", "").strip())
                price = float(row["Unit Price"])
                when = datetime.strptime(row["Order Date"].strip(), "%d/%m/%Y")
            except ValueError as exc:
                log.warning("Line %d rejected: %s", line_no, exc)
                continue
            totals[when.strftime("%Y-%m")] += qty * price
    return {month: round(value, 2) for month, value in sorted(totals.items())}
```

Copy it over `ai_suggestion.py` and run the tests again:

```text
6 passed in 0.02s
```

```text
2026-01 3440.0
2026-02 3940.0
2026-03 1695.0
Total: 9075.0
```

Every fix maps to a review finding: day-first dates, the Cancelled rule, `"5,000"`, duplicates, and a **specific** `except ValueError` that **logs** what it rejects.

## Review red flags in AI code

| Red flag | Why it's risky |
|---|---|
| `except Exception: pass` / `continue` | Silent data loss |
| Hard-coded formats, paths or magic numbers | Wrong assumptions about your environment |
| `eval()`, `exec()`, `shell=True`, SQL built with f-strings | Security holes (code or SQL injection) |
| Imports or functions you've never heard of | May not exist, or may be a look-alike malicious package |
| Tests that only check the code's own output | They pass even when the logic is wrong |
| Large rewrites of code you didn't ask to change | Hidden regressions; ask for a minimal diff |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| "It runs, so it works" | Wrong numbers in production | Known-answer tests |
| Letting the AI write the tests **and** the code from the same vague prompt | Tests repeat the same wrong assumption | Write or review tests from the spec yourself |
| Updating expected values until tests pass | The bug becomes "correct" | Expected values come from the business, not the code |
| Reviewing only the changed lines | Missed context (callers, config, data) | Read surrounding code; trace real data |
| Merging big AI PRs in one go | Unreviewable risk | Ask for small PRs, one concern each |

## Try it yourself

**Task:** Add a **regression test** for the duplicate-row bug: a tiny file with the same order on two identical lines should count it once. Run it against `ai_suggestion.py` (it should fail) and against the fixed version (it should pass).

<details markdown="1">
<summary>Show the solution</summary>

```python
def test_exact_duplicates_counted_once(tmp_path):
    line = "6,02/02/2026,A,Chattogram,F,P,200,3.40,Delivered\n"
    f = write_csv(tmp_path, [line, line])
    assert net_revenue_by_month(f) == pytest.approx({"2026-02": 680.0})
```

Against the AI version, `02/02/2026` happens to parse correctly (day and month are equal), so the failure is purely the duplicate: it returns `{'2026-02': 1360.0}`. With the fixed version it passes. A good regression test isolates **one** bug.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. AI-written code runs without errors. What's the right next step?

1. Merge it
2. Check it against known answers and rule-based tests
3. Ask the AI whether it's correct

<details markdown="1"><summary>Show answer</summary>
**B.** Asking the same model to grade itself is not verification.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why is `except Exception: continue` a red flag in data code?

1. It's slow
2. Bad rows disappear silently, so totals are wrong with no warning
3. It's not valid Python

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Where should a test's expected values come from?

1. The code's current output
2. The specification: business rules and known answers
3. Whatever makes the test pass

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- The worst AI bugs run cleanly and give believable wrong answers.
- Review with a checklist: assumptions, business rules, error handling, data quirks, security, dependencies, readability, and **trace real rows**.
- Test from the spec: known-answer tests on real data plus one-rule tests on tiny files (`tmp_path`).
- Fix, re-run, and keep the tests as **regression** protection in CI.

!!! job "Job-ready check"
    **Interview question:** *"An AI assistant wrote a data transformation for you. How do you decide whether to merge it?"*

    **Strong answer:** "I review it like any PR: check its assumptions against the real data format, the business rules, error handling and security. Then I prove it with tests written from the spec: known totals on a real sample, plus small tests for each rule and edge case. Only when those pass in CI, and I understand every line, does it merge."

    **Mini project:** Ask an AI assistant to write a function that returns **revenue by region** from `orders_raw.csv` using a *weak* prompt. Review it with the checklist, write known-answer tests (Dhaka 3,170; total 9,075), and document each bug you found in `docs/ai-review.md`.
