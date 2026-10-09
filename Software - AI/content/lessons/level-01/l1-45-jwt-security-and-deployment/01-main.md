---
title: JWT, HTTPOnly Cookies, Security & Deployment
order: 1
summary: Understand token claims, protected API boundaries, secure cookie storage and the deployment steps that turn a local full-stack app into a live system.
level: Intermediate
time: 90–120 min
curriculum_level: Level 01
source_module: '45'
source_type: source-curriculum
topics:
- JWT Structure & Token Generation
- Token Storage with HTTPOnly Cookies
- Session & Logout Management
- Protected API Routes
- User Profile Page & Update Profile
- 'Feature: Change Password'
- Error Handling & Polish
- Backend Deployment Setup and Deploy
- Frontend Deployment to Vercel & Final Review
prerequisites:
- level-01/l1-44-booking-system-and-authentication/01-main
keywords:
- jwt
- httponly
- cookie
- protected routes
- security
- deployment
reviewed: '2026-10-09'
files:
- level-01/backend-mongodb-practice.zip
resources:
- title: Node.js documentation
  url: https://nodejs.org/docs/latest/api/
  source: Node.js
  note: Official Node.js API documentation.
- title: Using middleware
  url: https://expressjs.com/en/guide/using-middleware.html
  source: Express
  note: Official explanation of the Express middleware/request-response cycle.
- title: Express routing
  url: https://expressjs.com/en/guide/routing.html
  source: Express
  note: Official routing guide.
---
## Start here

Security becomes confusing when JWT, sessions and cookies are treated as interchangeable words. Separate the concepts:

```text
JWT       = a token format containing signed claims
Cookie    = an HTTP mechanism for storing/sending a value
Session   = application concept for authenticated continuity
Auth rule = server decision about whether an action is allowed
```

A JWT can be stored in a cookie. A session can be implemented without JWT. The important engineering question is always: **what does the server trust, and why?**

## What you will learn

- JWT header/payload/signature mental model;
- token generation/verification concept;
- HTTPOnly cookie purpose;
- logout/session lifecycle;
- protected API routes;
- profile/password actions;
- error handling/security polish;
- backend + frontend production configuration.

## 1. JWT structure

A JWT is commonly represented as three encoded sections:

```text
header.payload.signature
```

The payload can contain claims such as a user ID or role. Encoding is **not encryption**. Do not place secrets in the payload assuming users cannot read them.

The signature lets the server detect unauthorized modification when verification uses the correct secret/key.

## 2. HTTPOnly cookies reduce browser-script exposure

An HTTPOnly cookie cannot be read through ordinary client-side JavaScript. That helps reduce one class of token theft, but it does not remove the need for CSRF considerations, secure transport, correct SameSite/Secure settings and robust server authorization.

Think defense-in-depth, not “one flag made auth secure.”

## 3. Protected route pattern

```text
request
  ↓
read trusted session/token
  ↓
verify authenticity/expiry
  ↓
load user state
  ↓
check permission/ownership
  ↓
controller logic
```

Keep authorization checks before protected business logic.

## 4. RBAC verified mental model

The practice package includes a small role/action policy:

```js
const can = (role, action) => ({
  admin: ["read", "create", "update", "delete"],
  moderator: ["read", "update"],
  user: ["read"],
}[role] ?? []).includes(action);
```

<span class="output-label">Verified output</span>

```text
admin: delete=true
moderator: delete=false
user: delete=false
```

Real applications need more than this array, but the rule is clear: authorization is a server-side policy decision.

## 5. Profile and password routes

Reuse the identity rules from Module 36. The server derives the target user from auth state, validates requested changes and never logs passwords/tokens.

## 6. Error handling and safe logging

Client response:

```json
{ "error": "Unable to complete request" }
```

Server log may contain a request ID and internal exception details. Do not send raw database stack traces or secret configuration back to the browser.

## 7. Deployment separates environments

A full-stack deployment requires matching configuration:

```text
Frontend URL
Backend URL
CORS allowed origin
Auth base/callback URLs
MongoDB URI
JWT/Auth secret
```

Use production environment variables on the host. Test with a clean browser session after deployment; local cookies and localhost assumptions can hide configuration mistakes.

## 8. Final review

Do not call the project secure because a route is hidden from navigation. Try direct unauthorized requests. Verify that the API itself rejects them.

JWT library code and cloud deployment were not executed in the release environment. The RBAC logic above **was** executed and its output is shown exactly.
