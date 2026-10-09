---
title: "Coding Agents, Copilots & Prompting for Code"
order: 1
summary: "Understand the range of AI coding tools, from autocomplete to autonomous agents, and write prompts and AGENTS.md instructions that give them the context, constraints and checks they need to produce correct code."
level: Beginner
time: "45 min"
topics: ["Coding agents & copilots", "Prompting for code"]
prerequisites: ["phase-0/testing-ci/01-pytest-ruff"]
keywords: [ai coding assistant, copilot, github copilot, coding agent, agent mode, claude code, cursor, codex, chat, autocomplete, prompt, prompting for code, context, constraints, known answers, agents.md, project instructions, small steps, plan first, hallucination]
reviewed: 2026-10-09
files: [phase-0/csv-cleaner-solution.zip, phase-0/python-refresher.zip, orders.sql, known_answers.csv]
resources:
  - title: "AGENTS.md — a simple, open format for guiding coding agents"
    url: "https://agents.md"
    source: "agents.md (open format)"
    note: "What to put in the file, with examples."
  - title: "About GitHub Copilot coding agent"
    url: "https://docs.github.com/en/copilot/concepts/agents/coding-agent"
    source: "GitHub Docs"
    note: "How an agent works on an issue and opens a pull request for review."
  - title: "Claude Code: best practices for agentic coding"
    url: "https://www.anthropic.com/engineering/claude-code-best-practices"
    source: "Anthropic Engineering"
    note: "Plan first, give the agent ways to verify its work, and keep instructions in a project file."
  - title: "AGENTS.md (Agent patterns)"
    url: "https://addyosmani.com/agents/15-agents-md/"
    source: "Addy Osmani"
    note: "Practical advice on writing effective agent instruction files."
---

## What is it?

AI coding tools range from small suggestions to agents that change many files on their own:

| Level | What it does | You stay in control by… |
|---|---|---|
| **Autocomplete** | Suggests the next line(s) as you type | Accepting or ignoring each suggestion |
| **Chat** | Answers questions, explains code, drafts a function | Copying in only what you understand |
| **Agent in the editor / terminal** | Reads your project, edits several files, runs commands and tests | Approving steps and reviewing the diff |
| **Background agent** | Works on an issue by itself and opens a **pull request** | Reviewing the PR like any colleague's |

Examples include GitHub Copilot, Cursor, Claude Code, OpenAI Codex and Gemini CLI. Products change fast; the **skills** in this module don't.

**Prompting for code** means giving the tool what a new colleague would need: context, a precise task, constraints, and a way to check the result.

!!! job "Why it matters at work"
    Most development teams now use AI assistants daily, and job adverts increasingly ask for experience with them. What separates juniors who benefit from those who cause incidents is **specification and verification**: clear instructions in, reviewed and tested code out. You are responsible for every line you commit, whoever typed it.

## Part 1: a weak prompt vs a strong prompt

**Weak:**

> Write a Python function that reads orders_raw.csv and returns net revenue by month.

This is the exact prompt behind `ai-review/ai_suggestion.py` in [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip). The code runs without errors, and reports **5,875** instead of **9,075** (next lesson). The model had to **guess** the date format, the meaning of "net", and what to do with messy rows.

**Strong:**

```text
Context: Python 3.14 project managed with uv. File data/orders_raw.csv is a raw
ERP export: columns Order ID, Order Date, Customer, Region, Category, Product,
Qty, Unit Price, Status. Dates are DAY-first (dd/mm/yyyy). Qty may contain
thousands separators ("5,000"). Status casing varies ("CANCELLED", "pending").
The file has blank rows and exact duplicate rows.

Task: write net_revenue_by_month(path) -> dict[str, float] returning
{"YYYY-MM": revenue}, where revenue = Qty * Unit Price, excluding Cancelled
orders (case-insensitive), skipping blank and duplicate rows.

Constraints: standard library only; type hints; no bare except — log rejected
rows with their line number; round to 2 decimals.

Check: for this file the answer must be {"2026-01": 3440.0, "2026-02": 3940.0,
"2026-03": 1695.0} (total 9075.0). Write pytest tests for: day-first dates,
cancelled excluded, "5,000" quantities. Run them and show me the output.
```

| Part | Why it helps |
|---|---|
| **Context** | Versions, file layout and real data quirks: the model can't see your data |
| **Task** | Exact name, inputs, output shape and definitions ("net" = excluding Cancelled) |
| **Constraints** | Libraries, style, error handling, what **not** to do |
| **Check** | Known answers and tests turn "looks right" into "proved right" |

## Part 2: work in small, checked steps

1. **Ask for a plan first** ("List the steps and the files you'll change. Don't write code yet"), and correct it while it's cheap.
2. **One small task per request**: one function, one test file, one bug.
3. **Make the agent run the checks** (`uv run pytest`, `uv run ruff check .`) and show you the output.
4. **Review the diff** before accepting (`git diff`), and **commit** after each working step, so you can always go back.
5. If it goes in circles, **stop**, reset with `git restore .`, and give a clearer, smaller prompt.

## Part 3: AGENTS.md — instructions that stay with the repo

Instead of repeating the same context in every prompt, put it in a file the tools read automatically. **AGENTS.md** is an open format supported by many coding agents (some tools also read their own file, such as `CLAUDE.md` or `.github/copilot-instructions.md`). The Phase 0 project includes one (in [csv-cleaner-solution.zip](../../../downloads/phase-0/csv-cleaner-solution.zip)):

```markdown
# AGENTS.md

## Setup and commands
- Install: `uv sync --dev`
- Test: `uv run pytest`
- Lint and format: `uv run ruff check .` and `uv run ruff format .`

## Rules
- Python 3.12+ syntax, type hints on every function.
- Never hard-code paths or column names in code: they belong in `config.toml`.
- Never swallow errors with a bare `except`. Reject the row, log the line number
  and reason, and count it in the report.
- Every change to cleaning behaviour needs a test in `tests/`.
- Known answer: `data/orders_raw.csv` → 12 rows written. Do not change the
  expected file to make a test pass.
- Don't add new dependencies without asking.

## Before you finish
Run `uv run ruff check . && uv run ruff format --check . && uv run pytest`.
```

Keep it short, specific and **checkable**: commands, rules and known answers, not essays.

## Safe-use rules

| Never | Instead |
|---|---|
| Paste secrets, passwords or API keys into a prompt | Use placeholders; keep secrets in environment variables |
| Paste confidential company or customer data into tools your employer hasn't approved | Use the approved tool, or anonymised samples |
| Trust package names the AI suggests without checking | Look the package up on PyPI first (invented or look-alike names exist) |
| Let an agent run destructive commands unattended (`rm -rf`, `git push --force`, database deletes) | Approve commands one by one, and work on a branch |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Vague one-line prompts | Plausible code built on wrong guesses | Context + task + constraints + check |
| Asking for a whole app at once | Huge, unreviewable output | Plan first, then small steps |
| Accepting code you don't understand | You can't debug it or defend it in review | Ask the AI to explain it, or rewrite it more simply |
| No tests or known answers | Wrong numbers ship silently | Put the expected result in the prompt |
| Letting the AI "fix" a test by changing the expected value | The bug is hidden, not fixed | Say so explicitly in AGENTS.md, and review test diffs |

## Try it yourself

**Task:** Rewrite this weak prompt as a strong one using the four parts: *"Write a SQL query for revenue by region."* Use the practice database (`orders` table with `quantity`, `unit_price`, `status`, `region`).

<details markdown="1">
<summary>Show a model answer</summary>

```text
Context: SQLite database orders.sql. Table orders(order_id, order_date, customer,
region, category, product, quantity, unit_price, status).
Task: net revenue (quantity * unit_price, excluding status = 'Cancelled') per
region, highest first, columns region and net_revenue rounded to 2 decimals.
Constraints: one SELECT, no subqueries needed, SQLite syntax.
Check: total must be 9075; Dhaka must be 3170. Show the result table.
```

Compare the result with `known_answers.csv`. If Dhaka isn't 3,170, the query is wrong.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What's the most useful thing to add to a code prompt?

1. "Please be accurate"
2. Context about the data, plus a known answer or test to check against
3. The word "expert"

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What is AGENTS.md for?

1. Listing the people on the team
2. Project instructions (commands, rules, checks) that coding agents read automatically
3. Storing API keys for agents

<details markdown="1"><summary>Show answer</summary>
**B.** And never put secrets in it: it's committed to the repository.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. A background agent opens a pull request. What do you do?

1. Merge it: the AI tested it
2. Review it and check CI like any colleague's PR
3. Close it without reading

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- AI tools range from autocomplete and chat to agents that edit files and open PRs. You stay responsible for the result.
- Strong prompts have **context, task, constraints and a check** (known answers, tests).
- Plan first, work in small steps, run the checks, review the diff, commit often.
- Put lasting instructions in **AGENTS.md**; never share secrets or unapproved data.

!!! job "Job-ready check"
    **Interview question:** *"How do you use AI coding assistants in your work?"*

    **Strong answer:** "For well-defined tasks I give the tool context, constraints and a known answer, ask for a plan first, and work in small steps. The repo has an AGENTS.md with our commands and rules. I review every diff, make sure tests and linting pass, and I never paste secrets or confidential data into unapproved tools. The AI speeds me up; the tests and review make it safe."

    **Mini project:** Write an AGENTS.md for your `sales-report` repo, then use any AI assistant to add one small feature with a four-part prompt. Save the prompt, the diff and the test output in `docs/ai-log.md`.
