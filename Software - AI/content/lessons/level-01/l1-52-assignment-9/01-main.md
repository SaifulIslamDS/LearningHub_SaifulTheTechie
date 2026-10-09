---
title: Assignment 9 — Full-Stack Project 1 Submission
order: 1
summary: Package the first complete production-oriented full-stack project with evidence of planning, architecture, security, payments, testing and deployment readiness.
level: Intermediate
time: 6–10 hours
curriculum_level: Level 01
source_module: '52'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites:
- level-01/l1-51-review-ui-ux-check-and-deployment/01-main
keywords:
- assignment
- fullstack project
- submission
- portfolio
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
## Assignment brief

Submit Full-Stack Project 1 as a **portfolio case study**, not merely a source-code dump.

The source curriculum defines Assignment 9 after requirement planning, architecture, core implementation, Stripe/webhooks and deployment review. Your submission should therefore prove those stages happened.

## Required artefacts

```text
README.md
/docs/PRD.md
/docs/architecture.md
frontend source
backend source
.env.example
API route summary
role/permission matrix
test checklist
screenshots or real deployment links
```

Never include real secret values.

## Capability checklist

Your project should demonstrate:

- problem/user/goal definition;
- responsive Next.js frontend;
- Node/Express REST backend;
- MongoDB persistence;
- TypeScript across meaningful parts of the stack;
- authentication;
- Admin/User/Moderator RBAC or an equivalent documented role model;
- protected routes and server authorization;
- CRUD;
- Stripe test Checkout integration if you have account access;
- verified webhook-driven payment record;
- loading, error and empty states;
- production environment plan;
- final end-to-end verification.

## Case-study narrative

Write five short sections:

1. **Problem** — what user pain did you address?
2. **Architecture** — what components/services exist and why?
3. **Hardest engineering decision** — auth, RBAC, payment or data design.
4. **Verification** — what did you actually test?
5. **What you would improve next** — specific technical debt or product scope.

This narrative becomes useful for interviews, freelance proposals and your personal portfolio.

## Final self-review

Choose a protected action, a data mutation and a payment event. Trace each through the system. If any step is “magic” to you, revisit that module before calling the project complete.

The bundled blueprint intentionally stops short of implementing the project for you. Its job is to give you professional planning artifacts while leaving the implementation as your evidence of skill.
