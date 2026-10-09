---
title: Track Your Code with Git & GitHub
order: 1
summary: Track changes, create meaningful commits and understand branches and pull requests.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '2'
source_type: source-curriculum
topics:
- What is version control system, Git vs GitHub
- Create a GitHub repository and explore GitHub
- 'Introduction to basic commands: git init, git add, git'
- (Mac and Linux only) set GitHub account for the
- (optional) VS Code terminal to set basic GitHub and GitHub Desktop
- Send small incremental changes to GitHub with git push
- Common GitHub-related issues for beginners
- Module Summary and basic git workflow
- '[advanced] Multiple developer workflow contributor on Private Repo'
- '[advanced ] git branch, pull request, merge'
prerequisites: []
keywords:
- web
- html
- css
- git
reviewed: '2026-10-09'
files: []
resources:
- title: Git documentation
  url: https://git-scm.com/doc
  source: Git
  note: Official Git documentation.
- title: GitHub Docs
  url: https://docs.github.com/en/get-started
  source: GitHub
  note: Official GitHub getting-started documentation.
---
## Start here

Git is the history system for your code. GitHub is a service that stores Git repositories online and adds collaboration features such as pull requests, issues and code review. They are related, but they are not the same thing.

A professional workflow is not “write everything, then upload the folder.” It is a sequence of small, explainable changes that can be reviewed, compared and restored.

## What you will learn

- what version control solves;
- the difference between Git and GitHub;
- `git init`, `git status`, `git add`, `git commit` and `git push`;
- how a local repository connects to a remote repository;
- why incremental commits are useful;
- the basic branch → pull request → merge workflow;
- how to diagnose common beginner Git problems.

## 1. The three places to think about

A beginner-friendly Git mental model is:

```text
working directory ── git add ──► staging area ── git commit ──► local history
                                                          │
                                                     git push
                                                          ▼
                                                   GitHub remote
```

The **working directory** is the files you are editing. The **staging area** is the exact set of changes you intend to put in the next commit. A **commit** is a named snapshot in the local repository history.

## 2. Create a repository

Inside the profile project from Module 1, run:

```bash
git init
git status
```

`git init` creates the hidden `.git` directory that stores repository metadata and history. `git status` is one of the commands you should use constantly because it tells you what Git currently sees.

Stage the two files:

```bash
git add index.html style.css
git status
```

Then commit them:

```bash
git commit -m "Build initial profile page"
```

A good commit message describes the result, not the mechanical action. `Build initial profile page` is more informative than `update files`.

## 3. Make incremental changes

Suppose you add a Projects section. Check the diff first:

```bash
git diff
```

Then stage and commit only that change:

```bash
git add index.html style.css
git commit -m "Add project cards to portfolio"
```

Small commits make review and debugging easier because each commit answers a clearer question: **what changed and why?**

## 4. Connect the repository to GitHub

Create an empty repository on GitHub. GitHub will show commands similar to:

```bash
git remote add origin https://github.com/USERNAME/profile-site.git
git branch -M main
git push -u origin main
```

The remote name `origin` is a convention. `-u origin main` records the upstream relationship, so later a plain `git push` usually knows where to send the branch.

Check the connection:

```bash
git remote -v
```

Never put passwords, API keys or private `.env` files into a public repository. Later modules will use `.gitignore` and environment variables more deeply.

## 5. Understand pull, fetch and push

```text
remote GitHub repository
       │       ▲
 git fetch     │ git push
       ▼       │
 local repository
       │
   git merge / git pull
       ▼
 working branch
```

`git fetch` downloads remote history without automatically changing your current files. `git pull` generally fetches and then integrates remote changes. `git push` sends local commits to the remote.

Before you push, develop the habit of checking:

```bash
git status
git log --oneline -5
```

## 6. Branches let work develop safely

Create a branch for a feature:

```bash
git switch -c feature/contact-form
```

Make the contact-form changes and commit them:

```bash
git add .
git commit -m "Add accessible contact form"
```

Switch back:

```bash
git switch main
```

Branches are lightweight pointers to commit history. They let a feature develop without forcing unfinished work onto the main branch.

## 7. Pull request workflow

A common team flow is:

```text
main
  │
  └── feature/contact-form
         │
         ├── commits
         │
         └── push branch to GitHub
                    │
                    ▼
               pull request
                    │
              review / changes
                    │
                    ▼
                  merge
```

A pull request is not a Git feature; it is a collaboration feature provided by hosting platforms such as GitHub. It gives teammates a place to discuss and review a proposed set of commits before they become part of the target branch.

## 8. Multiple developers and contributors

For a private repository, the owner can invite collaborators. In larger teams, developers usually create branches, push their own branches and open pull requests rather than editing the same branch simultaneously.

When two changes affect the same lines, Git may report a **merge conflict**. A conflict is not corruption. It means Git cannot safely decide which version should win, so a person must resolve it.

## 9. A practical daily loop

Use this loop until it becomes routine:

```bash
git status
# edit files
git diff
git add <specific-files>
git diff --staged
git commit -m "Describe the change"
git push
```

`git diff --staged` deserves special attention: it shows exactly what you are about to commit.

## 10. GUI tools are optional, not a substitute for the model

GitHub Desktop and VS Code source-control panels can make common tasks easier. Use them if they help you work, but still learn what **working tree**, **staging**, **commit**, **branch**, **remote**, **push** and **pull** mean. The graphical interface is controlling those same concepts.

## Practice file workflow

Continue using the Web Foundations project. Make at least four meaningful commits while you improve the page. On GitHub, read the commit history and confirm that another person could understand the story of the build from the messages alone.
