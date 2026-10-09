---
title: About & Sources
summary: "What the Saiful The Techie learning hub is, how source curricula are preserved, and how tutorials, practice files, video companions and verification fit together."
nav: about
---

## What this site is

**Software & AI Engineering Learning Hub** is a free, offline-capable, source-driven tutorial product under **Saiful The Techie**. It is being built for learners who want to progress from beginner foundations toward professional software and AI engineering work.

The two user-supplied source curricula are the **coverage backbone**. Saiful The Techie reorganizes that coverage into learner-friendly tutorials, step-by-step builds, verified code, practice packages, projects, glossary links, curated resources and optional YouTube companions.

## Current release

**v0.5.2 — Navigation, Video & Learning-Path Audit** is a corrective release on top of v0.5.1. It makes Level 01 and Level 02 independently collapsible in the curriculum sidebar, removes learner-facing source bookkeeping from module pages, eliminates duplicate module-title blocks, prevents broken YouTube embeds when the downloaded hub is opened through `file://`, and records a full beginner-to-career learning-path audit before the next content milestone.

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
- **Video companions** — optional reviewed external explanations; the written tutorial remains complete without them.
- **AI tutor prompt** — a lesson-aware copyable prompt that turns a frontier LLM into a guided mentor instead of an answer generator.
- **Roadmap** — future modules are preserved but separated from the active authored learning path.

## Build architecture

Markdown, YAML, code and assets are the source of truth. `build.py` generates `docs/`. **Never hand-edit normal content in `docs/`.**

## Quality rules

- Original tutorial writing under Saiful The Techie.
- Exact source-topic mapping is machine-checked against `curriculum.yml`.
- Runnable output is never fabricated.
- Practice downloads are catalogued and tied to tutorials.
- External resources are free/public and favour official documentation.
- YouTube videos are supplementary, reviewed and linked rather than redistributed. Embedded players use privacy-enhanced YouTube mode with an external fallback link.
- Every authored tutorial gets a contextual AI tutor prompt generated from its title, level, curriculum topics and practice files.
- Every release rebuilds, validates links and checks deterministic generated output.

## Branding

The public learning identity is **Saiful The Techie**. The interface follows the ecosystem's deep-navy / electric-cyan technology visual language in light and dark modes. The exact approved circular Saiful The Techie logo should be used when its original asset is available; the project must not invent or redraw a substitute.

## Credits

Compiled & Expanded by **Saiful Islam** under **Saiful The Techie**. Website: **saifulshuvo.com**.
