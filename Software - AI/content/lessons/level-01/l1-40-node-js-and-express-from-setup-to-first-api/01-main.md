---
title: Build Your First Node.js & Express API
order: 1
summary: Understand client-server architecture, the Node.js runtime and Express request flow, then build GET and POST endpoints that a frontend can consume.
level: Intermediate
time: 90–120 min
curriculum_level: Level 01
source_module: '40'
source_type: source-curriculum
topics:
- What you will learn from this Milestone-1 (Animated)
- 'Milestone Roadmap: Introduction to Backend Development'
- 'Architecture Planning: Client-Server Architecture'
- 'Node.js Internal: How it works?'
- 'Introduction to Express.js: Why do we need it?'
- 'Database Fundamentals: SQL vs NoSQL & MongoDB'
- 'Environment Setup: Installing Node, Express, and Nodemon'
- 'Creating your first API: GET method & fetch data'
- 'Creating a POST API: Sending Client Data to Server with CORS Setup'
- 'Recap: Displaying Server Data on the Client Side'
- Module Summary
prerequisites:
- level-01/l1-39-assignment-7/01-main
keywords:
- node.js
- express
- api
- http
- cors
- client server
- nosql
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

A backend is not “the folder where Express lives.” It is the trusted application boundary that receives requests, applies rules, communicates with data/services and sends responses.

```text
browser / mobile / other service
        ↓ HTTP request
backend server
        ↓
application logic + database/services
        ↓ HTTP response
client uses response
```

Before Express, understand the HTTP cycle itself.

## What you will learn

- client-server architecture;
- what Node.js contributes as a JavaScript runtime;
- why asynchronous/non-blocking I/O matters;
- what Express abstracts;
- SQL vs NoSQL at a beginner decision level;
- environment setup and development reload tools;
- GET and POST APIs;
- JSON request bodies and CORS;
- consuming a backend response from a frontend.

## 1. Run the verified HTTP baseline

The package contains `run/01_http_baseline.mjs`, which uses only Node's built-in `http` module. It starts a local server on an available port, calls its own `/api/health` endpoint and closes.

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  res.setHeader("content-type", "application/json");
  res.end(JSON.stringify({ ok: true, path: req.url, method: req.method }));
});
```

This is the core idea Express makes easier: inspect a request, choose application behavior, create a response.

<span class="output-label">Verified output</span>

```text
GET /api/health -> ok=true
```

That output is produced by the included script during release verification.

## 2. What Node.js is doing

Node runs JavaScript outside the browser and provides APIs for networking, files, processes and other operating-system capabilities. Your server can spend much of its time waiting for I/O: database queries, files, HTTP calls. Async programming lets the process continue handling other work instead of blocking on each wait.

Do not confuse “non-blocking” with “everything is parallel.” CPU-heavy work can still monopolize the process and may need different architecture.

## 3. Express adds routing and middleware

Reference-only Express version of the same idea:

```js
import express from "express";

const app = express();
app.use(express.json());

app.get("/api/destinations", (req, res) => {
  res.json({ data: [] });
});

app.post("/api/destinations", (req, res) => {
  res.status(201).json({ data: req.body });
});

app.listen(4000);
```

Express models an application as routes and middleware through the request-response cycle.

## 4. GET vs POST

A beginner-friendly distinction:

```text
GET  /api/destinations  → read the collection
POST /api/destinations  → create a new destination from submitted data
```

HTTP methods communicate intent. Later you will add `PATCH`/`PUT` and `DELETE`.

## 5. JSON body parsing

`express.json()` is middleware. It reads a JSON request body and makes the parsed value available as `req.body`. That value is still **untrusted input**. Parsing is not validation.

## 6. CORS

When a browser frontend and backend live on different origins, the browser applies cross-origin rules. CORS response headers tell the browser which cross-origin requests are permitted.

Do not “fix CORS” by allowing every origin in every production environment without understanding the policy. Configure allowed frontend origins intentionally.

## 7. SQL vs NoSQL and why MongoDB appears here

The source path chooses MongoDB, a document database, for Level 01. That lets you store JSON-like documents and work quickly with JavaScript objects. It does not mean MongoDB is universally better than SQL. Level 02 later teaches relational design and PostgreSQL so you can choose based on data relationships and constraints.

## 8. Frontend → backend connection

From a browser/React client:

```js
const response = await fetch("http://localhost:4000/api/destinations");
if (!response.ok) throw new Error("Request failed");
const payload = await response.json();
```

Now the frontend consumes an HTTP contract instead of importing backend memory directly.

## Practice path

1. Run `run/01_http_baseline.mjs`.
2. Change `/api/health` to `/api/profile` and return your own JSON object.
3. Read `reference/express-api.mjs`.
4. Rebuild it in a fresh Express project locally.
5. Call GET and POST from your browser or an API client.
6. Write down request method, URL, body, status and response for both calls.

Express was not installed in the release environment, so its code is **REFERENCE-ONLY**; only the built-in Node HTTP example is claimed as executed.
