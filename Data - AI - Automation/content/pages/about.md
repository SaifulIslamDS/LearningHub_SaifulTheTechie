---
title: "About & Contributing"
summary: "What this site is, how lessons are built, and how to add a new lesson."
nav: about
---

## What this site is

A free, text-first tutorial site for one integrated curriculum: Data Analytics, Data Science, Data Engineering, Machine Learning, LLMs and RAG, AI Agents, Automation, and Production AI. It is built to take a motivated learner from basics to job-ready skills.

- **Text-first:** short explanations, runnable examples and real business questions.
- **Practical:** every lesson has an exercise, a quiz and a job-ready check.
- **Open:** a plain static website. It works offline and is hosted on GitHub Pages.

## How every lesson is structured

Every lesson follows **Template v1**:

| Section | Purpose |
|---|---|
| What is it? | A plain-language definition with an everyday comparison |
| Why it matters at work | The job use case and how it appears in interviews |
| Syntax / core idea | The minimum pattern to remember |
| Examples | Real business questions, with checked results |
| Common mistakes | The errors beginners actually make |
| Try it yourself | An exercise with a hint and a hidden solution |
| Quick quiz | Three questions with explained answers |
| Summary | Four or five bullets to revise from |
| Job-ready check | An interview question, a strong answer and a mini project |
| Free resources | Official docs, interactive practice and free courses |

Each lesson also shows a **Last reviewed** date. Tools change quickly, so older pages are re-checked first.

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

The site skeleton covers all 10 phases and every module. Lessons are being written phase by phase. **Phases 0, 1 and 2 are complete**: 64 lessons, from Python, Git and testing, through SQL, Excel and Power BI, to pandas, statistics, A/B testing and machine learning foundations, plus three milestone projects and a library of practice files. The site also has a 168-term glossary linked from every lesson, scored quizzes, and share previews for LinkedIn. Next: Phase 3 (Data Engineering). The milestone plan is in `ROADMAP.md` in the repository.
