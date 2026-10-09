---
title: Work with Strings & Objects
order: 1
summary: Transform text and model structured data with object properties and nested values.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '12'
source_type: source-curriculum
topics:
- Introduction to string and string vs array
- String Comparison lowercase, uppercase and trip
- String Slice, Join, Concatenate and includes
- Reverse a String in Three Different Ways
- Introduction to Objects properties, and values
- What is Object Animated video
- 'Multiple ways to get & set object properties slide: [11-13]'
- Keys, Values, nested objects and delete
- Loop an object and Ways to declare an Object
- Module Summary and Practice Tasks
prerequisites: []
keywords:
- javascript
- fundamentals of strings & objects
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

Strings model text. Objects model named properties that belong together. These two ideas appear everywhere in application code: user profiles, API responses, configuration, database records and UI state.

## What you will learn

- string vs array behavior;
- case conversion, trimming, slicing, joining and searching;
- several ways to reverse text;
- object properties and nested objects;
- dot vs bracket notation;
- reading keys and values;
- deleting and iterating properties.

## 1. Strings are sequences, but they are not mutable arrays

```javascript
const name = "Saiful";
console.log(name[0]);
console.log(name.length);
```

```text
S
6
```

You can read characters by index, but operations normally return a new string rather than changing the original string in place.

## 2. Normalize text before comparison

```javascript
const input = "  DHAKA ";
const normalized = input.trim().toLowerCase();
console.log(normalized);
```

```text
dhaka
```

Normalizing case and surrounding whitespace is common when comparing user-entered text. Be careful with international text: language-aware comparisons can require more than simple `toLowerCase()`.

## 3. Slice, include and combine

```javascript
const tech = "JavaScript";
console.log(tech.slice(0, 4));
console.log(tech.includes("Script"));
```

```text
Java
true
```

Combine values with template strings:

```javascript
const role = "developer";
const message = `${name} is learning to become a ${role}.`;
```

## 4. Reverse a string by transforming it

```javascript
const reversed = "agent".split("").reverse().join("");
console.log(reversed);
```

```text
tnega
```

You can also reverse manually with a loop. The built-in chain is concise; the loop is useful practice because it exposes the transformation step by step.

## 5. Objects model a named record

```javascript
const learner = {
  name: "Saiful",
  track: "Software & AI Engineering",
  active: true,
};
```

Read properties:

```javascript
console.log(learner.name);
console.log(learner["track"]);
```

Dot notation is concise when the property name is known in the code. Bracket notation is necessary when the property name is stored in a variable:

```javascript
const field = "track";
console.log(learner[field]);
```

## 6. Nested objects

```javascript
const project = {
  title: "Learning Hub",
  owner: {
    name: "Saiful",
    website: "saifulshuvo.com",
  },
};

console.log(project.owner.website);
```

Later, optional chaining helps when an intermediate property might be missing:

```javascript
console.log(project.client?.company);
```

## 7. Keys, values and entries

```javascript
console.log(Object.keys(learner));
console.log(Object.values(learner));
console.log(Object.entries(learner));
```

`Object.entries()` is especially convenient when you want both names and values.

## 8. Loop over object properties

```javascript
for (const [key, value] of Object.entries(learner)) {
  console.log(key, value);
}
```

## 9. Delete only when deletion represents the domain

```javascript
delete learner.active;
```

In application state, it can sometimes be clearer to create a new object without the field rather than mutate an existing object. You will see immutable patterns more often in React.

## Practice with the verified script

Open `06_strings_objects.js`. Normalize user input, read nested properties with both dot and bracket notation, iterate through an object's entries and build a new display string from the values.

## Career build extension
## Model real information instead of isolated syntax

Strings represent text values; objects group related named values. Combine them in a small domain model:

```js
const learner = {
  name: "Saiful Islam",
  track: "Software & AI Engineering",
  skills: ["HTML", "CSS", "JavaScript"],
  active: true,
};
```

Read properties with dot notation when the property name is known:

```js
console.log(learner.name);
```

Use bracket notation when the key is dynamic:

```js
const field = "track";
console.log(learner[field]);
```

### Normalize strings before comparison

Human input may differ in case or spacing:

```js
const input = "  javascript ";
const normalized = input.trim().toLowerCase();
console.log(normalized === "javascript"); // true
```

### Transform text

Practice `slice`, `includes`, `split`, `join` and concatenation/template strings by creating a slug or display label. Avoid chaining many methods you cannot explain; inspect intermediate values while learning.

### Loop through object data

```js
for (const [key, value] of Object.entries(learner)) {
  console.log(key, value);
}
```

Nested objects and arrays appear everywhere in JSON APIs. Spend time reading their shape before trying to access deeply nested values.
