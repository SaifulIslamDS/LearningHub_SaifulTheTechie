---
title: Problem Solving with JavaScript + ES6 — Part 1
order: 1
summary: Solve collection-transformation problems with filter and map.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '18'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites: []
keywords:
- javascript
- problem solving with javascript + es6 — part 1
reviewed: '2026-10-09'
files:
- level-01/javascript-foundations.zip
resources:
- title: MDN JavaScript Guide
  url: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
  source: MDN
  note: Official browser-oriented JavaScript guide.
- title: MDN JavaScript Reference
  url: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference
  source: MDN
  note: Reference for language syntax and built-ins.
- title: Node.js documentation
  url: https://nodejs.org/docs/latest/api/
  source: Node.js
  note: Official runtime documentation.
---
## Start here

Modern array methods can express a data pipeline clearly when each step has one purpose.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Filtering and transforming API data is a routine frontend/full-stack task.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Core idea

Think source data → keep relevant records → transform them for the next consumer. While learning, use named intermediate arrays so each stage can be inspected.

## Worked example

```javascript
const products = [{name:"Keyboard",price:2500,stock:5},{name:"Mouse",price:900,stock:0},{name:"Monitor",price:18000,stock:3}];
const available = products.filter(p => p.stock > 0);
const labels = available.map(p => `${p.name}: BDT ${p.price}`);
console.log(labels.join("\n"));
```

<span class="output-label">Verified output</span>

```text
Keyboard: BDT 2500
Monitor: BDT 18000
```

<div class="verified"><b>RUN-HERE:</b> this output was executed with Node while preparing v0.3.0.</div>

## Practice files and code trail

This tutorial is paired with `javascript-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## ES6 problem-solving set — Part 1

Use modern syntax only where it makes the solution clearer.

### Challenge 1: normalize product data

Given:

```js
const products = [
  { id: 1, name: " Keyboard ", price: 4500 },
  { id: 2, name: "mouse", price: 1800 },
];
```

Return a new array with trimmed names and a `priceLabel` such as `BDT 4500`. Do not mutate the input objects.

### Challenge 2: safe profile label

Create a function that accepts a possibly incomplete user object and returns a useful label using default parameters, destructuring, nullish coalescing and optional chaining where appropriate.

### Challenge 3: merge settings

Merge default settings with user overrides using object spread. Explain which object's property wins when both contain the same key.

## Reasoning checkpoint

For every solution, explain:

- which value is input;
- which value is newly created;
- whether anything is mutated;
- what happens when a property is missing.

These questions prepare you for React state and API data handling.
