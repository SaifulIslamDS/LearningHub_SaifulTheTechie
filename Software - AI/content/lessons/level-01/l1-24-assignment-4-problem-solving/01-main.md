---
title: Assignment 4 — Typed Problem Solving
order: 1
summary: Complete a strict TypeScript problem-solving checkpoint with deterministic
  output and documented decisions.
level: Intermediate
time: 2–4 hours
curriculum_level: Level 01
source_module: '24'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites:
- level-01/l1-23-problem-solving-with-typescript/01-main
keywords:
- typescript
- assignment
- ranking
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

Assignment 4 is the TypeScript checkpoint. Build a typed student-results utility without `any`, with deterministic ranking and a clear README.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>An assignment should prove you can turn a short brief into a typed, explainable deliverable.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Reference solution slice

```typescript
type Student = { id: number; name: string; scores: number[] };
const average = (scores: number[]) => scores.reduce((a,b)=>a+b,0) / scores.length;
```

<span class="output-label">Verified output</span>
```text
Nila: 94.7
Rafi: 87.3
Asha: 86.7
```
<div class="verified"><b>RUN-HERE:</b> the included reference solution was compiled in strict mode and executed locally.</div>

## Requirements

- Model students and computed results with explicit types.
- Calculate averages to one decimal place.
- Rank descending by average, then by name for deterministic ties.
- Handle an empty input intentionally.
- Keep calculation functions pure.
- Include three additional tests/examples you chose yourself.

## Practice files and code trail

This tutorial is paired with `typescript-react-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Assignment brief

Create a TypeScript utility library with five functions and one small OOP-modeled domain.

Required evidence:

- strict TypeScript compile succeeds;
- no broad `any` escape hatches;
- at least one generic helper;
- at least one union/discriminated union;
- one utility type such as `Pick`, `Omit` or `Readonly` used for a real reason;
- one class that encapsulates an invariant;
- actual Node output from the compiled program.

Add a README explaining two errors TypeScript caught while you were developing. Those examples show the value of the type system better than a list of syntax features.
