# Saiful The Techie — Data, AI & Automation Path
## M8 / v0.9 Post–Data Quality Upgrade Approval & Continuation Handover

**Prepared for:** future ChatGPT / frontier-LLM continuation  
**Project owner:** Saiful Islam  
**Brand:** Saiful The Techie  
**Product:** Data, AI & Automation Path  
**Website:** saifulshuvo.com  
**Current stable release:** `v0.8 — Phase 3A: Data Engineering — storing & serving`  
**Current working checkpoint:** `v0.9 / M8 — ETL/ELT + Data Quality complete`  
**Current Phase 3 coverage:** `35 / 55 topics`  
**Current lesson source count:** `82 lessons`  
**Next approved M8 module:** `dbt`  
**Final target for this milestone:** `v0.9 — Phase 3B complete`  
**Date:** 2026-10-09

---

# 1. Purpose of this handover

This document adapts the approved deep-tutorial upgrade model to the current **Data, AI & Automation Path** project.

The project must continue evolving from a curriculum/topic coverage site into a complete, practical, self-study technical learning platform under **Saiful The Techie**.

The central change is:

> Do not merely cover a topic. Turn each topic into a complete learning experience with explanation, verified examples, hands-on implementation, synchronized practice files, professional context, curated resources and a clear progression to the next tutorial.

This upgrade applies to all new M8 work beginning with **dbt** and progressively to previously written lessons.

---

# 2. Current product identity

## Brand

**Saiful The Techie**

## Product

**Data, AI & Automation Path**

## Public identity

```text
Saiful The Techie
Data, AI & Automation Path
Hands-on Data, AI & Automation learning — from analytics foundations to production AI systems.
```

## Product purpose

A practical, beginner-to-career-ready learning path covering:

- engineering foundations
- SQL, Excel, Power BI and analytics
- Python, statistics and data science
- data engineering
- machine learning
- LLMs and RAG
- agents and automation
- LLMOps and governance
- integrated capstone work
- career and commercialisation

The intended progression is:

> **Beginner → Intermediate → Advanced → Professional / Career-Ready**

The platform should remain useful even when a learner has no access to any outside course.

---

# 3. Current technical architecture — PRESERVE

The existing source-driven static-site architecture remains approved:

```text
Markdown / YAML / source code / assets
        ↓
      build.py
        ↓
       docs/
        ↓
    validation
        ↓
 versioned ZIP package
```

Important project paths include:

```text
site.yml
curriculum.yml
build.py

assets/
content/
  lessons/
  projects/
  pages/
  glossary.yml
  downloads/
  _templates/

examples/
tools/
docs/

README.md
ROADMAP.md
CHANGELOG.md
CONTRIBUTING.md
handover/
.github/workflows/
```

`docs/` is generated output.

**Never hand-edit normal tutorial content in `docs/`.**

Correct workflow:

```text
edit source
↓
run packaging/generator tools
↓
run build.py
↓
regenerate docs/
↓
validate
↓
package the full project
```

---

# 4. Current M8 state

M8 is:

> **Phase 3B — Data Engineering: moving & trusting data**

Completed in the current working checkpoint:

## ETL / ELT — complete

- Modular pipelines
- Idempotency
- Incremental loads
- Replayability
- CDC

## Data Quality — complete

- Validation
- pytest for data
- Great Expectations
- Data contracts
- Freshness & alerting

Current Phase 3 progress:

```text
35 / 55 topics
```

The established Phase 3 known answers must remain consistent, including:

```text
Orders: 4,246
Net revenue: 5,478,357.79
```

Do not change the established Phase 2 data generator. If M8 needs new deterministic data, add a new fixed-seed generator.

---

# 5. Next approved M8 module

# dbt

The approved tutorials are:

```text
01. dbt Models and Tests
    Topics: Models · Tests

02. Snapshots and Macros
    Topics: Snapshots · Macros

03. Documentation and Marts
    Topic: Documentation & marts
```

Exact topic strings in lesson front matter must continue matching `curriculum.yml`.

---

# 6. New learning philosophy — APPROVED FOR THIS PROJECT

The default learning flow is now:

```text
CONCEPT
   ↓
MENTAL MODEL
   ↓
WHY IT MATTERS
   ↓
DETAILED EXPLANATION
   ↓
CODE / SQL / CONFIG / DATA EXAMPLE
   ↓
RUN / OBSERVE REAL OUTPUT
   ↓
EXPLAIN WHAT HAPPENED
   ↓
BUILD STEP-BY-STEP
   ↓
MODIFY / EXTEND
   ↓
COMPLETE IMPLEMENTATION
   ↓
DOWNLOADABLE PRACTICE FILES
   ↓
PROFESSIONAL / PRODUCTION CONTEXT
   ↓
OPTIONAL VIDEO COMPANION
   ↓
KEY TERMS
   ↓
CURATED FREE RESOURCES
   ↓
NEXT TUTORIAL
```

Short version:

> **Explain deeply → demonstrate → run → explain the result → build together → provide the implementation → connect to the next concept.**

For data and AI topics, the learning flow may also include:

- data-flow diagrams
- schemas and models
- query plans
- lineage
- before/after datasets
- pipeline state
- assertions/tests
- architecture decisions
- evaluation output
- cost/reliability trade-offs

---

# 7. New tutorial-page standard — APPROVED

A tutorial page should normally follow this pattern:

```text
Tutorial title

Short introduction

What you will learn

Prerequisites

────────────────────

Concept / mental model

Why it matters

Detailed explanation

Code / SQL / YAML / config example

Actual output where executable

How the code works

Additional concepts as needed

────────────────────

Build with me

Step 1
Step 2
Step 3
...

────────────────────

Complete implementation

Practice files

Professional / production context

Optional video companion

Key terms

Free resources to go deeper

Next tutorial
```

Tutorial length must follow the complexity of the topic.

A simple concept can be short.

A substantial topic such as dbt snapshots, orchestration, Spark partitions, Kafka, IAM, document chunking, RAG metadata or Terraform may require a long-form tutorial with substantial code and explanation.

Artificially equal lesson lengths are not required.

---

# 8. Sections that are no longer compulsory

The old template must not force these into every tutorial:

- Common mistakes
- Try it yourself
- Quick quiz
- Summary
- Job-ready check

They may still be included when they genuinely improve learning.

The generator/template must be updated so a tutorial remains fully valid when these sections are absent.

Existing quizzes do not need to be deleted immediately. This is a forward-compatible upgrade, followed by progressive refactoring.

---

# 9. What remains first-class

## Key terms

Keep the lesson-to-glossary connection.

Important technical terms should link back to the central glossary.

## Curated resources

Resources remain required where useful, but they should be explained rather than dumped as raw links.

Useful labels include:

```text
OFFICIAL
FREE
REFERENCE
INTERACTIVE
PRACTICE
VIDEO
ADVANCED
OPTIONAL
```

Every resource should explain **why it is useful**.

## Practice files

Practice files remain a major platform feature and must now be more tightly synchronized with tutorials.

---

# 10. Curriculum coverage vs tutorial architecture

`curriculum.yml` remains authoritative for **coverage**.

It does **not** control how many tutorial pages are required.

Approved rule:

> **One curriculum module does not have to equal one tutorial page.**

Likewise:

- one topic may require more than one tutorial;
- several tightly related topics may be taught together;
- a module page should represent a learning sequence, not merely mirror YAML structure.

Never silently drop a required topic.

Every completed module must still reconcile exactly to `curriculum.yml`.

---

# 11. Page responsibilities

## Curriculum page

Purpose:

> **Roadmap and coverage**

Show:

```text
Phase
  → Module
    → Topics
```

The curriculum page should not become the main tutorial experience.

## Module page

Purpose:

> **Module introduction + learning sequence**

Should include:

- concise module description
- what the learner will learn
- prerequisites
- logical tutorial sequence
- relevant practice files
- connection to the Phase 3 project
- progress

Avoid repeated titles and cover-page duplication.

## Tutorial page

Purpose:

> **Deep teaching**

It must be explanatory, practical, code/data-rich and progressive.

## Practice-file experience

Purpose:

> **Hands-on repetition and implementation**

## Project page

Purpose:

> **Integrate multiple skills into a meaningful production-style build**

## Glossary

Purpose:

> **Concise technical definitions connected to lessons**

## Resources

Purpose:

> **Curated external references and learning companions**

---

# 12. Practice-file workflow — UPGRADED

Where a tutorial benefits from a real project structure, prefer:

```text
tutorial-or-project/
├── starter/
├── completed/
└── README.md
```

Recommended learning flow:

```text
STARTER
   ↓
FOLLOW THE TUTORIAL
   ↓
RUN / VERIFY
   ↓
COMPLETED IMPLEMENTATION
```

The tutorial must explain:

- what to download;
- which file/folder to open first;
- what exists in the starter version;
- what the learner will add;
- how to run it;
- what real output to expect;
- what the completed version contains.

The written tutorial and downloadable implementation must not drift apart.

For Phase 3, continue integrating runnable material into:

```text
examples/phase-3/
content/downloads/phase-3/
content/downloads/phase-3/data-engineering-scripts.zip
```

A dedicated project folder may also be added when a tool such as dbt, Airflow, Spark or Kafka benefits from a multi-file structure.

---

# 13. Code and data become first-class learning content

Technical tutorials must increasingly include:

1. code / SQL / YAML / configuration;
2. actual output where executable;
3. explanation of that output;
4. explanation of the important lines;
5. a modification or extension;
6. integration into a larger workflow.

Code must never be decorative.

It should drive learning.

For SQL/data examples, show enough rows or summary output to explain what happened without overwhelming the learner.

For configuration-heavy tools, explain the purpose of every important file.

---

# 14. Verification discipline — NON-NEGOTIABLE

Never fabricate executable output.

Use these labels internally and in lessons where useful:

## RUN-HERE

The example was actually executed in the available environment.

Use the real output.

## RUN-BY-OWNER

The available environment cannot execute the tool reliably.

Provide a precise command/project for Saiful to run.

Do not fabricate output.

## REFERENCE-ONLY

The example depends on an unavailable external/cloud/paid environment.

Clearly state that it was not executed.

This verification discipline applies to:

- Python
- SQL
- dbt
- Great Expectations
- Airflow
- Dagster
- Prefect
- Terraform
- AWS/GCP
- BigQuery
- Spark
- Kafka
- vector/embedding tooling
- any other executable technology

---

# 15. YouTube companion layer — APPROVED

The learning hub may support a structured YouTube companion section.

YouTube is supplementary.

The written Saiful The Techie tutorial must remain complete without the video.

Preferred metadata:

```yaml
youtube:
  title: "..."
  creator: "..."
  url: "https://www.youtube.com/watch?v=..."
  video_id: "..."
  duration: "..."
  language: "English"
  level: "Beginner"
  reviewed: "YYYY-MM-DD"
  why_recommended: "..."
  timestamps:
    - label: "..."
      time: "..."
```

Preferred rendering:

```text
Video companion

[responsive embedded player when possible]

Why this video:
...

Recommended section:
...

Creator:
...

Duration:
...

Watch on YouTube ↗
```

Rules:

- verify the URL;
- prefer official sources or respected technical educators;
- prefer technically current material;
- use timestamps when only part of a long video is useful;
- default to one strong video, not a list;
- do not download or redistribute video content;
- keep a normal external link if embedding is unavailable.

Video metadata support should be added to the generator before or during the next approved module.

---

# 16. Saiful The Techie branding — NON-NEGOTIABLE

The entire public product is:

# Saiful The Techie

with the product identity:

# Data, AI & Automation Path

Do not expose or mention third-party curriculum brands or source-course branding in the public learning product or continuation package unless the owner explicitly asks for historical/source documentation.

Public identity:

```text
Saiful The Techie
Data, AI & Automation Path
```

Suggested footer identity:

```text
Compiled & Expanded by Saiful Islam
Saiful The Techie
saifulshuvo.com
```

---

# 17. Logo rule — IMPORTANT

The Saiful The Techie ecosystem has an approved **circular Saiful The Techie logo / portrait mark**.

Rules:

- use the exact approved logo when its actual binary file is available;
- do not fabricate a substitute;
- do not redraw the approved mark;
- do not permanently replace it with a generic `ST` icon;
- if the exact logo binary is unavailable, use a clean text wordmark fallback;
- keep the logo reference centralized so the exact asset can be swapped in later.

The current working checkpoint contains a generic `ST` vector mark.

That mark must **not** be treated as the final approved logo.

Before the next module is packaged:

1. use the exact approved circular logo if it becomes directly accessible as an asset;
2. otherwise remove/disable the generic substitute in the visible header and use the Saiful The Techie text wordmark fallback;
3. keep a stable central logo asset/config path for a future one-file swap.

---

# 18. UI / design-system direction — APPROVED

The UI should align with the Saiful The Techie ecosystem.

Desired feel:

> **modern, technical, calm, professional, readable, practical, documentation-oriented**

Avoid:

- flashy bootcamp sales-page styling;
- generic marketplace-template appearance;
- excessive gradients/glow;
- visual clutter;
- cramped content;
- repeated headings.

## Core visual direction

Use:

- deep navy / near-black primary surfaces;
- cyan / electric-blue accents;
- cool-light backgrounds in light mode;
- dark technical surfaces in dark mode;
- restrained borders;
- strong typography hierarchy;
- generous whitespace;
- readable code blocks;
- rounded but professional cards;
- subtle shadows;
- responsive layout.

## Header

Should support:

- approved Saiful The Techie logo, or text fallback;
- Saiful The Techie brand name;
- Data, AI & Automation Path product name;
- visible version;
- Home;
- Curriculum;
- Practice files;
- Glossary;
- Search;
- appearance switch.

Avoid unnecessary text truncation when space is available.

## Sidebar

Preserve the established Data, AI & Automation Path interaction rule:

- desktop docked behavior;
- mobile off-canvas behavior;
- curriculum navigation;
- progress information;
- active tutorial highlighting;
- open/close only through the explicit menu control or the `M` key;
- do not close because of outside clicks or topic clicks;
- persist state using the existing `daa-nav` localStorage key.

## Tutorial reading area

Prioritize:

- visible breadcrumb;
- strong tutorial title;
- readable line length;
- spacious paragraphs;
- code clarity;
- data/output clarity;
- practical callouts;
- practice-file connections;
- glossary terms;
- resource cards;
- optional video companion;
- previous/next navigation.

## Appearance

Both light and dark modes remain required.

## Mobile

No horizontal page overflow.

Code/table areas may scroll horizontally when necessary.

---

# 19. UX upgrade: reduce title repetition

Module pages and tutorials should not repeat the same module title through multiple layers.

Prefer a hierarchy such as:

```text
Phase 3 · Data Engineering

dbt

Transform tested warehouse data into documented analytical models.

What you'll learn

Tutorials
01 dbt Models and Tests
02 Snapshots and Macros
03 Documentation and Marts
```

Then each tutorial page uses its own distinct tutorial title.

---

# 20. Learning-depth standard

A learner should never be expected to understand a concept merely because its name appeared.

Major concepts should be introduced gradually.

For upcoming M8 work, this includes questions such as:

- What problem does dbt solve that SQL scripts alone do not?
- What is a dbt model?
- What really happens during `dbt build`?
- Why are data tests different from unit tests?
- What problem do snapshots solve?
- What is a slowly changing dimension in dbt terms?
- Why use macros?
- What makes a mart different from a staging model?
- What is data lineage?
- What problem does an orchestrator solve?
- What is a retry vs a backfill?
- What causes Spark shuffle?
- Why do Kafka producers and consumers exist?
- What does IAM actually control?
- Why use Terraform?
- What makes chunking good or bad for retrieval?
- When should embeddings be refreshed?

The platform must teach the mental model before assuming tool familiarity.

---

# 21. Career-outcome standard

The Data, AI & Automation Path is career-oriented.

Across the complete path, learners should progressively be able to:

- analyze data with SQL, Excel and BI tools;
- write Python for analysis and engineering;
- clean and validate data;
- build reproducible pipelines;
- model analytical data;
- work with relational databases and warehouses;
- use dbt;
- orchestrate data workflows;
- work with cloud storage and IAM fundamentals;
- use infrastructure-as-code concepts;
- reason about Spark and streaming;
- prepare data for RAG/AI systems;
- test and monitor data products;
- explain architecture decisions;
- build portfolio-quality projects;
- move toward Data/BI, Data Engineering, Data Science, AI Engineering and Automation roles.

---

# 22. Existing M8 lessons must be progressively upgraded

Do not block M8 by rewriting every older lesson in the whole site.

Apply the new standard in this order:

1. generator/template support;
2. M8 ETL/ELT lessons;
3. M8 Data Quality lessons;
4. all new dbt lessons;
5. remaining M8 modules as they are built;
6. older phases progressively when practical or during a dedicated platform/content upgrade.

The current 82 lessons do not all need an immediate rewrite before dbt begins.

However, no new M8 lesson should knowingly be created as a shallow old-template lesson.

---

# 23. Release/build rules — PRESERVE

Working M8 checkpoints should be delivered as **full merged project ZIPs**, not patch-only ZIPs.

Preferred working naming:

```text
data-ai-automation-path-v0.9-working-m8-<module>.zip
```

Examples:

```text
data-ai-automation-path-v0.9-working-m8-dbt.zip
data-ai-automation-path-v0.9-working-m8-ai-ready-data.zip
```

The final release is only:

```text
data-ai-automation-path-v0.9.zip
```

when all M8 scope is complete and validated.

The stable site version may remain `v0.8` during working checkpoints and should be bumped to `v0.9` for the actual M8 release.

Do not label an incomplete working checkpoint as the final release.

---

# 24. Release validation — NON-NEGOTIABLE

Before a final module checkpoint package, verify as much as possible:

- source structure is valid;
- curriculum mappings match exactly;
- prerequisites resolve;
- assets resolve;
- practice files exist;
- code examples are verified;
- known answers remain consistent;
- downloads catalogue matches actual files;
- generated packages are deterministic where practical;
- no duplicate IDs;
- search/index logic still recognizes new tutorials;
- appearance switching works when a build can be generated;
- responsive layout remains valid;
- ZIP integrity passes.

Before the **final v0.9 release**, additionally require:

- `python build.py` completes;
- no `WARNING:` lines;
- `Internal links: all OK`;
- Phase 3 = `55 / 55 topics`;
- Phase 3 project page is complete;
- roadmap/changelog/about/version are updated;
- deterministic build check passes;
- full browser QA is completed.

If the current environment cannot run the full build, mark that verification honestly as **RUN-BY-OWNER**.

Never simulate a successful build.

---

# 25. Milestone workflow — STANDING INSTRUCTION

After every completed M8 module/checkpoint, explicitly state:

> **Next approved milestone: [next module from the approved M8 working order]**

The owner may then reply simply:

> **Continue**

When the owner writes **Continue**:

- build the already-approved next milestone;
- do not ask for unnecessary reconfirmation;
- do not skip ahead;
- return a full merged working project ZIP;
- report real verification;
- state the next approved milestone again.

---

# 26. Approved M8 working order from this point

Current completed checkpoint:

```text
ETL / ELT ✅
Data Quality ✅
```

Next:

```text
dbt ← NEXT
AI-Ready Data
Orchestration
Big Data & Streaming
Cloud & IaC
Phase 3 Project — Production Analytics Platform
Final v0.9 audit + release
```

The roadmap's complete M8 topic set remains authoritative even when implementation order is optimized for tools that are easier to run locally first.

---

# 27. What must happen when the owner next writes “Continue”

The next build is:

# M8 — dbt

Before and during dbt development, apply the approved platform upgrade.

Implementation sequence:

```text
1. Open the latest full merged Data Quality checkpoint.
2. Re-read ROADMAP.md and curriculum.yml.
3. Upgrade the tutorial template so old compulsory blocks are optional.
4. Update build.py only as needed to support the new deep-tutorial structure safely.
5. Add optional YouTube companion metadata/rendering support.
6. Improve module-page hierarchy and reduce title repetition.
7. Correct logo handling:
   - exact approved logo if directly available;
   - otherwise text wordmark fallback;
   - do not use the generic ST substitute as final branding.
8. Keep the Saiful The Techie navy/cyan design system coherent in light and dark mode.
9. Refactor the completed M8 ETL/ELT and Data Quality lessons to the upgraded structure where needed.
10. Build the dbt module:
    - Models and Tests
    - Snapshots and Macros
    - Documentation and Marts
11. Build synchronized dbt practice material.
12. Execute dbt for real if the environment supports it.
13. If dbt cannot run here, mark it RUN-BY-OWNER and provide exact commands; never invent output.
14. Update glossary/download metadata.
15. Run structural verification.
16. Run the full site build if dependencies are available.
17. Package the entire merged working project.
18. State the next approved milestone.
```

---

# 28. dbt quality target

The dbt module must not be three short definition pages.

It should take the learner through a coherent mini-project.

A preferred practical sequence is:

```text
raw 2025 orders
   ↓
dbt source
   ↓
staging model
   ↓
cleaned / intermediate logic
   ↓
tests
   ↓
snapshot
   ↓
macro
   ↓
documented marts
   ↓
BI-ready output
```

The learner should understand:

- what dbt is and is not;
- why transformation belongs in version-controlled SQL;
- project structure;
- `dbt_project.yml`;
- profiles/connections;
- sources;
- models;
- materializations;
- refs and dependency graph;
- generic/data tests;
- build vs run vs test;
- snapshots;
- macros/Jinja;
- documentation;
- lineage;
- marts;
- how this connects to the final Phase 3 Production Analytics Platform.

Use the project's known answers for reconciliation.

---

# 29. Final continuation principle

The governing idea is now:

> **Do not merely preserve curriculum coverage. Build a complete Saiful The Techie learning experience.**

The Data, AI & Automation Path should combine:

```text
Saiful The Techie explanation
+
deep tutorial writing
+
verified code / SQL / configuration
+
real output
+
step-by-step builds
+
synchronized practice files
+
portfolio-style projects
+
glossary
+
curated official resources
+
carefully selected optional video companions
+
career-oriented engineering depth
```

The result should feel like a complete technical learning product, not a syllabus archive.

---

# 30. Quick continuation checklist

Before the next module:

- [ ] Open the latest full merged working ZIP
- [ ] Read this handover
- [ ] Read `ROADMAP.md`
- [ ] Read `curriculum.yml`
- [ ] Inspect current M8 lessons
- [ ] Inspect current Saiful The Techie UI assets
- [ ] Use exact approved logo if its binary is directly available
- [ ] Otherwise use text wordmark fallback
- [ ] Do not use a fabricated/generic logo as final identity
- [ ] Do not expose third-party curriculum branding
- [ ] Apply the deep-tutorial architecture
- [ ] Make old template blocks optional
- [ ] Synchronize practice files
- [ ] Add optional video companion support
- [ ] Implement only the current approved milestone
- [ ] Verify executable outputs honestly
- [ ] Preserve known answers
- [ ] Validate source structure
- [ ] Build generated site when environment permits
- [ ] Package the complete merged project ZIP
- [ ] State the next approved milestone

---

**Current stable release:** `v0.8 — Phase 3A`  
**Current working checkpoint:** `v0.9 / M8 — ETL/ELT + Data Quality complete`  
**Next approved milestone:** `M8 — dbt`  
**Brand:** Saiful The Techie  
**Product:** Data, AI & Automation Path  
**Compiled & Expanded by:** Saiful Islam  
**Website:** saifulshuvo.com
