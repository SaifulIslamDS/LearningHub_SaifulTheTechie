---
title: React Accessibility Foundations
order: 2
summary: Keep component abstractions semantic, keyboard-reachable and screen-reader
  friendly.
level: Intermediate
time: 35–50 min
curriculum_level: Level 01
source_module: ST
source_type: st-recommended
topics: []
prerequisites:
- level-01/l1-25-react-core-components-jsx-props-and-rendering/01-main
keywords:
- react
- accessibility
- semantic html
reviewed: '2026-10-09'
files: []
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
- title: React Accessibility
  url: https://react.dev/learn/accessibility
  source: React
  note: Official accessibility guidance.
---
## Start here

React does not replace HTML accessibility rules. A reusable component should preserve the semantics and keyboard behavior users expect from the underlying platform.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>An inaccessible design system can spread the same barrier across an entire product.</p></div>

## Core idea

Prefer native elements first: `<button>` for actions, `<a>` for navigation, `<label>` for inputs, semantic landmarks for structure. Add ARIA only when native semantics cannot express the pattern.

```jsx
<button type="button" onClick={onSave}>Save changes</button>
```

is better than a clickable `<div>` that requires you to recreate keyboard and accessibility behavior manually.
