---
title: Strict TypeScript & tsconfig
order: 2
summary: Use strict compiler settings as a practical quality gate instead of treating
  type errors as optional.
level: Intermediate
time: 35–50 min
curriculum_level: Level 01
source_module: ST
source_type: st-recommended
topics: []
prerequisites: []
keywords:
- typescript
- tsconfig
- strict
reviewed: '2026-10-09'
files: []
resources:
- title: TypeScript Handbook
  url: https://www.typescriptlang.org/docs/handbook/intro.html
  source: TypeScript
  note: Official guide to everyday TypeScript.
- title: Everyday Types
  url: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
  source: TypeScript
  note: Official reference for common type syntax.
- title: TypeScript 5.9 release notes
  url: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-9.html
  source: TypeScript
  note: Current documented TypeScript 5.x release notes reviewed for this milestone.
---
## Start here

`tsconfig.json` defines how the TypeScript compiler checks and emits a project. For learning and production code, strict mode is one of the highest-value defaults.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Teams need repeatable compiler behavior in local development, CI and production builds.</p></div>

## Core idea

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

Not every project needs every strictness option on day one. The important habit is to understand which safety checks are enabled and avoid weakening them merely to silence errors.
