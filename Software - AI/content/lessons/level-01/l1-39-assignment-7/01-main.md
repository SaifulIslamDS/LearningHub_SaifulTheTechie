---
title: Assignment 7 — Ship the Authenticated News App
order: 1
summary: Complete, review and document the authenticated Next.js project as a portfolio checkpoint.
level: Intermediate
time: 4–6 hours
curriculum_level: Level 01
source_module: '39'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites:
- level-01/l1-38-next-js-project-with-authentication-part-2/01-main
keywords:
- assignment
- authentication project
- portfolio
reviewed: '2026-10-09'
files:
- level-01/nextjs-fullstack-reference.zip
resources:
- title: Better Auth installation
  url: https://better-auth.com/docs/installation
  source: Better Auth
  note: Official installation and database adapter guidance.
- title: Better Auth basic usage
  url: https://better-auth.com/docs/basic-usage
  source: Better Auth
  note: Official email/password and social-provider usage.
- title: MongoDB adapter
  url: https://better-auth.com/docs/adapters/mongo
  source: Better Auth
  note: Official current MongoDB adapter setup.
- title: Next.js example
  url: https://better-auth.com/docs/examples/next-js
  source: Better Auth
  note: Official Next.js integration example.
---
## Assignment brief

Finish the news application from Modules 37–38 and turn it into a repository another developer can understand.

This is not only a styling assignment. Your evidence must show that authentication and ownership are enforced in the **server-side workflow**, not just hidden in the interface.

## Minimum feature set

- public news list and dynamic details;
- category filter/navigation;
- registration/login/logout;
- session-aware navigation;
- protected “create post” experience;
- “My Posts” query scoped to current user;
- delete rule that rejects non-owners;
- comments;
- loading, empty and error states;
- responsive layout;
- production environment documentation.

## Repository evidence

Include a README with:

```text
Project goal
Architecture
Route map
Authentication flow
Environment variable names (never values)
How to run locally
Known limitations
Deployment link
```

Add a short architecture diagram. A text diagram is acceptable if it is precise.

## Review the trust boundaries

Before submission, choose three protected actions and explain:

1. what the browser submits;
2. how the server identifies the user;
3. what validation runs;
4. what database condition prevents cross-user access.

If you cannot explain those four points, the project is not finished even if the UI looks complete.

## Portfolio framing

When presenting the project, do not say only “I built a news website.” Explain the engineering:

> Built an App Router application with server/client component boundaries, dynamic routes, session-based authentication, user-scoped mutations, loading/error states and deployment configuration.

That description demonstrates transferable capability.
