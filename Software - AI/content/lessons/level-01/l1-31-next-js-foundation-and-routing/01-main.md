---
title: Build Your First Next.js App Router Project
order: 1
summary: Move from React components to a routed Next.js application with layouts, dynamic segments, optimized assets and clear project structure.
level: Intermediate
time: 75–100 min
curriculum_level: Level 01
source_module: '31'
source_type: source-curriculum
topics:
- What you will learn from this Milestone (Animated)
- What is Next.js? Why choose Next.js?
- Creating a Next.js App and Understanding Project Structure
- Create pages, routing in Next.js, and navigation in Next.js
- Dynamic Routing in Next.js and Dynamic Route Segments
- Creating Multiple Layouts in Next.js
- 'Styling in Next.js: Global CSS, Custom CSS, and Tailwind CSS'
- Image Optimization in Next.js, not-found
- Font Optimization in Next.js
- Catch All Segment with Dynamic Segment
- Active links, and module summary
prerequisites:
- level-01/l1-30-assignment-5/01-main
keywords:
- next.js
- app router
- routing
- layout
- dynamic route
- image optimization
- font optimization
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
youtube:
  title: 'Next.js App Router: Routing, Data Fetching, Caching'
  creator: Vercel
  url: https://www.youtube.com/watch?v=gSSsZReIFRk
  video_id: gSSsZReIFRk
  duration: ≈12 min
  language: English
  level: Beginner / Intermediate
  reviewed: '2026-10-09'
  why_recommended: An official Vercel walkthrough that reinforces App Router mental models for routing, dynamic segments, data fetching, caching and metadata. Use current Next.js docs for version-sensitive details.
  timestamps:
  - label: Routing
    time: 00:10
  - label: Dynamic route segments
    time: 02:57
  - label: Data fetching
    time: 04:53
  - label: Caching
    time: 07:36
---
## Start here

React taught you how to describe an interface as components. Next.js adds the **application framework around those components**: routes, layouts, server rendering, data boundaries, asset optimization and conventions for production applications.

Do not treat Next.js as “React with extra syntax.” A better mental model is:

```text
React components
      +
file-system routes
      +
server/client execution choices
      +
data + caching conventions
      +
production tooling
      =
Next.js application
```

This tutorial builds the route skeleton contained in `nextjs-fullstack-reference.zip`. Create the project yourself first, then compare your files with the reference package.

## What you will learn

- why a framework is useful after learning React;
- how the App Router maps folders and files to URLs;
- how root and nested layouts compose pages;
- dynamic and catch-all route segments;
- navigation with `Link` and active navigation ideas;
- global CSS and utility/UI-library integration points;
- image, font and not-found conventions;
- how to organize a small project so later authentication and backend work have a clean home.

## 1. Create a project and read the folder tree

A current App Router project normally centers on the `app/` directory. The exact scaffold can change over time, so use the official `create-next-app` instructions rather than memorizing a one-time command output.

A small application may look like this:

```text
app/
├── layout.tsx
├── page.tsx
├── globals.css
├── products/
│   ├── page.tsx
│   └── [id]/
│       └── page.tsx
├── loading.tsx
└── not-found.tsx
lib/
└── products.ts
```

The important idea is that **the folder tree communicates the URL tree**. `app/page.tsx` maps to `/`. `app/products/page.tsx` maps to `/products`. A folder wrapped in square brackets describes a dynamic segment.

## 2. Root layout: the shell around every route

Open the reference file `app/layout.tsx`:

```tsx
import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Learning Store",
  description: "Next.js tutorial project",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header>
          <Link href="/">Learning Store</Link>
          <nav>
            <Link href="/products">Products</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

A layout is persistent structure. The `{children}` position is where the selected route is composed into that structure. This is a major architectural advantage: navigation, page chrome and shared providers do not need to be copied into every page.

## 3. Pages define route content

The home page is just a component in `app/page.tsx`:

```tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <h1>Learning Store</h1>
      <p>Build this app across Modules 31–39.</p>
      <Link href="/products">Browse products</Link>
    </>
  );
}
```

Notice what is *not* here: a route configuration array. The file location is the route configuration.

## 4. Dynamic route segments

Suppose product IDs come from data. Instead of creating one page file per product, use:

```text
app/products/[id]/page.tsx
```

Conceptually:

```text
/products/keyboard  → params.id = "keyboard"
/products/mouse     → params.id = "mouse"
```

A dynamic page can load that identifier, find its record and call `notFound()` if the record does not exist. The reference package includes a complete small example.

## 5. Catch-all routes

A catch-all segment such as `[...slug]` represents multiple path parts. A documentation product might use:

```text
app/docs/[...slug]/page.tsx

/docs/react/state        → ["react", "state"]
/docs/node/http/streams  → ["node", "http", "streams"]
```

Use this when the route hierarchy is data-driven. Do not choose it simply because it looks flexible; explicit routes are easier to understand when the URL structure is known.

## 6. Nested layouts

A dashboard often needs a different shell from public pages:

```text
app/
├── layout.tsx
└── dashboard/
    ├── layout.tsx
    ├── page.tsx
    └── settings/
        └── page.tsx
```

The root layout can provide the global document. The dashboard layout can add its own sidebar and dashboard navigation around every dashboard page.

## 7. Styling: choose clear ownership

Use global CSS for genuine global rules: typography, background, design tokens and resets. Use component-level conventions (CSS Modules, Tailwind classes or your chosen UI library) for component styling.

The reference package intentionally contains simple CSS because this module is about **framework architecture**, not visual complexity. When Hero UI is introduced later, it should sit on top of a route/component structure you already understand.

## 8. Images, fonts and not-found UI

Next.js provides framework primitives for optimized assets. The career-relevant lesson is not “always use one component.” It is to understand the responsibilities:

- define meaningful image dimensions and alternative text;
- avoid layout shifts;
- load fonts intentionally;
- design a useful 404/not-found state rather than exposing a blank route.

The `not-found.tsx` reference gives the learner a dedicated UI for invalid resources.

## 9. Active navigation

An active link needs knowledge of the current pathname, so it is usually a small client-side navigation concern. Keep the client boundary narrow: the whole layout does not need to become a Client Component just because one navigation item is interactive.

Think in boundaries:

```text
Server layout
├── Logo (server)
├── ActiveNav (client: reads pathname)
└── Page content (server by default)
```

That pattern becomes important when the app grows.

## Build with the practice package

1. Create a fresh Next.js App Router project from the official setup guide.
2. Reproduce `app/layout.tsx` and `app/page.tsx` yourself.
3. Create `/products` and verify navigation.
4. Create `[id]` and visit two different IDs.
5. Add a nested dashboard layout.
6. Add `not-found.tsx` and trigger it deliberately.
7. Only then compare with `nextjs-fullstack-reference.zip`.

The reference package is **REFERENCE-ONLY** in this release because Next.js packages were not installed in the release environment. The source has been reviewed against current official App Router documentation; no fabricated build output is shown.

## How this connects to your career path

A professional Next.js developer is expected to read a route tree and immediately answer: what URL does this file represent, which layout wraps it, where does the code execute, what data does it require, and what happens when loading or failure occurs? This module starts building that reasoning habit rather than teaching route syntax in isolation.
