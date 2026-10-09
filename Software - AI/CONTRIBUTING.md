# Contributing / Authoring Rules

## Source of truth

Edit `curriculum.yml`, `content/`, `examples/`, `tools/` or `assets/`. **Never hand-edit `docs/`.**

## Tutorial Architecture v2

A tutorial should read like a connected chapter, not a template filled with mandatory mini-sections. Use the sequence that best fits the concept, while aiming for this learning flow:

```text
concept
  → mental model
  → code/example
  → explain the code
  → build step-by-step
  → run/observe when executable
  → extend the feature
  → connect to downloadable code
  → next concept
```

Recommended elements:

1. `## Start here` — establish the mental model and why the topic matters.
2. `## What you will learn` — concise learner outcomes.
3. Multiple numbered/topic sections with explanations and code.
4. Real output only when the example was actually executed.
5. A build/project sequence aligned to the downloadable files.
6. Professional context when it naturally improves understanding.
7. Key terms — generated automatically from glossary metadata/keywords.
8. Free resources — defined in front matter and rendered automatically.

Do **not** force `Common mistakes`, `Try it yourself`, a three-question quiz, `Summary`, or `Job-ready check` into every tutorial. Practice and assessment can live in dedicated assignment/project pages when that creates a better learning flow. The existing quiz engine may remain available for future module reviews.

## Front matter

```yaml
---
title: "Learner-focused tutorial title"
order: 1
summary: "One-sentence outcome."
level: Beginner
time: "45–60 min"
curriculum_level: "Level 01"
source_module: "31"
source_type: source-curriculum   # source-curriculum | tutorial-expansion | st-recommended
topics:
  - "Exact topic text from curriculum.yml"
prerequisites: []
keywords: [next.js, routing]
reviewed: 2026-10-09
files: []
resources: []
---
```

> Fix the typo `ntime` to `time` when copying this block into a real lesson; it is shown here only to emphasize that metadata must be reviewed rather than pasted blindly.

### Curriculum mapping

For `source-curriculum` lessons, every `topics:` item must exactly match the corresponding module in `curriculum.yml`. The build checks this and also checks that any source module with authored source lessons has complete topic coverage.

### Verification labels

- **RUN-HERE** — executed while preparing the lesson; show the real output.
- **RUN-BY-OWNER** — cannot be executed in the authoring environment; provide a verification command/script and wait for owner output before claiming a result.
- **REFERENCE-ONLY** — reasonable to show as reference but not executed; state this in the lesson.

Never invent output.

## Practice files

- Put downloadable assets under `content/downloads/`.
- Add every file to `content/downloads/files.yml`.
- Keep source examples under `examples/`.
- Prefer `starter/` + `completed/` or `run/` + `reference/` structures so the learner understands how the files relate to the tutorial.
- Re-run `python tools/package_examples.py` after examples change.

## Release check

```bash
python tools/package_examples.py
python build.py
node --check assets/app.js
```

Run every executable example you can. Then build a second time and compare `docs/`. There must be no build warnings or broken internal links before release.

## Brand / interface

The product brand is **Saiful The Techie**. Preserve the ecosystem's deep-navy/electric-cyan/white technology language and the `AI · Data · Web · SaaS · Automation` / `Learn · Build · Explain · Share` brand cues. Do not invent a replacement portrait/logo if the approved circular asset is unavailable; use the text lockup until the approved binary is supplied.
