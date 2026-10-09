---
title: Design Reusable Logic with Functions
order: 1
summary: Package reusable behavior with parameters, arguments and return values.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '13'
source_type: source-curriculum
topics:
- What are functions and function syntax
- Function Intro with animation
- Function parameter, handle multiple parameters
- How Function works and argument vs parameters
- Function return and set return value to a variable
- Recap and conditional return of odd and even
- Different types of parameters for a function
- Sum of all numbers in an array using function
- Return all the even numbers of an array
- Function Summary and Practice Tasks
prerequisites: []
keywords:
- javascript
- fundamentals of functions
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

A function packages behavior behind a name. Good functions let you describe *what* a program does without repeating *how* every time.

## What you will learn

- function declarations and calls;
- parameters vs arguments;
- return values;
- multiple and default-like inputs;
- functions that process arrays;
- how to design a function around one clear responsibility.

## 1. Define and call a function

```javascript
function greet() {
  console.log("Welcome to the Learning Hub");
}

greet();
```

The function does nothing until it is called.

## 2. Parameters describe inputs

```javascript
function greetLearner(name) {
  return `Welcome, ${name}`;
}

console.log(greetLearner("Saiful"));
```

`name` is a **parameter** in the function definition. `"Saiful"` is the **argument** supplied in this call.

## 3. Return data instead of only printing it

```javascript
function calculateSubtotal(price, quantity) {
  return price * quantity;
}

const subtotal = calculateSubtotal(250, 4);
console.log(subtotal);
```

```text
1000
```

Returning a value makes the function reusable in other calculations, tests and interfaces. `console.log()` is useful for observation; it is not a substitute for a return value when callers need the result.

## 4. Conditional return

```javascript
function parity(number) {
  if (number % 2 === 0) return "even";
  return "odd";
}
```

Early returns can simplify control flow because the function exits as soon as the result is known.

## 5. Functions can accept arrays

```javascript
function sum(values) {
  let total = 0;

  for (const value of values) {
    total += value;
  }

  return total;
}

console.log(sum([10, 20, 30]));
```

```text
60
```

The function does not care whether the array contains three items or three hundred. That is a key reason functions and collections work so well together.

## 6. Return selected items

```javascript
function evenNumbers(values) {
  const result = [];

  for (const value of values) {
    if (value % 2 === 0) {
      result.push(value);
    }
  }

  return result;
}
```

Later, `filter()` expresses the same pattern more directly, but the loop version helps you understand what filtering actually means.

## 7. Design functions around contracts

Before writing a function, write its contract in plain language:

```text
name: calculateDiscountedTotal
input: subtotal number, discountPercent number
output: final total number
rule: never return a negative total
```

Then implement it:

```javascript
function calculateDiscountedTotal(subtotal, discountPercent) {
  const discount = subtotal * (discountPercent / 100);
  return Math.max(0, subtotal - discount);
}
```

Thinking in contracts becomes increasingly important in TypeScript, API design and testing.

## 8. One responsibility is easier to reuse

A function that fetches data, formats HTML, updates the DOM, writes a file and sends email is difficult to test and reuse. Prefer smaller functions with explicit inputs and outputs, then compose them into larger workflows.

## Practice with the verified script

Use `07_functions.js`. Add a function that receives an array of order totals and returns the average. Then create a second function that returns only totals above the average. Keep calculation separate from logging.

## Career build extension
## Design a function around one responsibility

A function is easier to reuse when its name, inputs and returned value form a clear contract:

```js
function calculateTotal(amounts) {
  let total = 0;
  for (const amount of amounts) total += amount;
  return total;
}
```

Call it:

```js
const revenue = calculateTotal([1200, 800, 2500]);
console.log(revenue); // 4500
```

### Parameters vs arguments

`amounts` is the parameter in the definition. `[1200, 800, 2500]` is the argument supplied during this call. Keep that vocabulary clear because documentation and interview questions use it constantly.

### Return values compose

Prefer returning useful values rather than printing inside every function. A returned value can feed another function, a condition or a UI component.

```js
function isEven(number) {
  return number % 2 === 0;
}

const evenNumbers = [1,2,3,4,5,6].filter(isEven);
```

### Arrays + functions

Write `sumArray`, `getEvenNumbers`, `findMaximum` and `calculateAverage`. For each function, decide what should happen for an empty array. That forces you to think about the contract rather than the happy path only.
