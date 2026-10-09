---
title: "Debugging: Read Tracebacks and Use Breakpoints Instead of Guessing"
order: 3
summary: "Read Python error messages, then use VS Code's debugger to pause code, inspect variables and step through logic until the bug is obvious."
level: Beginner
time: "40 min"
topics: ["Debugging"]
prerequisites: ["phase-0/dev-environment/01-vscode-python"]
keywords: [debugging, debugger, breakpoint, traceback, stack trace, keyerror, step over, step into, watch, variables, debug console, pdb, breakpoint(), logic bug]
reviewed: 2026-10-09
files: [phase-0/python-refresher.zip]
resources:
  - title: "Python debugging in VS Code"
    url: "https://code.visualstudio.com/docs/python/debugging"
    source: "VS Code docs"
    note: "Breakpoints, stepping, watch expressions and launch configurations."
  - title: "Errors and Exceptions (Python tutorial)"
    url: "https://docs.python.org/3/tutorial/errors.html"
    source: "Python official docs"
    note: "How to read and handle exceptions."
---

## What is it?

**Debugging** means finding out *why* code does something different from what you expect. There are two kinds of bug:

| Kind | What you see | Example |
|---|---|---|
| **Crash** | A **traceback** (error message) and the program stops | `KeyError: 'Status'` |
| **Logic bug** | The program runs, but the answer is **wrong** | The average is 447.50 but should be 516.67 |

A **debugger** lets you pause the program on any line (a **breakpoint**), look at every variable, and run one line at a time.

!!! job "Why it matters at work"
    Data pipelines rarely crash politely. More often, they quietly produce a wrong number. Engineers who can isolate a bug in minutes, instead of scattering `print()` everywhere, are noticeably more productive, and "walk me through how you'd debug this" is a common interview exercise.

## The practice script

Open `debug_me.py` from [python-refresher.zip](../../../downloads/phase-0/python-refresher.zip). It has **two bugs**:

```python
orders = [
    {"order_id": 1, "value": 420.0, "status": "Delivered"},
    {"order_id": 4, "value": 240.0, "status": "Cancelled"},
    {"order_id": 7, "value": 320.0, "status": "Shipped"},
    {"order_id": 9, "value": 810.0, "status": "Pending"},
]


def average_order_value(rows):
    # Business rule: cancelled orders don't count
    total = 0
    count = 0
    for row in rows:
        total += row["value"]
        count += 1
    return total / count


def open_orders(rows):
    return [r["order_id"] for r in rows if r["Status"] in ("Shipped", "Pending")]


print("Average order value:", average_order_value(orders))
print("Open orders:", open_orders(orders))
```

Run it:

```text
Average order value: 447.5
Traceback (most recent call last):
  File "debug_me.py", line 26, in <module>
    print("Open orders:", open_orders(orders))
                          ~~~~~~~~~~~^^^^^^^^
  File "debug_me.py", line 22, in open_orders
    return [r["order_id"] for r in rows if r["Status"] in ("Shipped", "Pending")]
                                           ~^^^^^^^^^^
KeyError: 'Status'
```

## Step 1: read the traceback from the bottom up

1. **Last line = what went wrong:** `KeyError: 'Status'`. The code asked a dictionary for a key that doesn't exist.
2. **The line above = where:** `line 22, in open_orders`, and the `^^^` markers point at `r["Status"]`.
3. **Higher lines = how we got there:** line 26 called `open_orders(...)`.

The keys are lowercase: `"status"`. Fix line 22, run it again, and the crash is gone. That was **bug 2**.

## Step 2: find the logic bug with the debugger

The average prints **447.5**, but the business rule says to skip cancelled orders: (420 + 320 + 810) ÷ 3 = **516.67**. There's no error message, so this is a logic bug. Use the debugger:

1. Click in the **gutter** left of the line `total += row["value"]`. A **red dot** (breakpoint) appears.
2. Press **F5** → choose **Python File**. The program **pauses** on that line.
3. Look at the **Variables** panel: `row`, `total` and `count`.
4. Press **F10 (Step Over)** a few times, and watch `total` and `count` change on each loop.
5. On the second loop, `row` is `{'order_id': 4, 'value': 240.0, 'status': 'Cancelled'}`, and it's **still added**. Found it: nothing implements the rule in the comment.

| Key | Action |
|---|---|
| **F5** | Start, or continue to the next breakpoint |
| **F10** | Step over: run the current line |
| **F11** | Step into: go inside a function call |
| **Shift+F11** | Step out: finish the current function |
| **Shift+F5** | Stop debugging |

!!! tip "Watch and Debug Console"
    In the **Watch** panel, add an expression like `total / max(count, 1)` to see it update live. In the **Debug Console**, type any Python, for example `[r["status"] for r in rows]`, while paused.

## Step 3: fix and confirm

```python
for row in rows:
    if row["status"] == "Cancelled":
        continue
    total += row["value"]
    count += 1
```

```text
Average order value: 516.67
Open orders: [7, 9]
```

*(The fixed file is `solutions/debug_me_fixed.py`, which rounds to 2 decimals.)*

## No editor? Use `breakpoint()`

Add `breakpoint()` on any line and run the script in a terminal. Python stops there in **pdb**, the built-in debugger. Type `p total` to print a variable, `n` for the next line, `c` to continue, and `q` to quit. It's useful on servers where you only have a terminal.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Reading a traceback from the top | You get lost in library internals | Start at the **last line**, then find **your** file in the lines above |
| Changing code randomly until it works | New bugs, and no understanding | Reproduce → pause → inspect → fix → re-run |
| Dozens of `print()` statements left in | Noisy output, and forgotten debug code | Breakpoints, or proper logging (in the CLI project) |
| Fixing without a check | The bug returns later | Add a test for it (Testing module) |
| Ignoring a "no error" wrong number | Wrong reports go out | Compare with a known answer (here 516.67) |

## Try it yourself

**Task:** With both bugs fixed, add a breakpoint **inside** `open_orders`, so you're paused in the list comprehension. Use the **Debug Console** to evaluate `[r["status"] for r in rows]`. What do you see, and how does it confirm the result `[7, 9]`?

<details markdown="1">
<summary>Show the solution</summary>

The Debug Console shows `['Delivered', 'Cancelled', 'Shipped', 'Pending']`. Only orders 7 (Shipped) and 9 (Pending) match `("Shipped", "Pending")`, so the result is `[7, 9]`. Evaluating expressions while paused is often faster than stepping line by line.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Where do you start reading a Python traceback?

1. The first line
2. The last line (the error type and message)
3. The middle

<details markdown="1"><summary>Show answer</summary>
**B.** The last line says *what* went wrong, and the lines above say *where*.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Your code runs without errors but returns the wrong total. What kind of bug is it, and what's the best tool?

1. A crash: read the traceback
2. A logic bug: use breakpoints and inspect the variables
3. A syntax error: reinstall Python

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which key runs the current line and moves to the next one, without going inside function calls?

1. F5
2. F10
3. F11

<details markdown="1"><summary>Show answer</summary>
**B — F10, Step Over.** F11 steps into functions.
</details>
</div>

## Summary

- **Crashes** give a traceback: read it **bottom-up** to find the error and your line.
- **Logic bugs** give wrong answers: pause with a **breakpoint** (F5), inspect **Variables**, step with **F10/F11**.
- Use **Watch** and the **Debug Console** to test ideas while paused, and `breakpoint()` in a terminal.
- Confirm every fix against a known answer, and later with a test.

!!! job "Job-ready check"
    **Interview question:** *"A report's average looks too low, but there are no errors. How do you investigate?"*

    **Strong answer:** "I'd reproduce it with a small input whose correct answer I know, set a breakpoint in the calculation, and step through, watching the running total and count. That shows which rows are included. Here, cancelled orders were being counted. After fixing it, I'd add a test with a cancelled order so it can't come back."

    **Mini project:** Plant a bug of your own in `01_basics.py` (for example, change `>=` to `>`). Ask a friend, or yourself tomorrow, to find it using only the debugger, and note how many steps it took.
