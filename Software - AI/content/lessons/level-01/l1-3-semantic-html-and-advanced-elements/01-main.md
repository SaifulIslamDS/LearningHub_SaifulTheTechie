---
title: Build Semantic Pages, Forms, Tables & Media
order: 1
summary: Use semantic layout, richer forms, tables, media and a Flexbox bridge.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '3'
source_type: source-curriculum
topics:
- HTML5 vs HTML, Audio, video, YouTube video, embed
- 'Explore HTML5: nav, main, header, footer, section, article,'
- 'HTML Form: label fieldset legend radio checkbox textarea reset submit'
- 'HTML Table: Table, tr, th, td, caption, colspan, thead, tbody, tfoot'
- CSS Flex Layout Basic Overview
- Recap CSS Box Model & auto property
- 'Navigation: Simple navbar and internal navigation among files'
- 'Hero: Create a Simple Banner with flexbox'
- 'Card: Create Some Card sections and style'
- 'HTML Overview: Summary, practice task'
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

HTML is most useful when it describes **what content means**, not only how you want it to look. Semantic HTML gives browsers, search engines, accessibility tools and other developers a clearer document structure.

This chapter extends your first page with media, landmarks, richer forms, tables and a reusable navigation/hero/card structure.

## What you will learn

- HTML5 semantic landmarks such as `header`, `nav`, `main`, `section`, `article` and `footer`;
- audio, video and embedded media;
- fieldsets, radio buttons, checkboxes and text areas;
- accessible table structure;
- how Flexbox starts to connect semantic structure to layout;
- internal navigation among files and page sections;
- how a hero section and card collection are assembled.

## 1. Choose elements for meaning first

Compare these two structures:

```html
<div class="top"></div>
<div class="menu"></div>
<div class="content"></div>
<div class="bottom"></div>
```

and:

```html
<header class="site-header"></header>
<nav aria-label="Primary"></nav>
<main></main>
<footer></footer>
```

Both can be styled, but the second structure communicates roles directly. That helps code review and often helps assistive technologies interpret the page.

A simple article layout could be:

```html
<main>
  <article>
    <header>
      <h1>How I built my first portfolio</h1>
      <p>Published <time datetime="2026-10-09">9 October 2026</time></p>
    </header>

    <section aria-labelledby="lessons">
      <h2 id="lessons">What I learned</h2>
      <p>...</p>
    </section>
  </article>
</main>
```

Use `section` when a region has its own thematic purpose, often with a heading. Use `article` for content that could reasonably stand on its own.

## 2. Add audio, video and embedded content

Native media elements make the relationship explicit:

```html
<video controls width="640">
  <source src="demo.mp4" type="video/mp4">
  Your browser does not support the video element.
</video>
```

For a YouTube video you usually embed the provider's player using an `iframe`:

```html
<iframe
  src="https://www.youtube.com/embed/VIDEO_ID"
  title="Project demo"
  loading="lazy"
  allowfullscreen>
</iframe>
```

The `title` is important because an iframe otherwise gives screen-reader users little information about what the embedded region contains.

## 3. Build richer forms

Group related controls with `fieldset` and `legend`:

```html
<fieldset>
  <legend>Preferred contact method</legend>

  <label>
    <input type="radio" name="contact" value="email" checked>
    Email
  </label>

  <label>
    <input type="radio" name="contact" value="phone">
    Phone
  </label>
</fieldset>
```

For independent yes/no choices, use checkboxes:

```html
<label>
  <input type="checkbox" name="updates" value="yes">
  Send project updates
</label>
```

Use a text area for multi-line content:

```html
<label for="message">Message</label>
<textarea id="message" name="message" rows="6"></textarea>
```

## 4. Tables are for relationships in tabular data

Do not use a table merely to place content in columns. Use it when row/column relationships matter.

```html
<table>
  <caption>Project learning plan</caption>
  <thead>
    <tr>
      <th scope="col">Week</th>
      <th scope="col">Focus</th>
      <th scope="col">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>HTML and CSS</td>
      <td>Complete</td>
    </tr>
  </tbody>
</table>
```

`thead`, `tbody` and `tfoot` describe table regions. `colspan` lets a cell span multiple columns, but use merged cells carefully because complex tables are harder to understand.

## 5. Flexbox connects document structure to layout

HTML should remain meaningful even before styling. CSS then controls visual arrangement:

```css
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
```

Flexbox is good when you are arranging items primarily in one direction: a navigation row, a toolbar, a set of buttons or a row of cards.

## 6. Internal navigation

Link to another file:

```html
<a href="projects.html">Projects</a>
```

Link to a section in the current file:

```html
<a href="#contact">Contact</a>
...
<section id="contact">...</section>
```

The fragment after `#` targets an element ID. IDs on a page should be unique.

## 7. Build a hero section

A hero is typically the first prominent content block. Keep the HTML simple:

```html
<section class="hero">
  <div class="hero__copy">
    <p class="eyebrow">Software & AI Engineering</p>
    <h1>I build practical digital products.</h1>
    <p>Learning full-stack development, data and AI through real projects.</p>
    <a class="button" href="#projects">View projects</a>
  </div>
  <img src="images/profile.jpg" alt="Saiful Islam">
</section>
```

Then use CSS layout rather than adding extra HTML purely for positioning.

## 8. Build reusable project cards

```html
<section id="projects" aria-labelledby="projects-title">
  <h2 id="projects-title">Projects</h2>
  <div class="cards">
    <article class="card">
      <h3>Learning Hub</h3>
      <p>A static tutorial site generated from structured content.</p>
      <a href="#">Read case study</a>
    </article>
  </div>
</section>
```

The card is an `article` because each project can be understood as a self-contained item.

## 9. Extend the practice project

Use the Web Foundations package and improve the profile page:

1. replace generic wrappers with semantic landmarks;
2. add primary navigation;
3. add a hero section;
4. add an accessible contact form;
5. add a small table only if you genuinely have tabular information;
6. add project cards;
7. verify the page still makes sense with CSS temporarily disabled.

That last check is useful: if your content order becomes confusing without styling, the HTML structure probably needs improvement.
