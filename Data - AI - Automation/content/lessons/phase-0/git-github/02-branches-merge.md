---
title: "Branches & Merge: Work on Changes Without Breaking Main"
order: 2
summary: "Create a branch for each change, merge it back, and calmly resolve a merge conflict when two branches edit the same line."
level: Beginner
time: "45 min"
topics: ["Branches & merge"]
prerequisites: ["phase-0/git-github/01-repos-commits"]
keywords: [git branch, git switch, git merge, fast-forward, merge commit, merge conflict, conflict markers, feature branch, main branch, git log graph, resolve conflict]
reviewed: 2026-10-09
resources:
  - title: "Git Branching — Basic Branching and Merging"
    url: "https://git-scm.com/book/en/v2"
    source: "Pro Git book (official)"
    note: "Chapter 3 explains branches, merges and conflicts with diagrams."
  - title: "Introduction to GitHub (interactive course)"
    url: "https://github.com/skills/introduction-to-github"
    source: "GitHub Skills"
    note: "Practise branches and merges in a real repository."
---

## What is it?

- A **branch** is a separate line of work. `main` holds the working version, and each new feature or fix gets its own branch.
- **Merging** brings a branch's commits back into `main`.
- A **merge conflict** happens when two branches change the **same lines** differently, and Git asks you to decide.

```text
main:     A---B---C-----------M
                   \         /
feature:            D---E---
```

!!! job "Why it matters at work"
    Teams never edit `main` directly. Every change, whether a new SQL model, a dashboard measure or a bug fix, goes on a branch, is reviewed in a pull request (next lesson) and is merged. Resolving conflicts without panic is a basic expectation in any engineering team.

## Example 1: create a branch and commit on it

```bash
git switch -c feature/achievement      # create the branch and move to it
```

```text
Switched to a new branch 'feature/achievement'
```

Add the line `print("Achievement: 94.5%")` to `report.py`, then commit:

```bash
git commit -am "Add achievement %"
git branch          # list branches; * marks where you are
```

## Example 2: merge it back (fast-forward)

```bash
git switch main
git merge feature/achievement
```

```text
Updating fcc10c8..4457684
Fast-forward
 report.py | 1 +
 1 file changed, 1 insertion(+)
```

**Fast-forward** means `main` hadn't moved, so Git simply moved `main` forward to the branch's commit. Delete the finished branch:

```bash
git branch -d feature/achievement
```

```text
Deleted branch feature/achievement (was 4457684).
```

## Example 3: a merge conflict, step by step

Two people rename the same label. On `feature/a` the first line becomes `print("Net revenue Q1: 9,075")`. Meanwhile, on `main` it becomes `print("Quarter 1 net revenue: 9,075")`. Merge:

```bash
git merge feature/a
```

```text
Auto-merging report.py
CONFLICT (content): Merge conflict in report.py
Automatic merge failed; fix conflicts and then commit the result.
```

Open `report.py`:

```text
<<<<<<< HEAD
print("Quarter 1 net revenue: 9,075")
=======
print("Net revenue Q1: 9,075")
>>>>>>> feature/a
print("Q1 target: 9,600")
print("Achievement: 94.5%")
```

| Marker | Means |
|---|---|
| `<<<<<<< HEAD` … `=======` | Your current branch's version (`main`) |
| `=======` … `>>>>>>> feature/a` | The incoming branch's version |

`git status --short` shows `UU report.py` (both modified, unmerged).

**Resolve it:** edit the file into the version you want (keep one, the other, or combine them), **delete all three marker lines**, then:

```bash
git add report.py
git commit -m "Merge feature/a: keep short label"
```

!!! tip "VS Code helps"
    VS Code highlights conflicts with buttons: **Accept Current**, **Accept Incoming**, **Accept Both**, or the **Merge Editor**. Always read the result before committing.

## Example 4: see the history as a graph

```bash
git log --oneline --graph
```

```text
*   cc21d45 Merge feature/a: keep short label
|\
| * 4cb03c8 Rename label (a)
* | ba472ca Rename label (main)
|/
* 4457684 Add achievement %
* fcc10c8 Show Q1 target
* 91fa0f4 Ignore logs and venv
* 50ff5b0 Add Q1 revenue report
```

The two lines of work split and come back together in a **merge commit**.

## Branch naming

| Type | Example |
|---|---|
| New feature | `feature/region-filter` |
| Bug fix | `fix/cancelled-in-average` |
| Documentation | `docs/readme-setup` |
| Experiment | `exp/llm-summary` |

Short, lowercase, hyphens, one purpose per branch.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Working directly on `main` | Unreviewed changes, harder to undo | `git switch -c <branch>` before you start |
| Long-lived branches | Big, painful conflicts | Merge small branches often |
| Committing conflict markers | Broken code (`SyntaxError` on `<<<<<<<`) | Search for `<<<<<<<` before `git add` |
| Switching branches with unsaved edits | Git refuses, or edits follow you | Commit first, or `git stash` |
| Panicking mid-conflict | Random edits | `git merge --abort` returns to before the merge |

## Try it yourself

**Task:** Create `fix/label-case` from `main`, change `Achievement` to `Q1 achievement`, commit, switch to `main`, merge, and delete the branch. Was it a fast-forward?

<details markdown="1">
<summary>Show the solution</summary>

```bash
git switch -c fix/label-case
# edit report.py
git commit -am "Clarify achievement label"
git switch main
git merge fix/label-case
git branch -d fix/label-case
```

Yes: `main` had no new commits since you branched, so Git prints **Fast-forward**.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What creates a new branch and switches to it?

1. `git branch -d name`
2. `git switch -c name`
3. `git merge name`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. When does a merge conflict happen?

1. Whenever you merge
2. When both branches changed the same lines differently
3. When a branch has more than 3 commits

<details markdown="1"><summary>Show answer</summary>
**B.** Changes to different lines or files merge automatically.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. You're mid-conflict and want to start over. What do you run?

1. `git merge --abort`
2. `rm -rf .git`
3. `git commit -m "conflict"`

<details markdown="1"><summary>Show answer</summary>
**A.** It restores the state from before the merge.
</details>
</div>

## Summary

- One branch per change: `git switch -c feature/x`.
- `git merge` brings it back. **Fast-forward** if `main` didn't move, otherwise a **merge commit**.
- Conflicts: read the markers, edit, delete the markers, `git add`, `git commit`.
- `git log --oneline --graph` shows how branches split and join.

!!! job "Job-ready check"
    **Interview question:** *"How do you handle a merge conflict?"*

    **Strong answer:** "I read both versions between the markers, decide the correct result, often by talking to whoever wrote the other change, remove the markers, run the tests, then stage and commit. To avoid conflicts, I keep branches small and merge `main` into them often."

    **Mini project:** Recreate the conflict from Example 3 in your own repo, resolve it with VS Code's merge buttons, and save the `git log --oneline --graph` output in your notes.
