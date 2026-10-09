---
title: "uv, Virtual Environments & Packages: One Project, One Environment"
order: 2
summary: "Create isolated project environments, add and lock packages, and run code reproducibly — with uv, the fast all-in-one Python project tool."
level: Beginner
time: "40 min"
topics: ["uv / virtual environments", "Package management"]
prerequisites: ["phase-0/dev-environment/01-vscode-python"]
keywords: [uv, virtual environment, venv, .venv, pip, pyproject.toml, uv.lock, lock file, dependencies, uv init, uv add, uv run, uv sync, uv python install, reproducible]
reviewed: 2026-10-09
files: [phase-0/csv-cleaner-solution.zip]
resources:
  - title: "uv documentation"
    url: "https://docs.astral.sh/uv/"
    source: "Astral (official)"
    note: "Installation and an overview of every feature."
  - title: "Working on projects"
    url: "https://docs.astral.sh/uv/guides/projects/"
    source: "Astral (official)"
    note: "uv init, add, run, sync and the lock file."
  - title: "Installing and managing Python"
    url: "https://docs.astral.sh/uv/guides/install-python/"
    source: "Astral (official)"
    note: "Let uv install Python versions for you."
  - title: "Python environments in VS Code"
    url: "https://code.visualstudio.com/docs/python/environments"
    source: "VS Code docs"
    note: "How VS Code finds and uses .venv folders."
---

## What is it?

- A **virtual environment** is a private folder of packages for **one project**. Project A can use pandas 2 and project B pandas 3 without conflict.
- **Package management** means adding, updating and **locking** those packages, so that everyone (and every server) installs exactly the same versions.
- **uv** does all of it with one fast tool: it installs Python, creates the `.venv`, adds packages, writes a lock file and runs your code.

!!! job "Why it matters at work"
    "Works on my machine" bugs are mostly environment bugs. Projects with a `pyproject.toml` and a lock file can be installed identically on a colleague's laptop, in CI and in production. uv has quickly become a standard tool in Python teams, and you'll see `uv sync` and `uv run` in many modern repositories.

## Install uv

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac / Linux / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a **new** terminal, then check: `uv --version`.

## Example 1: create a project

```bash
uv init sales-report
cd sales-report
```

uv creates:

```text
sales-report/
├── .git/             ← a Git repository (Git lessons)
├── .gitignore
├── .python-version   ← "3.14": which Python this project uses
├── README.md
├── main.py           ← a hello-world script
└── pyproject.toml    ← project name, Python version, dependencies
```

```toml
[project]
name = "sales-report"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []
```

## Example 2: add a package

```bash
uv add pandas
```

```text
Using CPython 3.14.6
Creating virtual environment at: .venv
Resolved 6 packages in 1.10s
Installed 4 packages in 14ms
 + numpy==2.5.3
 + pandas==3.0.6
 + python-dateutil==2.9.0.post0
 + six==1.17.0
```

Three things happened:

1. A **`.venv`** folder was created, holding the project's own Python and packages.
2. `pyproject.toml` now lists `"pandas>=3.0.6"` under `dependencies`.
3. A **`uv.lock`** file records the **exact** versions of pandas **and** its dependencies (numpy, dateutil, six).

*(Your version numbers will be newer if you run this later. That's fine.)*

## Example 3: run code in the environment

```bash
uv run main.py
```

```text
Hello from sales-report!
```

`uv run` checks that the environment matches the lock file (installing anything missing), then runs the command **inside** `.venv`. You don't need to "activate" anything.

## Example 4: dev tools, removing packages, and syncing

```bash
uv add --dev pytest        # a development-only tool (tests): not needed in production
uv tree --depth 1          # what the project depends on
uv remove pandas           # remove a package (and its now-unused dependencies)
uv sync                    # make .venv match uv.lock exactly (e.g. after git pull)
```

```text
sales-report v0.1.0
├── pandas v3.0.6
└── pytest v9.1.1 (group: dev)
```

**Which files go into Git?**

| File | Commit it? | Why |
|---|---|---|
| `pyproject.toml` | ✅ Yes | What the project needs |
| `uv.lock` | ✅ Yes | Exact versions, so everyone gets the same |
| `.python-version` | ✅ Yes | Same Python for everyone |
| `.venv/` | ❌ No | It's rebuilt by `uv sync`, and it's big. uv's `.gitignore` already excludes it |

## The classic way (you'll still see it)

Before uv, people used two separate tools:

```bash
python -m venv .venv                    # create the environment
source .venv/bin/activate               # Mac/Linux   (Windows: .venv\Scripts\activate)
pip install pandas                      # install into it
pip freeze > requirements.txt           # record versions
```

It works, but you manage Python versions, activation and the lock file by hand. Read it, recognise it, and prefer uv for new projects.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `pip install` into the global Python | Version clashes between projects | One environment per project (`uv add`) |
| Committing `.venv` to Git | A huge repository, broken on other computers | Ignore `.venv`, and commit `uv.lock` instead |
| Not committing `uv.lock` | Colleagues get different versions | Commit it with every dependency change |
| Running `python script.py` with the wrong interpreter | `ModuleNotFoundError` | `uv run script.py`, or select `.venv` in VS Code |
| Editing `uv.lock` by hand | A broken lock file | Change dependencies with `uv add` / `uv remove` only |

## Try it yourself

**Task:** Download [csv-cleaner-solution.zip](../../../downloads/phase-0/csv-cleaner-solution.zip), unzip it, and inside the `csv-cleaner` folder run `uv sync --dev`, then `uv run pytest`. How many tests pass, and which Python version did uv use?

<details markdown="1">
<summary>Show a hint</summary>

Look at the `.python-version` file, and at the first lines uv prints during `uv sync`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

`uv sync --dev` reads `.python-version` (**3.14**). It downloads that Python if needed, creates `.venv`, and installs pytest and ruff at the exact locked versions. Then `uv run pytest` reports **17 passed**. You never installed pytest yourself: the project's files described everything.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Which file records the **exact** versions of every installed package?

1. `pyproject.toml`
2. `uv.lock`
3. `.python-version`

<details markdown="1"><summary>Show answer</summary>
**B — `uv.lock`.** `pyproject.toml` lists what you asked for, and the lock file records exactly what was resolved.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Should `.venv` be committed to Git?

1. Yes, always
2. No: commit `pyproject.toml` and `uv.lock`, and rebuild it with `uv sync`
3. Only on Windows

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does `uv run main.py` do before running the script?

1. Nothing special
2. Makes sure the environment matches the lock file
3. Upgrades every package to the latest version

<details markdown="1"><summary>Show answer</summary>
**B.** It keeps the environment in sync, then runs inside it.
</details>
</div>

## Summary

- One project = one **virtual environment** (`.venv`).
- `uv init` → `uv add <pkg>` → `uv run <script>`. Use `uv sync` to rebuild from the lock file.
- Commit `pyproject.toml`, `uv.lock` and `.python-version`. Never commit `.venv`.
- Recognise the classic `venv` + `pip` + `requirements.txt` workflow, and prefer uv for new projects.

!!! job "Job-ready check"
    **Interview question:** *"How do you make sure a Python project installs the same way on every machine?"*

    **Strong answer:** "Declare dependencies in `pyproject.toml`, lock exact versions in a lock file (with uv, `uv.lock`), pin the Python version, and commit all three. Everyone, including CI, runs `uv sync` to get an identical environment, and dependency changes go through `uv add` in a reviewed commit."

    **Mini project:** Create `sales-report` with uv, add pandas, and write `main.py` that reads `orders.csv` and prints net revenue (9,075). Commit `pyproject.toml` and `uv.lock`, and check that `.venv` is ignored.
