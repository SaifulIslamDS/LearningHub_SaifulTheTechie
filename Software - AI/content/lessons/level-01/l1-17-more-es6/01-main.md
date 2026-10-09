---
title: More ES6 & JavaScript Semantics
order: 1
summary: Understand truthiness, strict equality, scope, closures and array transformation methods.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '17'
source_type: source-curriculum
topics:
- Module overview — primitive and non-primitive data types
- null vs undefined and why undefined happens
- Truthy and falsy values in JavaScript
- == vs === and implicit conversion
- Block scope, global scope, and hoisting
- (Advanced) Closure in detail
- (Optional) Callback function and passing different functions
- (Advanced) Pass by reference vs pass by value
- Pass by value and pass by reference (Animated)
- Pre/post increment and pre/post decrement
- 'Array power methods: map, forEach, filter, find (Part 1)'
- 'Array power methods: slice, reduce (Part 2)'
- Module summary and interview questions
prerequisites: []
keywords:
- javascript
- more es6 & javascript semantics
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

This module moves from syntax into **JavaScript behavior**: value categories, equality, scope, closures and the array methods used constantly in modern frontend and backend code.

## What you will learn

- primitive vs non-primitive values;
- `null` and `undefined`;
- truthy and falsy values;
- `==` vs `===`;
- scope and hoisting;
- closures and callbacks;
- value vs reference behavior;
- increment/decrement;
- `map`, `forEach`, `filter`, `find`, `slice` and `reduce`.

## 1. Primitive values and references

Primitive values such as numbers, strings and booleans behave like values copied directly:

```javascript
let a = 10;
let b = a;
b = 20;
console.log(a);
```

```text
10
```

Objects and arrays are accessed through references:

```javascript
const original = { score: 10 };
const alias = original;
alias.score = 20;
console.log(original.score);
```

```text
20
```

Both variables point to the same object.

## 2. `null` vs `undefined`

Use `null` when your application intentionally represents “no value.” `undefined` often means no value was assigned, no argument was supplied or a property was missing.

```javascript
const profile = { avatarUrl: null };
let lastLogin;
```

## 3. Truthy and falsy

Conditions convert values to booleans. Falsy values include:

```text
false
0
-0
0n
""
null
undefined
NaN
```

Most other values—including empty arrays and empty objects—are truthy.

## 4. Strict equality avoids coercion surprises

```javascript
console.log(5 == "5");
console.log(5 === "5");
```

```text
true
false
```

`==` can coerce types before comparison. `===` compares without that equality coercion. Prefer strict equality unless you deliberately understand and want the coercion behavior.

## 5. Scope

```javascript
const app = "hub";

function example() {
  const local = "inside";
  if (true) {
    const block = "block";
    console.log(app, local, block);
  }
}
```

`block` is not available outside the `if` block. `local` is not available outside the function. `app` is visible inside because outer scopes can be read from inner scopes.

## 6. Closure

A closure lets a function keep access to variables from the scope where it was created:

```javascript
function createCounter() {
  let count = 0;

  return function next() {
    count += 1;
    return count;
  };
}

const counter = createCounter();
console.log(counter());
console.log(counter());
```

```text
1
2
```

Closures power many patterns: event handlers, private state, factories and hooks.

## 7. Callbacks

```javascript
function process(value, operation) {
  return operation(value);
}

const doubled = process(5, n => n * 2);
```

A callback is simply a function passed as data to another function so that the receiving function can call it.

## 8. `map`, `filter` and `find`

```javascript
const prices = [120, 250, 80, 400];

const withTax = prices.map(price => price * 1.05);
const expensive = prices.filter(price => price >= 200);
const firstLarge = prices.find(price => price >= 200);
```

Use:

- `map` when every input item becomes an output item;
- `filter` when some items remain;
- `find` when you need the first matching item;
- `forEach` when you deliberately want a side effect for each item rather than a returned collection.

## 9. `reduce` combines many values into one result

```javascript
const total = prices.reduce((sum, price) => sum + price, 0);
console.log(total);
```

```text
850
```

The second argument (`0`) is the initial accumulator. Always choose an initial value that matches the result type you intend to build.

## 10. `slice` returns a shallow section

```javascript
const firstTwo = prices.slice(0, 2);
```

`slice` does not mutate the original array. Do not confuse it with `splice`, which can mutate.

## Practice with the verified script

Use `11_more_es6.js`. For each operation, state whether it mutates, returns a new value, returns one item or reduces many items to one result. That vocabulary becomes important when you manage React state.
