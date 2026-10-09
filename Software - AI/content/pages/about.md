---
title: About & Sources
summary: "What the Saiful The Techie learning hub is, how source curricula are preserved, and how tutorials, practice files, video companions and verification fit together."
nav: about
---

## What this site is

**Software & AI Engineering Learning Hub** is a free, offline-capable, source-driven tutorial product under **Saiful The Techie**. It is being built for learners who want to progress from beginner foundations toward professional software and AI engineering work.

The two user-supplied source curricula are the **coverage backbone**. Saiful The Techie reorganizes that coverage into learner-friendly tutorials, step-by-step builds, verified code, practice packages, projects, glossary links, curated resources and optional YouTube companions.

## Current release

**v0.5.0 — Next.js + Full-Stack** extends Level 01 through Modules 31–52 and also applies the post-v0.4 tutorial-architecture upgrade: deeper tutorial writing, reduced title repetition, practice-file synchronization, optional video companions and removal of compulsory quiz/mistake/summary/job-ready blocks.

Framework/cloud examples are labelled honestly when the build environment cannot execute them. Node-based examples are executed where possible and their output is verified rather than invented.

## Content labels

| Label | Meaning |
|---|---|
| Source curriculum | Explicitly maps to topics from the supplied Level 01 / Level 02 curriculum |
| Tutorial expansion | Saiful The Techie explanation or implementation material needed to teach a source topic properly |
| ST Recommended | Important professional bridge material added beyond the source curriculum |

## Learning-product architecture

The site separates page responsibilities:

- **Curriculum** — roadmap and source-topic coverage.
- **Module page** — module purpose, tutorial sequence, downloads and source map.
- **Tutorial page** — deep teaching, code, implementation and practice-file connection.
- **Practice files** — starters, runnable examples and references.
- **Projects** — integrated builds.
- **Glossary** — plain-English technical vocabulary.
- **Video companions** — optional external explanations; the written tutorial remains complete without them.

## Build architecture

Markdown, YAML, code and assets are the source of truth. `build.py` generates `docs/`. **Never hand-edit normal content in `docs/`.**

## Quality rules

- Original tutorial writing under Saiful The Techie.
- Exact source-topic mapping is machine-checked against `curriculum.yml`.
- Runnable output is never fabricated.
- Practice downloads are catalogued and tied to tutorials.
- External resources are free/public and favour official documentation.
- YouTube videos are supplementary, reviewed and linked rather than redistributed.
- Every release rebuilds, validates links and checks deterministic generated output.

## Branding

The public learning identity is **Saiful The Techie**. The interface follows the ecosystem's deep-navy / electric-cyan technology visual language in light and dark modes. The exact approved circular Saiful The Techie logo should be used when its original asset is available; the project must not invent or redraw a substitute.

## Credits

Compiled & Expanded by **Saiful Islam** under **Saiful The Techie**. Website: **saifulshuvo.com**.
