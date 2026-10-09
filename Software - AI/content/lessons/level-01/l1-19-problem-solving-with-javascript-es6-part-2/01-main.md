---
title: Problem Solving with JavaScript + ES6 — Part 2
order: 1
summary: Aggregate records with reduce and rank results deterministically.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '19'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites: []
keywords:
- javascript
- problem solving with javascript + es6 — part 2
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

Many business problems are aggregations: totals by customer, category, status or date.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Dashboards, APIs and reporting logic often need grouped totals before presentation or storage.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Core idea

Use `reduce` with a deliberate initial accumulator. `Object.entries` turns an object of grouped totals into sortable `[key,value]` pairs. Define tie-break rules so rankings are deterministic.

## Worked example

```javascript
const orders = [{customer:"A",amount:1200},{customer:"B",amount:900},{customer:"A",amount:800}];
const totals = orders.reduce((acc, order) => { acc[order.customer] = (acc[order.customer] ?? 0) + order.amount; return acc; }, {});
console.log(JSON.stringify(totals));
const winner = Object.entries(totals).sort((a,b) => b[1]-a[1])[0];
console.log(`Top customer: ${winner[0]} (${winner[1]})`);
```

<span class="output-label">Verified output</span>

```text
{"A":2000,"B":900}
Top customer: A (2000)
```

<div class="verified"><b>RUN-HERE:</b> this output was executed with Node while preparing v0.3.0.</div>

## Practice files and code trail

This tutorial is paired with `javascript-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## ES6 problem-solving set — Part 2

Now use array methods to express transformations and aggregation.

### Challenge 1: delivered revenue

```js
const orders = [
  { id: 1, status: "delivered", amount: 1200 },
  { id: 2, status: "cancelled", amount: 900 },
  { id: 3, status: "delivered", amount: 2500 },
];
```

Use `filter` and `reduce` to calculate delivered revenue. Then write the same result with a loop and compare readability.

### Challenge 2: find one vs filter many

Use `find` to get one object by ID. Use `filter` to get all items above a price threshold. Explain why these methods return different shapes.

### Challenge 3: report rows

Use `map` to transform order objects into display rows containing `id`, `amount` and a human-readable status label.

## Make intermediate values visible

When a method chain is confusing, split it:

```js
const delivered = orders.filter(order => order.status === "delivered");
const amounts = delivered.map(order => order.amount);
const revenue = amounts.reduce((sum, amount) => sum + amount, 0);
```

Once you understand each stage, a shorter chain becomes easy to read rather than mysterious.
