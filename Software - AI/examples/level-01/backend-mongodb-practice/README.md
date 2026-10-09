# Backend & MongoDB practice package

`run/` contains framework-independent Node.js programs that are executed during release verification. They let you learn HTTP, CRUD state, query objects, RBAC and payment-record idempotency without depending on cloud accounts.

`reference/` mirrors Express, MongoDB, Better Auth and Stripe tutorial snippets. Those files require packages and/or services and are clearly marked **REFERENCE-ONLY**.

- `run/06_error_contract.mjs` — executable validation + stable API error-envelope example used by the ST Recommended production-error tutorial.
