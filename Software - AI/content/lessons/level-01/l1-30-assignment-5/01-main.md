---
title: Assignment 5 — React Application
order: 1
summary: Complete a portfolio-ready React checkpoint that demonstrates component design,
  state ownership and interaction constraints.
level: Intermediate
time: 6–10 hours
curriculum_level: Level 01
source_module: '30'
source_type: source-curriculum
topics:
- Practice / assignment specified in the source (no lesson-level breakdown provided).
prerequisites:
- level-01/l1-29-simple-react-spa-with-bpl-dream/01-main
keywords:
- react
- assignment
- portfolio
- state
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
---
## Start here

Assignment 5 is the React checkpoint. Build an interactive selection application from a written brief, not by copying a finished implementation.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Frontend work is mostly turning requirements and edge cases into predictable state transitions and understandable UI.</p></div>

## What you will learn

- Practice / assignment specified in the source (no lesson-level breakdown provided).

## Reference logic slice

```javascript
const chosen = players.filter(p => p.price <= 40);
const cost = chosen.reduce((sum,p)=>sum+p.price,0);
```

<span class="output-label">Verified output</span>
```text
Chosen: A, B
Cost: 75, remaining: 15
```
<div class="verified"><b>RUN-HERE:</b> core selection/budget logic was executed with Node. The final assignment must be completed in a real React/Vite environment.</div>

## Assignment requirements

- Responsive component layout.
- Data-driven cards with stable keys.
- Select/remove interactions.
- Duplicate and limit validation.
- Budget/remaining calculation from one source of truth.
- Clear loading/empty/error states if external data is used.
- Keyboard-accessible controls.
- README with architecture and run/deploy instructions.
- Public deployment when your environment allows it.

## Practice files and code trail

This tutorial is paired with `react-vite-starter-reference.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Assignment brief

Build a React single-page application that demonstrates component composition, props, state, events, immutable updates and API/static-data rendering.

Minimum evidence:

- reusable card/list components;
- at least two pieces of state that interact;
- a validation rule before a state change;
- add/remove behavior using immutable updates;
- loading/empty/error feedback where data is asynchronous;
- responsive layout;
- deployed link when available;
- README containing component tree and state-ownership explanation.

Before submitting, draw the component tree and mark where each state value lives. If the same state is duplicated in unrelated components, revisit lifting state or deriving values from one source of truth.
