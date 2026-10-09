---
title: Assignment 6 — Build a Next.js Product Browser
order: 1
summary: Turn routing, rendering and data-fetching concepts into a small portfolio-ready App Router application.
level: Intermediate
time: 3–5 hours
curriculum_level: Level 01
source_module: '34'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites:
- level-01/l1-33-advanced-data-fetching-and-ui-integration/01-main
keywords:
- assignment
- next.js project
- routing
- rendering
reviewed: '2026-10-09'
files:
- level-01/nextjs-fullstack-reference.zip
resources:
- title: Next.js App Router documentation
  url: https://nextjs.org/docs/app
  source: Next.js
  note: Official App Router documentation for routing, rendering, data and production conventions.
- title: Layouts and Pages
  url: https://nextjs.org/docs/app/getting-started/layouts-and-pages
  source: Next.js
  note: Official guide to file-system routes, layouts and pages.
- title: Server and Client Components
  url: https://nextjs.org/docs/app/getting-started/server-and-client-components
  source: Next.js
  note: Official explanation of the server/client boundary and hydration.
---
## Assignment brief

Build a small **Product Browser** that proves you can translate React knowledge into a structured Next.js App Router application.

The source curriculum specifies Assignment 6 without lesson-level details, so this Saiful The Techie expansion turns that checkpoint into a concrete build while keeping it aligned with Modules 31–33.

## Required user journey

```text
Home
  ↓
Products list
  ↓
Product details /products/[id]
  ├─ valid ID → detail content
  └─ invalid ID → not-found UI
```

Add a dashboard route so you also demonstrate a second application area and layout decision.

## Required engineering evidence

Your repository should show:

- App Router pages and layouts;
- navigation with `Link`;
- at least one dynamic route;
- server-first data loading;
- a loading UI;
- a not-found UI;
- at least one narrowly scoped Client Component for genuine interactivity;
- reusable product-card UI;
- responsive styling;
- a README explaining the route tree and your server/client decisions.

## Suggested folder shape

```text
app/
├── layout.tsx
├── page.tsx
├── loading.tsx
├── not-found.tsx
├── products/
│   ├── page.tsx
│   └── [id]/page.tsx
└── dashboard/page.tsx
components/
lib/
```

## Build sequence

Start from an empty project, not the completed reference. First make the routes work with static content. Then introduce sample data. Then add the dynamic page. Then add loading/failure behavior. Finally add styling and one client interaction.

Use the reference package only to compare structure after you have built your own version.

## Completion standard

You should be able to explain, without reading your code:

1. why each URL maps to its file;
2. what the root layout owns;
3. which component runs on the client and why;
4. where the product data is loaded;
5. what happens when an ID is invalid;
6. how you would replace the sample array with a real API later.

That explanation is more valuable than simply showing that the page renders.
