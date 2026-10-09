---
title: Model Reusable Data with Advanced TypeScript
order: 1
summary: Use interfaces, generics, assertions, enums/literals and utility types to model reusable APIs safely.
level: Intermediate
time: 50–70 min
curriculum_level: Level 01
source_module: '22'
source_type: source-curriculum
topics:
- Type Assertions and Type Casting Strategies
- Interfaces for Structured Type Definitions
- Generics for Reusable and Scalable Types
- Enums and as const for Immutable Patterns
- Utility Types for Efficient Type Transformations
- Module Summary
prerequisites:
- level-01/l1-21-typescript-fundamentals/01-main
keywords:
- typescript
- interface
- generics
- utility types
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

Advanced TypeScript is mostly about expressing relationships between types so you do not have to repeat the same shape manually. Interfaces, generics and utility types let a codebase stay flexible while preserving useful constraints.

## What you will learn

- type assertions;
- interfaces and type aliases;
- generic functions and types;
- enums and `as const`;
- utility types;
- how to choose the least powerful type feature that clearly models the problem.

## 1. Type assertions are claims, not runtime checks

```typescript
const input = document.querySelector("#email") as HTMLInputElement | null;
```

An assertion tells TypeScript to treat a value as a type you claim. It does not validate the actual runtime value. Prefer narrowing and validation when uncertainty comes from external data.

## 2. Interface vs type alias

```typescript
interface User {
  id: string;
  name: string;
}

type Status = "draft" | "published";
```

Both can describe object shapes. Type aliases also describe unions, tuples, primitives and type transformations. Interfaces support declaration merging and are often comfortable for extendable object contracts. Consistency within a project matters more than turning the choice into a rigid rule.

## 3. Generics preserve relationships

Without a generic, a reusable function may lose information:

```typescript
function first<T>(items: T[]): T | undefined {
  return items[0];
}
```

Call it with strings and the result is `string | undefined`; call it with `User[]` and the result becomes `User | undefined`.

## 4. Generic constraints

```typescript
function getId<T extends { id: string | number }>(value: T) {
  return value.id;
}
```

The generic remains flexible while requiring the property this function actually needs.

## 5. `keyof` connects keys to an object type

```typescript
function getProperty<T, K extends keyof T>(object: T, key: K): T[K] {
  return object[key];
}
```

This models a real relationship: the key must belong to the object, and the return type depends on that key.

## 6. Prefer literal unions or `as const` when they model the domain cleanly

```typescript
const roles = ["admin", "editor", "viewer"] as const;
type Role = (typeof roles)[number];
```

This gives you a runtime array and a compile-time union from one source.

## 7. Utility types transform existing contracts

```typescript
type User = {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
};

type UserPatch = Partial<Pick<User, "name" | "email">>;
type PublicUser = Omit<User, "email">;
```

Other useful built-ins include `Required`, `Readonly` and `Record`.

## 8. Reuse types around domain boundaries

A good sign that you need a type abstraction is repeated domain structure: API responses, form values, entity IDs, permissions or reusable component props. Avoid building complicated generic machinery before the problem exists.

## Practice with the verified script

Open `02_more_typescript.ts`. Trace each generic argument and utility type back to the concrete values. Change a property type deliberately and observe where the compiler reports the mismatch.

## Career build extension
## Build reusable types without over-engineering

Advanced types are valuable when they remove duplication or preserve relationships between inputs and outputs.

### Interface vs type alias

Both can describe object shapes. Interfaces are especially natural for extendable object contracts; type aliases can represent unions, intersections and mapped/conditional compositions. Prefer consistency over ideological rules.

### Generic mental model

A generic preserves a type relationship:

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
```

If callers pass `Course[]`, the result is `Course | undefined`. You did not throw away the type as `any`.

### Constraints

```ts
function getId<T extends { id: string }>(value: T) {
  return value.id;
}
```

The function accepts different objects but requires the capability it actually uses.

### `keyof`

```ts
function getField<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

This connects key choice to the object's real properties.

### Utility and mapped types

Use `Partial`, `Pick`, `Omit`, `Record`, `Required` and `Readonly` to derive new contracts from existing ones. Derivation reduces duplicated types that silently drift apart.

Use these tools to clarify a domain, not to build type puzzles nobody on the team can maintain.
