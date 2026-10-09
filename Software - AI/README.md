# Saiful The Techie — Software & AI Engineering Learning Hub

**Current release:** v0.5.0  
**Milestone:** Next.js + Full-Stack  
**Compiled & Expanded by:** Saiful Islam  
**Brand:** Saiful The Techie  
**Website:** https://saifulshuvo.com

A free, offline-capable, source-driven tutorial site for learning software engineering from web foundations through full-stack, production systems and AI engineering.

The supplied Level 01 and Level 02 curricula remain the **coverage backbone**. The public learning experience is reorganized under Saiful The Techie as deep tutorials, connected code, practice packages, projects, glossary links, curated resources and optional video companions.

## v0.5.0 highlights

- Completed source-curriculum tutorial coverage through **Level 01 Module 52**.
- Added Next.js App Router, rendering, data fetching/caching, Better Auth, authenticated projects, Node/Express, MongoDB CRUD/querying, JWT/security, Stripe Checkout/webhooks and the first major full-stack project sequence.
- Applied the **post-v0.4 tutorial architecture upgrade**: module pages introduce the sequence; tutorial pages teach; curriculum pages remain roadmap/source maps.
- Removed the former compulsory `Common mistakes`, `Try it yourself`, `Quick quiz`, `Summary` and `Job-ready check` sections from the default lesson architecture.
- Deepened representative earlier tutorials and gave learner-facing tutorial titles that differ from their source-module titles.
- Added three **ST Recommended** professional bridge tutorials: API testing/HTTP contracts, environment variables/secrets, and production error contracts/observability.
- Added an optional **YouTube companion system** with structured metadata, responsive privacy-enhanced embeds, timestamps and fallback “Watch on YouTube” links.
- Added curated companions to selected Next.js, Better Auth, Express/MongoDB and Stripe tutorials.
- Expanded resource cards so structured resource types such as `OFFICIAL` and `REFERENCE` can be displayed.
- Added/expanded deterministic practice bundles for Next.js/authentication, Node/MongoDB and Full-Stack Project 1.

## Learning architecture

```text
Curriculum page
  roadmap + source topics
        ↓
Module page
  purpose + sequence + downloads + source map
        ↓
Tutorial page
  mental model + detailed explanation + code + build trail
        ↓
Practice package
  starter / runnable / reference / completed material
        ↓
Project
  integrated implementation
```

Optional external learning sits alongside the tutorial:

```text
Saiful The Techie written tutorial
+ verified/reference code
+ synchronized practice files
+ optional YouTube companion
+ glossary
+ official/free resources
```

## Source architecture

```text
site.yml                         site identity, version, release metadata
curriculum.yml                   two levels, exact source modules/topics, role tracks
build.py                         Markdown/YAML -> static HTML generator
assets/                          Saiful The Techie UI CSS/JS + social image
content/
  lessons/<level>/<module>/      tutorial Markdown; _module.md = module intro
  projects/                      level project briefs
  pages/                         About / How to learn
  glossary.yml                   central glossary
  downloads/                     practice files + files.yml catalogue
  _templates/                    current tutorial-authoring template
examples/                        runnable/reference source examples
tools/                          deterministic packaging helpers
docs/                            GENERATED site; do not hand-edit
handover/                        continuation context + governing prompt
.github/workflows/               build and external-link checking
ROADMAP.md                       milestone plan
CHANGELOG.md                     release history
CONTRIBUTING.md                  authoring rules
```

## Build locally

Requirements: Python 3.13+ and the packages in `requirements.txt`. Node.js is used to verify executable JavaScript/Node examples. TypeScript compiler access is used for TypeScript regression verification.

```bash
pip install -r requirements.txt
python tools/package_examples.py
python build.py
```

Open `docs/index.html` directly for offline use. Embedded YouTube companions naturally require internet access; the written tutorials remain available offline.

## Verification philosophy

Never fabricate executable output.

- **RUN-HERE** — executed in the release environment; shown output is real.
- **RUN-BY-OWNER** — requires an owner/local/cloud environment; provide a precise verification step.
- **REFERENCE-ONLY** — shown for teaching, but not claimed as executed.

Next.js, Better Auth, MongoDB Atlas, Stripe and deployment integrations include reference material where the release environment could not responsibly install/use the external service stack. Framework-independent Node examples are executed locally.

## Editorial labels

- **Source curriculum** — maps exactly to topic text in the supplied curricula.
- **Tutorial expansion** — Saiful The Techie teaching/implementation expansion.
- **ST Recommended** — professional bridge material beyond the source curriculum.

## Branding

The public product is **Saiful The Techie — Software & AI Engineering Learning Hub**. The interface uses the ecosystem-aligned deep-navy / electric-cyan technology language in light and dark modes.

The exact approved circular Saiful The Techie logo asset from earlier ecosystem work is still not available as an original binary in this runtime. The project therefore keeps the approved text/wordmark fallback rather than inventing or redrawing a substitute. When the original logo asset becomes available, add it centrally under `assets/` and regenerate `docs/`.

## Publishing

The generated `docs/` folder is GitHub Pages-ready. Set `site_url` and `github_repo` in `site.yml` once the deployment target is chosen. Until then, canonical absolute URLs and `sitemap.xml` are intentionally omitted.

See `handover/HANDOVER.md` for the full continuation protocol.

## Next approved milestone

**v0.6.0 — Advanced Software Engineering**
