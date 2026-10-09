# Validation Report — v0.5.0

**Product:** Saiful The Techie — Software & AI Engineering Learning Hub  
**Release:** v0.5.0 — Next.js + Full-Stack + Tutorial Architecture v2  
**Validated:** 2026-10-09

## Result

**PASS** — the source-driven site builds successfully, internal links pass, generated output is deterministic, practice ZIPs are valid, the new Tutorial Architecture v2 structural rules are present, and locally executable examples used by this release were re-run successfully.

The expected configuration NOTE remains: `site_url` is empty until the live site/repository is chosen, so absolute sharing URLs and `sitemap.xml` are intentionally omitted.

## Release size and coverage

- **212 generated HTML pages**
- **66 authored tutorial lessons**
  - 53 `source-curriculum`
  - 13 `st-recommended`
- **53 module intro / learning-map sources**
- **135 curriculum/module entries** represented by the curriculum roadmap
- **7 downloadable practice ZIPs**
- Level 01 source tutorial coverage extends through **Module 52**
- v0.5 adds the Level 01 **Modules 31–52** Next.js + Full-Stack learning slice

## Tutorial Architecture v2 checks

The post-v0.4 learner-experience redesign was validated in generated output:

- Curriculum page is a linked, collapsible roadmap rather than a tutorial wall.
- Curriculum contains **135 collapsible module entries** and **135 Open module links**.
- Module 1 generated page contains **one H1**, removing the repeated-title problem identified by the owner.
- The flagship HTML/CSS tutorial retains **Key terms in this lesson**.
- The flagship tutorial retains **Free resources to go deeper**.
- No authored lesson contains the old mandatory H2 headings:
  - Common mistakes
  - Try it yourself
  - Quick quiz
  - Summary
  - Job-ready check
- Download/practice material appears as tutorial support, while the written page remains the primary teaching experience.

## Build validation

Commands executed:

```bash
python -m py_compile build.py
node --check assets/app.js
python tools/package_examples.py
python build.py
python build.py
```

Both builds reported:

```text
Built 212 pages: 2 levels, 135 modules, 66 lessons -> docs/
NOTE: site_url is empty in site.yml, so sitemap.xml and absolute share links (og:url, og:image) were skipped. Set it once the site is live.
Internal links: all OK
```

The two generated `docs/` directories were compared with `diff -rq`. **No differences were found.**

## Structural HTML validation

A local parser checked all generated HTML pages.

```text
HTML_PAGES 212
DUPLICATE_ID_PAGES 0
CURRICULUM_DETAILS_TAGS 135
CURRICULUM_OPEN_MODULE_LINKS 135
MODULE1_H1_COUNT 1
FLAGSHIP_HAS_KEY_TERMS True
FLAGSHIP_HAS_RESOURCES True
OLD_MANDATORY_HEADINGS 0
ERROR_COUNT 0
```

Internal link validation is also performed by `build.py` and passed.

## Practice-package validation

`tools/package_examples.py` rebuilt the deterministic practice bundles.

Packages present:

- `javascript-foundations.zip`
- `web-foundations-starter.zip`
- `react-vite-starter-reference.zip`
- `typescript-react-foundations.zip`
- `nextjs-fullstack-reference.zip`
- `backend-mongodb-practice.zip`
- `fullstack-project-1-blueprint.zip`

All catalogued download paths resolve. All seven ZIPs passed `ZipFile.testzip()` with no corrupt member.

The Web Foundations package now contains aligned `starter/` and `completed/` code. New v0.5 packages clearly separate executable local examples from framework/service reference integrations.

## Executed code verification

Environment:

```text
Python 3.13.5
Node v22.16.0
npm 10.9.2
TypeScript 5.8.3
```

### JavaScript regression — RUN-HERE

All **14** JavaScript foundation programs executed with Node.

### React logic regression — RUN-HERE

All **4** framework-independent React logic programs executed with Node.

### TypeScript regression — RUN-HERE

All **5** TypeScript programs compiled with:

```bash
tsc --strict --target ES2022 --module commonjs
```

The emitted JavaScript then executed successfully with Node.

### v0.5 backend/domain programs — RUN-HERE

Six locally executable programs were run:

```text
GET /api/health -> ok=true

[{"id":"2","name":"Sundarbans Mangrove"}]

{"price":{"$gte":2000,"$lte":5000},"tags":{"$in":["featured","popular"]}}
[{"$match":{"status":"confirmed"}},{"$group":{"_id":"$destination","bookings":{"$sum":1}}},{"$sort":{"bookings":-1}}]

admin: delete=true
moderator: delete=false
user: delete=false

stored
duplicate ignored
records=1

valid-errors=0
{"error":{"code":"VALIDATION_FAILED","message":"destinationId is required; date is required; travellers must be a positive integer","requestId":"req_demo_001"}}
```

These validate the local HTTP baseline, CRUD-domain logic, query-object/aggregation mental model, RBAC decision logic, idempotent payment-record behavior and a consistent validation-error contract.

## Framework/service verification boundary

The following packages/services were **not available in the release runtime**:

```text
next=NOT_INSTALLED
express=NOT_INSTALLED
mongodb=NOT_INSTALLED
better-auth=NOT_INSTALLED
stripe=NOT_INSTALLED
mongod=NOT_AVAILABLE
mongosh=NOT_AVAILABLE
```

Therefore:

- Next.js project files are **REFERENCE-ONLY** in this release.
- Express integration source is **REFERENCE-ONLY**.
- MongoDB driver/server integration is **REFERENCE-ONLY**.
- Better Auth integration is **REFERENCE-ONLY**.
- Stripe Checkout/webhook integration is **REFERENCE-ONLY**.

The tutorials explicitly preserve that boundary. No framework/service success output is fabricated.

## Branding validation

The source and generated site identify the learning product as **Saiful The Techie — Software & AI Engineering Learning Hub**, using the ecosystem-aligned deep-navy/electric-cyan visual system and the identity cues:

- `AI · Data · Web · SaaS · Automation`
- `Learn · Build · Explain · Share`

The owner-approved **exact circular portrait logo** from earlier ecosystem work could be visually located in prior ecosystem material, but the standalone raw binary was not available to this build runtime. The release therefore keeps the text-based identity fallback and **does not fabricate/redraw a substitute portrait or generic ST logo**.

## Known limitations / not claimed

- No live MongoDB/Atlas integration was executed.
- No Better Auth provider/OAuth flow was executed.
- No Stripe account/test-mode checkout/webhook was executed.
- No live deployment to Vercel/Railway/Render was performed.
- Automated screenshot/visual-regression testing is not part of this release validation; HTML/CSS/interaction source and structural output were validated, but the final browser UI should still receive normal human visual review when published.
- `site_url` and `github_repo` remain unset pending the owner's publication target.

## Next approved milestone

**v0.6.0 — Advanced Software Engineering**

Primary Level 02 scope: advanced TypeScript/OOP, Node/Express backend engineering, PostgreSQL/relational design and advanced SQL, plus the first Drizzle ORM modules.
