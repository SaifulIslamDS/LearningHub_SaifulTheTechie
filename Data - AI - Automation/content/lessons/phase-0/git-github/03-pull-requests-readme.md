---
title: "GitHub, Pull Requests & READMEs: Collaborate and Show Your Work"
order: 3
summary: "Push a repository to GitHub, propose changes through a pull request, review others' code, and give every project a README and structure that employers understand in a minute."
level: Beginner
time: "50 min"
topics: ["Pull requests", "README & project structure"]
prerequisites: ["phase-0/git-github/02-branches-merge"]
keywords: [github, remote, origin, git push, git pull, git clone, pull request, pr, code review, approve, merge pull request, readme, markdown, project structure, src layout, portfolio, fork]
reviewed: 2026-10-09
files: [phase-0/csv-cleaner-solution.zip]
resources:
  - title: "Hello World (GitHub quickstart)"
    url: "https://docs.github.com/get-started/quickstart/hello-world"
    source: "GitHub Docs"
    note: "Create a repo, a branch, a pull request and merge it — all in the browser."
  - title: "Pull requests documentation"
    url: "https://docs.github.com/en/pull-requests/reference/pull-requests"
    source: "GitHub Docs"
    note: "Reviews, merge methods and protected branches."
  - title: "Introduction to GitHub (interactive course)"
    url: "https://github.com/skills/introduction-to-github"
    source: "GitHub Skills"
    note: "Free guided practice."
---

## What is it?

- **GitHub** hosts your Git repositories online. Your local repo and the GitHub copy (called the **remote**, usually named `origin`) stay in sync with `push` and `pull`.
- A **pull request (PR)** says: *"Here is my branch. Please review it and merge it into `main`."* It shows the diff, lets people comment, and runs automated checks.
- A **README** is the front page of a repository: what it does, how to run it, and what the result looks like.

!!! job "Why it matters at work"
    In most teams, **every** change reaches `main` through a reviewed PR with passing checks. For job seekers, your GitHub profile *is* your portfolio: a recruiter spends about a minute on a repo, and the README decides whether they look further.

## Part 1: put your repo on GitHub

1. On GitHub, click **New repository** → name it `sales-report` → leave it **empty** (no README) → **Create**.
2. Connect and push your local repo:

```bash
git remote add origin https://github.com/<your-username>/sales-report.git
git push -u origin main
```

`-u` remembers the link, so afterwards a plain `git push` or `git pull` works.

| Command | Does |
|---|---|
| `git clone <url>` | Download a repo (with full history) to a new folder |
| `git push` | Send your new commits to GitHub |
| `git pull` | Fetch and merge others' commits from GitHub |
| `git remote -v` | Show where `origin` points |

!!! tip "Authentication"
    GitHub doesn't accept your account password for Git. The easiest route is **GitHub CLI** (`gh auth login`) or VS Code's built-in GitHub sign-in. Both store a token for you.

## Part 2: the pull request workflow

```text
1. git switch -c fix/exclude-cancelled     ← branch
2. edit, commit, commit                    ← small commits
3. git push -u origin fix/exclude-cancelled
4. GitHub → "Compare & pull request"       ← open PR
5. Review: comments, suggestions, checks   ← discuss
6. Merge → delete branch → git pull on main
```

**A good PR description:**

```markdown
## What
Exclude cancelled orders from the average order value.

## Why
The business rule says cancelled orders don't count. The report showed 447.50 instead of 516.67.

## How I tested
- Added test `test_average_skips_cancelled`
- `uv run pytest` → all passing

Closes #12
```

`Closes #12` automatically closes issue 12 when the PR is merged.

### Reviewing a PR

| Do | Don't |
|---|---|
| Ask questions: "What happens if `rows` is empty?" | Write "this is wrong" with no reason |
| Point to specific lines, and suggest code | Rewrite the whole thing your way |
| Check tests and the business rule | Approve without reading the diff |
| Separate must-fix from nice-to-have ("nit:") | Block a PR on personal style (that's what ruff is for) |

Merge buttons: **Create a merge commit** (keeps every commit), **Squash and merge** (one tidy commit, common in teams), **Rebase and merge** (linear history).

## Part 3: README & project structure

Open the Phase 0 reference project, [csv-cleaner-solution.zip](../../../downloads/phase-0/csv-cleaner-solution.zip). Its layout is a modern Python standard:

```text
csv-cleaner/
├── .github/workflows/ci.yml   ← automatic tests on every push/PR
├── .gitignore
├── .python-version            ← 3.14
├── README.md                  ← start here
├── config.toml                ← settings, not hard-coded
├── data/orders_raw.csv        ← small sample input
├── pyproject.toml             ← name, dependencies, tool settings
├── src/csv_cleaner/           ← the code (a package)
│   ├── __init__.py
│   ├── cleaner.py             ← logic
│   ├── cli.py                 ← command line
│   └── config.py
├── tests/                     ← pytest tests
└── uv.lock                    ← exact versions
```

| Folder/file | Why it's there |
|---|---|
| `src/` | Code is separated from data, tests and docs, and it's importable as a package |
| `tests/` | Anyone can run `uv run pytest` and trust the result |
| `data/` | A **small** sample only, never confidential or large data |
| `pyproject.toml` + `uv.lock` | Reproducible install with one command |
| `.github/workflows/` | Checks run automatically (Testing & CI module) |

### A README that works in 60 seconds

```markdown
# csv-cleaner
Clean messy CSV exports with repeatable, configurable rules.

## Quick start
uv sync --dev
uv run csv-clean data/orders_raw.csv
uv run pytest

## Example output
Rows read: 14 | blank removed: 1 | duplicates removed: 1 | rejected: 0 | written: 12

## How it works
(one diagram or 3 bullets)

## Results / screenshots
## What I learned / next steps
```

The order matters: **what it is → how to run it → proof it works → details.**

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Pushing directly to `main` in a team | No review, broken builds | Branch + PR; turn on branch protection |
| Giant PRs (2,000 lines) | Nobody reviews properly | Small PRs, ideally under ~300 changed lines |
| A README that says only the project name | Visitors leave | Purpose, quick start, example output, screenshot |
| Everything in one folder (`final.py`, `test2.py`, `data.xlsx`) | Looks like a scratchpad | `src/`, `tests/`, `data/`, `docs/` |
| Forgetting `git pull` before starting new work | Conflicts with others' changes | Pull `main`, then branch |

## Try it yourself

**Task:** Use GitHub's [Hello World guide](https://docs.github.com/get-started/quickstart/hello-world) to create a repo, open a PR from a branch that edits the README, and merge it. Then write a three-section PR description (**What / Why / How I tested**) for a change that adds `print("Achievement: 94.5%")` to `report.py`.

<details markdown="1">
<summary>Show a model description</summary>

```markdown
## What
Print Q1 achievement % (net revenue ÷ target) in the report.

## Why
Managers asked for the headline achievement figure next to revenue and target.

## How I tested
Ran `python report.py`: shows 9,075 / 9,600 / 94.5%, matching the known answers file.
```
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What is a pull request?

1. Downloading the latest code
2. A request to review and merge a branch into another branch
3. A GitHub backup

<details markdown="1"><summary>Show answer</summary>
**B.** (`git pull` is a different thing: it downloads and merges.)
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What should come first in a README?

1. The licence text
2. What the project does and how to run it
3. The full commit history

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which is the better code review comment?

1. "Wrong."
2. "If `rows` is empty this divides by zero. Could we return 0 and add a test?"
3. "I'd write it differently."

<details markdown="1"><summary>Show answer</summary>
**B.** Specific, explains the risk, suggests a fix.
</details>
</div>

## Summary

- `git remote add origin …` + `git push -u origin main` publishes your repo; `clone`, `pull` and `push` keep it in sync.
- Changes reach `main` through **PRs**: branch → push → describe (What/Why/How tested) → review → merge.
- Review kindly and specifically; let tools handle style.
- A clear **structure** (`src/`, `tests/`, `pyproject.toml`, CI) and a **README** with quick start and proof make a repo portfolio-ready.

!!! job "Job-ready check"
    **Interview question:** *"Walk me through how a change gets from your laptop to production in your team."*

    **Strong answer:** "I pull `main`, create a branch, make small commits and push. I open a PR describing what, why and how I tested it. CI runs linting and tests, and a teammate reviews. After approval and green checks, we squash-merge to `main`, which triggers deployment."

    **Mini project:** Push your `sales-report` repo to GitHub with a README following the 60-second template, then make one change through a PR (even reviewing it yourself) and merge it.
