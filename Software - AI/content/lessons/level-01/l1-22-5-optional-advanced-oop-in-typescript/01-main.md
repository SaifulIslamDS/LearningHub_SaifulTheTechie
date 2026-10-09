---
title: OOP in TypeScript
order: 1
summary: Model behavior with classes, inheritance, access modifiers, polymorphism,
  abstraction and encapsulation.
level: Intermediate
time: 50–70 min
curriculum_level: Level 01
source_module: '22.5'
source_type: source-curriculum
topics:
- Introduction to OOP
- Understanding Classes & Object Modeling
- Constructors and Method Design
- Inheritance and Code Reusability
- Type Narrowing and Type Safety
- Access Modifiers and Data Protection
- Getters, Setters, and Static Members
- Polymorphism in Practice
- Abstraction for Scalable Design
- Encapsulation and Data Integrity
- Module Summary
prerequisites:
- level-01/l1-22-more-typescript/01-main
keywords:
- typescript
- oop
- classes
- inheritance
- polymorphism
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

Object-oriented programming (OOP) organizes code around objects that combine state and behavior. TypeScript adds access modifiers, interfaces and static checking to JavaScript classes, which can make certain domain models easier to express.

OOP is one tool, not the definition of “professional code.” Use classes when they make responsibilities and invariants clearer; use functions and plain objects when those are simpler.

## What you will learn

- classes and instances;
- constructors;
- inheritance;
- type guards;
- access modifiers;
- getters, setters and static members;
- polymorphism;
- abstraction and encapsulation.

## 1. Class and instance

```typescript
class Course {
  constructor(
    public readonly id: string,
    public title: string,
  ) {}

  rename(nextTitle: string) {
    if (!nextTitle.trim()) throw new Error("Title is required");
    this.title = nextTitle.trim();
  }
}

const course = new Course("ts-01", "TypeScript");
```

The constructor establishes initial state. `rename()` centralizes one rule instead of letting every caller manipulate title state differently.

## 2. Inheritance reuses behavior through an is-a relationship

```typescript
class User {
  constructor(public name: string) {}
}

class Admin extends User {
  canManageUsers() {
    return true;
  }
}
```

Inheritance can be useful, but deep hierarchies become rigid. Composition—building objects from smaller capabilities—is often easier to change.

## 3. Type guards narrow unions

```typescript
function describe(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}
```

For objects, `in` and `instanceof` can also narrow types.

## 4. Access modifiers communicate boundaries

```typescript
class Wallet {
  #balance = 0;

  deposit(amount: number) {
    if (amount <= 0) throw new Error("Amount must be positive");
    this.#balance += amount;
  }

  get balance() {
    return this.#balance;
  }
}
```

JavaScript private fields (`#balance`) are enforced at runtime. TypeScript `private` is primarily a type-system restriction. Understand which kind of privacy you actually need.

## 5. Polymorphism through a shared contract

```typescript
interface Notifier {
  send(message: string): Promise<void>;
}

class EmailNotifier implements Notifier {
  async send(message: string) {
    console.log(`email: ${message}`);
  }
}
```

Another implementation can satisfy the same contract. Callers can depend on `Notifier` instead of a specific delivery channel.

## 6. Abstraction hides unnecessary implementation details

A payment service might expose `charge()` without forcing every caller to know how tokens, retries and provider requests work. The abstraction is valuable when it creates a stable, meaningful boundary—not simply because “OOP requires abstraction.”

## 7. Encapsulation protects invariants

An invariant is something that should always remain true: quantity cannot be negative, an order needs at least one item, a published article must have a title. Encapsulate state changes where that helps enforce the rule consistently.

## Practice with the verified script

Use `03_oop_typescript.ts`. Identify which rules belong inside the class and which could stay as pure functions. Refactor one class to use composition instead of inheritance and compare the trade-offs.

## Career build extension
## Model behavior, not just classes

OOP is useful when objects have identity, state and behavior that belong together.

```ts
class Account {
  constructor(public readonly id: string, private balance = 0) {}

  deposit(amount: number) {
    if (amount <= 0) throw new Error("Amount must be positive");
    this.balance += amount;
  }

  getBalance() { return this.balance; }
}
```

The private state cannot be changed arbitrarily from outside. Methods enforce rules.

### Inheritance vs composition

Inheritance can model a true “is-a” relationship, but composition is often easier to change. Do not create inheritance trees only because the language supports `extends`.

### Polymorphism

Program against a shared contract when multiple implementations should be interchangeable. For example, different notification services can implement the same `send()` interface.

### Abstraction + encapsulation

Abstraction exposes the useful contract; encapsulation hides internal state/implementation choices. Together they let one part of a system change without forcing every caller to know how it works internally.

Use OOP when it improves the model. A plain function/object is still correct for many problems.
