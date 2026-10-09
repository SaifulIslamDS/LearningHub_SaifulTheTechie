---
title: Plan an AI-First Full-Stack Product with a PRD
order: 1
summary: Turn a product idea into users, goals, stories, database entities, architecture decisions and a build roadmap before writing implementation code.
level: Intermediate
time: 100–140 min
curriculum_level: Level 01
source_module: '47'
source_type: source-curriculum
topics:
- What is a PRD and Why It Matters in AI-First Development
- 'Requirement Analysis: Define Problem, Users, and Goals'
- Writing User Stories and Feature List with AI
- Prompt Engineering for Project Planning
- 'Prototyping: Wireframe and UI Planning with AI Tools'
- 'Tech Stack Overview: Next.js, Hero UI, Node, Express, MongoDB, TypeScript'
- Database Planning and Entity Relationship Design
- Project Roadmap and Milestone Planning
prerequisites:
- level-01/l1-46-assignment-8/01-main
keywords:
- prd
- requirements
- user stories
- prompt engineering
- wireframe
- erd
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

A capable developer does not begin every project with `npm create`. First decide what should be built and how success will be recognized.

For Full-Stack Project 1, use the bundled **SkillBridge** blueprint or substitute your own idea while preserving the planning discipline.

```text
problem
  ↓
users
  ↓
goals + constraints
  ↓
features / user stories
  ↓
data model
  ↓
architecture
  ↓
milestones
  ↓
implementation
```

## What you will learn

- what a PRD is and why it prevents random feature building;
- define problem, users and measurable goals;
- write user stories/features with AI assistance without outsourcing judgment;
- use prompts for planning and critique;
- produce wireframes/prototypes;
- connect Next.js, Hero UI, Node/Express, MongoDB and TypeScript conceptually;
- identify entities/relationships;
- turn scope into milestones.

## 1. Define the problem before features

Weak:

> Build a marketplace with dashboard, chat, AI and payments.

Stronger:

> Learners need a simple way to discover mentoring packages, buy one safely and see their purchase history.

The second statement gives features a reason to exist.

## 2. Name your users and their goals

For SkillBridge:

```text
Visitor    → understand services
User       → register, buy, view own purchases
Moderator  → manage content quality
Admin      → manage services/users/payments
```

Now role-based access is not an arbitrary technical feature; it follows from product responsibilities.

## 3. Write user stories that describe value

```text
As a user,
I want to see a service detail page,
so that I can decide whether to purchase it.
```

Add acceptance criteria:

```text
- price and description are visible
- unavailable service cannot be purchased
- invalid ID shows a not-found state
```

Acceptance criteria make implementation testable.

## 4. Use AI as a planning partner, not the product owner

A useful prompt includes your actual context:

```text
Act as a software product reviewer.
Here is my problem statement, users, constraints and proposed features.
Find ambiguous requirements, missing edge cases and features that should be removed from the MVP.
Do not add features unless they solve a stated user goal.
```

Then decide which suggestions are valid. Preserve your product logic in the PRD rather than keeping it only in chat history.

## 5. Wireframe the workflow

Before visual polish, draw the screens and transitions:

```text
Home → Services → Service detail → Login → Checkout → Success
                              ↘ Dashboard → Purchases
Admin → Dashboard → Manage services/users/payments
```

A paper sketch is enough if it clarifies information and actions.

## 6. Tech stack responsibilities

```text
Next.js + Hero UI  → frontend routes and UI
Node + Express     → REST/business API
MongoDB            → application data
TypeScript         → contracts and safer implementation
Stripe             → payment workflow
```

Avoid saying “we use Next.js because it is popular.” Connect every technology to a requirement.

## 7. Database planning

Possible entities:

```text
User
Service
Purchase/Order
Payment
```

Relationships:

```text
User 1 ── * Purchase * ── 1 Service
Purchase 1 ── * PaymentEvent (optional audit model)
```

MongoDB does not remove the need to think about relationships.

## 8. Milestone plan

Break delivery into vertical capabilities:

```text
M1 public catalogue
M2 authentication
M3 user dashboard + CRUD
M4 RBAC/admin
M5 Stripe checkout + webhook
M6 deployment + final testing
```

Each milestone should leave the project in a testable state.

## Use the blueprint

Open `fullstack-project-1-blueprint/docs/PRD.md`. Rewrite it in your own words and change at least one product decision. The blueprint is a starting artifact, not a finished assignment answer.
