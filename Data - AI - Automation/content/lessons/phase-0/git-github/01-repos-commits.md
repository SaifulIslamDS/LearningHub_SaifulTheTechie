---
title: "Git Repositories & Commits: Save Your Work in Safe Steps"
order: 1
summary: "Create a repository, stage and commit changes, ignore files that don't belong, and read the history with status, diff and log."
level: Beginner
time: "45 min"
topics: ["Repositories & commits"]
prerequisites: ["phase-0/dev-environment/01-vscode-python"]
keywords: [git, repository, repo, commit, git init, git status, git add, staging area, git commit, git log, git diff, .gitignore, commit message, version control, restore]
reviewed: 2026-10-09
resources:
  - title: "Pro Git book (free)"
    url: "https://git-scm.com/book/en/v2"
    source: "git-scm.com (official)"
    note: "Chapters 1–2 cover everything in this lesson."
  - title: "Introduction to GitHub (interactive course)"
    url: "https://github.com/skills/introduction-to-github"
    source: "GitHub Skills"
    note: "Free, hands-on course inside a real repository."
---

## What is it?

- A **repository (repo)** is a project folder whose history Git tracks. The history lives in a hidden `.git` folder.
- A **commit** is a saved snapshot of your files, with a message, an author and a unique ID (like `50ff5b0`).
- The **staging area** sits between your files and a commit: you choose *which* changes go into the next snapshot.

```text
working folder  --git add-->  staging area  --git commit-->  history
 (you edit)                   (next snapshot)                (saved forever)
```

!!! job "Why it matters at work"
    Every data, analytics and AI team keeps SQL, Python, notebooks, dbt models and even Power BI projects in Git. Small commits with clear messages let you undo mistakes, explain what changed, and show reviewers your work. "Is your code on GitHub?" is a standard hiring question.

## Example 1: create a repository and the first commit

```bash
git init sales-report
cd sales-report
```

Create `report.py` with one line: `print("Q1 net revenue: 9,075")`. Then ask Git what it sees:

```bash
git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	report.py

nothing added to commit but untracked files present (use "git add" to track)
```

Stage the file, then commit it:

```bash
git add report.py
git commit -m "Add Q1 revenue report"
```

```text
[main (root-commit) 50ff5b0] Add Q1 revenue report
 1 file changed, 1 insertion(+)
 create mode 100644 report.py
```

*(Your commit ID will be different: it depends on time, author and content.)*

## Example 2: ignore files that don't belong

Logs, virtual environments and caches should never be committed. Create a `.gitignore` file:

```text
.venv/
*.log
__pycache__/
```

Now a `run.log` file is invisible to Git. `git status --short` shows only the new `.gitignore`:

```text
?? .gitignore
```

`??` = untracked, `A` = staged (added), `M` = modified, `UU` = conflict (next lesson).

!!! warning "Never commit secrets"
    Passwords, API keys and `.env` files must go in `.gitignore` **before** the first commit. Once pushed, assume a secret is leaked: change it.

## Example 3: see what changed with `git diff`

Add a second line, `print("Q1 target: 9,600")`, then run `git diff`:

```text
diff --git a/report.py b/report.py
index 4fd8f9d..ba4f1d5 100644
--- a/report.py
+++ b/report.py
@@ -1 +1,2 @@
 print("Q1 net revenue: 9,075")
+print("Q1 target: 9,600")
```

Lines starting with `+` were added, and `-` were removed. Commit it: `git commit -am "Show Q1 target"` (`-a` stages every already-tracked file that changed).

## Example 4: read the history

```bash
git log --oneline
```

```text
fcc10c8 Show Q1 target
91fa0f4 Ignore logs and venv
50ff5b0 Add Q1 revenue report
```

Newest first. Each line is one commit you can inspect (`git show fcc10c8`) or return to.

## Undo cheatsheet

| You want to… | Command |
|---|---|
| Throw away unsaved edits to a file | `git restore report.py` |
| Unstage a file (keep the edits) | `git restore --staged report.py` |
| Fix the message of the last commit (not yet pushed) | `git commit --amend -m "Better message"` |
| Undo a pushed commit safely | `git revert <id>` (creates a new "undo" commit) |

## Good commit messages

| Weak | Strong |
|---|---|
| `update` | `Add Q1 target to revenue report` |
| `fix stuff` | `Exclude cancelled orders from average` |
| `final version 2` | `Rename region column to match SQL schema` |

Rule of thumb: **imperative mood, under ~60 characters, says *what* and *why*.** One logical change per commit.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `git add .` without checking | Logs, data dumps or secrets get committed | `git status` first, and keep a good `.gitignore` |
| Huge commits ("did everything") | Hard to review or undo | Small commits, one idea each |
| Committing large data files | A slow, bloated repo | Keep samples only, or use storage outside Git |
| Forgetting `git config user.name/email` | Commits with the wrong author | Set them once per computer |
| Running `git init` inside another repo | Confusing nested repositories | One repo per project folder |

## Try it yourself

**Task:** In your `sales-report` repo, add a line `print("Achievement: 94.5%")`, commit it with a good message, then show the last **two** commits only.

<details markdown="1">
<summary>Show a hint</summary>

`git log` accepts `-n 2` (or simply `-2`).
</details>

<details markdown="1">
<summary>Show the solution</summary>

```bash
git commit -am "Add Q1 achievement percentage"
git log --oneline -2
```

The newest commit is on top, followed by `Show Q1 target`.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `git add report.py` do?

1. Saves a commit
2. Puts the file's current changes in the staging area for the next commit
3. Uploads the file to GitHub

<details markdown="1"><summary>Show answer</summary>
**B.** `git commit` saves the snapshot, and `git push` uploads it.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which file stops `run.log` and `.venv/` from being tracked?

1. `README.md`
2. `.gitignore`
3. `pyproject.toml`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. You pushed a bad commit to a shared branch. What's the safe way to undo it?

1. `git revert <id>`
2. Delete the `.git` folder
3. `git commit --amend` and force-push

<details markdown="1"><summary>Show answer</summary>
**A.** Revert adds a new commit that undoes the change, without rewriting shared history.
</details>
</div>

## Summary

- `git init` creates a repo; `git status` tells you what Git sees.
- `git add` → staging area → `git commit -m "..."` → history.
- `.gitignore` keeps logs, environments and secrets out.
- `git diff` shows changes; `git log --oneline` shows history.
- Small commits with clear, imperative messages.

!!! job "Job-ready check"
    **Interview question:** *"What's the difference between `git add`, `git commit` and `git push`?"*

    **Strong answer:** "`add` stages chosen changes, `commit` saves them as a snapshot in my local history with a message, and `push` sends my commits to the remote repository, such as GitHub, so others can see them."

    **Mini project:** Put your `python-practice` folder from the first lesson under Git: a `.gitignore`, at least three small commits, and a `git log --oneline` that tells the story.
