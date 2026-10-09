---
title: Repeat Work with JavaScript Loops
order: 1
summary: Repeat work with for, while, break and continue, and reason about stopping rules.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '10'
source_type: source-curriculum
topics:
- What is a Loop? Explore the for loop
- Introduction to While Loop
- Problem-solving with While Loop
- Introduction to For Loop
- Problem-solving with For Loop (Task)
- Different ways to use loop
- When to use a break and continue
- (optional) Introduction to Do While Loop
- Difference between types of loops Module Summary
prerequisites: []
keywords:
- javascript
- fundamental concepts of loops
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

A loop repeats a block of code while a condition or sequence says repetition should continue. Loops are one of the first tools that let a program handle **any number of items** instead of hard-coding one statement per item.

## What you will learn

- `while` and `for` loops;
- counters and loop conditions;
- solving repeated calculations;
- `break` and `continue`;
- `do...while`;
- how to choose the simplest loop for the job.

## 1. A `while` loop

```javascript
let count = 1;

while (count <= 3) {
  console.log(count);
  count += 1;
}
```

```text
1
2
3
```

A working loop needs three ideas: starting state, continuation condition and a change that eventually makes the condition false.

## 2. Solve a running total

```javascript
let n = 1;
let total = 0;

while (n <= 5) {
  total += n;
  n += 1;
}

console.log(total);
```

```text
15
```

`total` is an **accumulator**. It carries a result forward from one iteration to the next.

## 3. A `for` loop groups the loop controls

```javascript
for (let i = 0; i < 5; i += 1) {
  console.log(i);
}
```

The header contains initialization, condition and update. Use a `for` loop when those parts naturally belong together.

## 4. Loop over an array

```javascript
const prices = [120, 250, 80, 400];
let sum = 0;

for (let i = 0; i < prices.length; i += 1) {
  sum += prices[i];
}

console.log(sum);
```

```text
850
```

Notice the condition `i < prices.length`. Using `<=` would attempt one index beyond the end of the array.

## 5. `break` stops the loop

```javascript
const values = [4, 9, 13, 20];

for (const value of values) {
  if (value > 10) {
    console.log(value);
    break;
  }
}
```

This prints the first matching value and stops searching.

## 6. `continue` skips the rest of one iteration

```javascript
for (let i = 1; i <= 5; i += 1) {
  if (i % 2 === 0) continue;
  console.log(i);
}
```

```text
1
3
5
```

## 7. `do...while` guarantees one execution

```javascript
let attempts = 0;

do {
  attempts += 1;
} while (attempts < 1);
```

Use it when the body really should run once before you test whether another repetition is needed. It is less common than `for` and `while` in many application codebases.

## 8. Choose loops by intent

- Use `for...of` when you only need each value.
- Use a traditional `for` loop when you need index control.
- Use `while` when repetition is driven by a condition rather than a known collection length.
- Later, methods such as `map`, `filter` and `reduce` can express common array transformations more declaratively.

## Practice with the verified script

Use `04_loops.js`. Change the array and loop limits, then implement three tasks: total all prices, count prices above a threshold and stop when the first value above 300 is found.

## Career build extension
## Choose a loop from the shape of the problem

A loop is not a goal. It is a tool for repeated work. Ask what controls repetition:

```text
Known number of iterations?      → for loop is often clear
Repeat until condition changes?  → while loop can fit naturally
Need at least one execution?     → do...while may fit
Need to stop early?              → break
Need to skip one item?           → continue
```

### Trace the state by hand

```js
let total = 0;
for (let i = 1; i <= 4; i++) {
  total += i;
  console.log(i, total);
}
```

Before running it, write the values:

```text
i=1 total=1
i=2 total=3
i=3 total=6
i=4 total=10
```

That habit makes nested logic and off-by-one errors much easier to debug.

### Use loops to solve data problems

```js
const orders = [1200, 800, 2500, 300];
let highValueCount = 0;

for (const amount of orders) {
  if (amount >= 1000) highValueCount++;
}

console.log(highValueCount); // 2
```

Now change the task: calculate total revenue, find the largest order, or stop when the first order above 2000 appears. One dataset can teach several loop patterns.
