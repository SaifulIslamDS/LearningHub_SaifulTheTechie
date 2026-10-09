---
title: Set Up Your Developer Workspace and Learning Routine
order: 1
summary: Set up VS Code, Node.js, Git and GitHub, then design a practical study routine
  and support workflow you can sustain.
level: Beginner
time: 45–75 min
curriculum_level: Level 01
source_module: '0'
source_type: source-curriculum
topics:
- How to access the course
- Time management and build your own routine
- Everything you need to know about assignments
- How to get Support Effectively
- Install Visual Studio Code, Node, Git, GitHub
- (Only For Mac Users)Install VS Code, Node, Git SCM,
- How to use Helpdesk and overall Course Rules
- Actionable Dashboard, Certificate, and AI Integration
- How to get the best out of this course and SCIC and Mindset
- Why is AI advancing so rapidly, and what capabilities and limitations define its
  current state?
- Can AI Replace Developers?
- How NOT to Use AI (Common Mistakes)
- How NOT to Fear AI (Beginner's Mindset)
- Developer vs Engineer Mindset
prerequisites: []
keywords:
- vscode
- node
- git
- github
- terminal
- developer tools
reviewed: '2026-10-09'
files: []
resources:
- title: Visual Studio Code documentation
  url: https://code.visualstudio.com/docs
  source: Microsoft
  type: OFFICIAL
  note: Official setup and editor documentation.
- title: Node.js download and documentation
  url: https://nodejs.org/
  source: Node.js
  type: OFFICIAL
  note: Official Node.js downloads and docs.
- title: Git documentation
  url: https://git-scm.com/doc
  source: Git
  type: OFFICIAL
  note: Official Git reference and book.
- title: GitHub Docs — Get started
  url: https://docs.github.com/en/get-started
  source: GitHub
  type: OFFICIAL
  note: Official account, repository and workflow guidance.
---
## Start here

A developer environment is simply the set of tools you use to **write, run, inspect and save code**. You do not need an expensive computer or dozens of extensions. You need a small toolchain that behaves predictably.

For this learning path, the core setup is:

```text
VS Code     → edit files
Node.js     → run JavaScript and developer tools
Git         → record versions locally
GitHub      → store/share repositories online
Browser     → run and inspect frontend applications
Terminal    → control tools with commands
```

## What you will learn

- how to install and verify the core tools;
- what each tool is responsible for;
- how Windows, macOS and Linux differ at a practical level;
- how to organize a learning folder and GitHub account;
- how to plan assignments and ask for support effectively;
- how to build a routine that emphasizes practice over video consumption;
- how AI fits into the workflow without replacing your reasoning.

## 1. Install VS Code

Download Visual Studio Code from its official site and install the stable version for your operating system.

Create a folder such as:

```text
software-ai-learning/
├── level-01/
│   ├── web-foundations/
│   ├── javascript/
│   └── react/
└── projects/
```

Open the **folder**, not only an individual file, in VS Code. The Explorer panel then shows the project structure and the integrated terminal starts in the right context.

Useful built-in capabilities include:

- Explorer for files and folders;
- search across the project;
- source-control integration;
- terminal;
- debugger;
- extension marketplace.

Do not install a large extension list on day one. Add a tool when you understand the problem it solves.

## 2. Install Node.js and verify it

Node.js lets you execute JavaScript outside the browser and provides the runtime used by much of the modern web-development toolchain.

After installation, open a new terminal and run:

```bash
node --version
npm --version
```

The exact version numbers depend on when you install them. The important thing is that both commands return a version instead of “command not found.”

Create a quick verification file:

```javascript
// hello.js
const learner = "Saiful";
console.log(`Hello, ${learner}. Your Node.js setup works.`);
```

Run it:

```bash
node hello.js
```

Expected logic:

```text
Hello, Saiful. Your Node.js setup works.
```

Your local Node version may differ from the environment used to build this learning hub, so treat version-sensitive setup instructions as something to verify against current official docs.

## 3. Install Git and understand what it does

Git records snapshots of a project so you can understand what changed and return to earlier states.

Verify the installation:

```bash
git --version
```

Then configure the identity that Git writes into your commits:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

This does not log you into GitHub. Git and GitHub solve different problems:

```text
Git      = version-control system on your computer
GitHub   = online hosting/collaboration service for Git repositories
```

You will learn the full workflow in the dedicated Git module.

## 4. Create and secure your GitHub account

Create a GitHub account if you do not already have one. Use a professional username where possible, enable two-factor authentication, and complete enough profile information that a recruiter can understand who you are.

Do not commit secrets such as API keys, passwords or `.env` files. Later modules will teach environment variables and production configuration in depth.

## 5. macOS and Linux notes

The course concepts are the same across systems, but installation paths and shell commands can differ. On macOS and Linux, Git may already exist or may be installed with a package manager. Verify before installing another copy.

When an instruction is operating-system specific, prefer the official installation documentation for your platform rather than forcing a Windows command to work unchanged.

## 6. Design a routine you can actually maintain

A sustainable routine is better than an aggressive plan that collapses after three days.

For a two-hour session, try:

```text
15 min  → review yesterday's code
35 min  → new concept
50 min  → code/build
15 min  → debug/modify independently
5 min   → note what to continue next
```

If you have only one hour, shrink the blocks but preserve **hands-on time**.

Avoid measuring progress only by hours watched. A better measure is: *What can I now build or explain without looking at the solution?*

## 7. Treat assignments as integration points

An assignment is not merely a score. It exposes weak connections between concepts.

Before starting one:

1. read the requirements completely;
2. rewrite them as a checklist;
3. identify the concepts each requirement tests;
4. build in small increments;
5. commit working checkpoints;
6. verify the final result against the requirements.

Do not wait until the deadline to make your first Git commit.

## 8. Ask for support effectively

A useful support request contains evidence.

Instead of:

```text
My code is not working. Please fix it.
```

send something like:

```text
Goal: submit a form and print the values.
Expected: console shows the name once.
Actual: the page reloads before I can inspect the output.
Error: no console error.
What I tried: added an onSubmit handler and console.log.
Relevant code: [small reproducible snippet]
```

This habit helps human mentors, teammates and AI assistants diagnose the real problem quickly.

## 9. Use the dashboard, progress and certificate as feedback—not the goal

Completion indicators help you resume where you stopped. A certificate can document participation. Neither is a substitute for the ability to build.

Use the dashboard to manage sequence and progress; use GitHub projects to prove capability.

## 10. Adopt an engineer mindset from the beginning

AI is improving quickly, and modern tools can generate substantial code. That increases the value of people who can specify requirements, verify behavior, debug systems and make trade-offs.

A developer may focus on *writing code that works*. An engineering mindset asks additional questions:

- What happens when input is invalid?
- Can another person maintain this?
- Is user data protected?
- How do we know it is working in production?
- What will break when usage increases?
- Can I explain why this solution is appropriate?

You do not need advanced answers yet. Begin training yourself to ask the questions.

## 11. Use AI as a multiplier, not a substitute

Good uses of AI at this stage include:

- asking for a simpler explanation of an error;
- generating additional practice questions;
- reviewing code you already attempted;
- comparing two possible approaches;
- turning an error message into a debugging checklist.

Risky uses include copying an entire generated project you cannot explain or running commands without understanding their effect.

The **Learn this lesson with AI** box below gives you a safer tutoring prompt for this exact chapter.
