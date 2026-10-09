---
title: Build React Interfaces with Components, JSX & Props
order: 1
summary: Build component-driven UI with JSX, props, conditional rendering and stable list identity.
level: Intermediate
time: 50–70 min
curriculum_level: Level 01
source_module: '25'
source_type: source-curriculum
topics:
- What you will learn from this Milestone-1 (Animated)
- What is React, React vs Next JS
- What is component, component types, build your first component
- JSX, its rules and add dynamic content to JSX
- Explore JSX and Props basics
- How to pass and read Props in React
- Read-only props and introduction to conditional rendering
- 'Six ways to do Conditional Rendering: If, Ternary and AND'
- (Advanced) Rendering lists of users using map
- Module Summary and Recap
- 'React Simplified: AI Shows You What''s Important'
prerequisites:
- level-01/l1-24-assignment-4-problem-solving/01-main
keywords:
- react
- jsx
- components
- props
- rendering
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

React helps you build interfaces as a tree of components. Each component receives inputs, reads current state/context and returns a description of the UI for that moment.

The most important beginner mental model is:

```text
inputs (props + state)
        ↓
   component function
        ↓
      JSX tree
        ↓
React reconciles changes
        ↓
      browser DOM
```

## What you will learn

- what React adds beyond plain DOM manipulation;
- React vs Next.js;
- components and JSX;
- props and one-way data flow;
- conditional rendering;
- list rendering and stable keys;
- how to break a screen into meaningful component boundaries.

## 1. React vs Next.js

**React** is the UI library: components, props, state, hooks and rendering. **Next.js** is a framework built around React that adds routing, server rendering, data-fetching conventions, server/client boundaries, optimization and production tooling.

Learn React's component model first so Next.js does not feel like unrelated magic.

## 2. Your first component

```jsx
function Welcome() {
  return <h1>Welcome to the Learning Hub</h1>;
}
```

A component name begins with a capital letter. JSX looks like HTML but is JavaScript syntax transformed into React element descriptions.

## 3. JSX embeds JavaScript expressions

```jsx
function CourseTitle() {
  const title = "React Foundations";
  return <h2>{title}</h2>;
}
```

Inside JSX, `{}` switches into JavaScript expression mode.

JSX rules include:

- close elements (`<img />`);
- return one parent tree (a fragment `<>...</>` can group siblings);
- use `className` rather than HTML's `class` attribute in JSX;
- camelCase many DOM properties/events such as `onClick`.

## 4. Props are read-only component inputs

```jsx
function CourseCard({ title, level }) {
  return (
    <article>
      <h2>{title}</h2>
      <p>{level}</p>
    </article>
  );
}

export default function App() {
  return <CourseCard title="React" level="Beginner" />;
}
```

The parent owns the values it passes. The child should not mutate props.

## 5. Composition builds larger UI from smaller pieces

```jsx
function Page() {
  return (
    <>
      <Header />
      <main>
        <CourseList />
      </main>
      <Footer />
    </>
  );
}
```

Split components around meaningful responsibilities, not arbitrary line counts. A component is a good candidate for extraction when it has a coherent purpose, is reused, has its own state/behavior or makes the parent easier to understand.

## 6. Conditional rendering

Early return:

```jsx
function Profile({ user }) {
  if (!user) return <p>Please sign in.</p>;
  return <h2>{user.name}</h2>;
}
```

Ternary:

```jsx
<p>{active ? "Active" : "Inactive"}</p>
```

Logical AND:

```jsx
{isAdmin && <AdminBadge />}
```

Use the form that makes the decision easiest to read.

## 7. Render lists with stable identity

```jsx
const courses = [
  { id: "html", title: "HTML" },
  { id: "react", title: "React" },
];

function CourseList() {
  return (
    <ul>
      {courses.map(course => (
        <li key={course.id}>{course.title}</li>
      ))}
    </ul>
  );
}
```

Keys help React match items across renders. Use a stable domain ID when available. Avoid `Math.random()` and be careful with indexes when list order can change.

## 8. Build a small course browser

Break the screen into:

```text
App
├── Header
├── CourseFilters
└── CourseList
    └── CourseCard × N
```

Keep the course data in `App` for now. Pass each course to `CourseCard`. In the next module, state will make filtering interactive.

## 9. AI-assisted coding without surrendering understanding

An AI coding assistant can generate a component quickly, but you should still be able to answer:

- what props enter it;
- what state it owns;
- which component owns each piece of data;
- why each list key is stable;
- what renders when a condition changes.

If you cannot explain those decisions, treat the generated code as a draft to study rather than finished work.

## Practice package

The React/Vite starter reference includes a simple project shape and offline sample data. The release environment could not install React packages, so framework execution is **REFERENCE-ONLY** here. Use the files to create the project locally with Vite, then implement the component tree above.
