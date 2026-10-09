---
title: Assignment 2 — JavaScript Problem Solving
order: 1
summary: Solve a small numeric data-processing assignment independently.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '15'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites: []
keywords:
- javascript
- assignment 2 — javascript problem solving
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

This assignment checks whether you can combine variables, arrays, loops, conditions and functions without step-by-step copying.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Independent decomposition and verification are the bridge from tutorials to project work.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Core idea

Brief: write `analyzeTemperatures(values)` returning min, max and average for a non-empty numeric array. Decide what invalid/empty input should do, and write at least three tests.

## Worked example

```javascript
function analyzeTemperatures(values) {
  if (!Array.isArray(values) || values.length === 0) return null;
  let min = values[0], max = values[0], sum = 0;
  for (const value of values) { if (value < min) min = value; if (value > max) max = value; sum += value; }
  return { min, max, average: sum / values.length };
}
console.log(JSON.stringify(analyzeTemperatures([28, 31, 30, 29, 32])));
```

<span class="output-label">Verified output</span>

```text
{"min":28,"max":32,"average":30}
```

<div class="verified"><b>RUN-HERE:</b> this output was executed with Node while preparing v0.3.0.</div>

## Practice files and code trail

This tutorial is paired with `javascript-foundations.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Assignment brief

Complete a small set of JavaScript problems using variables, conditionals, arrays, loops, strings, objects and functions. Each answer should be a named function with sample calls and clear output.

Suggested problems:

1. calculate discounted price from price + percentage;
2. count vowels in a string;
3. return only even numbers from an array;
4. find the most expensive product object;
5. calculate total revenue from delivered orders only.

## Submission standard

For each problem include:

```text
Problem statement
Function signature
Example input
Actual output
One edge case
Short explanation of your approach
```

Run every solution. If you use AI for review, keep your original attempt and note what you changed after the review. The assignment is evidence of reasoning, not evidence that you can paste generated code.
