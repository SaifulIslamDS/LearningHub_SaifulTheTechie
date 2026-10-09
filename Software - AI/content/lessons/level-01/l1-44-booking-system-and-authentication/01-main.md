---
title: Add Booking & Authentication to the Travel App
order: 1
summary: Model bookings as user-owned records, connect authentication and implement create/list/cancel booking workflows.
level: Intermediate
time: 3–4 hours
curriculum_level: Level 01
source_module: '44'
source_type: source-curriculum
topics:
- BetterAuth Implementation initialization
- MongoDB Adapter Integration
- Sign Up Form and Functionalities Implementation
- Sign In Implementation with Google Login
- Booking System Architecture Overview
- 'Feature: Create Booking Form and Send POST API'
- 'Feature: Store Booking in Database'
- 'Feature: My Bookings Page & Cancel Booking'
- Module Recap
prerequisites:
- level-01/l1-43-project-setup-and-destination-crud/01-main
keywords:
- booking system
- authentication
- ownership
- mongodb adapter
- google login
reviewed: '2026-10-09'
files:
- level-01/backend-mongodb-practice.zip
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
## Project goal

A booking system introduces a relationship between three things:

```text
User ── creates ──> Booking ── references ──> Destination
```

This is where authentication stops being a standalone feature and starts protecting business data.

## What you will build

- Better Auth initialization with MongoDB;
- sign-up and Google sign-in flow;
- a booking data model;
- booking creation endpoint;
- database persistence;
- “My Bookings” user-scoped query;
- cancel booking workflow.

## 1. Model booking ownership

A useful beginner booking record could include:

```js
{
  userId,
  destinationId,
  travelDate,
  guests,
  status: "confirmed",
  createdAt
}
```

The important field is `userId`, and it must come from trusted session state when the server creates the record.

## 2. Authentication before booking

Require a valid session for booking operations. The browser can show a sign-in button, but the backend must still reject unauthenticated booking requests.

```text
POST /api/bookings
  ↓
read authenticated user
  ↓
validate destination/date/guests
  ↓
store { userId: session.user.id, ... }
```

## 3. Booking form

The form should submit only the booking choices:

```json
{
  "destinationId": "...",
  "travelDate": "2026-12-05",
  "guests": 2
}
```

Do not ask the browser to submit a trusted `userId`.

## 4. “My Bookings” query

```text
GET /api/bookings/me
```

The server derives the user ID from session state and filters the collection. This is safer and clearer than `GET /api/bookings?userId=...` when ordinary users must never choose another user's identity.

## 5. Cancel a booking

Cancellation is not always the same as deleting historical data. A realistic design can update:

```js
{ status: "cancelled", cancelledAt: new Date() }
```

That preserves history. The source curriculum uses “cancel booking”; implementing it as a status transition teaches better domain thinking than deleting blindly.

## 6. Google login

Social sign-in changes how identity is established, not how booking ownership works. Once a valid session exists, the booking system should not care whether the user logged in by password or Google.

That separation is a valuable design test.

## Build checkpoint

Two users should be able to create bookings, and each user's “My Bookings” page must return only their records. Attempting to cancel another user's booking should fail at the server boundary.

Better Auth and MongoDB integration are **REFERENCE-ONLY** here because external packages/services were not available to the release environment. Use the current official adapter/provider docs during implementation.

## Data-flow walkthrough

Trace one real booking from the screen to storage:

```text
User opens destination
   ↓
chooses travel date + guests
   ↓
frontend POSTs booking choices
   ↓
backend reads authenticated session
   ↓
backend checks destination exists
   ↓
backend creates booking with trusted userId
   ↓
MongoDB returns inserted ID
   ↓
frontend shows confirmed booking
```

Now trace cancellation. The browser supplies the booking ID, but the backend must query using **both booking identity and ownership** (or explicitly check ownership after loading it). That is what prevents user A from cancelling user B's record.

When you later add payment, keep booking state and payment state separate enough to represent “booking created but payment pending” or “payment failed”. Real domains often have more states than a simple boolean `paid`.
