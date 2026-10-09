---
title: Build an Authenticated News App — Part 1
order: 1
summary: 'Build the public experience of a Next.js news application: structure, navigation, categories, filtering, loading and dynamic detail pages.'
level: Intermediate
time: 2–3 hours
curriculum_level: Level 01
source_module: '37'
source_type: source-curriculum
topics:
- Project Overview, Setup & Header Design
- Font & Date-FNS Integration and not-found page
- Implement Marquee & Design Navbar
- Recap & Design Grid Layout, Fetch Categories
- Display Categories & Design Sidebar
- Load News Data & Filter News Based on Category
- Display News Card and handle loading
- Show all News data and show dynamic news
- Module Summary
prerequisites:
- level-01/l1-36-authentication-advanced-profile-password-and-ema/01-main
keywords:
- next.js project
- news app
- categories
- filtering
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
## Project goal

Now combine the framework pieces into one coherent application. The source curriculum uses a news-style project. In Part 1, build the **public reading experience** before adding account-owned mutations in Part 2.

```text
Header / navbar
      ↓
category navigation
      ↓
news list / grid
      ↓
dynamic article detail
```

## What you will build

- initial project structure and header;
- font and date formatting;
- custom not-found route;
- navigation/marquee-style information strip;
- responsive grid and category sidebar;
- category-driven filtering;
- news cards and loading UI;
- dynamic detail routes.

## 1. Define the data shape before the card

```ts
type NewsItem = {
  id: string;
  title: string;
  category: string;
  excerpt: string;
  publishedAt: string;
};
```

A clear shape improves every later decision: list rendering, filter logic, route params and database migration.

## 2. Build static layout first

Start with the header, main grid and sidebar using placeholder data. This prevents “API debugging” and “layout debugging” from happening at the same time.

```text
Root layout
├── Header
├── Info strip / marquee
└── Main
    ├── CategorySidebar
    └── NewsGrid
        └── NewsCard
```

## 3. Format dates at the display boundary

Keep stored data machine-friendly (for example ISO timestamps). Convert it to a human-readable format close to the component that presents it. If you use `date-fns`, keep that dependency concern out of your domain data.

## 4. Fetch categories and news separately

Categories describe navigation. News items describe content. They may eventually come from different endpoints or cache at different rates, so keep the functions separate:

```ts
const categories = await getCategories();
const news = await getNews();
```

## 5. Filtering should be explainable

If the selected category is represented by a route or query parameter, you gain shareable state. If it exists only in client memory, a copied URL may not reproduce the same view.

For a beginner build, either is acceptable if you can explain the trade-off. For a content site, URL-driven filtering is often more useful.

## 6. News card responsibilities

A card should render one item and link to its detail page. It should not know how the entire collection was fetched.

```tsx
function NewsCard({ item }: { item: NewsItem }) {
  return (
    <article>
      <p>{item.category}</p>
      <h2>{item.title}</h2>
      <p>{item.excerpt}</p>
      <Link href={`/news/${item.id}`}>Read article</Link>
    </article>
  );
}
```

## 7. Loading is part of the route

Use route loading UI for the list/detail areas. A skeleton is useful when it resembles the content shape; a simple status is better than a decorative skeleton that gives no information.

## 8. Dynamic article detail

Create `app/news/[id]/page.tsx`. Load one item based on the route param. If it does not exist, show the not-found state.

This is the same route/data pattern you learned with products. Reusing patterns is a core engineering skill.

## Build checkpoint

Part 1 is complete when a visitor can:

1. load the home page;
2. browse categories;
3. see responsive cards;
4. filter the list;
5. open a dynamic article page;
6. see a loading state during data work;
7. reach a designed not-found page from an invalid ID.

Authentication comes next. Keeping public read behavior working first gives you a stable baseline before adding session-dependent mutations.
