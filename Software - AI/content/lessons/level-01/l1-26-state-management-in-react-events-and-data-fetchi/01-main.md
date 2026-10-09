---
title: State, Events & Data Fetching
order: 1
summary: Manage React state and events, understand re-rendering, and reason about
  effects and asynchronous data.
level: Intermediate
time: 50–70 min
curriculum_level: Level 01
source_module: '26'
source_type: source-curriculum
topics:
- 'Vite Project Setup: Folder structure, files, environment overview'
- 'Event Handling: onClick, onChange, onSubmit and handling patterns'
- 'State in React: Why state matters, how re-rendering works'
- 'useState Hook: Declaring state, updating state, reading'
- 'use() Hook: Modern data-fetching hook, concept and'
- 'API Call with use(): Load and render live data from an API'
- 'Async/Await in React: Fetching data with async functions, clean approach'
- 'useEffect Hook: Side effects, dependencies, and lifecycle (optional deep dive)'
- 'Axios in React: Fetching data professionally'
- 'Thinking in React: Component mindset, homework'
prerequisites:
- level-01/l1-25-react-core-components-jsx-props-and-rendering/01-main
keywords:
- react
- state
- events
- useState
- useEffect
- fetch
reviewed: '2026-10-09'
files:
- level-01/react-vite-starter-reference.zip
resources:
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
- title: Vite Getting Started
  url: https://vite.dev/guide/
  source: Vite
  note: Official Vite setup guide. Current site showed Vite 8.3.x during review.
- title: Synchronizing with Effects
  url: https://react.dev/learn/synchronizing-with-effects
  source: React
  note: Official guidance on when effects are appropriate.
---
## Start here

Components become applications when they can respond to events, remember state and synchronize with external data. React's core rule remains simple: **render UI from current inputs and state**.

## What you will learn

- Vite project structure;
- event handlers;
- state and re-rendering;
- `useState`;
- modern async data loading concepts including `use()`;
- `fetch`, `async/await`, `useEffect` and Axios;
- how to separate server data from local UI state.

## 1. Event handlers describe what should happen

```jsx
function SaveButton() {
  function handleClick() {
    console.log("save requested");
  }

  return <button onClick={handleClick}>Save</button>;
}
```

Pass the function, not the result of calling it. `onClick={handleClick()}` would execute during render rather than waiting for the click.

Forms typically use `onSubmit`:

```jsx
function SearchForm() {
  function handleSubmit(event) {
    event.preventDefault();
    // read/validate form values
  }

  return <form onSubmit={handleSubmit}>...</form>;
}
```

## 2. State is component memory

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

Calling the setter schedules a new render with updated state. Do not treat state like an ordinary variable that you mutate directly.

## 3. Use functional updates when the next state depends on the previous state

```jsx
setCount(current => current + 1);
```

This form is safer when multiple updates may be queued.

For arrays:

```jsx
setSelected(current => [...current, newItem]);
```

Avoid `selected.push(newItem); setSelected(selected);` because the same array object was mutated.

## 4. Lift state when siblings need the same source of truth

```text
App owns selectedCountry
├── CountryList receives onSelect
└── CountryDetails receives selectedCountry
```

If two siblings need to coordinate, move their shared state to the nearest common parent and pass data/handlers down.

## 5. Async/await with `fetch`

Outside React, the data flow is ordinary JavaScript:

```javascript
async function loadCountries() {
  const response = await fetch("https://restcountries.com/v3.1/all?fields=name,flags,region,population");

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}
```

Always decide what should happen for loading, success, empty data and error states.

## 6. Client-side fetching with an effect

A common pattern:

```jsx
useEffect(() => {
  const controller = new AbortController();

  async function load() {
    try {
      setStatus("loading");
      const response = await fetch(url, { signal: controller.signal });
      if (!response.ok) throw new Error("Request failed");
      const data = await response.json();
      setCountries(data);
      setStatus("success");
    } catch (error) {
      if (error.name !== "AbortError") setStatus("error");
    }
  }

  load();
  return () => controller.abort();
}, [url]);
```

The cleanup prevents an obsolete request from continuing when the effect is replaced or the component unmounts.

## 7. `use()` and framework data flow

Modern React exposes `use()` for reading a Promise or context in supported rendering patterns. Its usefulness depends heavily on the framework and whether the component runs on the server or client. Treat it as part of the larger data-flow model rather than a replacement for understanding promises.

When we reach Next.js, server components let you await data directly in server-rendered components, which often removes the need for a client-side effect for initial data.

## 8. Axios is an HTTP client, not a new data model

```javascript
const { data } = await axios.get(url);
```

Axios can offer convenient defaults and interceptors. Native `fetch` is also capable. Choose based on project needs rather than assuming one is automatically “professional.”

## 9. Think in state categories

Before adding a hook, classify the value:

- **derived value** — calculate from existing props/state;
- **local UI state** — selected tab, open dialog, draft input;
- **server data** — fetched from API/database;
- **URL state** — filters or pagination that should be shareable;
- **global client state** — genuinely shared app state.

Many bugs come from storing the same truth in two places.

## Practice with verified logic

The package includes framework-independent React logic scripts that were executed during release validation. Use them to understand immutable state updates and transformations first, then implement those transformations inside components locally.
