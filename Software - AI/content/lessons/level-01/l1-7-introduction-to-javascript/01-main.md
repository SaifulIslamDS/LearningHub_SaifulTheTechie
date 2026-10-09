---
title: Learn JavaScript by Building Small Programs
order: 1
summary: Run JavaScript with Node, declare variables, work with primitive values and perform arithmetic.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '7'
source_type: source-curriculum
topics:
- Introduction to JavaScript, Run JavaScript in VSCode
- Maths Needed to start learning Programming Language
- What is a variable? Five things you need to declare a variable
- Variable Animated Video [animation]
- Variable data types, Numeric, String, Boolean
- JavaScript Keyword, Variable name, naming convention
- Know the fundamentals of JS Numbers
- Introduction to arithmetic operators [animation]
- (advanced) Mathematical operation shorthand
- Module Summary and Practice Task
prerequisites: []
keywords:
- javascript
- introduction to javascript
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

HTML and CSS can describe and style a page, but they do not by themselves create application behavior. **JavaScript** is the programming language that lets your code make decisions, calculate values, respond to events, transform data and communicate with APIs.

In this chapter, focus less on memorizing syntax and more on learning how a program stores information and changes it step by step.

## What you will learn

- how to run JavaScript in Node.js and the browser console;
- variables and the role of `let` and `const`;
- strings, numbers and booleans;
- naming conventions and reserved keywords;
- arithmetic operators and operator precedence;
- assignment shortcuts such as `+=`;
- the small amount of mathematics you need to begin solving programming problems.

## 1. Run your first JavaScript program

Create `hello.js`:

```javascript
const learner = "Saiful";
console.log(`Hello, ${learner}!`);
```

Run it with Node:

```bash
node hello.js
```

Expected output:

```text
Hello, Saiful!
```

You can also run small expressions in your browser DevTools console. Node is useful for file-based practice; the browser console is useful when you are inspecting web-page behavior.

## 2. A variable is a named place for a value

```javascript
const course = "Software & AI Engineering";
let completedLessons = 7;
```

Use `const` when the variable binding should not be reassigned. Use `let` when the variable must point to a different value later.

```javascript
let completedLessons = 7;
completedLessons = 8;
```

The word `const` does **not** make an object deeply immutable. It only prevents reassignment of the variable itself. You will see this distinction again when you work with arrays and objects.

## 3. Five parts of a useful variable declaration

Look at:

```javascript
const hourlyRate = 25;
```

You can identify:

1. declaration keyword — `const`;
2. variable name — `hourlyRate`;
3. assignment operator — `=`;
4. value — `25`;
5. statement ending — semicolon, optional in many cases but used consistently in this hub.

Good names carry meaning. `hourlyRate` is clearer than `x` when the value represents money per hour.

## 4. Primitive values you will use constantly

```javascript
const name = "Saiful";     // string
const age = 30;            // number
const learning = true;     // boolean
const score = null;        // deliberate empty value
let feedback;              // undefined until assigned
```

JavaScript has more types, but strings, numbers, booleans, `null` and `undefined` are enough to start building useful logic.

Inspect types:

```javascript
console.log(typeof name);      // string
console.log(typeof age);       // number
console.log(typeof learning);  // boolean
```

`typeof null` is a historical JavaScript oddity: it returns `"object"`. Treat that as language history, not as proof that `null` behaves like a normal object.

## 5. Naming rules and conventions

Valid names can contain letters, digits, `_` and `$`, but cannot begin with a digit. Reserved language keywords such as `if`, `return` and `class` cannot be used as variable names.

Prefer `camelCase` for ordinary JavaScript variables and functions:

```javascript
const totalRevenue = 9075;
const customerCount = 12;
```

Use names that describe the domain. Real code is read far more often than it is typed.

## 6. Numbers and arithmetic

```javascript
const unitPrice = 250;
const quantity = 4;
const subtotal = unitPrice * quantity;
const discount = 100;
const total = subtotal - discount;

console.log(total);
```

Output:

```text
900
```

Core arithmetic operators:

```text
+  addition
-  subtraction
*  multiplication
/  division
%  remainder
** exponentiation
```

The remainder operator is especially useful for even/odd checks:

```javascript
const value = 18;
console.log(value % 2 === 0);
```

```text
true
```

## 7. Operator precedence and parentheses

This expression:

```javascript
const result = 10 + 5 * 2;
```

produces `20`, because multiplication has higher precedence than addition. Parentheses make intention explicit:

```javascript
const result = (10 + 5) * 2;
```

Now the result is `30`.

Do not rely on memory for complex precedence. Parentheses are often the clearest documentation.

## 8. Assignment shorthand

```javascript
let score = 10;
score += 5;  // score = score + 5
score -= 2;
score *= 3;
```

These operators are convenient when a variable is updated from its current value. You will use them frequently in loops and accumulators.

## 9. The programming mindset

A beginner often asks, “What syntax do I need?” A better question is:

> What information do I have, what result do I need, and what small transformations connect the two?

For example:

```text
unit price + quantity
        ↓
      multiply
        ↓
     subtotal
        ↓
 subtract discount
        ↓
       total
```

That thought process matters more than any single JavaScript keyword.

## 10. Follow the verified practice scripts

The JavaScript foundations download contains runnable scripts used throughout Modules 7–20. Start with `01_basics.js`, run it with Node, then change one value at a time. Predict the output **before** running the script. Prediction is one of the fastest ways to discover whether your mental model is correct.
