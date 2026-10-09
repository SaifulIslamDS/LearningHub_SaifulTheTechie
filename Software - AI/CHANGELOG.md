# Changelog

## v0.5.0 — 2026-10-09

### Tutorial architecture upgrade

- Reworked the learning model from curriculum-fragment pages toward long-form, build-oriented tutorials.
- Curriculum page is now a collapsible roadmap/source map; module pages introduce the sequence; tutorials provide the teaching depth.
- Removed the former compulsory Common mistakes, Try it yourself, Quick quiz, Summary and Job-ready check blocks from the default template and existing authored lessons.
- Added a new tutorial template centered on mental models, code, explanation, implementation and practice-file synchronization.
- Retitled representative earlier tutorials so learner-facing tutorial titles no longer simply repeat the source-module heading.
- Deepened flagship tutorials for HTML/CSS, JavaScript, TypeScript and React while preserving exact source mapping.

### Next.js + Full-Stack curriculum

- Added source-curriculum tutorial coverage for Level 01 Modules 31–52.
- Added Next.js App Router, routing/layouts, rendering/hydration, Server/Client Components, data fetching/caching and production UI concepts.
- Added Better Auth architecture and advanced profile/password/email flows plus an authenticated Next.js project sequence.
- Added Node/Express fundamentals, REST CRUD, MongoDB operators/aggregation, booking/auth, JWT/security and deployment.
- Added Full-Stack Project 1 planning, architecture, CRUD/auth/RBAC, Stripe Checkout/webhooks, optimization/deployment and final assignment guidance.
- Added three ST Recommended bridge tutorials: API testing/HTTP contracts, environment variables/secrets, and production error contracts/observability.

### YouTube companion system

- Added structured optional `youtube:` lesson metadata.
- Added responsive privacy-enhanced YouTube embeds, useful timestamp links, review dates and external fallbacks.
- Added curated companions to selected Next.js, Better Auth, Express/MongoDB and Stripe lessons.
- Written tutorials remain complete without external video access.

### Practice and resources

- Added deterministic Next.js/authentication, backend/MongoDB and Full-Stack Project 1 practice bundles.
- Added verified framework-independent Node examples for HTTP, CRUD transformations, query objects, RBAC, payment idempotency and error contracts.
- Improved curated resource rendering with optional resource-type badges and explanations.
- Extended glossary coverage for full-stack, authentication, API contracts, configuration and observability.

### Verification boundary

- Framework-independent JavaScript/Node examples were executed locally.
- Existing JavaScript, TypeScript and React-logic examples were re-run as regression checks.
- Next.js, Better Auth package runtime, MongoDB Atlas, Stripe and production deployment code is marked REFERENCE-ONLY where the release environment could not responsibly install/use those services.
- Official documentation was used for current framework/library guidance; selected YouTube companion URLs were reviewed on 2026-10-09.

### Release validation

- Source-topic coverage checked through Level 01 Module 52.
- Internal links and generated HTML validated.
- Practice-file catalogue and ZIP integrity validated.
- YouTube metadata/embed rendering validated.
- `assets/app.js` syntax checked with Node.
- Two consecutive generated `docs/` builds compared for deterministic output.

### Expected configuration note

`site_url` and `github_repo` remain intentionally blank until deployment is chosen, so canonical absolute URLs and `sitemap.xml` are not emitted yet.

---

## v0.5.0 — 2026-10-09 — Next.js + Full-Stack

### Tutorial architecture

- Introduced Tutorial Architecture v2: deep explanatory tutorial chapters, concise module learning maps and a roadmap-only Curriculum page.
- Removed mandatory Common mistakes, Try it yourself, per-lesson Quick quiz, Summary and Job-ready check sections from the standard authoring template.
- Preserved glossary key terms, free official resources, progress tracking and downloadable files.
- Reworked source module pages to avoid repeated title blocks and moved source-topic lists into a collapsible mapping section.
- Deepened major v0.1–v0.4 lessons, including HTML/CSS, Git, semantic HTML, CSS layout, JavaScript, TypeScript, React and project/problem-solving pages.

### New curriculum coverage

- Authored Level 01 Modules 31–52: Next.js, rendering/data, Better Auth, authenticated project, Node/Express, MongoDB, booking/security/deployment, full-stack planning/architecture, RBAC, Stripe/webhooks and project submission.
- Source-topic coverage is exact against `curriculum.yml` for every authored source module through Module 52.

### Practice packages

- Web Foundations package upgraded to `starter/` + `completed/` tutorial code.
- Added `nextjs-fullstack-reference.zip`.
- Added `backend-mongodb-practice.zip` with six locally executable Node/domain programs and clearly separated reference integrations.
- Added `fullstack-project-1-blueprint.zip` with PRD, architecture and environment templates.

### Verification

- Pure Node HTTP, CRUD, Mongo query-object, RBAC and payment-idempotency examples executed locally.
- Previous JavaScript, TypeScript and React logic examples re-run as regression checks.
- Next.js, Express, MongoDB, Better Auth and Stripe packages/services were not available locally; framework/service integration remains REFERENCE-ONLY.
- Official current documentation reviewed for Next.js App Router/caching, Better Auth MongoDB adapter, Express middleware/routing, MongoDB driver/aggregation and Stripe Checkout/webhooks.
- Build completes without warnings and internal links pass.
- Deterministic package/build checks included in the release validation report.

### Branding

- UI further aligned with Saiful The Techie ecosystem cues: `AI · Data · Web · SaaS · Automation` and `Learn · Build · Explain · Share` inside the deep-navy/electric-cyan design system.
- Approved circular portrait logo raw binary still unavailable to the build runtime; no substitute portrait/logo was fabricated.

## v0.4.0 — 2026-10-09

### Saiful The Techie rebrand and UI

- Reframed the product explicitly as **Saiful The Techie — Software & AI Engineering Learning Hub**.
- Reworked the site design around the established ecosystem visual language: deep navy surfaces, electric cyan/blue accents, white/cyan wordmark treatment and a technology-focused visual hierarchy.
- Added a new 1200×630 Saiful The Techie social/OG image.
- The approved circular portrait logo binary from the earlier ecosystem conversation was not accessible in this runtime. No substitute logo was fabricated; the release uses a text wordmark fallback and keeps the layout ready for the approved asset.
- Updated top bar, footer, hero, light/dark palette and curriculum page branding while preserving offline behavior and accessibility-oriented navigation.

### TypeScript + React curriculum

- Completed source-curriculum tutorial coverage for **Level 01 Modules 21–30**.
- Added TypeScript fundamentals, advanced typing, optional OOP, TypeScript problem solving and Assignment 4.
- Added React core concepts, props/rendering, state/events/data-fetching, Countries Explorer, DOM/BOM React bridge, BPL-DREAM SPA and Assignment 5.
- Added three clearly labelled **ST Recommended** lessons: strict `tsconfig`/compiler discipline, React accessibility foundations, and React DevTools/testing mindset.
- Extended the glossary with TypeScript, React, DOM/BOM and related engineering terms.

### Practice and verification

- Added five TypeScript example programs, compiled under `--strict` and executed with Node.
- Added four framework-independent React logic examples and executed them with Node.
- Added deterministic `typescript-react-foundations.zip` and `react-vite-starter-reference.zip` practice downloads.
- React JSX/Vite source examples are explicitly labelled **REFERENCE-ONLY** because npm package installation was unavailable in the build environment; no framework execution is claimed.

### Release validation

- Source topic coverage checked against `curriculum.yml` for all authored source modules through Module 30.
- Standard lesson quiz count, prerequisites and practice-file references checked by the generator.
- Internal links and HTML generation validated.
- `assets/app.js` syntax checked with Node.
- TypeScript/JavaScript practice code re-run for release verification.
- Two consecutive generated `docs/` builds compared for deterministic output.

### Expected configuration note

`site_url` and `github_repo` remain intentionally blank until the live repository/site is chosen, so canonical absolute URLs and `sitemap.xml` are not emitted yet.

---

## v0.3.0 — 2026-10-09

- Migrated the learning hub to a Markdown/YAML + examples/assets → `build.py` → generated `docs/` architecture.
- Completed JavaScript Engineering Foundations for Level 01 Modules 7–20 while preserving Web Foundations Modules 1–6.
- Added verified Node outputs, scored quizzes, progress, glossary linking and deterministic practice bundles.
- Established the release verification and deterministic-build workflow.
