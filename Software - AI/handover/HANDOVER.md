# Handover: Saiful The Techie — Software & AI Engineering Learning Hub

> **Current release:** v0.5.0 (2026-10-09)  
> **Next approved milestone:** **v0.6.0 — Advanced Software Engineering**  
> **Owner:** Saiful Islam  
> **Brand:** Saiful The Techie

## 1. Product

A free, offline-capable, source-driven tutorial website that transforms two user-supplied curricula into a beginner-to-advanced Software & AI Engineering learning path.

The curricula define **coverage**, not the exact tutorial-page structure. Saiful The Techie may split broad source modules into learner-friendly tutorials and add original explanation, verified examples, practice packages, projects, curated resources, video companions and clearly labelled professional bridge content.

## 2. Current teaching architecture

The post-v0.4 upgrade is now the governing learning model:

```text
CONCEPT
→ MENTAL MODEL
→ DETAILED EXPLANATION
→ CODE
→ RUN / OBSERVE
→ EXPLAIN THE CODE
→ BUILD STEP-BY-STEP
→ COMPLETE / REFERENCE IMPLEMENTATION
→ PRACTICE FILES
→ OPTIONAL VIDEO COMPANION
→ KEY TERMS
→ FREE RESOURCES
→ NEXT TUTORIAL
```

Do not revert to the old fixed lesson template.

These are **not compulsory in every tutorial**:

- Common mistakes
- Try it yourself
- Quick quiz
- Summary
- Job-ready check

They may appear only when they genuinely improve a lesson.

## 3. Page responsibilities

- **Curriculum:** collapsible roadmap and source-topic map.
- **Module:** concise introduction, learning sequence, tutorial cards, downloads, source coverage.
- **Tutorial:** the actual teaching product; detailed, code-rich and practical.
- **Practice:** repetition, executable examples and starter/reference/completed files.
- **Project:** integrated multi-skill build.
- **Glossary:** technical vocabulary.
- **Resources:** curated external references.

Avoid repeated visible titles. Tutorial titles should describe the learner action/outcome rather than simply echo the source-module name.

## 4. Content labels

- **Source curriculum** — topic coverage mapped exactly from `curriculum.yml`.
- **Tutorial expansion** — Saiful The Techie explanation/implementation needed to teach a source topic well.
- **ST Recommended** — useful professional material beyond the source curriculum.

Never silently represent added material as source curriculum.

## 5. Source architecture

```text
index.html                    offline redirect to docs/
build.py                      Markdown/YAML -> docs/
site.yml                      identity/version/site URLs
curriculum.yml                2 levels, 135 module/supplement entries, exact topic lists
requirements.txt              build dependencies
assets/                       shared Saiful The Techie UI CSS/JS + OG image
content/
  lessons/<level>/<module>/   tutorial Markdown; _module.md = module intro
  projects/                   level projects
  pages/                      About / How to learn
  glossary.yml                central glossary
  downloads/                  practice packages + files.yml
  _templates/                 current deep-tutorial template
examples/                     runnable/reference source examples
tools/                        deterministic package helpers
docs/                         GENERATED; never hand-edit
handover/                     this file + governing prompt + post-v0.4 approval record
.github/workflows/            build / link checking
README.md / ROADMAP.md / CHANGELOG.md / CONTRIBUTING.md
```

## 6. Build / verification

```bash
pip install -r requirements.txt
python tools/package_examples.py
python build.py
node --check assets/app.js
```

`build.py` must finish with no `WARNING:` lines and `Internal links: all OK`.

Build twice and compare `docs/`; generated output should be deterministic.

### Execution truth

Never fabricate output.

- **RUN-HERE** — actually executed here.
- **RUN-BY-OWNER** — needs owner/local/account environment; provide exact verification instructions.
- **REFERENCE-ONLY** — teaching/reference code not claimed as executed.

## 7. Practice files

Practice files are first-class content. Prefer tutorial-aligned packages with starter/reference/completed material or clearly named runnable/reference subfolders.

A tutorial must explain what to download, what state it starts in, what to change and how the reference/completed state relates to the written code.

All downloads must be listed in `content/downloads/files.yml`.

## 8. YouTube companion system

YouTube is supplementary. The written tutorial must stand alone.

Structured front matter:

```yaml
youtube:
  title: "..."
  creator: "..."
  url: "https://www.youtube.com/watch?v=..."
  video_id: "..."
  duration: "≈20 min"
  language: "English"
  level: "Intermediate"
  reviewed: "YYYY-MM-DD"
  why_recommended: "..."
  timestamps:
    - label: "Relevant section"
      time: "04:20"
```

`build.py` renders a privacy-enhanced `youtube-nocookie.com` iframe, timestamp links and a direct external fallback.

Use one primary companion by default. Verify availability/relevance with web access. Prefer official channels or respected educators. Current official docs remain authoritative for version-sensitive details.

## 9. Saiful The Techie design system

Keep the ecosystem-aligned technical UI:

- deep navy / midnight surfaces
- electric cyan / vivid blue accents
- clean cool-light backgrounds
- readable dark mode
- strong typography hierarchy
- restrained borders and shadows
- professional rounded cards
- high-quality code blocks
- responsive mobile layout
- persistent/toggleable curriculum sidebar
- version visible in top bar
- search, progress, glossary, code-copy controls and on-page TOC

Do not copy the third-party course visual identity.

### Logo boundary

Use the exact approved circular Saiful The Techie logo only when the actual original asset is available. Do not fabricate/redraw a substitute. The current text/wordmark fallback is intentional.

## 10. v0.5 delivered scope

Level 01 now has authored source coverage through **Module 52**:

- Modules 31–34 — Next.js routing/rendering/data fetching + assignment
- Modules 35–39 — Better Auth + authenticated Next.js project + assignment
- Modules 40–46 — Node/Express, MongoDB, REST/CRUD, booking, JWT/security + assignment
- Modules 47–52 — Full-Stack Project 1 planning, architecture, core implementation, RBAC, Stripe/webhooks, deployment + assignment

Also delivered:

- ST Recommended API testing/HTTP contracts
- ST Recommended environment variables/secrets/config
- ST Recommended production errors/observability
- optional YouTube companion renderer + curated examples
- deep-tutorial template and earlier flagship refactors

## 11. Next approved task — v0.6.0

**Advanced Software Engineering** — Level 02 Modules 01–17:

- advanced TypeScript / OOP
- Node runtime and core modules
- Express + TypeScript
- PostgreSQL connection and CRUD
- clean/scalable backend architecture
- relational modelling and database design
- normalization
- PostgreSQL management/data types
- SQL querying, dates, groups and joins
- subqueries, views, functions, procedures, triggers and indexing
- production database assignment

Before writing:

1. Read `ROADMAP.md`, this handover, `CONTRIBUTING.md`, `curriculum.yml` Level 02 Modules 01–17 and the current tutorial template.
2. Baseline build current v0.5.
3. Check available PostgreSQL/tooling before claiming runnable output.
4. Plan a connected backend/database practice project instead of isolated snippets only.
5. Research current official docs for version-sensitive technology.

## 12. Standing conversation workflow

After every completed release, explicitly state:

> **Next approved milestone: [name from ROADMAP.md]**

If the owner replies only **Continue**, immediately build that approved milestone without unnecessary reconfirmation.
