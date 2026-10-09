---
title: API Testing & HTTP Contracts Before the Frontend
order: 2
summary: Learn to inspect requests and responses directly so you can debug an API before React or Next.js is involved.
level: Intermediate
curriculum_level: Level 01
source_module: '40'
source_type: st-recommended
topics: []
prerequisites:
- level-01/l1-40-node-js-and-express-from-setup-to-first-api/01-main
keywords:
- http
- api
- status code
- api testing
- curl
reviewed: '2026-10-09'
files:
- level-01/backend-mongodb-practice.zip
resources:
- title: HTTP response status codes
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
  source: MDN
  type: REFERENCE
  note: A practical reference for what common HTTP status codes mean.
- title: Express routing guide
  url: https://expressjs.com/en/guide/routing.html
  source: Express
  type: OFFICIAL
  note: Official reference for routing and route methods.
---
## Start here

A frontend can hide the real shape of an API problem. A button may say “Something went wrong,” while the server actually returned a very useful `400`, `401`, `404` or `500` response. Professional developers learn to inspect the HTTP conversation directly.

Think of an API as a contract:

```text
request
├── method
├── URL
├── headers
└── optional body
        ↓
server route + middleware + application logic
        ↓
response
├── status
├── headers
└── body
```

If you can reason about those pieces without a frontend, debugging becomes much faster.

## What you will learn

- how to test an endpoint before connecting React or Next.js;
- why status codes are part of the API contract;
- how to inspect JSON request and response bodies;
- how to separate transport errors from application errors;
- how to record a repeatable API test case.

## 1. Start with the verified Node baseline

Open `backend-mongodb-practice.zip`, then run:

```bash
node run/01_http_baseline.mjs
```

This release executes that file during verification. It creates a temporary HTTP server on a free local port, calls it with `fetch()`, prints the result, then closes the server.

Verified output:

```text
GET /api/health -> ok=true
```

The value of this tiny program is not the feature. It proves the complete request → server → response loop works without Express, MongoDB or a browser.

## 2. Turn observations into a test case

For every endpoint, write down at least:

```text
Method: GET
URL: /api/destinations
Auth: none
Body: none
Expected status: 200
Expected response shape: { data: [...] }
```

For a create endpoint:

```text
Method: POST
URL: /api/destinations
Content-Type: application/json
Body: { "name": "Sundarbans" }
Expected status: 201
Expected response shape: { data: { id, name } }
```

The exact response shape is your design decision. Consistency is the important part.

## 3. Status codes carry meaning

A beginner API sometimes returns `200` for everything. That makes clients harder to write because success and failure must be guessed from text.

| Situation | Typical status |
|---|---:|
| Successful read | `200 OK` |
| Successful create | `201 Created` |
| Invalid request data | `400 Bad Request` |
| Not authenticated | `401 Unauthorized` |
| Authenticated but not allowed | `403 Forbidden` |
| Resource does not exist | `404 Not Found` |
| Unexpected server failure | `500 Internal Server Error` |

Do not memorize this table as a law for every API. Learn the meaning, then design a consistent contract.

## 4. Test with `curl` or an API client

When your Express server is running locally, a command-line request might be:

```bash
curl -i http://localhost:4000/api/destinations
```

A JSON POST could look like:

```bash
curl -i   -X POST http://localhost:4000/api/destinations   -H "content-type: application/json"   -d '{"name":"Sundarbans"}'
```

`-i` is useful while learning because it includes response headers and the status line.

Tools such as Bruno, Postman or Insomnia provide a visual interface for the same HTTP ideas. The career skill is understanding the request, not memorizing a particular client.

## 5. Keep frontend debugging out of backend debugging

If an endpoint fails, test it directly first.

```text
Does direct API request fail?
├── yes → debug server / database / validation / auth
└── no  → debug frontend URL / request body / browser CORS / state handling
```

This separation prevents you from changing React code to solve a server bug or changing server code to solve a frontend state bug.

## Build with the practice package

1. Run `run/01_http_baseline.mjs`.
2. Change the path to `/api/profile` and return `{ name, track }`.
3. Add a second request using `POST` and print the method/body you receive.
4. In your Express reference project, create a small collection of saved requests in your preferred API client.
5. Name each request after the behavior: `list destinations`, `create destination`, `missing destination`, `unauthorized booking`.

The result is the beginning of a repeatable API test suite, even before formal automated integration tests arrive later in the roadmap.

## Professional context

Teams often reproduce API bugs with a minimal HTTP request before opening the full application. That habit gives you clearer bug reports, easier backend/frontend collaboration and safer refactoring because the contract is visible.
