---
title: Build a Countries Explorer in React
order: 1
summary: Build an API-driven React project with reusable cards, state lifting, immutable updates and data visualization.
level: Intermediate
time: 5–8 hours
curriculum_level: Level 01
source_module: '27'
source_type: source-curriculum
topics:
- 'Project Setup: Countries API integration, project structure and data fetching'
- 'UI Rendering: Display country list with basic component'
- 'Country Card: Show flags, conditional text, and error handling'
- 'React Styling: styling with CSS, Tailwind CSS and DaisyUI'
- 'Responsive Grid: Build 3-column layout using Tailwind responsive classes'
- 'Interactive UI: Conditional CSS classes and toggle state on user click'
- 'State Lifting: Pass state and events between parent and child components'
- 'Immutable State: Update arrays without mutation using spread and filter'
- 'Data Visualization: Integrate Recharts, process API data'
- 'Deployment: Ship to Netlify/Surge/Vercel 15'
prerequisites:
- level-01/l1-26-state-management-in-react-events-and-data-fetchi/01-main
keywords:
- react
- project
- api
- state lifting
- recharts
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
- title: REST Countries
  url: https://restcountries.com/
  source: REST Countries
  note: Public country-data API used by the source project concept.
- title: Recharts
  url: https://recharts.org/en-US/
  source: Recharts
  note: Charting library reference.
- title: Tailwind CSS
  url: https://tailwindcss.com/docs/installation/using-vite
  source: Tailwind CSS
  note: Current official Vite integration instructions.
- title: daisyUI
  url: https://daisyui.com/docs/install/
  source: daisyUI
  note: Official installation docs.
---
## Project goal

Build a responsive **Countries Explorer** that fetches country data, renders reusable cards, supports interaction and turns API data into a small visualization.

This project connects component composition, state, data loading and deployment instead of teaching each idea in isolation.

## What you will build

```text
Countries Explorer
├── Header
├── Controls
│   ├── Search
│   └── Region filter
├── CountryGrid
│   └── CountryCard × N
└── SummaryChart
```

## 1. Define the data you actually need

Do not begin by rendering every field returned by an API. Decide the UI contract first:

```typescript
type Country = {
  name: { common: string };
  flags: { svg: string; alt?: string };
  region: string;
  population: number;
};
```

Even in a JavaScript project, thinking in a shape like this improves clarity.

## 2. Fetch a focused endpoint

```javascript
const url =
  "https://restcountries.com/v3.1/all?fields=name,flags,region,population";
```

Load once for this project, then store the result as server data. Keep search/filter state separately.

## 3. Render the list

```jsx
function CountryGrid({ countries, onSelect }) {
  return (
    <div className="grid">
      {countries.map(country => (
        <CountryCard
          key={country.name.common}
          country={country}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}
```

A production dataset should have a stable unique identifier when possible. For this small API, the common name is adequate for demonstration but not a universal database key strategy.

## 4. Build the card

```jsx
function CountryCard({ country, onSelect }) {
  return (
    <article className="country-card">
      <img
        src={country.flags.svg}
        alt={country.flags.alt || `Flag of ${country.name.common}`}
      />
      <h2>{country.name.common}</h2>
      <p>{country.region}</p>
      <p>{country.population.toLocaleString()} people</p>
      <button onClick={() => onSelect(country)}>Select</button>
    </article>
  );
}
```

## 5. Filter without mutating the source array

```javascript
const visibleCountries = countries
  .filter(country =>
    country.name.common.toLowerCase().includes(search.toLowerCase())
  )
  .filter(country => !region || country.region === region);
```

`visibleCountries` is derived data. You usually do not need another piece of state for it.

## 6. Lift selected state

Keep selection in the parent when both the grid and another component need it:

```jsx
const [selected, setSelected] = useState([]);

function selectCountry(country) {
  setSelected(current => {
    const exists = current.some(
      item => item.name.common === country.name.common
    );

    return exists
      ? current.filter(item => item.name.common !== country.name.common)
      : [...current, country];
  });
}
```

This update is immutable: each change returns a new array.

## 7. Responsive layout

Whether you use Tailwind, DaisyUI or regular CSS, keep the layout goal independent from the library:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1rem;
}
```

The source curriculum uses Tailwind/DaisyUI; this hub explains the underlying layout so you can transfer the skill to another UI system later.

## 8. Visualize processed API data

Compute region totals before passing values to a chart library:

```javascript
const populationByRegion = Object.values(
  countries.reduce((acc, country) => {
    acc[country.region] ??= { region: country.region, population: 0 };
    acc[country.region].population += country.population;
    return acc;
  }, {})
);
```

Recharts can then render that prepared array. The transformation itself is plain JavaScript and can be tested independently.

## 9. Loading and error states are part of the product

A working app needs more than the happy path:

```text
idle → loading → success
             ↘ error
```

Give the user visible feedback for loading and a meaningful retry/error message when a request fails.

## 10. Deploy deliberately

Before deploying to Netlify, Surge or Vercel:

- run a production build locally;
- check browser-console errors;
- test a narrow screen;
- verify remote API requests work over HTTPS;
- confirm direct navigation to routes if you are using a router;
- put setup/run instructions in the README.

## Practice files

The React reference package includes offline sample data so you can develop the transformation logic even when the external API is unavailable. Use the real API only after the UI works with deterministic local data.
