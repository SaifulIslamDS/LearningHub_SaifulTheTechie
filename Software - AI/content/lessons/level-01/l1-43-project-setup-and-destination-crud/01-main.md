---
title: Build Destination CRUD End to End
order: 1
summary: Start a travel application and wire a UI to create, list, view, edit and delete destinations through a real backend contract.
level: Intermediate
time: 3–4 hours
curriculum_level: Level 01
source_module: '43'
source_type: source-curriculum
topics:
- Project Initialization & Dependencies Setup
- UI Library Integration (Hero UI) and Navbar & Footer
- Database Connection & Server Design
- Home Page Design & explore Swiper.js
- 'Feature: Add Destination Form and create Post API'
- 'Feature: GET All Destinations & Display'
- 'Feature: Destination Details Page'
- 'Feature: Edit Destination'
- 'Feature: Delete Destination'
- Module Summary
prerequisites:
- level-01/l1-42-deep-dive-into-mongodb-operators-and-queries/01-main
keywords:
- crud project
- destination
- api integration
- Hero UI
- Swiper
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
## Project goal

Modules 40–42 taught the backend pieces. Now build a vertical feature that crosses the whole stack:

```text
Next.js / React UI
       ↓
Express REST API
       ↓
MongoDB destinations collection
```

The feature is **Destination CRUD**: create, list, view, edit and delete travel destinations.

## What you will build

- project initialization and dependencies;
- a reusable navbar/footer and UI-library integration point;
- backend/database connection layer;
- home page/slider section;
- add-destination form;
- GET list and detail pages;
- edit and delete flows;
- clear API boundaries between frontend and backend.

## 1. Define the resource contract

Start with the shape:

```ts
type Destination = {
  id: string;
  name: string;
  country: string;
  price: number;
  description: string;
  imageUrl?: string;
};
```

Then define the HTTP contract before writing components:

```text
GET    /api/destinations
GET    /api/destinations/:id
POST   /api/destinations
PATCH  /api/destinations/:id
DELETE /api/destinations/:id
```

This becomes the agreement between the two applications.

## 2. Keep server design separate from page design

Backend folders might begin as:

```text
server/
├── app.ts
├── db.ts
└── routes/
    └── destinations.ts
```

Frontend might begin as:

```text
app/
├── page.tsx
└── destinations/
    ├── page.tsx
    ├── new/page.tsx
    └── [id]/page.tsx
```

Do not make the Next.js folder tree mirror MongoDB internal details. They have different responsibilities.

## 3. Add destination

The form gathers human input. The backend validates it and inserts the document.

```text
form submit
  ↓ POST
Express parses + validates
  ↓
MongoDB insertOne
  ↓ 201
UI navigates/refetches
```

Build the plain form first. Replace controls with Hero UI components only after the data flow works.

## 4. List and details

The list endpoint should return enough data for cards. The details endpoint can return the full description. This distinction becomes useful when records grow larger.

## 5. Edit

Pre-fill the form from existing data, then submit only the intended changes with `PATCH`. After success, render the server-confirmed state rather than assuming every write succeeded.

## 6. Delete

Deletion is destructive. Ask for confirmation in the UI, but remember the server remains the authority. Handle “record not found” separately from an internal failure.

## 7. Home page and Swiper/UI polish

A slider library can improve presentation, but treat it as optional polish around already-working data. The project should still be understandable if that dependency is temporarily removed.

## Build order

1. API list route with static/in-memory data.
2. Replace it with MongoDB.
3. Build list page.
4. Build create form.
5. Build details.
6. Build edit.
7. Build delete.
8. Add Hero UI/Swiper styling.
9. Test all five CRUD paths again.

The bundled backend package contains the verified pure-JS CRUD core plus reference Express/MongoDB snippets. MongoDB/Express execution remains **REFERENCE-ONLY** in this release environment.
