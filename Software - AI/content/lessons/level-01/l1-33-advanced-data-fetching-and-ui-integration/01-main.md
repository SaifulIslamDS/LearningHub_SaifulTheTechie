---
title: Data Fetching, Caching & Production UI in Next.js
order: 1
summary: Connect server data, freshness decisions, prerendered routes, lazy loading and a reusable UI layer without losing control of the architecture.
level: Intermediate
time: 80–110 min
curriculum_level: Level 01
source_module: '33'
source_type: source-curriculum
topics:
- 'Data Fetching Recap: How data flows in Next.js App Router'
- 'Server Components: Fetching real data directly in Server Components'
- 'Caching Behavior: Understanding default cache and when it breaks'
- 'Caching Behavior: Dynamic Fetching - Using cache: ''no- store'' for always-fresh data'
- 'ISR with Revalidate: Incremental Static Regeneration in real projects'
- 'generateStaticParams: Optimizing dynamic routes at build'
- Lazy loading with next/dynamic
- 'Hero UI Setup: Installing and configuring Hero UI in Next.js (theme + config)'
- 'Hero UI with Data: Rendering fetched data using Hero UI Cards and Lists'
- 'Module Summary: Recap, best practices, and practice'
prerequisites:
- level-01/l1-32-next-js-rendering-basics/01-main
keywords:
- data fetching
- cache
- revalidation
- isr
- generateStaticParams
- lazy loading
- Hero UI
reviewed: '2026-10-09'
files:
- level-01/nextjs-fullstack-reference.zip
resources:
- title: Next.js App Router documentation
  url: https://nextjs.org/docs/app
  source: Next.js
  note: Official App Router documentation.
- title: Linking and Navigating
  url: https://nextjs.org/docs/app/getting-started/linking-and-navigating
  source: Next.js
  note: Official guide to navigation, prefetching and route transitions.
- title: Revalidating data
  url: https://nextjs.org/docs/app/getting-started/revalidating
  source: Next.js
  note: Official current guide to caching/revalidation behavior.
---
## Start here

Fetching data is easy. Designing **when it should be fetched, how fresh it must be, what can be reused, and what the user sees while it arrives** is the engineering problem.

Do not begin with a caching API. Begin with the product requirement:

```text
What data is this?
How often can it change?
Who is allowed to see it?
How expensive is it to compute?
What happens if the source is slow?
```

Only then choose rendering and caching behavior.

## What you will learn

- server-first data flow in the App Router;
- fresh vs reusable data;
- how the source curriculum's `cache: 'no-store'` and revalidation concepts fit modern Next.js;
- prebuilding dynamic routes with `generateStaticParams`;
- lazy loading with `next/dynamic`;
- integrating a component library such as Hero UI without letting it dictate application architecture;
- designing loading, error and empty states around fetched data.

## 1. Fetch where the data is consumed

A server page can call a data function directly:

```tsx
export default async function ProductsPage() {
  const products = await getProducts();
  return <ProductGrid products={products} />;
}
```

Keep the data function separate from display code:

```ts
export async function getProducts() {
  const response = await fetch('https://example.test/api/products');
  if (!response.ok) throw new Error('Could not load products');
  return response.json();
}
```

That separation makes the function easier to replace with a database call later.

## 2. Freshness is a business decision

Imagine three values:

- a course description changes once a month;
- inventory changes every few minutes;
- the signed-in user's notifications change continuously.

They do not deserve identical caching policy.

The source curriculum names `cache: 'no-store'` and ISR/revalidation. Those concepts remain useful, but current Next.js has evolving caching models. Treat the **freshness requirement** as stable knowledge and consult the current framework docs for the exact API supported by the project version.

### Always-fresh reference pattern

```ts
const response = await fetch(url, { cache: 'no-store' });
```

### Time-based revalidation reference pattern

```ts
const response = await fetch(url, { next: { revalidate: 3600 } });
```

Current Next.js documentation also describes Cache Components and newer `use cache`/`cacheLife` patterns. The tutorial therefore teaches both the source curriculum terminology and the durable engineering idea: **cache intentionally, invalidate intentionally, and do not guess about freshness.**

## 3. Prebuild known dynamic paths

If product IDs are known during build, `generateStaticParams` can provide them:

```tsx
export function generateStaticParams() {
  return products.map(product => ({ id: product.id }));
}
```

This does not mean every dynamic route should be prebuilt. Use it when the route set is bounded and pre-rendering is valuable.

## 4. Lazy load expensive client-only features

Suppose a chart is heavy and only appears after the user opens analytics. Load it later rather than adding it to the initial bundle.

```tsx
import dynamic from 'next/dynamic';

const AnalyticsChart = dynamic(() => import('./analytics-chart'));
```

Lazy loading is not a substitute for good component boundaries. It is a delivery optimization after you understand what the component does and where it executes.

## 5. UI libraries are presentation tools, not architecture

Hero UI appears in the source curriculum. Use it for buttons, cards, inputs and other interface primitives, but preserve your own responsibilities:

```text
page / feature
    ↓
data function
    ↓
domain data
    ↓
UI component/library
```

Avoid a structure where database calls or authorization rules live inside arbitrary UI components merely because that component library is convenient.

## 6. Render fetched data through a clear component contract

```tsx
function ProductCard({ product }: { product: Product }) {
  return (
    <article>
      <h2>{product.name}</h2>
      <p>BDT {product.price}</p>
    </article>
  );
}
```

The component does not need to know whether data came from a static array, MongoDB or an API. This separation lets the same UI survive later backend changes.

## 7. Design the four essential data states

A professional data-driven screen needs more than the happy path:

```text
loading  → work is pending
success  → data exists
empty    → request succeeded, no records
error    → work failed
```

Build each state deliberately. “No data” is not automatically an error, and an error is not automatically an empty list.

## Build extension

Using the Next.js reference package:

1. add an artificial async data function;
2. render products in a server page;
3. add a loading state;
4. trigger a not-found state from an invalid product ID;
5. add `generateStaticParams` for the sample products;
6. sketch where a Hero UI card could replace the plain article element;
7. document whether each data source should be cached or always fresh and **why**.

This framework-specific project remains **REFERENCE-ONLY** in the release environment. The tutorial avoids claiming a Next.js build that was not executed.
