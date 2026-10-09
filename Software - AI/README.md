# Saiful The Techie — Software & AI Engineering Learning Hub

**Current release:** v0.5.2  
**Milestone:** Navigation, Video & Learning-Path Audit  
**Compiled & Expanded by:** Saiful Islam  
**Brand:** Saiful The Techie  
**Website:** https://saifulshuvo.com

A free, offline-capable, source-driven tutorial site designed to progress from absolute beginner through professional software and AI engineering.

The supplied Level 01 and Level 02 curricula remain the coverage backbone. Saiful The Techie reorganizes them into deep tutorials, connected code, practice packages, projects, glossary links, curated resources, video companions and AI tutor prompts.

## v0.5.2 highlights

- Level 01 and Level 02 in the left curriculum menu are now **independently collapsible buttons**.
- Removed learner-facing **Source module** badges and **Source mapping** lines from module pages while keeping internal curriculum traceability in `curriculum.yml`.
- Removed duplicate module-title blocks so each module page has one primary H1.
- Fixed the YouTube **Error 153** experience for downloaded `file://` use: the static page now shows a clean video fallback, and the iframe is injected only when the hub is served over HTTP(S).
- Preserved the direct **Watch on YouTube** link on every video companion.
- Added `LEARNING_PATH_AUDIT.md`, a full beginner → advanced → career-readiness audit.
- Corrected the future release sequence after discovering that the previous roadmap skipped Level 01 Modules 53–67 and did not explicitly schedule the Level 02 professional/bonus modules.

## Current size

- **216 generated HTML pages**
- **70 authored tutorials** — 57 curriculum tutorials + 13 ST Recommended
- **70 AI tutor prompts**
- **61 reviewed YouTube companions**
- **135 curriculum/module entries**
- **7 deterministic practice ZIPs**
- **0 generated `Coming soon` labels**

## Learning architecture

```text
Curriculum
  ↓
Module learning map
  ↓
Deep tutorial
  ↓
Code / build
  ↓
Practice package
  ↓
Optional video companion
  ↓
AI tutor prompt
  ↓
Glossary + official/free resources
  ↓
Project / stage gate
```

The written tutorial remains primary. Video and AI are reinforcement layers, not substitutes.

## Source architecture

```text
site.yml
curriculum.yml
build.py
assets/
content/
examples/
tools/
docs/          GENERATED — never hand-edit
handover/
ROADMAP.md
CHANGELOG.md
CONTRIBUTING.md
LEARNING_PATH_AUDIT.md
```

## Build locally

```bash
pip install -r requirements.txt
python tools/package_examples.py
python build.py
```

Basic navigation and tutorial content work by opening `docs/index.html` directly.

For embedded YouTube playback, serve the folder over HTTP so the browser can provide the page identity/referrer expected by YouTube:

```bash
cd docs
python -m http.server 8000
```

Then open `http://localhost:8000/`. If the hub is opened through `file://`, the video section intentionally shows a clean external-link fallback instead of a broken player.

## Verification philosophy

Never fabricate output.

- **RUN-HERE** — actually executed here.
- **RUN-BY-OWNER** — requires the learner/owner environment.
- **REFERENCE-ONLY** — useful teaching code, but not claimed as executed.

## Branding

The public product is **Saiful The Techie — Software & AI Engineering Learning Hub**. The interface uses the ecosystem-aligned deep-navy / electric-cyan technical design system in light and dark modes.

The exact approved circular Saiful The Techie logo binary is still unavailable in this build runtime, so the approved wordmark fallback remains in use rather than fabricating a replacement.

## Learning-path audit

Read `LEARNING_PATH_AUDIT.md` before expanding the curriculum further. The audit concludes that the architecture and curriculum direction can support an absolute-beginner-to-career path, but the current release must not yet be described as career-ready because Level 01 completion, Level 02, production engineering, AI engineering and explicit career preparation are still pending.

## Next approved milestone

**v0.6.0 — Complete Level 01: Full Stack Project 2 + AI-Assisted Coding (Modules 53–67)**
