---
title: Set Up the Full-Stack Architecture
order: 1
summary: Turn the PRD into separate frontend/backend projects, TypeScript configuration, database connection, environment boundaries and a coherent first page.
level: Intermediate
time: 2–3 hours
curriculum_level: Level 01
source_module: '48'
source_type: source-curriculum
topics:
- 'Project Initialization: Next.js + Node + Express Setup'
- TypeScript Configuration Across Frontend and Backend
- Hero UI Integration and Theme Customization
- MongoDB Atlas Connection and Database Design
- Folder Structure, Naming Conventions, and Code Organization
- Environment Variables Setup and .gitignore Configuration
- Implement Navbar, Footer and Homepage Hero Section
- 'Homepage Static Sections: Features, Testimonials, and CTA'
- Connect Frontend and Backend and API Base URL
prerequisites:
- level-01/l1-47-requirement-analysis-and-planning/01-main
keywords:
- architecture
- typescript config
- environment variables
- mongodb atlas
- folder structure
reviewed: '2026-10-09'
files:
- level-01/fullstack-project-1-blueprint.zip
resources:
- title: Next.js App Router documentation
  url: https://nextjs.org/docs/app
  source: Next.js
  note: Official framework reference used by the frontend.
- title: Express documentation
  url: https://expressjs.com/
  source: Express
  note: Official backend framework documentation.
- title: MongoDB Node.js Driver
  url: https://www.mongodb.com/docs/drivers/node/current/
  source: MongoDB
  note: Official database driver reference.
---
## Start here

Planning becomes engineering when you convert requirements into a repository structure with clear boundaries.

A beginner-friendly split is:

```text
project/
├── frontend/  → Next.js + UI
├── backend/   → Node + Express + TypeScript
└── docs/      → PRD + architecture + API notes
```

A monorepo tool is not required to understand this architecture. Clarity comes first.

## What you will build

- initialize frontend and backend separately;
- configure TypeScript in both;
- integrate Hero UI at the presentation layer;
- connect MongoDB Atlas through environment configuration;
- establish naming/folder conventions;
- configure `.gitignore` and `.env.example`;
- build navbar/footer/home hero/static sections;
- connect frontend to backend through a configurable API base URL.

## 1. Separate deployable responsibilities

The frontend knows how to present and request data. The backend owns trusted business operations and database access.

```text
frontend never imports backend MongoDB client
backend never imports React page component
```

They communicate through HTTP contracts.

## 2. TypeScript configuration

Use strict settings as the default learning target. The exact config differs between Next.js and a standalone Node project, but both should catch unsafe assumptions rather than suppressing errors globally.

Create shared *conceptual* types where useful, but do not create a tangled build setup just to share one interface during a beginner project.

## 3. UI library integration

Install/configure Hero UI according to its current official setup for your Next.js version. Keep your app structure readable without the library:

```text
app → feature/page components → reusable UI primitives
```

UI components should not secretly own database access.

## 4. Database connection

Backend configuration:

```text
MONGODB_URI=<secret deployment value>
```

The repository contains only:

```text
MONGODB_URI=
```

in `.env.example`.

## 5. Folder conventions

A small API can grow into:

```text
src/
├── app.ts
├── config/
├── modules/
│   ├── auth/
│   ├── services/
│   └── payments/
├── middleware/
└── utils/
```

Do not over-engineer five files for one trivial function. The goal is responsibility, not maximum folder count.

## 6. Homepage first slice

Build navbar, hero, features, testimonials and CTA using static content. Why before backend integration? It creates a stable frontend shell while the API is still evolving.

## 7. API base URL

Frontend environment:

```text
NEXT_PUBLIC_API_URL=http://localhost:4000
```

Then centralize request construction instead of scattering hard-coded localhost URLs through components.

## 8. First connection test

Create a backend health endpoint:

```json
{ "ok": true, "service": "skillbridge-api" }
```

Call it from the frontend. This small test proves routing, CORS, configuration and network connectivity before you build complex CRUD.

The blueprint package contains the PRD/architecture and environment skeleton. Express/Next/MongoDB project execution remains **REFERENCE-ONLY** in this release environment.
