---
title: Write Cleaner JavaScript with Modern ES6
order: 1
summary: Use modern JavaScript syntax including defaults, template strings, arrow functions, spread, destructuring and optional chaining.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '16'
source_type: source-curriculum
topics:
- Milestone Roadmap (Animated)
- ES6 intro — difference between var, let, and const
- Default parameters for not-provided values
- Template strings — multiline and dynamic strings
- 'Arrow functions: syntax, params, return'
- Spread operator, array max, copy arrays
- (Advanced) Object and array destructuring
- Keys, values, entries, delete, seal, freeze
- Nested object, dot vs bracket notation, optional chaining
- 'Looping objects: for…in, for…of, entries'
- Boost ES6 skills with AI — summary and practice
prerequisites: []
keywords:
- javascript
- es6 fundamentals
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

“ES6” originally referred to ECMAScript 2015, a major JavaScript language update. In everyday conversation, developers often use the label loosely for modern JavaScript features introduced around that era and later. The important goal is not the date; it is learning patterns that make data transformation and application code clearer.

## What you will learn

- `var` vs `let` vs `const`;
- default parameters;
- template strings;
- arrow functions;
- spread syntax;
- object/array destructuring;
- object utilities and immutability helpers;
- optional chaining;
- `for...in`, `for...of` and entries.

## 1. Prefer block-scoped declarations

```javascript
const appName = "Learning Hub";
let currentLesson = 16;
```

`let` and `const` are block scoped. `var` has function scope and hoisting behavior that can surprise beginners. You will still encounter `var` in older code, but use `const` by default and `let` when reassignment is needed.

## 2. Default parameters

```javascript
function createGreeting(name = "Learner") {
  return `Hello, ${name}!`;
}
```

Defaults apply when the argument is `undefined` or omitted.

## 3. Template strings

```javascript
const name = "Saiful";
const lessons = 16;
const message = `${name} has reached lesson ${lessons}.`;
```

Backticks support expressions and multi-line strings, reducing awkward concatenation.

## 4. Arrow functions

```javascript
const square = number => number * number;
console.log(square(6));
```

```text
36
```

Arrow functions have different `this` behavior from traditional functions. For small data transformations that do not need their own `this`, they are extremely common.

## 5. Spread creates a shallow copy or combines iterables

```javascript
const base = ["HTML", "CSS"];
const extended = [...base, "JavaScript"];
```

For objects:

```javascript
const user = { name: "Saiful", role: "learner" };
const promoted = { ...user, role: "developer" };
```

Spread is **shallow**. Nested objects still refer to the same nested values unless you copy those too.

## 6. Destructuring extracts values by shape

```javascript
const project = { title: "Learning Hub", status: "active" };
const { title, status } = project;
```

Array destructuring uses position:

```javascript
const coordinates = [23.81, 90.41];
const [latitude, longitude] = coordinates;
```

## 7. Object utilities

```javascript
const settings = { theme: "dark", compact: false };

console.log(Object.keys(settings));
console.log(Object.values(settings));
console.log(Object.entries(settings));
```

`Object.freeze()` prevents certain direct mutations to an object, but again it is shallow.

## 8. Optional chaining

```javascript
const city = user.address?.city;
```

If `address` is `null` or `undefined`, the expression returns `undefined` instead of trying to read `.city` and throwing an error.

Combine it with nullish coalescing when you need a fallback only for missing values:

```javascript
const cityLabel = user.address?.city ?? "Unknown city";
```

## 9. `for...of` vs `for...in`

```javascript
for (const value of [10, 20, 30]) {
  console.log(value);
}
```

`for...of` iterates iterable values. `for...in` iterates enumerable property keys and is commonly used with objects, though `Object.entries()` is often clearer when you need both key and value.

## Practice with the verified script

Open `10_es6_fundamentals.js`. Rewrite one older-style function with default parameters, an arrow function, destructuring and spread. Then inspect the output and confirm that the original object or array is unchanged where you intended immutability.

## Career build extension
## Modern syntax should improve clarity, not hide logic

ES6 introduced patterns you will use constantly in React, Node and Next.js. Practice them on ordinary objects before they appear inside framework code.

### `let` and `const`

Default to `const` when the binding does not need reassignment. Use `let` for intentional reassignment. Avoid `var` in new application code unless you are specifically learning its historical function scope/hoisting behavior.

### Default parameters + template strings

```js
function greet(name = "Learner") {
  return `Welcome, ${name}!`;
}
```

### Arrow functions

```js
const total = (a, b) => a + b;
```

Arrow functions are concise, but remember they have different `this` behavior from traditional functions. You do not need that distinction for every beginner callback, but you should know it exists.

### Spread copies containers, not deeply nested values

```js
const skills = ["HTML", "CSS"];
const nextSkills = [...skills, "JavaScript"];
```

For objects:

```js
const user = { name: "Saiful", active: false };
const updated = { ...user, active: true };
```

This pattern becomes central to immutable React state updates.

### Destructuring and optional chaining

```js
const course = { title: "React", author: { name: "Saiful" } };
const { title } = course;
console.log(course.author?.name);
```

Use optional chaining when absence is genuinely possible. Do not add `?.` everywhere to silence misunderstandings about your data model.

### Object iteration

`Object.keys`, `Object.values` and `Object.entries` give different views of an object. Practice each with `for...of` so you can read API response objects confidently.
