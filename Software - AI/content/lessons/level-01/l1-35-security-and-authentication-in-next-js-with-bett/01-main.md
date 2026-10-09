---
title: Authentication in Next.js with Better Auth
order: 1
summary: Design registration, login, session and social sign-in around a server-owned authentication boundary using Better Auth and MongoDB.
level: Intermediate
time: 90–120 min
curriculum_level: Level 01
source_module: '35'
source_type: source-curriculum
topics:
- What you will learn from this Milestone-1 (Animated)
- 'BetterAuth Intro: Architecture overview and project setup'
- 'MongoDB Adapter: Configure BetterAuth with MongoDB'
- 'Auth Client & Register: Create auth client helper and registration page'
- 'Login Page: Build login UI and handle credentials sign-in'
- 'Session Management: Access session data in Components'
- 'Route Protection: Protect routes with proxy'
- 'Google OAuth: Config, credentials setup, and callback URLs'
- 'GitHub OAuth: GitHub sign-in and save social users to the database'
- 'Logout & Deploy: Complete logout system and deployment'
- 'Module Summary: auth flow review, and practice task'
prerequisites:
- level-01/l1-34-assignment-6/01-main
keywords:
- authentication
- better auth
- session
- oauth
- mongodb adapter
- route protection
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
youtube:
  title: Better Auth in Next.js (Complete Tutorial)
  creator: Cosden Solutions
  url: https://www.youtube.com/watch?v=x4hQ2Hmuy3k
  video_id: x4hQ2Hmuy3k
  duration: ≈35 min
  language: English
  level: Intermediate
  reviewed: '2026-10-09'
  why_recommended: A focused end-to-end Better Auth walkthrough covering installation, database setup, Next.js integration, server actions, UI and client usage. Pair it with Better Auth official docs because the library evolves quickly.
  timestamps:
  - label: Installation
    time: 00:57
  - label: Database setup
    time: 08:15
  - label: Next.js integration
    time: '13:38'
  - label: Auth server actions
    time: '18:47'
---
## Start here

Authentication is not “a login page.” It is the system that answers **who is making this request, how do we know, and what identity state can the application trust?**

Use this architecture:

```text
browser form / social button
        ↓
auth client
        ↓
Better Auth server handler
        ↓
database adapter
        ↓
user + account + session records
        ↓
session checked by server-side application code
```

This module follows the source curriculum's Better Auth + MongoDB direction. The exact library APIs can evolve, so the reference files are intentionally paired with current official documentation rather than frozen as timeless syntax.

## What you will learn

- Better Auth's role in the application;
- configuring a MongoDB adapter;
- registration and credential login;
- creating/using an auth client;
- reading session information;
- protecting routes at the correct boundary;
- adding Google and GitHub OAuth conceptually;
- logout and deployment configuration.

## 1. Separate authentication from application features

Keep auth setup in a dedicated server module. The current Better Auth MongoDB adapter documentation uses the separate `@better-auth/mongo-adapter` package.

Reference shape:

```ts
import { betterAuth } from "better-auth";
import { MongoClient } from "mongodb";
import { mongodbAdapter } from "@better-auth/mongo-adapter";

const client = new MongoClient(process.env.MONGODB_URI!);
const db = client.db();

export const auth = betterAuth({
  database: mongodbAdapter(db, { client }),
  emailAndPassword: { enabled: true },
});
```

The bundled `reference-auth/auth.ts` mirrors this structure. Never place a real database URI or secret in source control.

## 2. Registration is a server-backed identity operation

A form collects name, email and password. Client validation can improve feedback, but the server remains authoritative.

The auth client can call the library's sign-up method. Treat the returned `data` and `error` as application states, not as console messages to ignore.

```text
submit
  ↓
validate fields
  ↓
auth request
  ├─ error → explain safely
  └─ success → session / next route
```

Avoid leaking whether an unrelated account exists in places where that information creates security risk.

## 3. Login creates trusted session state

The browser presents credentials. The auth system validates them and creates session state according to its configuration. Your application should then read **session state**, not trust a role or user ID supplied by a form field.

A UI can say “Welcome, Saiful,” but a protected server operation must independently determine the signed-in user from the authenticated request.

## 4. Session management crosses server and UI concerns

A header may need the current user's name. A server route may need the current user's ID. A client menu may need to know whether “Logout” should be visible.

Those needs are different. Do not make the browser the source of truth simply because it is convenient for rendering.

## 5. Route protection is more than redirecting

A redirect improves UX, but **authorization must be enforced wherever protected data/actions are accessed**.

Bad mental model:

```text
Hide dashboard link = secure dashboard
```

Correct mental model:

```text
UI guard → convenience
server/session check → security boundary
```

The source curriculum mentions protecting routes with proxy/middleware-style behavior. Use the current Better Auth and Next.js guidance for the exact integration mechanism in your chosen versions.

## 6. Google and GitHub OAuth

OAuth lets the application rely on an external identity provider. The configuration usually needs:

- provider credentials stored as environment variables;
- an approved callback URL;
- a matching application URL in local and deployed environments;
- database records linking the provider account to the local user.

Do not paste provider client secrets into browser code.

## 7. Logout is a state transition

Logout should invalidate/end the current session and then update the UI. Clearing a cosmetic localStorage value is not equivalent to ending a server-trusted session.

## 8. Deployment checklist

Before deployment, make sure environment-specific values are explicit:

```text
MONGODB_URI
BETTER_AUTH_SECRET
BETTER_AUTH_URL
GOOGLE_CLIENT_ID / SECRET
GITHUB_CLIENT_ID / SECRET
```

Use the hosting provider's secret configuration. Keep `.env` ignored and commit `.env.example` containing names only.

## Build with the reference package

The included Next.js package provides `reference-auth/auth.ts`, `auth-client.ts` and `.env.example`. Reproduce them step-by-step while reading current Better Auth documentation. The build environment did not install Better Auth or connect to MongoDB/OAuth providers, therefore this implementation is **REFERENCE-ONLY**, not presented as executed authentication.
