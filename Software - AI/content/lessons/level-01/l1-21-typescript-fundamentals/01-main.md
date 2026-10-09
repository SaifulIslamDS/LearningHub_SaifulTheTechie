---
title: Make JavaScript Safer with TypeScript
order: 1
summary: Add static type safety to JavaScript with primitives, objects, functions, unions and safe nullable values.
level: Beginner
time: 50–70 min
curriculum_level: Level 01
source_module: '21'
source_type: source-curriculum
topics:
- Introduction to Typescript(What and why)
- Setting Up and Running TypeScript
- Primitive vs Non-Primitive Types
- Object Types, Literals, and Optional Properties
- 'Functions in TypeScript: Typing Inputs and Outputs'
- Rest, Spread, and Destructuring Techniques
- Conditional Expressions, Nullish Coalescing & Optional Chaining
- 'Special Types: Nullable, Unknown, and Never'
- Module Summary
prerequisites: []
keywords:
- typescript
- types
- unknown
- never
reviewed: '2026-10-09'
files:
- level-01/typescript-react-foundations.zip
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

TypeScript adds a static type system on top of JavaScript. The browser and Node.js do not execute TypeScript syntax directly in the normal workflow; TypeScript is checked and transformed into JavaScript first.

The goal is not “add types everywhere.” The goal is to make important assumptions explicit enough that tools can catch mismatches before runtime.

## What you will learn

- what TypeScript adds to JavaScript;
- setup and compilation;
- primitive and non-primitive types;
- typed objects and optional properties;
- typed function inputs and outputs;
- rest, spread and destructuring;
- nullish coalescing and optional chaining;
- `null`, `unknown` and `never`.

## 1. Your first typed variable

```typescript
const course: string = "Software & AI Engineering";
const completed: number = 21;
const active: boolean = true;
```

TypeScript can often infer these types, so this is also valid:

```typescript
const course = "Software & AI Engineering";
```

Prefer inference when the type is obvious. Add explicit annotations where they clarify a public contract or TypeScript cannot infer what you intend.

## 2. Compile TypeScript

A typical project has a `tsconfig.json` and compiles `.ts` files with `tsc` or uses a tool/framework that invokes TypeScript for you.

```bash
npx tsc --noEmit
```

`--noEmit` asks TypeScript to check the project without writing JavaScript output. This is useful in CI and during development.

## 3. Arrays and object types

```typescript
const skills: string[] = ["TypeScript", "React", "Node.js"];

type Learner = {
  id: number;
  name: string;
  website?: string;
};

const learner: Learner = {
  id: 1,
  name: "Saiful",
};
```

`website?` is optional. It may be absent.

## 4. Functions are contracts

```typescript
function calculateSubtotal(price: number, quantity: number): number {
  return price * quantity;
}
```

The parameter types describe what callers may provide; the return type describes what callers can expect back.

## 5. Rest parameters

```typescript
function sum(...values: number[]): number {
  return values.reduce((total, value) => total + value, 0);
}
```

Spread can then supply an array as arguments:

```typescript
const values = [10, 20, 30];
console.log(sum(...values));
```

## 6. Destructuring with typed objects

```typescript
function labelLearner({ name, website }: Learner): string {
  return website ? `${name} — ${website}` : name;
}
```

## 7. Optional chaining and nullish coalescing

```typescript
const city = learnerProfile.address?.city ?? "Unknown";
```

Optional chaining stops property access when an intermediate value is nullish. `??` supplies a fallback only when the left side is `null` or `undefined`—not for legitimate values such as `0` or an empty string.

## 8. `unknown` forces you to prove something before using it

```typescript
function printLength(value: unknown) {
  if (typeof value === "string") {
    console.log(value.length);
  }
}
```

`unknown` is safer than `any` for data you have not validated yet because TypeScript prevents arbitrary operations until the type is narrowed.

## 9. `never` represents an impossible/never-returning path

```typescript
function fail(message: string): never {
  throw new Error(message);
}
```

You will also see `never` in exhaustive checks when a union has no cases left.

## 10. Follow the verified TypeScript scripts

The TypeScript/React foundations download includes `.ts` examples that were compiled in strict mode during release validation. Read the TypeScript source, run a type check, then compare the emitted/runtime behavior with the JavaScript concepts you already know.

## Career build extension
## Think in contracts, not annotations everywhere

TypeScript is most useful when a type expresses an expectation at a boundary.

```ts
type Course = {
  id: string;
  title: string;
  published?: boolean;
};

function formatCourse(course: Course): string {
  return `${course.id}: ${course.title}`;
}
```

The type lets tools detect mismatched shapes before runtime.

### Primitive vs non-primitive

Use primitives (`string`, `number`, `boolean`) for values. Use arrays/objects/tuples for structure. Let inference work when the initializer is obvious; add annotations where they clarify a public function, model or ambiguous value.

### Function types

```ts
function calculatePrice(price: number, discount = 0): number {
  return price - price * discount;
}
```

Parameter and return types create a reusable contract for callers.

### Rest, spread and destructuring remain JavaScript

TypeScript does not replace JavaScript semantics. It describes them. Practice the same ES6 patterns while preserving type information.

### `unknown` before unsafe `any`

When external data has an unknown shape, `unknown` forces you to check it before use. `never` commonly appears when a code path cannot produce a value or when exhaustive logic has no remaining case.

This mindset becomes essential when you read API bodies later: type declarations do not validate network data at runtime.
