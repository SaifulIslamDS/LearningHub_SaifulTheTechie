---
title: Fundamental Concepts of Array — Part 1
order: 1
summary: Store ordered collections, read by index and add/remove elements with core methods.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '9'
source_type: source-curriculum
topics:
- Store more than one value in a variable using Array
- Array Animated video
- Array length, index, Get and set by index
- Add/remove elements from arrays using push, pop, shift & unshift
- All about basic array methods, isArray
prerequisites: []
keywords:
- javascript
- fundamental concepts of array — part 1
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

An array stores an ordered collection of values under one variable name. Instead of creating `product1`, `product2`, `product3`, you can model the collection directly.

## What you will learn

- array literals;
- length and zero-based indexes;
- reading and replacing items;
- `push`, `pop`, `shift` and `unshift`;
- checking arrays with `Array.isArray()`;
- how mutation changes the same array object.

## 1. Create an array

```javascript
const skills = ["HTML", "CSS", "JavaScript"];
```

The first item is at index `0`, not `1`:

```javascript
console.log(skills[0]);
console.log(skills[2]);
```

```text
HTML
JavaScript
```

## 2. Length and last index

```javascript
console.log(skills.length);
```

```text
3
```

Because indexing starts at zero, the last valid index is usually `length - 1`:

```javascript
const lastSkill = skills[skills.length - 1];
```

## 3. Read and update by index

```javascript
const tools = ["VS Code", "Git", "Chrome"];
tools[1] = "GitHub";
console.log(tools);
```

```text
[ 'VS Code', 'GitHub', 'Chrome' ]
```

Even though `tools` was declared with `const`, the array's contents can change. `const` prevents `tools = anotherArray`, not mutation of the existing array.

## 4. Add and remove from the end

```javascript
const modules = ["HTML", "CSS"];
modules.push("JavaScript");
const removed = modules.pop();
```

`push()` adds to the end. `pop()` removes and returns the last item.

## 5. Add and remove from the beginning

```javascript
const queue = ["B", "C"];
queue.unshift("A");
const first = queue.shift();
```

`unshift()` and `shift()` work at the beginning. For very large collections, changing the beginning can require more internal movement than changing the end, but correctness and readability matter more than micro-optimization at this stage.

## 6. Check whether a value is an array

```javascript
console.log(Array.isArray(skills));
console.log(Array.isArray("HTML"));
```

```text
true
false
```

`typeof []` returns `"object"`, so `Array.isArray()` is the reliable built-in check.

## 7. Model real collections

Arrays become especially useful when items share a shape:

```javascript
const courses = [
  { id: 1, title: "HTML", complete: true },
  { id: 2, title: "JavaScript", complete: false },
];
```

Now the array models an ordered collection and each object models one course. Later you will traverse, filter, transform and render collections like this constantly.

## Practice with the verified script

Open `03_arrays.js`. Add items, remove items, replace one item by index and print the array after each operation. The important skill is to predict which indexes still exist after every mutation.

## Career build extension

Arrays become useful when the program has **many records of the same kind**. Instead of creating `product1`, `product2`, `product3`, store products in one collection:

```js
const products = [
  { id: 1, name: "Keyboard", price: 4500 },
  { id: 2, name: "Mouse", price: 1800 },
  { id: 3, name: "Stand", price: 2200 },
];
```

The array has a length of `3`. Index `0` is the first product. Index `2` is the third. Reading an index outside the array returns `undefined`, which is an important signal to check boundaries.

### Add and remove intentionally

```js
products.push({ id: 4, name: "Webcam", price: 3200 });
const last = products.pop();
```

`push`/`pop` work at the end. `unshift`/`shift` work at the beginning. These methods mutate the original array, so later in React you will often prefer creating a new array with spread, `map` or `filter` instead.

### Test the shape

```js
console.log(Array.isArray(products)); // true
```

Do not use `typeof products === "array"`; JavaScript reports arrays as objects through `typeof`.

### Read before you transform

Before learning advanced array methods, become comfortable with this sequence:

```text
collection → length → index → value → add/remove → verify result
```

Use DevTools or Node to inspect the array after every mutation. This builds the state-awareness you need for loops and later immutable React updates.
