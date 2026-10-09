---
title: Make Decisions with JavaScript Conditionals
order: 1
summary: Compare values and control program flow with if/else, logical operators and ternaries.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '8'
source_type: source-curriculum
topics:
- Compare variables and Comparison operator
- Introduction to Conditionals,
- If_else statement animated
- Conditional branching if Else Condition
- Multiple condition Logical Operators(&&, ||)
- Multi-level If-else if-else condition
- (optional) Nested if-else condition
- (advanced )If-else shorthand Ternary Operator
- (advanced) Logical Not Operator
- Homework and Making Decisions in your code
prerequisites: []
keywords:
- javascript
- fundamental concepts of conditionals
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

Programs become useful when they can choose different paths. A conditional evaluates an expression and decides which block of code should run.

## What you will learn

- comparison operators;
- `if`, `else if` and `else`;
- logical `&&` and `||`;
- nested conditions;
- the ternary operator;
- logical NOT `!`;
- how to turn a business rule into readable decision logic.

## 1. Comparisons produce booleans

```javascript
const age = 22;
console.log(age >= 18);
```

```text
true
```

Common comparisons:

```text
===  strictly equal
!==  strictly not equal
>    greater than
>=   greater than or equal
<    less than
<=   less than or equal
```

Prefer strict equality (`===`) while learning because it avoids JavaScript's automatic type conversion in equality checks.

## 2. `if` controls whether a block runs

```javascript
const stock = 12;

if (stock > 0) {
  console.log("Available");
}
```

The expression inside parentheses is converted to a boolean. If it is truthy, the block runs.

## 3. Use `else` for the alternative path

```javascript
const stock = 0;

if (stock > 0) {
  console.log("Available");
} else {
  console.log("Out of stock");
}
```

## 4. Multiple branches with `else if`

```javascript
const score = 76;

if (score >= 80) {
  console.log("A");
} else if (score >= 70) {
  console.log("B");
} else if (score >= 60) {
  console.log("C");
} else {
  console.log("Needs improvement");
}
```

Order matters. Put the most restrictive/highest condition first when later branches assume earlier thresholds have already failed.

## 5. Combine rules with logical operators

A candidate might be eligible only when both conditions are true:

```javascript
const hasPortfolio = true;
const yearsExperience = 2;

if (hasPortfolio && yearsExperience >= 1) {
  console.log("Eligible for review");
}
```

`&&` means both sides must be truthy. `||` means at least one side must be truthy.

```javascript
const isAdmin = false;
const isOwner = true;

if (isAdmin || isOwner) {
  console.log("Can edit");
}
```

## 6. Nested conditions are valid, but depth costs readability

```javascript
if (user) {
  if (user.active) {
    if (user.role === "admin") {
      console.log("Admin area");
    }
  }
}
```

Sometimes nesting expresses the rule clearly. Often it is easier to use early returns inside a function or combine conditions.

## 7. Ternary for a small expression

```javascript
const theme = prefersDark ? "dark" : "light";
```

A ternary is useful when you are selecting **one value from two alternatives**. It becomes harder to read when several decisions are nested into one line.

## 8. Logical NOT

```javascript
const isLoggedIn = false;

if (!isLoggedIn) {
  console.log("Please sign in");
}
```

`!` flips a boolean-like value. Two NOT operators (`!!value`) are sometimes used to convert a value explicitly to `true` or `false`.

## 9. Translate a real rule before coding it

Suppose free delivery applies when:

- order value is at least 2,000; **or**
- the customer is a premium member.

Write the rule in plain language first:

```text
freeDelivery = highValueOrder OR premiumCustomer
```

Then code it:

```javascript
const total = 1750;
const premium = true;
const freeDelivery = total >= 2000 || premium;

console.log(freeDelivery);
```

```text
true
```

That habit—plain-language rule first, code second—scales well when business logic becomes more complex.

## Practice with the verified script

Open `02_conditionals.js` from the JavaScript foundations package. Before each run, change inputs and write down which branch you expect to execute. Then run the script and compare the actual result with your prediction.
