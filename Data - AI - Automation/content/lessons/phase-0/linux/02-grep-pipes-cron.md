---
title: "grep, sort & Pipes, then cron: Answer Questions and Automate Jobs"
order: 2
summary: "Search logs and CSVs with grep, chain commands with pipes to count and rank, redirect output to files, and schedule a script to run every day with cron."
level: Beginner
time: "50 min"
topics: ["grep, sort & pipes", "cron concepts"]
prerequisites: ["phase-0/linux/01-filesystem-terminal"]
keywords: [grep, pipe, "|", sort, uniq, uniq -c, cut, wc, redirect, ">", ">>", "2>", stderr, stdout, log analysis, cron, crontab, schedule, shell script, set -euo pipefail, bash script]
reviewed: 2026-10-09
files: [phase-0/linux-practice.zip]
resources:
  - title: "The Shell — pipes and redirection (Missing Semester)"
    url: "https://missing.csail.mit.edu/2026/course-shell/"
    source: "MIT — The Missing Semester of Your CS Education"
    note: "Pipes, redirection and shell scripting basics."
  - title: "crontab.guru"
    url: "https://crontab.guru"
    source: "crontab.guru"
    note: "Type a cron schedule and read it back in plain English."
  - title: "The Linux command line for beginners"
    url: "https://ubuntu.com/tutorials/command-line-for-beginners"
    source: "Ubuntu (Canonical)"
    note: "Includes pipes and redirection."
---

## What is it?

- **`grep`** finds lines that contain a pattern.
- A **pipe `|`** sends one command's output into the next command. Small tools chain into a data pipeline: `cut` → `sort` → `uniq -c` → `sort -rn`.
- **Redirection** saves output: `>` overwrites a file, `>>` appends, `2>` captures error messages.
- **cron** runs commands on a schedule (every day at 06:00, every Monday…).

!!! job "Why it matters at work"
    "Why did last night's job fail?" is answered by grepping logs. Quick counts with pipes let you sanity-check a file in seconds, before opening Python. And many data jobs still run on cron, or on schedulers (Airflow, GitHub Actions) that use **the same cron syntax**.

All examples run in `~/practice` from [linux-practice.zip](../../../downloads/phase-0/linux-practice.zip).

## Example 1: grep a log

The log `logs/cleaner-2026-03.log` has 10 days of CSV-cleaner runs.

```bash
grep ERROR logs/cleaner-2026-03.log
```

```text
2026-03-03 06:00:00,951 ERROR csv_cleaner: Input file not found: data/orders_raw.csv
2026-03-06 06:00:00,977 ERROR csv_cleaner: Missing required columns: Status
2026-03-09 06:00:00,932 ERROR csv_cleaner: Input file not found: data/orders_raw.csv
```

| Option | Does | Example → result |
|---|---|---|
| `-c` | Count matching lines | `grep -c ERROR logs/cleaner-2026-03.log` → `3` |
| `-i` | Ignore case | `grep -ci warning logs/cleaner-2026-03.log` → `3` |
| `-v` | Lines that **don't** match | `grep -v INFO logs/cleaner-2026-03.log` |
| `-h` | Hide file names (several files) | `grep -h Dhaka data/monthly/*.csv` |
| `-E` | Several patterns | `grep -E 'ERROR|WARNING' …` |
| `-r` | Search all files in folders | `grep -r "TODO" src/` |

## Example 2: pipes — count and rank

**How many orders per status?** Take column 9, drop the header, sort, count:

```bash
cut -d, -f9 data/orders.csv | tail -n +2 | sort | uniq -c
```

```text
      1 Cancelled
      8 Delivered
      1 Pending
      2 Shipped
```

**Which region has the most orders?** Add `sort -rn` (numeric, largest first):

```bash
cut -d, -f4 data/orders.csv | tail -n +2 | sort | uniq -c | sort -rn
```

```text
      5 Dhaka
      3 Chattogram
      2 Narayanganj
      2 Gazipur
```

| Piece | Job |
|---|---|
| `cut -d, -f4` | Column 4, using comma as the delimiter |
| `tail -n +2` | Start from line 2 (skip the header) |
| `sort` | Group identical values together (`uniq` needs this) |
| `uniq -c` | Count each group |
| `sort -rn` | Rank by count, descending |

The same numbers you got with `GROUP BY` in SQL and a PivotTable in Excel.

!!! warning "Know the limits"
    `cut -d,` breaks on quoted CSV fields that contain commas (`"Dhaka, North"`). For quick checks it's great; for real processing, use Python or SQL.

**Which error types happened?**

```bash
grep ERROR logs/cleaner-2026-03.log | cut -d: -f4 | sort | uniq -c
```

```text
      2  Input file not found
      1  Missing required columns
```

**Which days had problems?**

```bash
grep -E 'ERROR|WARNING' logs/cleaner-2026-03.log | cut -c1-10 | sort -u
```

```text
2026-03-03
2026-03-04
2026-03-06
2026-03-07
2026-03-09
```

## Example 3: redirect output to files

```bash
grep ERROR logs/cleaner-2026-03.log > reports/errors.txt      # create/overwrite
grep WARNING logs/cleaner-2026-03.log >> reports/errors.txt   # append
wc -l reports/errors.txt
```

```text
6 reports/errors.txt
```

Programs write normal output to **stdout** and errors to **stderr**. Redirect them separately:

```bash
ls missing.csv 2> reports/err.txt
cat reports/err.txt
```

```text
ls: cannot access 'missing.csv': No such file or directory
```

`command > out.log 2>&1` sends **both** into one file, which is exactly what scheduled jobs do.

## Part 4: a shell script for a scheduled job

`scripts/daily_clean.sh` runs the CSV cleaner (the Phase 0 project) and logs the result:

```bash
#!/usr/bin/env bash
# Run the CSV cleaner every day and keep a log. Used in the cron lesson.
set -euo pipefail                      # stop on errors, unset variables and failed pipes

cd "$HOME/practice"                    # always start from a known folder
echo "$(date '+%F %T') starting daily clean" >> logs/cron.log
uv run --project "$HOME/csv-cleaner" csv-clean data/orders_raw.csv \
    -c "$HOME/csv-cleaner/config.toml" \
    -o "reports/orders_$(date +%F).csv" >> logs/cron.log 2>&1
```

| Line | Why |
|---|---|
| `#!/usr/bin/env bash` | "Run me with bash" |
| `set -euo pipefail` | Fail fast instead of carrying on after an error |
| `cd "$HOME/practice"` | cron starts in your home folder, so never rely on relative paths |
| `$(date +%F)` | Today's date (`2026-10-09`) in the file name |
| `>> logs/cron.log 2>&1` | Keep every run's output and errors for later grepping |

Make it executable and test it by hand **before** scheduling: `chmod +x scripts/daily_clean.sh && ./scripts/daily_clean.sh`.

## Part 5: cron concepts

Edit your schedule with `crontab -e`, and list it with `crontab -l`. Each line is **5 time fields + a command**:

```text
┌──────── minute (0–59)
│ ┌────── hour (0–23)
│ │ ┌──── day of month (1–31)
│ │ │ ┌── month (1–12)
│ │ │ │ ┌ day of week (0–6, Sunday = 0)
│ │ │ │ │
0 6 * * * $HOME/practice/scripts/daily_clean.sh
```

| Schedule | Meaning |
|---|---|
| `0 6 * * *` | Every day at 06:00 |
| `30 7 * * 1-5` | Weekdays at 07:30 |
| `0 */4 * * *` | Every 4 hours, on the hour |
| `0 9 1 * *` | 09:00 on the 1st of every month |

Check any schedule at [crontab.guru](https://crontab.guru).

!!! tip "cron isn't your terminal"
    cron runs with a **minimal environment**: a short `PATH`, no aliases, your home as the folder, and a server time zone that may be UTC. Use full paths, log everything, and test by hand. On WSL, cron only runs while WSL is running. GitHub Actions and Airflow use this same 5-field syntax.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `uniq -c` without `sort` first | Counts split across groups | Always `sort | uniq -c` |
| Forgetting to skip the header | "status" counted as a value | `tail -n +2` |
| `>` when you meant `>>` | Yesterday's log is overwritten | `>>` for logs |
| Relative paths in cron jobs | "No such file" at 06:00 | `cd` to a known folder, or use absolute paths |
| No logging in scheduled jobs | Silent failures | `>> job.log 2>&1`, then grep it |

## Try it yourself

**Task:** Using only the log file and pipes, find the **total number of rows written** across all runs in March.

<details markdown="1">
<summary>Show a hint</summary>

`grep -o 'written: [0-9]*'` prints only the matching part. Then keep the number, and add them up with `paste -sd+ | bc`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```bash
grep -o 'written: [0-9]*' logs/cleaner-2026-03.log | cut -d' ' -f2 | paste -sd+ | bc
```

```text
103
```

Seven successful runs: 12 + 13 + 14 + 15 + 15 + 17 + 17 = 103. (The three ERROR days wrote nothing.)
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `|` do?

1. Saves output to a file
2. Sends one command's output into the next command
3. Runs two commands at the same time, unrelated

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. When does `0 6 * * 1-5` run?

1. Every day at 06:00
2. At 06:00, Monday to Friday
3. On the 6th of each month

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. Which keeps the old contents of `job.log` and adds new output?

1. `> job.log`
2. `>> job.log`
3. `2> job.log`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- `grep` (with `-c`, `-i`, `-v`, `-E`) finds lines in logs and data.
- Pipes chain small tools: `cut | tail -n +2 | sort | uniq -c | sort -rn` = a quick GROUP BY.
- `>` overwrites, `>>` appends, `2>` captures errors, `2>&1` merges both.
- Scheduled scripts use `set -euo pipefail`, full paths and logging.
- cron: 5 fields + command. Check it at crontab.guru, and test by hand first.

!!! job "Job-ready check"
    **Interview question:** *"A nightly job failed. How do you find out what happened?"*

    **Strong answer:** "I check the job's log: `grep -E 'ERROR|WARNING'` for the failing night, then look at the lines around it with `grep -C 3`. I count how often it happens with `grep -c` across days to see if it's new or recurring, fix the cause, and make sure the job logs enough context next time."

    **Mini project:** Write `scripts/error_report.sh` that writes today's date, the number of ERROR lines, and the error types (with counts) to `reports/error_report.txt`. Schedule it in cron for 07:00 on weekdays, and paste the crontab line into your notes.
