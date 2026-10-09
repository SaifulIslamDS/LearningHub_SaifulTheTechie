---
title: Understand Rendering, Hydration & Server/Client Components
order: 1
summary: Build a correct mental model of where React work happens in Next.js and how server-rendered HTML becomes interactive.
level: Intermediate
time: 70–95 min
curriculum_level: Level 01
source_module: '32'
source_type: source-curriculum
topics:
- What is Rendering? What is CSR and SSR?
- About Hydration. CSR vs. SSR and Next Js Rendering Techniques
- Client Components vs. Server Components
- Loading Data Using Client Component
- Loading Data Using Server Component and Client Component inside Server Component
- Displaying All Foods, Food Details and Use of error.js and loading.js
- Module Summary
prerequisites:
- level-01/l1-31-next-js-foundation-and-routing/01-main
keywords:
- rendering
- csr
- ssr
- hydration
- server component
- client component
- loading
reviewed: '2026-10-09'
files:
- level-01/nextjs-fullstack-reference.zip
resources:
- title: Next.js App Router documentation
  url: https://nextjs.org/docs/app
  source: Next.js
  note: Official App Router documentation for routing, rendering, data and production conventions.
- title: Layouts and Pages
  url: https://nextjs.org/docs/app/getting-started/layouts-and-pages
  source: Next.js
  note: Official guide to file-system routes, layouts and pages.
- title: Server and Client Components
  url: https://nextjs.org/docs/app/getting-started/server-and-client-components
  source: Next.js
  note: Official explanation of the server/client boundary and hydration.
---
## Start here

The fastest way to become confused in Next.js is to memorize labels such as CSR, SSR and Server Components without understanding **when code executes and what crosses the network**.

Use this mental model:

```text
request / navigation
       ↓
server decides and renders server work
       ↓
HTML + React server payload + referenced client JS
       ↓
browser displays HTML
       ↓
client components hydrate and become interactive
```

This module is about execution boundaries. Once those boundaries are clear, data fetching and authentication become much easier.

## What you will learn

- client-side rendering and server rendering;
- what hydration actually means;
- why App Router pages/layouts are server-side by default;
- when a component must be a Client Component;
- fetching data on either side of the boundary;
- composing a Client Component inside a Server Component;
- loading and error conventions for a route.

## 1. Rendering means turning application state into UI

At the React level, rendering answers: *given these inputs, what UI tree should exist?* Next.js adds the question: *where and when should that work happen?*

### Client-side rendering

A browser can download JavaScript, call an API and render UI after the page starts. That can be useful for highly interactive, user-specific surfaces, but it also means the browser needs more work before it can show useful content.

### Server rendering

The server can render the route before the browser receives it. The browser can show meaningful HTML sooner, while interactive client pieces become active afterward.

Do not reduce this to “SSR is fast, CSR is slow.” Real applications mix strategies.

## 2. Hydration: making pre-rendered client UI interactive

Hydration is often explained too vaguely. Imagine the server sends this button as HTML:

```html
<button>Like</button>
```

The user can see it immediately, but HTML alone does not contain your React `onClick` function. Hydration is the React process that connects the client-side component code and event handlers to the already-rendered interface.

A hydration problem commonly means the browser's first render disagrees with what the server rendered. That is why browser-only values such as `window`, random values or current-time formatting need careful boundaries.

## 3. Server Components are the default mental starting point

In the App Router, start with a Server Component unless the component actually needs client capabilities.

A server page can load data directly:

```tsx
import { getProducts } from "@/lib/products";

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

There is no `useEffect` here and no “loading data after mount” requirement. The component can await the data as part of server rendering.

## 4. Client Components exist for client capabilities

Use `'use client'` when you need state, event handlers, effects or browser-only APIs:

```tsx
'use client';

import { useState } from 'react';

export function QuantityPicker() {
  const [qty, setQty] = useState(1);

  return (
    <button onClick={() => setQty(qty + 1)}>
      Quantity: {qty}
    </button>
  );
}
```

The directive creates a client boundary. Avoid turning a large page into a Client Component just to support one interactive button. Extract the interactive island instead.

## 5. Compose the two worlds

A Server Component can fetch a product and render a small Client Component inside it:

```tsx
import { QuantityPicker } from './quantity-picker';

export default async function ProductPage() {
  const product = await getProduct();

  return (
    <article>
      <h1>{product.name}</h1>
      <p>BDT {product.price}</p>
      <QuantityPicker />
    </article>
  );
}
```

This is one of the most useful Next.js habits: **keep data/security work on the server when possible; move only the interactivity that needs the browser into client components.**

## 6. Loading data in a Client Component

Sometimes the browser genuinely owns the interaction. A search-as-you-type UI might request new results after each input change. In that case a Client Component can call an API. But ask yourself why the request belongs there.

A good decision checklist is:

```text
Does it need browser state/events? → client may own it
Is it needed for initial page content? → server is often simpler
Does it need a secret? → never expose that secret to the client
Is it user-specific? → consider server/session boundary carefully
```

## 7. `loading.tsx` and `error.tsx` are part of the user experience

Long-running data work should not leave an unexplained blank screen. Route-level loading UI gives the framework a fallback while route content is prepared.

```tsx
export default function Loading() {
  return <p>Loading products…</p>;
}
```

Error UI is a different concern: something failed. Design these states as deliberately as the success state.

## 8. Food/product list → detail route mental exercise

Use the source curriculum's “all foods / food details” idea with the included product data:

```text
/products
  ↓ server loads list
click product
  ↓ navigation
/products/[id]
  ↓ server loads one record
not found?
  ├─ yes → notFound() → not-found.tsx
  └─ no  → product page
```

That flow joins routing, server data and failure handling into one coherent model.

## Practice path

Open `nextjs-fullstack-reference.zip` and identify each file as **server by default**, **client because it needs browser interactivity**, or **route-state UI** such as `loading.tsx` and `not-found.tsx`.

Then add one interactive quantity component without marking the whole product page `'use client'`.

The Next.js-specific code is **REFERENCE-ONLY** in this release environment. The important verified result here is the architecture: the included project files are internally consistent and link the same `products` data across list/detail routes.
