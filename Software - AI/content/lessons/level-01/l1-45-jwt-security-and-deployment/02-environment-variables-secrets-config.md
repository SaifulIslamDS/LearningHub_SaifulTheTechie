---
title: Environment Variables, Secrets & Production Configuration
order: 2
summary: Separate code from environment-specific configuration and learn what should never be committed to a public repository.
level: Intermediate
curriculum_level: Level 01
source_module: '45'
source_type: st-recommended
topics: []
prerequisites:
- level-01/l1-45-jwt-security-and-deployment/01-main
keywords:
- environment variable
- secret
- config
- deployment
- security
reviewed: '2026-10-09'
files:
- level-01/backend-mongodb-practice.zip
resources:
- title: Node.js environment variables
  url: https://nodejs.org/api/environment_variables.html
  source: Node.js
  type: OFFICIAL
  note: Official Node.js documentation for environment variables and .env files.
- title: Keeping your API credentials secure
  url: https://docs.stripe.com/keys-best-practices
  source: Stripe
  type: OFFICIAL
  note: Security guidance for secret keys and restricted access.
---
## Start here

Applications behave differently in development, test and production. The database URL changes. OAuth callback URLs change. A payment secret key changes. Logging and allowed frontend origins may change.

Those values should not be scattered through source files.

A useful mental model is:

```text
application code = versioned behavior
configuration    = environment-specific values
secret           = sensitive configuration with restricted access
```

Keeping these concerns separate makes deployment safer and makes local development easier to reproduce.

## What you will learn

- what belongs in an environment variable;
- why `.env` is convenience, not a magic security boundary;
- how to validate required configuration at startup;
- how to keep browser-visible configuration separate from server secrets;
- how to prepare a safe `.env.example` for collaborators.

## 1. Read configuration from the environment

Node exposes process-level environment values through `process.env`.

```js
const port = Number(process.env.PORT ?? 4000);
const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  throw new Error("DATABASE_URL is required");
}
```

This is much better than hard-coding a real connection string into source code. If a secret reaches Git history, deleting the line in a later commit does not automatically invalidate the leaked credential.

## 2. Fail fast when required config is missing

Create one configuration boundary rather than reading `process.env` everywhere.

```js
export function loadConfig(env = process.env) {
  const required = ["DATABASE_URL", "AUTH_SECRET"];
  const missing = required.filter((key) => !env[key]);

  if (missing.length) {
    throw new Error(`Missing required config: ${missing.join(", ")}`);
  }

  return {
    databaseUrl: env.DATABASE_URL,
    authSecret: env.AUTH_SECRET,
    port: Number(env.PORT ?? 4000),
    nodeEnv: env.NODE_ENV ?? "development",
  };
}
```

A startup failure is easier to diagnose than an authentication error twenty minutes later caused by an undefined secret.

## 3. `.env` and `.env.example` have different jobs

A local `.env` might contain real development values:

```text
DATABASE_URL=mongodb://127.0.0.1:27017/travel
AUTH_SECRET=local-development-secret
PORT=4000
```

That file should normally be ignored by Git.

A committed `.env.example` documents the required names without real credentials:

```text
DATABASE_URL=
AUTH_SECRET=
PORT=4000
```

That small file becomes part of your project's onboarding documentation.

## 4. Browser configuration is public

If a framework intentionally exposes a variable to browser JavaScript, treat that value as public. A frontend bundle cannot keep a secret from the person downloading and running it.

Never put these in browser-exposed configuration:

- database passwords;
- Stripe secret keys;
- signing secrets;
- private API credentials;
- OAuth client secrets.

A public base URL or analytics identifier may be fine. The distinction is architectural: **the browser is not a trusted secret store**.

## 5. Production platforms store configuration outside Git

Vercel, Railway, Render and other platforms provide environment/configuration controls. The exact UI changes, but the principle is stable:

```text
repository
  code + .env.example
        ↓ deploy
hosting environment
  real secret values
        ↓
application process
```

If a credential is exposed, rotate or revoke the credential. Merely hiding a repository file does not make an already leaked secret safe again.

## Build with the practice package

Open the `.env.example` files in the Next.js/full-stack practice packages.

1. List every configuration value the project needs.
2. Mark each as **public configuration** or **server secret**.
3. Create a local `.env` that is ignored by Git.
4. Add startup validation for required server values.
5. Intentionally remove one required value and confirm the application fails with a clear message.

This tutorial does not include real credentials. Never paste production secrets into a public learning repository.

## Professional context

Configuration discipline becomes more important as a system gains multiple environments, background workers, payment providers and AI APIs. A clean configuration boundary is one of the simplest changes that makes a student project look more like production engineering.
