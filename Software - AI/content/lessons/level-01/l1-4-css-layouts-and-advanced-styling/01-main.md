---
title: Build Layouts with Flexbox, Grid & Positioning
order: 1
summary: Use units, Flexbox, Grid, pseudo-classes and positioning with a responsive mindset.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '4'
source_type: source-curriculum
topics:
- CSS Units & Box Model Recap — px, %, em, rem, auto
- Flexbox Fundamentals — Direction, Justify, Align
- Flexbox in Practice — Build Navbar & Login Layout
- Hero Section Design — Banner using Flexbox
- Card Component Design — Layout & Styling
- CSS Grid Fundamentals — Columns, Gap, Basic Layout
- Grid in Practice — Build a Calendar Layout
- Pseudo Classes — Hover, Focus, Visited
- Pseudo Elements & Selectors — Before, After, nth-child
- CSS Positioning — Static, Relative, Absolute, Fixed, Sticky, z-index
prerequisites: []
keywords:
- web
- html
- css
- git
reviewed: '2026-10-09'
files: []
resources:
- title: MDN HTML
  url: https://developer.mozilla.org/en-US/docs/Web/HTML
  source: MDN
  note: Official HTML reference.
- title: MDN CSS
  url: https://developer.mozilla.org/en-US/docs/Web/CSS
  source: MDN
  note: Official CSS reference.
- title: Chrome DevTools
  url: https://developer.chrome.com/docs/devtools/
  source: Chrome for Developers
  note: Official browser debugging documentation.
---
## Start here

CSS layout becomes much easier when you stop treating every property as an isolated trick and instead ask two questions:

1. **What is the container trying to arrange?**
2. **In one dimension or two?**

Flexbox is usually strongest for one-dimensional alignment. Grid is designed for two-dimensional rows and columns. Positioning is useful for deliberate offsets and overlays, not as the default page-layout system.

## What you will learn

- when to use `px`, `%`, `em`, `rem` and `auto`;
- Flexbox direction, alignment and distribution;
- practical navbar, login, hero and card layouts;
- CSS Grid columns and gaps;
- pseudo-classes and pseudo-elements;
- normal flow and `static`, `relative`, `absolute`, `fixed` and `sticky` positioning;
- stacking with `z-index`.

## 1. Choose units by what should be relative to what

A useful starting model:

| Unit | Relative to | Good for |
|---|---|---|
| `px` | CSS pixel | Borders, icons, controlled minimums |
| `%` | Parent/context | Fluid widths |
| `em` | Current element's font size | Component-relative spacing |
| `rem` | Root font size | Consistent type/spacing scale |
| `auto` | Browser/layout algorithm | Natural sizing and automatic margins |

Example:

```css
.page {
  width: min(70rem, calc(100% - 2rem));
  margin-inline: auto;
  padding-block: 3rem;
}
```

This creates a fluid page that uses available width but stops growing beyond a readable maximum.

## 2. Flexbox: arrange one main axis

```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
```

The **main axis** follows `flex-direction`. With the default `row`, `justify-content` works horizontally and `align-items` works across the vertical cross-axis.

For navigation links:

```css
.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
```

## 3. Build a login layout

```html
<main class="auth-layout">
  <section class="auth-intro">
    <h1>Welcome back</h1>
    <p>Continue your learning path.</p>
  </section>

  <form class="auth-card">...</form>
</main>
```

```css
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  padding: 2rem;
}
```

At narrow widths you can change the direction:

```css
@media (max-width: 48rem) {
  .auth-layout {
    flex-direction: column;
    align-items: stretch;
  }
}
```

This is your first important responsive pattern: preserve the same semantic content and change only the layout rule.

## 4. Hero layout with Flexbox

```css
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: clamp(2rem, 7vw, 6rem);
}

.hero > * {
  flex: 1 1 0;
}
```

`flex: 1 1 0` lets both children grow and shrink from an equal base. It is not always the correct choice, but it is useful for understanding how items share space.

## 5. Grid: rows and columns together

A responsive card grid can be surprisingly concise:

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: 1.25rem;
}
```

Read that as: create as many columns as fit, but do not let a card become narrower than the chosen minimum; let each final column share remaining space.

A simple calendar is another natural Grid problem:

```css
.calendar {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}
```

## 6. Pseudo-classes represent state or structure

```css
a:hover { text-decoration-thickness: 0.15em; }
input:focus { outline: 3px solid #18dff5; }
a:visited { color: #6d4ac7; }
.card:nth-child(2n) { background: #f7fbff; }
```

Do not remove focus indicators unless you replace them with an equally visible alternative. Keyboard users need to know which element currently has focus.

## 7. Pseudo-elements create generated decoration

```css
.section-title::after {
  content: "";
  display: block;
  width: 4rem;
  height: 0.2rem;
  margin-top: 0.5rem;
  background: #18dff5;
}
```

`::before` and `::after` are useful for decoration. Important content should still exist in the HTML rather than only in generated CSS content.

## 8. Positioning and normal flow

Most elements begin in **normal flow**. Keep them there unless you have a reason not to.

```css
.card {
  position: relative;
}

.card__badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
}
```

The relatively positioned card establishes the containing block for its absolutely positioned badge.

`fixed` attaches an element to the viewport. `sticky` behaves like normal flow until a threshold is reached:

```css
.docs-nav {
  position: sticky;
  top: 1rem;
}
```

## 9. `z-index` is about stacking contexts, not just big numbers

A larger `z-index` does not automatically beat every other element on the page. Stacking contexts can isolate groups of elements. When layering becomes confusing, inspect the element in DevTools instead of escalating values from `10` to `999999`.

## 10. Extend the profile project

Use your practice project to implement:

1. a Flexbox header;
2. a two-column hero that stacks on small screens;
3. a responsive Grid for project cards;
4. visible hover and focus states;
5. one decorative pseudo-element;
6. a sticky navigation experiment;
7. no horizontal scroll at phone width.

Resize gradually from narrow to wide. Responsive design is not two screenshots called “mobile” and “desktop”; it is the behavior between them.
