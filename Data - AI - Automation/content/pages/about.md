---
title: "About & Contributing"
summary: "What this site is, how lessons are built, and how to add a new lesson."
nav: about
---

## What this site is

A free, text-first **Saiful The Techie** tutorial site for an integrated curriculum covering Data Analytics, Data Science, Data Engineering, Machine Learning, LLMs and RAG, AI Agents, Automation, and Production AI. It is built to take a motivated learner from basics to job-ready skills.

- **Text-first:** clear mental models, runnable examples and real business questions.
- **Practical:** tutorials prioritize verified code/data, step-by-step builds and synchronized practice files; quizzes and other review blocks are used only when they improve the topic.
- **Open:** a plain static website. It works offline and is hosted on GitHub Pages.

## How tutorials are structured

The approved **Template v2** is flexible rather than rigid. A substantial tutorial normally moves through:

```text
Concept → mental model → detailed explanation → code/data/config
→ real output → explain the result → build step-by-step
→ complete implementation → practice files → professional context
→ key terms → curated resources → next tutorial
```

A small topic may be short. A major topic can be several thousand words with substantial code. **Common mistakes, exercises, quizzes, summaries and job-ready checks are optional**, not compulsory interruptions.

Practice packages increasingly use a `starter/` → tutorial → `completed/` workflow so the written lesson and downloadable implementation stay synchronized.

## Quality rules

- **Original writing only.** We learn from other sites' formats but never copy their text.
- **Every example result is run, not guessed.** Example outputs come from actually running the code on the practice files.
- **Facts are checked against official documentation** before a lesson is published.
- **External links are free resources** that don't require payment to be useful.

## Add or edit a lesson

1. Copy `content/_templates/lesson-template.md` into `content/lessons/<phase-id>/<module-id>/`. Name it like `03-case-expressions.md`.
2. Fill in the front matter: title, order, summary, level, time, and which `topics` from `curriculum.yml` it covers.
3. Write the lesson using the section structure above.
4. Run `python build.py`. It rebuilds the `docs/` folder and reports any broken internal links.
5. Open `docs/index.html` to check the result, then commit.

A topic listed in `curriculum.yml` shows as **Coming soon** until a lesson file lists it under `topics`.

## Licence

- **Lesson content:** CC BY-NC-SA 4.0. You may share and adapt it with credit, for non-commercial use, under the same licence.
- **Site code:** MIT.

Details are on the [licence page](license.html).

## Status

The site skeleton covers all 10 phases and every module. **Phases 0, 1 and 2 are complete. Phase 3 is now 40 of 55 topics complete with 21 lessons; the full source contains 85 lessons.** M8 has completed ETL/ELT, Data Quality and dbt in the current working checkpoint. The glossary contains **199 terms**. **Next approved M8 module: AI-Ready Data.** The milestone plan is in `ROADMAP.md` in the repository.
