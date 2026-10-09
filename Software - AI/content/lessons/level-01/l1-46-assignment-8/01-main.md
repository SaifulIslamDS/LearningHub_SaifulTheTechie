---
title: Assignment 8 — Deliver the Travel Booking API
order: 1
summary: Consolidate destination CRUD, authentication, booking ownership, security and deployment into a full-stack checkpoint.
level: Intermediate
time: 5–8 hours
curriculum_level: Level 01
source_module: '46'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites:
- level-01/l1-45-jwt-security-and-deployment/01-main
keywords:
- assignment
- booking api
- fullstack checkpoint
reviewed: '2026-10-09'
files:
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
## Assignment brief

Complete the travel application from Modules 43–45 as a coherent product rather than a collection of demo routes.

## Required capabilities

**Destinations**

- create/list/detail/edit/delete;
- input validation;
- stable API response shape.

**Authentication**

- registration/login/logout;
- session/token handled through a server-trusted mechanism;
- optional Google login if credentials are available.

**Bookings**

- authenticated creation;
- “My Bookings” scoped by session user;
- cancellation that preserves meaningful history;
- ownership protection.

**Security/deployment**

- secrets in environment configuration;
- protected backend routes;
- intentional CORS configuration;
- useful error responses;
- live frontend/backend connection when you have deployment access.

## API contract document

Include a table like:

| Method | Route | Auth | Purpose |
|---|---|---:|---|
| GET | `/api/destinations` | No | List destinations |
| POST | `/api/destinations` | Admin | Create destination |
| POST | `/api/bookings` | User | Create own booking |
| GET | `/api/bookings/me` | User | List own bookings |
| PATCH | `/api/bookings/:id/cancel` | Owner | Cancel own booking |

## Evidence of understanding

Record or write a short walkthrough showing one request end-to-end:

```text
button/form
  → HTTP request
  → auth middleware
  → validation
  → database operation
  → response
  → UI state
```

This is the transition from tutorial follower to full-stack developer: you can trace behavior through every layer.

## Verification expectation

If you cannot deploy during learning, provide local screenshots/request logs and state that deployment is pending. Do not invent a live URL. Honest engineering evidence is part of this Learning Hub's standard.
