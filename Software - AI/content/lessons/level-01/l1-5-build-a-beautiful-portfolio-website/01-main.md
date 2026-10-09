---
title: Build & Publish Your Developer Portfolio
order: 1
summary: Integrate HTML, CSS, responsive design and Git into a published portfolio.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '5'
source_type: source-curriculum
topics:
- Module Introduction, project overview, and git setup
- Set Google fonts and set navbar and primary colour
- Banner content and portfolio image using flex
- Simple image background, and about section
- Use Flexbox for about info and start the What I am
- Technical skills, flex gap, and how to apply flex
- Resume section Education and Experience area
- Style contact form and GitHub page hosting, live link
- Module summary and Font Awesome
prerequisites: []
keywords:
- web
- html
- css
- git
reviewed: '2026-10-09'
files:
- level-01/web-foundations-starter.zip
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
- title: Git documentation
  url: https://git-scm.com/doc
  source: Git
  note: Official Git documentation.
- title: GitHub Docs
  url: https://docs.github.com/en/get-started
  source: GitHub
  note: Official GitHub getting-started documentation.
---
## Start here

A portfolio is an engineering deliverable, not only a visual page. It should provide credible evidence of what you can build and explain.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>Recruiters, clients and collaborators use a portfolio to inspect decisions, code, demos and communication quality.</p></div>

## What you will learn

- Module Introduction, project overview, and git setup
- Set Google fonts and set navbar and primary colour
- Banner content and portfolio image using flex
- Simple image background, and about section
- Use Flexbox for about info and start the What I am
- Technical skills, flex gap, and how to apply flex
- Resume section Education and Experience area
- Style contact form and GitHub page hosting, live link

## Core idea

Recommended sequence: semantic structure → design tokens → navigation/hero → project grid → resume/contact → responsive/accessibility checks → Git history → deployment. Every project card should explain the problem, stack and evidence link.

## Practice files and code trail

This tutorial is paired with `web-foundations-starter.zip`. Use the download as working material, not as a replacement for the explanation above. Open the starter/reference files, follow the code in order, run what can be run locally, and compare your result with the tutorial before moving on.

## Career build extension
## Build the portfolio as a real product page

A portfolio is your first opportunity to practice **information architecture**, not only CSS. Decide what a recruiter or client needs to learn in the first minute:

```text
Who are you?
What do you build?
What skills can you prove?
What projects show those skills?
How can someone contact you?
```

Build the page in that order. A decorative animation is less important than a clear answer to those questions.

### 1. Navbar and design tokens

Start with a few reusable CSS variables rather than repeating colors everywhere:

```css
:root {
  --brand: #0b9cf4;
  --ink: #071426;
  --surface: #f4f8fc;
  --max: 1100px;
}
```

Create navigation links that point to real section IDs. Test them with keyboard navigation as well as a mouse.

### 2. Hero section

Use Flexbox to separate introduction copy from an optional image. The text should explain your direction in one or two sentences. Avoid filler such as “Welcome to my website.”

```html
<section class="hero">
  <div>
    <p class="eyebrow">Software & AI learner</p>
    <h1>I build practical digital products.</h1>
    <p>I am developing full-stack and AI engineering skills through hands-on projects.</p>
    <a class="button" href="#projects">View projects</a>
  </div>
  <img src="portrait.jpg" alt="Saiful Islam">
</section>
```

### 3. About + skills

The About section should explain your direction. The skills section should show evidence rather than a random logo wall. Group technologies by purpose: frontend, backend, data, tools.

```css
.skills {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}
```

### 4. Resume / experience section

Use semantic headings and dates. If you are transitioning careers, connect previous professional experience to transferable skills such as analysis, quality, operations or project coordination instead of pretending it did not exist.

### 5. Project cards

Every project card should answer:

```text
Problem → what did you build → technology → proof/link
```

A strong card is more valuable than a progress bar claiming “JavaScript 90%”.

### 6. Contact form

A static portfolio can still contain a correctly structured form even before you connect a backend. Label every input, use the correct input type and explain clearly if the form is only a UI demo.

### 7. GitHub Pages / deployment

Commit the project, push it to GitHub and follow the current GitHub Pages instructions. The important skill is the release loop:

```text
edit → test → commit → push → verify live site
```

After deployment, open the site on a phone-sized viewport and check navigation, text wrapping, image size, focus states and contact links.

## Portfolio quality checklist

- meaningful `<title>` and description;
- one clear `<h1>`;
- semantic sections;
- mobile layout works without horizontal scrolling;
- project links are real;
- no placeholder text;
- repository README explains the build;
- live URL is tested after each important release.
