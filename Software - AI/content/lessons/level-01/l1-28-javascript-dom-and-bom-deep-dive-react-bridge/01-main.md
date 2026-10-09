---
title: JavaScript DOM & BOM Deep Dive — React Bridge
order: 1
summary: Understand DOM selection/manipulation, events, browser APIs, storage, async
  fetch and how React changes the interaction model.
level: Intermediate
time: 50–70 min
curriculum_level: Level 01
source_module: '28'
source_type: source-curriculum
topics:
- 'DOM Basics: Document Object Model and its Tree Structure'
- 'DOM Selection: getElement Methods vs querySelector'
- 'DOM Manipulation: Changing Text, Attributes, and Styling'
- 'Event Handling: addEventListener and Common Event'
- 'Event Flow: Bubbling, Capturing, and Event Delegation'
- 'BOM Essentials: Window Object, Location, and History API'
- 'Timing in JavaScript: setTimeout, setInterval, and clearTimeout'
- 'Browser Storage: localStorage, sessionStorage — Read, Write, Delete'
- 'Async JavaScript: Promise, fetch API, and the React Connection'
- 'Vanilla JS vs React: Virtual DOM, Diffing, and the Component Mindset'
prerequisites:
- level-01/l1-27-react-project-countries-explorer/01-main
keywords:
- dom
- bom
- events
- localStorage
- fetch
- virtual dom
reviewed: '2026-10-09'
files: []
resources:
- title: MDN DOM introduction
  url: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction
  source: MDN
  note: Browser-oriented DOM reference.
- title: MDN Web Storage API
  url: https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API
  source: MDN
  note: Official browser storage reference.
- title: MDN Using Fetch
  url: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  source: MDN
  note: Fetch and async request reference.
- title: React documentation
  url: https://react.dev/
  source: React
  note: Official React documentation. Reviewed against React 19.3.
- title: Describing the UI
  url: https://react.dev/learn/describing-the-ui
  source: React
  note: Components, JSX, props and list rendering.
- title: Adding Interactivity
  url: https://react.dev/learn/adding-interactivity
  source: React
  note: Events and state from the official learning path.
---
## Start here

React does not replace the browser platform. React ultimately creates, updates and removes DOM nodes on your behalf. Understanding the **DOM** (Document Object Model) and **BOM** (browser-provided window/navigation APIs) makes React behavior much easier to debug.

## What you will learn

- the DOM tree;
- element selection and manipulation;
- events, bubbling, capturing and delegation;
- `window`, `location` and `history`;
- timers;
- `localStorage` and `sessionStorage`;
- promises and `fetch`;
- how React's virtual representation relates to the DOM.

## 1. HTML becomes a DOM tree

Given:

```html
<main id="app">
  <h1>Learning Hub</h1>
  <button>Continue</button>
</main>
```

The browser exposes objects representing those nodes. JavaScript can query them:

```javascript
const app = document.getElementById("app");
const button = document.querySelector("button");
```

## 2. Manipulate content and attributes

```javascript
const heading = document.querySelector("h1");
heading.textContent = "Software & AI Engineering";
heading.setAttribute("data-track", "software-ai");
heading.classList.add("highlight");
```

Direct DOM manipulation is fine in plain JavaScript. Inside React-owned UI, let React control the elements it renders rather than manually changing those same nodes behind its back.

## 3. Events

```javascript
button.addEventListener("click", event => {
  console.log("clicked", event.currentTarget);
});
```

`event.target` is the element where the event originated. `event.currentTarget` is the element whose listener is currently running.

## 4. Bubbling and delegation

Many events bubble from a target through ancestors. That allows event delegation:

```javascript
const list = document.querySelector("#courses");

list.addEventListener("click", event => {
  const button = event.target.closest("button[data-course-id]");
  if (!button) return;

  console.log(button.dataset.courseId);
});
```

One listener can handle many dynamically created child buttons.

## 5. Browser objects

```javascript
console.log(window.innerWidth);
console.log(location.href);
```

Navigate with browser history APIs when appropriate:

```javascript
history.pushState({}, "", "/courses?level=1");
```

Framework routers build abstractions on top of these browser capabilities.

## 6. Timers

```javascript
const timerId = setTimeout(() => {
  console.log("runs once later");
}, 1000);

clearTimeout(timerId);
```

Intervals repeat until cleared:

```javascript
const intervalId = setInterval(tick, 1000);
clearInterval(intervalId);
```

Timers schedule work; they do not pause the JavaScript thread like a sleep statement.

## 7. Web storage

```javascript
localStorage.setItem("theme", "dark");
const theme = localStorage.getItem("theme");
localStorage.removeItem("theme");
```

`localStorage` persists across browser restarts for an origin until cleared. `sessionStorage` is scoped to a browsing session/tab context. Both store strings, so objects are commonly serialized with JSON.

Never treat web storage as a safe place for arbitrary secrets.

## 8. Async JavaScript and `fetch`

```javascript
async function loadCourses() {
  const response = await fetch("/api/courses");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
```

`fetch()` returns a Promise. React data-loading patterns build on the same Promise model you learn in plain JavaScript.

## 9. Vanilla DOM vs React

Plain JavaScript might say:

```javascript
heading.textContent = currentTitle;
```

React encourages:

```jsx
<h1>{currentTitle}</h1>
```

You describe the UI for the current data; React compares render output and updates the browser DOM. That comparison/reconciliation model is why React state changes cause UI updates without you manually finding each element.

## Bridge to Next.js

Next.js adds another dimension: some React components can render on the server, where browser-only APIs such as `window` and `localStorage` do not exist. Understanding that boundary is essential in the next milestone.

## Career build extension
## Use DOM knowledge to understand what React abstracts

React eventually updates the browser DOM, so vanilla DOM knowledge gives you a debugging foundation.

### Selection and mutation

```js
const title = document.querySelector("h1");
title.textContent = "Updated title";
title.classList.add("active");
```

### Event delegation

```js
list.addEventListener("click", event => {
  const button = event.target.closest("button[data-id]");
  if (!button) return;
  console.log(button.dataset.id);
});
```

One ancestor handler can manage many dynamic child buttons because events bubble.

### Browser APIs

`window`, `location`, `history`, timers, `localStorage` and `sessionStorage` belong to the browser environment. This explains why a Next.js Server Component cannot simply call `window.localStorage`: that code executes where no browser `window` exists.

### Promise/fetch bridge

```js
const response = await fetch('/api/items');
if (!response.ok) throw new Error('Request failed');
const items = await response.json();
```

React does not change how promises or HTTP work. It changes how application state is connected to rendered UI.

### Vanilla vs virtual UI model

Vanilla DOM code says “find this node and mutate it.” React code says “given state X, the UI should look like Y,” then React coordinates the DOM updates. Understanding both models helps you debug libraries instead of treating them as magic.
