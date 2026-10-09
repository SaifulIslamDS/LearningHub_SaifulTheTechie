---
title: "GitHub Actions: Run Lint and Tests on Every Push"
order: 2
summary: "Write a CI workflow that installs your project with uv, runs ruff and pytest on every push and pull request, and read the results on GitHub — plus scheduled workflows with cron."
level: Beginner
time: "45 min"
topics: ["GitHub Actions"]
prerequisites: ["phase-0/testing-ci/01-pytest-ruff", "phase-0/git-github/03-pull-requests-readme"]
keywords: [github actions, ci, continuous integration, workflow, yaml, .github/workflows, on push, pull_request, jobs, steps, runs-on, ubuntu-latest, uses, run, actions/checkout, setup-uv, matrix, schedule, cron, secrets, status check, badge]
reviewed: 2026-10-09
files: [phase-0/csv-cleaner-solution.zip]
resources:
  - title: "Quickstart for GitHub Actions"
    url: "https://docs.github.com/en/actions/get-started/quickstart"
    source: "GitHub Docs"
    note: "Create and run your first workflow."
  - title: "Using uv in GitHub Actions"
    url: "https://docs.astral.sh/uv/guides/integration/github/"
    source: "Astral (official)"
    note: "The setup-uv action, caching and Python versions."
  - title: "crontab.guru"
    url: "https://crontab.guru"
    source: "crontab.guru"
    note: "Check schedule expressions for scheduled workflows."
---

## What is it?

- **CI (continuous integration)** means every change is automatically checked (lint, format, tests) on a clean machine, not just on your laptop.
- **GitHub Actions** is GitHub's built-in CI. You describe a **workflow** in a YAML file inside `.github/workflows/`, and GitHub runs it on a fresh virtual machine (a **runner**) whenever something happens (a push, a pull request, a schedule).

```text
git push ──► GitHub ──► runner (fresh Ubuntu)
                         1. get the code
                         2. install uv + Python
                         3. install exact dependencies (uv.lock)
                         4. ruff check · ruff format --check · pytest
                         ──► ✅ or ❌ shown on the commit and the PR
```

!!! job "Why it matters at work"
    In professional teams a PR cannot merge until CI is green. CI catches "works on my machine" problems, forgotten files and broken tests before review. A green CI badge in a portfolio repository shows employers you work like an engineer. The same Actions platform is also used to schedule data jobs and deploy apps.

## Example: the csv-cleaner workflow

From [csv-cleaner-solution.zip](../../../downloads/phase-0/csv-cleaner-solution.zip), file `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Install uv
        uses: astral-sh/setup-uv@v9

      - name: Install Python (version from .python-version)
        run: uv python install

      - name: Install the project and dev tools
        run: uv sync --locked --dev

      - name: Lint
        run: uv run ruff check .

      - name: Check formatting
        run: uv run ruff format --check .

      - name: Run tests
        run: uv run pytest
```

| Part | Meaning |
|---|---|
| `on:` | **When** to run: pushes to `main`, and every pull request |
| `jobs: test:` | One job called `test` (jobs run in parallel by default) |
| `runs-on: ubuntu-latest` | A fresh Linux machine for every run |
| `uses:` | A ready-made **action** from the marketplace (`owner/name@version`) |
| `run:` | A shell command, exactly as you'd type it in the terminal |
| `--locked` | Fail if `uv.lock` is out of date, instead of silently changing versions |

If any step fails (exit code not 0), the job stops and turns **red ❌**.

## Run the same checks locally first

CI should never surprise you. Run the same commands before pushing:

```bash
uv sync --locked --dev
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

```text
All checks passed!
8 files already formatted
.................                                                        [100%]
17 passed in 0.05s
```

## See it on GitHub

1. Push the project to a new GitHub repository (Git module).
2. Open the **Actions** tab: you'll see a run called **CI** with a yellow dot (running), then ✅ or ❌.
3. Click the run → the `test` job → expand any step to read its log. A failed step shows the same pytest or ruff output you'd see locally.
4. On a pull request, the result appears as a **status check** at the bottom. With **branch protection** (Settings → Branches), you can require it to pass before merging.

!!! tip "Add a badge to your README"
    `![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)` shows a live green/red badge on your project page.

## Keep actions up to date

Actions run on Node.js inside GitHub's runners. GitHub removed Node 20 from runners on 23 September 2026, so workflows pinned to old major versions (for example `actions/checkout@v4`) can fail. Use current major versions (`actions/checkout@v7`, `astral-sh/setup-uv@v9`, `actions/setup-python@v7`), and let **Dependabot** propose updates.

## Scheduled workflows (cron in the cloud)

The same 5-field cron syntax from the Linux lesson, in UTC:

```yaml
on:
  schedule:
    - cron: "0 6 * * 1-5"     # 06:00 UTC, Monday–Friday
  workflow_dispatch:          # also allow a manual "Run workflow" button
```

Useful for nightly data refreshes or link checks. (This website's own repository runs a weekly link check this way.) Scheduled runs can start a few minutes late at busy times.

## More useful features

| Feature | What for | Snippet |
|---|---|---|
| **Matrix** | Test several Python versions | `strategy: matrix: python: ["3.13", "3.14"]` |
| **Secrets** | API keys and passwords, never in the YAML | `${{ secrets.API_KEY }}` |
| **Artifacts** | Keep output files (reports, coverage) | `actions/upload-artifact` |
| **Caching** | Faster runs | `setup-uv` with `enable-cache: true` |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Wrong folder (`.github/workflow/`) | Nothing runs | Exactly `.github/workflows/*.yml` |
| YAML indentation errors | "Invalid workflow file" | Spaces, not tabs; check the Actions tab error |
| Not committing `uv.lock` | `--locked` fails, or versions differ | Commit it with dependency changes |
| Secrets pasted in the workflow | Leaked keys in public history | Repository **Settings → Secrets** |
| Old action versions | Failures after runner updates | Current major versions + Dependabot |
| Pushing without running checks locally | A red CI, and a noisy history | Run the four commands first |

## Try it yourself

**Task:** Break the csv-cleaner formatting on purpose (add the line `x=1` to the end of `src/csv_cleaner/cli.py`), then run the CI commands locally. Which step fails, and what would GitHub show?

<details markdown="1">
<summary>Show the solution</summary>

Lint passes (`All checks passed!`): `x=1` is valid code. The **Check formatting** step fails:

```text
unformatted: File would be reformatted
  --> src/csv_cleaner/cli.py:84:2
   |
83 |     sys.exit(main())
   - x=1
84 + x = 1
   |

1 file would be reformatted, 7 files already formatted
```

It exits with code 1, so on GitHub the run turns ❌ at **Check formatting**, the **Run tests** step is skipped, and the PR shows a failed status check. Fix it (delete the line, or run `uv run ruff format .`), commit and push: the PR updates and CI reruns automatically.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Where do workflow files live?

1. `workflows/` in the repository root
2. `.github/workflows/`
3. Anywhere, as long as the file ends in `.yml`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `on: pull_request` mean?

1. Run when someone opens or updates a PR
2. Run only after the PR is merged
3. Create a pull request automatically

<details markdown="1"><summary>Show answer</summary>
**A.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Where should an API key used by a workflow be stored?

1. In the YAML file
2. In repository secrets, used as `${{ secrets.NAME }}`
3. In the README

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- CI runs your checks on a clean machine for every push and PR; GitHub Actions does it with YAML in `.github/workflows/`.
- A Python CI job: checkout → setup-uv → `uv sync --locked --dev` → ruff check → ruff format --check → pytest.
- Read failures in the Actions tab; require green checks with branch protection.
- Use `schedule` (UTC cron) for recurring jobs, secrets for keys, and current action versions.

!!! job "Job-ready check"
    **Interview question:** *"What does your CI pipeline check, and why?"*

    **Strong answer:** "On every push and PR, a clean runner installs the exact locked dependencies with uv, then runs ruff lint, a format check and the pytest suite. That proves the project installs from scratch and the rules still hold. The PR can't merge until it's green, so `main` always works."

    **Mini project:** Add a CI workflow to your own `sales-report` repository (lesson 3 of the Git module), make it fail once on purpose, fix it, and add the CI badge to your README.
