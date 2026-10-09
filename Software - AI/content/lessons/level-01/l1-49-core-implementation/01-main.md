---
title: Implement CRUD, Authentication & RBAC
order: 1
summary: Build the core product across API routes, Next.js pages, JWT/session authentication, role policies and role-specific dashboards.
level: Intermediate
time: 4–6 hours
curriculum_level: Level 01
source_module: '49'
source_type: source-curriculum
topics:
- Building REST API Structure with Node & Express
- 'CRUD API Routes: Create, Read, Update, Delete'
- Frontend Pages and Layout with Next.js + Hero UI
- 'Authentication System Setup: JWT, Login and Register API'
- Implement Login and Register UI and Connect with API
- 'Role-Based Access Control (RBAC): Admin, User, and Moderator'
- Protecting Frontend Routes Based on User Roles
- Dashboard Pages for Different Roles
- Connecting All Frontend Pages with Backend APIs
prerequisites:
- level-01/l1-48-project-setup-and-architecture/01-main
keywords:
- core implementation
- rest
- crud
- rbac
- dashboard
- authentication
reviewed: '2026-10-09'
files:
- level-01/fullstack-project-1-blueprint.zip
- level-01/backend-mongodb-practice.zip
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

Core implementation means connecting previously learned patterns into a product where **data, identity and permissions agree**.

```text
Next.js page
   ↓
API client
   ↓
Express route
   ↓
auth + validation + authorization
   ↓
service/database work
   ↓
response
   ↓
UI state
```

Trace every feature through that chain.

## What you will build

- REST API structure;
- CRUD routes for the primary resource;
- frontend list/detail/forms;
- login/register API/UI;
- role-based access for Admin/User/Moderator;
- protected frontend experiences;
- different dashboards by role;
- complete frontend/backend connectivity.

## 1. Build one vertical slice before all routes

Start with **read services**:

```text
GET /api/services → backend → MongoDB → JSON → frontend list
```

Only after it works, add service details and mutations. Vertical slices reveal integration problems earlier than building the whole backend and whole frontend separately.

## 2. CRUD API contract

```text
GET    /api/services
GET    /api/services/:id
POST   /api/services          Admin
PATCH  /api/services/:id      Admin/Moderator rule
DELETE /api/services/:id      Admin
```

Document the permission next to the route. That forces security into the feature design.

## 3. Authentication

Whether your implementation uses Better Auth or your own JWT exercise, the invariant is the same: protected operations derive identity from trusted server auth state.

Login UI should handle loading, success and failure explicitly. Never store passwords or log them for debugging.

## 4. RBAC policy

Use a centralized policy instead of scattered role strings:

```js
const permissions = {
  admin: new Set(["service:create", "service:update", "service:delete"]),
  moderator: new Set(["service:update"]),
  user: new Set([]),
};
```

The included `run/04_rbac.mjs` demonstrates the same idea with simpler actions and has been executed during verification.

## 5. Protect API first, UI second

UI can hide “Delete” for users, but an ordinary user can still send an HTTP request manually. Therefore:

```text
API authorization = security
UI role rendering = user experience
```

Implement both, in that order of trust.

## 6. Role dashboards

Do not create three unrelated applications. Share layout/components, then show role-relevant capabilities:

```text
/dashboard
  User      → purchases/profile
  Moderator → review/manage allowed content
  Admin     → users/services/payments
```

A server-side role check can decide what data the dashboard is allowed to load.

## 7. Connect all pages through one API layer

Create a small request helper rather than calling `fetch` with different base URLs everywhere. Centralization simplifies auth headers/cookies, errors and production configuration.

## Integration checkpoint

Pick one admin mutation and one user-owned read. Trace each from UI event to database operation and back. Write the trace in your README. That exercise exposes architectural gaps better than adding another decorative page.
