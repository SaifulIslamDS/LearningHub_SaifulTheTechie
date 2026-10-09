---
title: "Set Up Python and VS Code: Your Daily Workbench"
order: 1
summary: "Install Python and VS Code, choose the right interpreter, and run your first script from the editor and the terminal."
level: Beginner
time: "40 min"
topics: ["VS Code", "Python"]
keywords: [python install, python version, vs code, visual studio code, extension, pylance, interpreter, select interpreter, terminal, run python file, path, python 3.14]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip]
resources:
  - title: "Quick Start Guide for Python in VS Code"
    url: "https://code.visualstudio.com/docs/python/python-quick-start"
    source: "VS Code docs"
    note: "Official setup, running and debugging in a few minutes."
  - title: "Python extension for VS Code"
    url: "https://marketplace.visualstudio.com/items?itemName=ms-python.python"
    source: "Visual Studio Marketplace"
    note: "Lists the extensions it installs (Pylance, Python Debugger, Python Environments)."
  - title: "The Python Tutorial"
    url: "https://docs.python.org/3/tutorial/"
    source: "Python official docs"
    note: "The official, free Python tutorial."
  - title: "Status of Python versions"
    url: "https://devguide.python.org/versions/"
    source: "Python Developer's Guide"
    note: "Which versions are supported, and until when."
---

## What is it?

- **Python** is the language of data and AI work. You install an **interpreter**: the program that runs `.py` files.
- **VS Code** (Visual Studio Code) is a free code editor. With the **Python extension**, it understands Python: completion, error highlighting, running and debugging.

Think of Python as the engine and VS Code as the dashboard you drive it from.

!!! job "Why it matters at work"
    Every data engineering, data science and AI role assumes you can set up and run Python projects without help. VS Code is the most widely used editor for Python, and the same setup scales from a 10-line script to a production service.

## Step 1: install Python

Use **Python 3.14**, the current stable version. Python 3.15 is being released this month: wait until the libraries you need support it before switching.

| Your computer | Easiest way |
|---|---|
| **Windows** | Download the installer from <https://www.python.org/downloads/>. **Tick "Add python.exe to PATH"** on the first screen |
| **Mac** | The python.org installer, or `brew install python@3.14` |
| **Linux / WSL** | Use **uv** (next lesson): `uv python install 3.14` |

!!! tip "Already using uv?"
    uv can download and manage Python versions for you, per project. Many teams now use uv instead of installing Python by hand. The next lesson shows how.

Check it worked. Open a terminal (**Windows:** PowerShell; **Mac/Linux:** Terminal):

```bash
python --version
```

```text
Python 3.14.6
```

(On Mac and Linux the command may be `python3`. Your patch number may differ.)

## Step 2: install VS Code and the Python extension

1. Download VS Code from <https://code.visualstudio.com> and install it.
2. Open the **Extensions** view (**Ctrl+Shift+X**, Mac **Cmd+Shift+X**), search for **Python** (publisher: Microsoft), and click **Install**.
3. It automatically adds **Pylance** (code intelligence), **Python Debugger** and **Python Environments**.

## Step 3: open a folder and run a script

1. **File → Open Folder…**, then create or choose a folder such as `python-practice`.
2. Create a file `hello.py`:

```python
region = "Dhaka"
revenue = 3170
print(f"{region} net revenue: {revenue:,}")
```

3. Click the **▷ Run Python File** button at the top right of the editor. The **terminal** panel opens and shows:

```text
Dhaka net revenue: 3,170
```

You can also run it yourself in the terminal (**View → Terminal**, or **Ctrl+`**):

```bash
python hello.py
```

## Step 4: pick the right interpreter

VS Code needs to know **which** Python to use, because you may have several. Look at the **status bar** (bottom right), or run **Python: Select Interpreter** from the Command Palette (**Ctrl+Shift+P**). Choose 3.14, or the project's `.venv` interpreter once you've created one in the next lesson.

!!! mistake "\"It works in the terminal but not in VS Code\""
    That almost always means VS Code is using a different interpreter from your terminal. Select the right one (usually the project's `.venv`), and the import errors disappear.

## Useful VS Code habits

| Shortcut | Does |
|---|---|
| **Ctrl+Shift+P** | Command Palette: find any command by name |
| **Ctrl+P** | Open a file by name |
| **Ctrl+`** | Show or hide the terminal |
| **Shift+Enter** | Run the selected lines in the Python terminal |
| **F12** | Go to the definition of a function |
| **Ctrl+/** | Comment or uncomment lines |

(Mac: use **Cmd** instead of **Ctrl**.)

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Not ticking "Add to PATH" on Windows | `python` isn't recognised in the terminal | Re-run the installer → Modify → add to PATH, or use the `py` launcher |
| Opening a single file instead of a folder | No project settings, wrong interpreter | Always **File → Open Folder** |
| Several Pythons, wrong one selected | `ModuleNotFoundError` in VS Code only | **Python: Select Interpreter** |
| Installing the newest Python on day one | Some libraries aren't available yet | Use the current stable version that your libraries support |

## Try it yourself

**Task:** In `hello.py`, add two more variables, `target = 3600` and `achievement = revenue / target`, and print the achievement as a percentage with one decimal.

<details markdown="1">
<summary>Show a hint</summary>

An f-string with the `:.1%` format turns 0.8806 into `88.1%`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```python
region = "Dhaka"
revenue = 3170
target = 3600
achievement = revenue / target
print(f"{region} net revenue: {revenue:,}")
print(f"{region} achievement: {achievement:.1%}")
```

```text
Dhaka net revenue: 3,170
Dhaka achievement: 88.1%
```

That's the same 88.1% as the Power BI lesson.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. VS Code shows `ModuleNotFoundError`, but the same script works in your terminal. What's the most likely cause?

1. VS Code can't run Python
2. VS Code is using a different interpreter
3. The file is too long

<details markdown="1"><summary>Show answer</summary>
**B.** Select the same interpreter with **Python: Select Interpreter**.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which shortcut opens the Command Palette?

1. Ctrl+Shift+P
2. Ctrl+P
3. Ctrl+`

<details markdown="1"><summary>Show answer</summary>
**A.** Ctrl+P opens files, and Ctrl+` toggles the terminal.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Why might you wait before moving to a brand-new Python release?

1. New versions are slower
2. Some libraries may not support it yet
3. VS Code doesn't support it

<details markdown="1"><summary>Show answer</summary>
**B.** Libraries with compiled parts need time to publish builds for a new version.
</details>
</div>

## Summary

- Install the current stable **Python** (3.14 now), and check it with `python --version`.
- Install **VS Code** and the Microsoft **Python** extension (with Pylance, Debugger and Environments).
- Always **open a folder**, select the right **interpreter**, and run with ▷ or `python file.py`.
- Learn a handful of shortcuts: they save hours each month.

!!! job "Job-ready check"
    **Interview question:** *"A colleague's script runs on their laptop but fails on yours with an import error. What do you check?"*

    **Strong answer:** "First, which Python interpreter and environment I'm using, versus theirs. Then whether the project's dependencies are installed in that environment. A project file like `pyproject.toml` with a lock file, used with uv, prevents this by giving everyone the same versions."

    **Mini project:** Create a `python-practice` folder, open it in VS Code, and run `hello.py` both ways (▷ button and terminal). Take a screenshot showing the selected interpreter in the status bar.
