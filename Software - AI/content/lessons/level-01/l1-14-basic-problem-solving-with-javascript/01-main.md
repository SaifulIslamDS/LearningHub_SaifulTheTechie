---
title: Solve Programming Problems Step by Step
order: 1
summary: Translate a plain-language requirement into inputs, rules, code and checks.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '14'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites: []
keywords:
- javascript
- basic problem solving with javascript
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

Problem solving is translating a requirement into a sequence you can verify, not memorizing syntax.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Real tasks arrive as vague requirements. Engineers clarify them, define edge cases and test known answers.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Core idea

Use this loop: restate the problem → identify inputs/output → write rules/edge cases → solve one tiny example by hand → code → test normal, boundary and invalid cases.

## Worked example

```javascript
const orders = [{id:1,status:"Delivered",amount:1200},{id:2,status:"Cancelled",amount:800},{id:3,status:"Delivered",amount:1500},{id:4,status:"Pending",amount:500}];
let deliveredRevenue = 0; let deliveredCount = 0;
for (const order of orders) { if (order.status !== "Delivered") continue; deliveredRevenue += order.amount; deliveredCount++; }
console.log(`Delivered orders: ${deliveredCount}`);
console.log(`Delivered revenue: BDT ${deliveredRevenue}`);
```

<span class="output-label">Verified output</span>

```text
Delivered orders: 2
Delivered revenue: BDT 2700
```

<div class="verified"><b>RUN-HERE:</b> this output was executed with Node while preparing v0.3.0.</div>

## Practice files and code trail

This tutorial is paired with `javascript-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Problem solving is a repeatable process

Do not start by typing random code. Use this sequence:

```text
1. Restate the problem in your own words.
2. Identify inputs and expected output.
3. Work one small example by hand.
4. Break the solution into steps.
5. Implement the simplest correct version.
6. Test normal + edge cases.
7. Improve naming/structure only after it works.
```

### Example: highest order value

Input:

```js
[1200, 850, 3400, 2200]
```

Hand solution: start with the first value, compare every later value, replace the current maximum when a larger value appears.

```js
function maxOrder(orders) {
  if (orders.length === 0) return null;
  let max = orders[0];
  for (const amount of orders) {
    if (amount > max) max = amount;
  }
  return max;
}
```

Test:

```js
console.log(maxOrder([1200, 850, 3400, 2200])); // 3400
console.log(maxOrder([])); // null
```

The algorithm matters more than clever syntax. After you understand it, compare your version with `Math.max(...orders)` and explain the trade-off.

## Practice ladder

Solve these without AI first, then use AI to review your solution:

- count positive numbers;
- find the longest string;
- remove duplicate values;
- calculate total value from an array of objects;
- return the top-scoring object;
- group simple records by a category.

When asking AI for help, provide your attempt and ask for a hint or critique rather than a complete replacement solution.
