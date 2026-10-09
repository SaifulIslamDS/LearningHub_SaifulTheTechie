---
title: "Linux Filesystem & Terminal Workflow: Move Around Like an Engineer"
order: 1
summary: "Navigate the Linux filesystem, create, copy, move and inspect files, understand paths and permissions, and build fast terminal habits (on Windows, through WSL)."
level: Beginner
time: "45 min"
topics: ["Filesystem", "Terminal workflow"]
prerequisites: ["phase-0/dev-environment/01-vscode-python"]
keywords: [linux, bash, terminal, shell, wsl, ubuntu, filesystem, path, absolute path, relative path, home directory, pwd, ls, cd, mkdir, cp, mv, rm, cat, head, tail, less, wc, permissions, chmod, tab completion, history]
reviewed: 2026-10-09
files: [phase-0/linux-practice.zip]
resources:
  - title: "Install Linux on Windows with WSL"
    url: "https://learn.microsoft.com/en-us/windows/wsl/install"
    source: "Microsoft Learn"
    note: "One command: wsl --install."
  - title: "The Shell (Missing Semester)"
    url: "https://missing.csail.mit.edu/2026/course-shell/"
    source: "MIT — The Missing Semester of Your CS Education"
    note: "Free lecture notes and video on shell basics."
  - title: "The Linux command line for beginners"
    url: "https://ubuntu.com/tutorials/command-line-for-beginners"
    source: "Ubuntu (Canonical)"
    note: "A gentle, step-by-step tutorial."
---

## What is it?

- The **terminal** (also called the shell; usually **bash**) lets you control a computer by typing commands instead of clicking.
- The **filesystem** is the tree of folders and files, starting at `/` (the **root**). Your personal folder is your **home**, written `~` (for example `/home/learner`).

```text
/
├── home/
│   └── learner/        ← ~  (your home)
│       └── practice/
│           ├── data/
│           └── logs/
├── etc/                ← system settings
└── tmp/                ← temporary files
```

!!! job "Why it matters at work"
    Servers, cloud machines, Docker containers and CI runners almost all run Linux, usually with **no graphical interface**. Data engineers check logs, move files and schedule jobs from the terminal every day, and AI coding agents run terminal commands that you must be able to read and verify.

## Get a Linux terminal

| Your computer | Do this |
|---|---|
| **Windows** | Open PowerShell as admin and run `wsl --install`, then restart. You get **Ubuntu** inside Windows. In VS Code, install the **WSL** extension to edit files there |
| **Mac** | Open **Terminal**. macOS uses zsh, which is almost identical for these lessons |
| **Linux** | Open **Terminal** |

Then download [linux-practice.zip](../../../downloads/phase-0/linux-practice.zip) and unzip it into your home folder as `~/practice`. (In WSL, Windows downloads are under `/mnt/c/Users/<you>/Downloads/`.)

```bash
cd ~
unzip /mnt/c/Users/<you>/Downloads/linux-practice.zip   # WSL example
```

## Example 1: where am I, and what's here?

```bash
cd ~/practice
pwd
```

```text
/home/learner/practice
```

```bash
ls
```

```text
README.md
data
logs
reports
scripts
```

```bash
ls -lh data        # -l long format, -h human-readable sizes
```

```text
total 12K
drwxr-xr-x 2 learner learner 4.0K Oct  9 09:52 monthly
-rw-r--r-- 1 learner learner  963 Oct  9 09:52 orders.csv
-rw-r--r-- 1 learner learner 1.1K Oct  9 09:52 orders_raw.csv
```

The first column starts with `d` for a directory and `-` for a file, followed by the **permissions** (see below).

## Paths: absolute vs relative

| Path | Meaning |
|---|---|
| `/home/learner/practice/data` | **Absolute**: starts at `/`, works from anywhere |
| `data/orders.csv` | **Relative**: from the current folder |
| `.` | The current folder |
| `..` | The parent folder |
| `~` | Your home folder |

```bash
cd data        # go into data
cd ..          # back up one level
cd ~           # home (or just: cd)
cd -           # back to the previous folder
```

## Example 2: create, copy, move and delete

```bash
mkdir -p reports/2026/q1              # -p creates all missing parent folders
cp data/orders.csv reports/2026/q1/   # copy
mv reports/2026/q1/orders.csv reports/2026/q1/orders_q1.csv   # move = rename
ls -R reports                          # -R lists sub-folders too
```

```text
reports:
2026

reports/2026:
q1

reports/2026/q1:
orders_q1.csv
```

```bash
rm reports/2026/q1/orders_q1.csv      # delete a file
rm -r reports/2026                    # delete a folder and everything in it
```

!!! warning "There is no recycle bin"
    `rm` deletes immediately and permanently. Double-check the path, never run `rm -rf` on a path built from a variable you haven't printed, and use `ls` on the same path first.

## Example 3: look inside files

```bash
head -3 data/orders.csv     # first 3 lines
```

```text
order_id,order_date,customer,region,category,product,quantity,unit_price,status
1,2026-01-05,Rahim Traders,Dhaka,Fabric,Cotton Twill,120,3.50,Delivered
2,2026-01-08,Karim Garments,Chattogram,Trims,Metal Buttons,5000,0.04,Delivered
```

```bash
tail -2 data/orders.csv     # last 2 lines
wc -l data/orders.csv data/orders_raw.csv   # count lines
```

```text
11,2026-03-03,Sun Fashion,Narayanganj,Trims,Zippers,1500,0.28,Delivered
12,2026-03-09,Karim Garments,Chattogram,Fabric,Denim 12oz,250,5.10,Shipped
  13 data/orders.csv
  15 data/orders_raw.csv
  28 total
```

13 lines = 1 header + **12 orders**, the same 12 as in SQL, Excel and Power BI.

| Command | Use it for |
|---|---|
| `cat file` | Print a small file |
| `less file` | Scroll a big file (`q` to quit, `/word` to search) |
| `head -n 20` / `tail -n 20` | Start or end of a file |
| `tail -f app.log` | Watch a log grow live (Ctrl+C to stop) |
| `wc -l` | Count lines (rows) |

## Permissions in one minute

`-rw-r--r--` = **owner** can read/write, **group** can read, **others** can read. A script needs **x** (execute) to run:

```bash
chmod +x scripts/daily_clean.sh
ls -l scripts
```

```text
total 4
-rwxr-xr-x 1 learner learner 492 Oct  9 09:52 daily_clean.sh
```

## Terminal workflow habits

| Habit | How |
|---|---|
| **Tab completion** | Type `cd da` + **Tab** → `cd data/`. Fewer typos |
| **History** | **↑** repeats previous commands; **Ctrl+R** searches them |
| **Stop a command** | **Ctrl+C** |
| **Clear the screen** | **Ctrl+L** or `clear` |
| **Help** | `man ls`, or `ls --help` |
| **Open the folder in VS Code** | `code .` |
| **Chain commands** | `mkdir out && cd out` (the second runs only if the first succeeds) |

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Spaces in file names (`my file.csv`) | Commands treat it as two files | Use quotes (`"my file.csv"`), or better, no spaces |
| Working in Windows folders from WSL (`/mnt/c/...`) | Slow, permission oddities | Keep projects in your Linux home (`~/`) |
| Using `rm -rf` casually | Data lost forever | `ls` the path first; delete specific files |
| Lost in folders | Commands fail with "No such file" | `pwd`, then use absolute paths or `cd ~` |
| Case mistakes (`Data` vs `data`) | Linux is case-sensitive | Use Tab completion |

## Try it yourself

**Task:** From `~/practice`, create `reports/monthly-copy`, copy all three files from `data/monthly` into it, and show how many lines each copy has.

<details markdown="1">
<summary>Show a hint</summary>

`*` matches any characters: `data/monthly/*.csv` means "every CSV in that folder".
</details>

<details markdown="1">
<summary>Show the solution</summary>

```bash
mkdir -p reports/monthly-copy
cp data/monthly/*.csv reports/monthly-copy/
wc -l reports/monthly-copy/*.csv
```

```text
   6 reports/monthly-copy/orders_2026-01.csv
   6 reports/monthly-copy/orders_2026-02.csv
   3 reports/monthly-copy/orders_2026-03.csv
  15 total
```

Each file has 1 header line, so January and February have 5 orders each and March has 2: the same 12 orders as `orders.csv`.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What does `cd ..` do?

1. Goes to the home folder
2. Goes up one folder, to the parent
3. Deletes the current folder

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which is an **absolute** path?

1. `data/orders.csv`
2. `../logs`
3. `/home/learner/practice/data/orders.csv`

<details markdown="1"><summary>Show answer</summary>
**C.** It starts at the root `/`.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. How do you watch a log file as new lines are written?

1. `head log`
2. `tail -f log`
3. `wc -l log`

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- The filesystem is a tree from `/`; your home is `~`. Use `pwd`, `ls` and `cd` to move around.
- `mkdir -p`, `cp`, `mv`, `rm` (carefully) manage files; `head`, `tail`, `less` and `wc -l` inspect them.
- Permissions decide who can read, write and execute: `chmod +x` makes a script runnable.
- On Windows, use **WSL** and keep projects in your Linux home.
- Tab completion, history (↑, Ctrl+R) and Ctrl+C make you fast and safe.

!!! job "Job-ready check"
    **Interview question:** *"A file arrived on a Linux server. How do you quickly check it before loading it?"*

    **Strong answer:** "I check that it's there and its size with `ls -lh`, look at the header and first rows with `head`, the last rows with `tail` to catch truncation, and count rows with `wc -l` to compare with what the source system says it sent."

    **Mini project:** Write the five commands you'd use to check `orders_raw.csv` (exists, size, header, last rows, row count) in a `notes.md`, with their outputs.
