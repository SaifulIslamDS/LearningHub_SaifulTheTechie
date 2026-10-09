---
title: Build a Stateful React SPA with BPL-DREAM
order: 1
summary: Build a responsive stateful React SPA with player selection, validation, removal and user feedback.
level: Intermediate
time: 4–7 hours
curriculum_level: Level 01
source_module: '29'
source_type: source-curriculum
topics:
- BPL Dream project setup and include Tailwind and daisiUI
- Create navbar and Create Fake Data for the players and load data
- Set Layout and make React responsive
- Building Player Card Component
- State Management & Toggle Functionality
- Player Selection & Validation System
- Selected Players Component & Remove Functionality
- React Toastify Integration and deploy to Surge/Netlify/Vercel
prerequisites:
- level-01/l1-28-javascript-dom-and-bom-deep-dive-react-bridge/01-main
keywords:
- react
- spa
- validation
- state
- toast
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
- title: React Toastify
  url: https://fkhadra.github.io/react-toastify/introduction/
  source: React Toastify
  note: Official toast library documentation.
---
## Project goal

Build a small single-page application that lets a user browse players, select a limited squad, remove selections and receive clear feedback. The original project theme is BPL-DREAM; the engineering lessons transfer to carts, wishlists, booking selections and many other interfaces.

## 1. Define the state before the UI

A useful first model:

```text
players          source data
selectedPlayers  user selection
view             available | selected
credits          optional domain value
```

Avoid storing values that can be derived from those sources.

## 2. Shape the player data

```javascript
const players = [
  {
    id: "p-01",
    name: "Player One",
    role: "All-rounder",
    country: "Bangladesh",
    price: 850000,
  },
];
```

Stable IDs are essential for both React keys and selection logic.

## 3. Component tree

```text
App
├── Navbar
├── Hero
├── ViewToggle
├── AvailablePlayers
│   └── PlayerCard × N
└── SelectedPlayers
    └── SelectedPlayer × N
```

`App` owns the shared selection because both available and selected views need it.

## 4. Select with validation

```javascript
function addPlayer(player) {
  setSelected(current => {
    if (current.some(item => item.id === player.id)) {
      return current;
    }

    if (current.length >= 6) {
      return current;
    }

    return [...current, player];
  });
}
```

The core logic is independent of the toast library. UI feedback should explain **why** an action was rejected, but the domain rule should still protect state.

## 5. Remove immutably

```javascript
function removePlayer(id) {
  setSelected(current => current.filter(player => player.id !== id));
}
```

This returns a new array and fits React's state model.

## 6. Toggle views

```jsx
<button onClick={() => setView("available")}>Available</button>
<button onClick={() => setView("selected")}>Selected ({selected.length})</button>
```

Render one panel based on the state:

```jsx
{view === "available" ? (
  <AvailablePlayers players={players} onSelect={addPlayer} />
) : (
  <SelectedPlayers players={selected} onRemove={removePlayer} />
)}
```

## 7. Responsive cards

Build the card grid with Tailwind/DaisyUI if following the source stack, but keep the layout intention clear: readable cards, consistent action placement and no horizontal overflow at narrow widths.

## 8. Toast notifications are feedback, not business logic

React Toastify can show messages such as “Already selected” or “Squad limit reached.” Keep the rule in the state-update path and call the notification from a deliberate result/handler. Do not rely on the toast itself to prevent invalid state.

## 9. Deployment checklist

- production build succeeds;
- every image has a stable source/fallback;
- duplicate selection is blocked;
- remove works after several add/remove cycles;
- selected count always matches array length;
- mobile layout remains usable;
- README explains run/deploy steps;
- live URL and repository are both accessible.

## Verified logic package

The release includes a framework-independent BPL selection script that executes the selection rules without React. Use that to understand and test the state transition, then wire the same logic into your React components locally.

## Career build extension
## Treat BPL-DREAM as a state-design exercise

The important project challenge is not the cricket theme. It is coordinating shared data and user actions.

Model players:

```js
{
  id: "p1",
  name: "Player A",
  price: 25,
  role: "All-rounder"
}
```

Keep available players and selected player IDs conceptually separate. Derive selected objects rather than duplicating full data when possible.

### Selection rule

```text
click Select
  ↓
already selected? → show feedback
budget enough?    → otherwise reject
selection limit?  → otherwise reject
  ↓
update state immutably
```

### Removal

Filter by stable ID:

```js
setSelected(ids => ids.filter(id => id !== playerId));
```

### Responsive cards

Use your UI framework to implement the visual system, but test narrow screens with long names/prices and empty states.

### Toast feedback

Notifications should report meaningful results (“Already selected”, “Not enough balance”), not replace visible application state. A user should still be able to understand the selected list after the toast disappears.

When deploying, verify refresh/deep-link behavior and asset paths on the actual host rather than assuming the local dev server proves production behavior.
