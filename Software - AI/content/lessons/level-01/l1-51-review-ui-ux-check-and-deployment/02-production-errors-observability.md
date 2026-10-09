---
title: Production Error Contracts & First Observability Habits
order: 2
summary: Design errors that help users, frontend code and developers without leaking sensitive implementation details.
level: Intermediate
curriculum_level: Level 01
source_module: '51'
source_type: st-recommended
topics: []
prerequisites:
- level-01/l1-51-review-ui-ux-check-and-deployment/01-main
keywords:
- error handling
- validation
- logging
- observability
- api contract
reviewed: '2026-10-09'
files:
- level-01/backend-mongodb-practice.zip
resources:
- title: Express error handling
  url: https://expressjs.com/en/guide/error-handling.html
  source: Express
  type: OFFICIAL
  note: Official guidance for propagating and handling errors in Express applications.
- title: HTTP response status codes
  url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
  source: MDN
  type: REFERENCE
  note: Status-code reference for designing consistent error responses.
---
## Start here

A production application does not become reliable by hiding every failure behind “Something went wrong.” It becomes easier to operate when failures have a consistent contract, useful logs and enough context to trace what happened.

At the same time, an API must avoid returning stack traces, database credentials or internal implementation details to users.

Separate the audiences:

```text
user / frontend needs
  safe message + status + stable error code

operator / developer needs
  timestamp + request context + internal cause + stack/log data
```

## What you will learn

- how validation errors differ from unexpected server errors;
- how to design a consistent JSON error envelope;
- why logs and client responses should not contain the same detail;
- how request IDs help trace failures;
- what “observability” means at an introductory level.

## 1. Design a stable response shape

One useful pattern is:

```json
{
  "error": {
    "code": "DESTINATION_NOT_FOUND",
    "message": "Destination was not found",
    "requestId": "req_8f21"
  }
}
```

The frontend can make decisions based on `code`, while `message` remains safe for display. `requestId` gives support/developers a way to find the matching server log.

Do not make frontend logic depend on parsing a human sentence. Human text can change; stable machine-readable codes are easier to test.

## 2. Validation failures are expected failures

If a booking needs `destinationId`, `date` and `travellers`, validate before doing database work.

```js
function validateBooking(input) {
  const errors = [];

  if (!input.destinationId) errors.push("destinationId is required");
  if (!input.date) errors.push("date is required");
  if (!Number.isInteger(input.travellers) || input.travellers < 1) {
    errors.push("travellers must be a positive integer");
  }

  return errors;
}
```

That is different from an unexpected database outage. Both are errors, but they deserve different status codes, messages and operational urgency.

## 3. Log internal context, return safe context

Server log (internal):

```text
ERROR request=req_8f21 route=POST /api/bookings user=usr_14
MongoServerSelectionError: connection timed out
```

Client response (external):

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Booking service is temporarily unavailable",
    "requestId": "req_8f21"
  }
}
```

The client does not need your database hostname or stack trace.

## 4. Add a request identifier

At the start of a request, generate or accept a correlation/request ID. Attach it to logs and return it in an error response or header.

```text
request req_8f21
  ↓ auth
  ↓ validation
  ↓ service
  ↓ database
  ↓ response

Every log line carries req_8f21
```

Later, production observability tools can connect logs, metrics and traces. At this level, the important habit is **structured context instead of random console messages**.

## 5. What to observe first

Start with a few signals:

- request count;
- error count and error rate;
- response duration;
- slow database operations;
- authentication failures;
- payment/webhook failures;
- deployment version.

These answer practical questions: “Is the system failing?”, “Where?”, “Since when?”, and “Did the new deployment change behavior?”

## Build with the practice package

1. Run `run/06_error_contract.mjs` from the practice package.
2. Inspect the successful validation result and the stable error object.
3. Add one new validation rule.
4. Create an Express error middleware that converts known application errors to your JSON envelope.
5. Log the internal cause separately from the safe client message.
6. Add a generated `requestId` to both.

This release executes the framework-independent error-contract example. Express middleware integration remains REFERENCE-ONLY unless you run the Express project locally.

## Professional context

Reliability work begins before expensive observability platforms. Consistent errors, request context, safe messages and clear logs are foundational engineering habits that make later monitoring, alerting and incident investigation much easier.
