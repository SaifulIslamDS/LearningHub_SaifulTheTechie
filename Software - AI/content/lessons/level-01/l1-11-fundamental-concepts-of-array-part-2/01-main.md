---
title: Fundamental Concepts of Array — Part 2
order: 1
summary: Traverse arrays, reverse safely and sort numbers correctly.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '11'
source_type: source-curriculum
topics:
- Array Traversal using for and while Loop
- Reversing an array with/without reverse method
- Sort an array problems and solution
- Module Summary and Practice Tasks
prerequisites: []
keywords:
- javascript
- fundamental concepts of array — part 2
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

Traversal means visiting array elements in a predictable order. `sort()` and `reverse()` mutate the array they are called on.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Data transformations and UI lists depend on predictable traversal and ordering.</p></div>

## What you will learn

- Array Traversal using for and while Loop
- Reversing an array with/without reverse method
- Sort an array problems and solution

## Core idea

For numeric ascending sort, use `(a,b) => a-b`. If original order matters, copy first with spread before sorting/reversing.

## Worked example

```javascript
const nums = [30, 5, 12, 100, 20];
const reversed = [...nums].reverse();
const sorted = [...nums].sort((a, b) => a - b);
console.log(`Original: ${nums.join(", ")}`);
console.log(`Reversed: ${reversed.join(", ")}`);
console.log(`Sorted: ${sorted.join(", ")}`);
```

<span class="output-label">Verified output</span>

```text
Original: 30, 5, 12, 100, 20
Reversed: 20, 100, 12, 5, 30
Sorted: 5, 12, 20, 30, 100
```

<div class="verified"><b>RUN-HERE:</b> this output was executed with Node while preparing v0.3.0.</div>

## Practice files and code trail

This tutorial is paired with `javascript-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Traverse an array deliberately

Array traversal means visiting elements in a predictable order. With an index loop you have both value and position:

```js
const tools = ["Git", "Node", "React"];
for (let i = 0; i < tools.length; i++) {
  console.log(i, tools[i]);
}
```

A `for...of` loop is clearer when you only need values:

```js
for (const tool of tools) {
  console.log(tool);
}
```

## Reverse without hiding the algorithm

`reverse()` mutates an array. Before relying on it, understand manual reversal:

```js
const numbers = [10, 20, 30];
const reversed = [];
for (let i = numbers.length - 1; i >= 0; i--) {
  reversed.push(numbers[i]);
}
```

This teaches index movement and protects the original array.

## Sorting needs a comparison rule

Default JavaScript sorting compares strings, which surprises beginners:

```js
[2, 10, 3].sort(); // lexical ordering, not numeric intent
```

Use a numeric comparator:

```js
const scores = [2, 10, 3];
scores.sort((a, b) => a - b);
console.log(scores); // [2, 3, 10]
```

For objects, compare a property:

```js
users.sort((a, b) => b.score - a.score);
```

The comparator expresses the ordering rule. Learn to explain why a negative, zero or positive result changes item order.

## Practice sequence

Use one array of order objects. Print them, reverse a copy, sort by amount ascending, sort by amount descending, then sort by customer name. Observe which operations mutate the original and which create a new array.
