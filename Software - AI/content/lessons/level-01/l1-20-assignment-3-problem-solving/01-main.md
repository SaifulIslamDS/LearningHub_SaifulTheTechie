---
title: Assignment 3 — ES6 Problem Solving
order: 1
summary: Build a small expense analyzer with modern array/object methods and tests.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '20'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites: []
keywords:
- javascript
- assignment 3 — es6 problem solving
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

This is the JavaScript/ES6 independence gate. The task combines transformation, aggregation, edge cases and explanation.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Small data utilities resemble logic used in dashboards, APIs and frontend summaries.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Core idea

Brief: calculate total spending, spending by category, top category, and expenses above a threshold. Do not mutate original records. Handle empty input and define tie behavior.

## Worked example

```javascript
const expenses = [{category:"Food",amount:900},{category:"Transport",amount:450},{category:"Food",amount:350},{category:"Learning",amount:1200}];
const total = expenses.reduce((sum, item) => sum + item.amount, 0);
const byCategory = expenses.reduce((acc, item) => { acc[item.category] = (acc[item.category] ?? 0) + item.amount; return acc; }, {});
console.log(`Total: BDT ${total}`);
for (const [category, amount] of Object.entries(byCategory)) console.log(`${category}: ${amount}`);
```

<span class="output-label">Verified output</span>

```text
Total: BDT 2900
Food: 1250
Transport: 450
Learning: 1200
```

<div class="verified"><b>RUN-HERE:</b> this output was executed with Node while preparing v0.3.0.</div>

## Practice files and code trail

This tutorial is paired with `javascript-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Assignment brief

Build a small JavaScript **order analytics** script using ES6 features and array methods.

Your input should be an array of at least eight order objects. Produce:

- delivered orders;
- total delivered revenue;
- highest-value delivered order;
- unique customer names;
- a new display array using `map`;
- a safe lookup by optional nested property.

Use `const`/`let`, template strings, destructuring, spread and at least three of `map`, `filter`, `find`, `reduce`.

## Evidence

Commit the input data, source code and actual terminal output. Add a short README explaining one place where immutable copying prevented accidental data changes.
