---
title: Build Your First HTML & CSS Page
order: 1
summary: Build a correct first page, connect CSS, understand selectors and the box model.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '1'
source_type: source-curriculum
topics:
- What you will learn from this Milestone-1 (Animated)
- 'Web & HTML: VSCode setup, first HTML file, page structure'
- 'HTML Text: Headings, paragraphs, formatting tags'
- 'HTML Essentials: Lists, links, images, buttons'
- 'HTML Forms: Input types, select, option, form UI'
- 'CSS Basics: Inline, internal, external styles'
- 'CSS Selectors: Tag, class, id, universal, combined selectors'
- 'CSS Box Model: Margin, padding, border, width, height'
- 'CSS Styling: Font, background, position'
- 'CSS Display: visibility, box-shadow'
- Module Summary & Practise Task
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
---
## Start here

Every website eventually becomes **HTML, CSS and JavaScript inside a browser**. In this first tutorial we deliberately start with only HTML and CSS so that you can see the two jobs clearly:

- **HTML** describes the structure and meaning of the page.
- **CSS** controls how that structure looks and how it is laid out.

If you later work with React, Next.js or another framework, you will still produce the same kinds of HTML elements and CSS rules. Strong foundations here make later debugging much easier.

<div class="admonition note"><p class="admonition-title">Build goal</p><p>Turn the starter files into a small profile page with a heading, introduction, skill list, links, image, contact form and a styled card layout.</p></div>

## What you will learn

By the end of this chapter you should be able to:

- create a valid HTML document in VS Code;
- use headings, paragraphs, lists, links, images and buttons;
- build a basic form with useful input types;
- connect an external stylesheet correctly;
- select elements with tag, class and ID selectors;
- reason about the CSS box model;
- apply fonts, backgrounds, spacing and simple positioning;
- understand the difference between `display`, `visibility` and visual effects such as `box-shadow`.

## 1. Create the project folder

Create a folder named `profile-site` and place two files inside it:

```text
profile-site/
├── index.html
└── style.css
```

The downloadable Web Foundations package contains the same basic structure. Use the **starter** copy while following this tutorial and compare it with the **completed** copy only after you have tried the steps yourself.

A browser does not care whether you use VS Code, another editor or even Notepad. VS Code is useful because it gives you syntax highlighting, file navigation and extensions, but the browser ultimately reads ordinary text files.

## 2. Understand the HTML document

Start with this complete document:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Saiful Islam — Profile</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="profile">
    <h1>Saiful Islam</h1>
    <p>Software & AI Engineering learner.</p>
  </main>
</body>
</html>
```

Read it from the outside inward:

### `<!doctype html>`

This tells the browser to use modern HTML standards mode. It is not an HTML element and it does not create anything visible on the page.

### `<html lang="en">`

`<html>` is the root element. The `lang` attribute tells browsers and assistive technologies which language the document primarily uses. It also helps search engines and translation tools.

### `<head>` and `<body>`

The **head** contains information *about* the document: character encoding, viewport rules, page title, linked stylesheets and other metadata. The **body** contains the content that becomes the visible page.

### Character encoding

```html
<meta charset="utf-8">
```

UTF-8 lets your page represent a very large range of characters consistently. Put this metadata near the beginning of the `<head>`.

### Responsive viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Without this setting, a phone browser may render the page as if it were a much wider desktop page and then scale it down. The viewport declaration gives responsive CSS the dimensions you expect.

### Connecting CSS

```html
<link rel="stylesheet" href="style.css">
```

`href="style.css"` is a **relative path**. It means: “find `style.css` in the same folder as this HTML file.” If your CSS appears to do nothing, checking this path should be one of your first debugging steps.

## 3. Build a meaningful content hierarchy

Headings are not just large text. They create a hierarchy.

```html
<h1>Saiful Islam</h1>
<h2>About me</h2>
<h2>Skills</h2>
<h2>Projects</h2>
```

Use one clear page-level heading, then nest sections logically. Do not choose `<h3>` merely because you want smaller text; choose the heading level for meaning, then use CSS for size.

Add paragraphs and emphasis:

```html
<p>
  I am learning <strong>software engineering</strong> and
  <em>AI application development</em>.
</p>
```

`<strong>` communicates importance. `<em>` communicates emphasis. Browsers usually render them in bold and italics, but their main value is semantic meaning.

## 4. Lists, links, images and buttons

A skill list is a natural use of an unordered list:

```html
<section>
  <h2>Skills</h2>
  <ul>
    <li>HTML and CSS</li>
    <li>JavaScript</li>
    <li>Git and GitHub</li>
  </ul>
</section>
```

Use links for navigation:

```html
<a href="https://saifulshuvo.com/">Visit my website</a>
```

For a link that opens in a new tab, also consider the relationship between the two browsing contexts:

```html
<a href="https://github.com/" target="_blank" rel="noopener">
  GitHub
</a>
```

Images need a source and useful alternative text when the image communicates content:

```html
<img
  src="images/profile.jpg"
  alt="Portrait of Saiful Islam"
  width="320"
  height="320"
>
```

A **button** is for an action; a **link** is for navigation. This distinction becomes important later when you add JavaScript and accessibility behavior.

```html
<button type="button">Show projects</button>
```

## 5. Build a real form

Forms collect structured input from a user. Labels matter because they explain what each control is for and make the form easier to use with assistive technology.

```html
<form class="contact-form">
  <div>
    <label for="name">Name</label>
    <input id="name" name="name" type="text" autocomplete="name" required>
  </div>

  <div>
    <label for="email">Email</label>
    <input id="email" name="email" type="email" autocomplete="email" required>
  </div>

  <div>
    <label for="topic">Topic</label>
    <select id="topic" name="topic">
      <option value="project">Project</option>
      <option value="job">Job opportunity</option>
      <option value="other">Other</option>
    </select>
  </div>

  <button type="submit">Send message</button>
</form>
```

Notice how the `for` value on each label matches the input's `id`. The `name` attribute is the key that would be sent when a real form is submitted to a server.

At this stage the form does not send email. That requires backend logic or a form service later. The purpose here is to build correct interface structure.

## 6. Add the external stylesheet

Open `style.css` and begin with a small reset:

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f4f8fc;
  color: #071426;
  line-height: 1.6;
}
```

`box-sizing: border-box` changes how width and height calculations work. With it, declared width includes the element's padding and border. This usually makes layouts easier to reason about.

## 7. Understand CSS selectors

CSS rules have a selector and a declaration block:

```css
.profile {
  max-width: 48rem;
  margin: 4rem auto;
  padding: 2rem;
}
```

`.profile` is a **class selector**. It matches any element whose `class` list contains `profile`.

Compare common selector types:

```css
p { color: #334155; }        /* tag selector */
.profile { padding: 2rem; }  /* class selector */
#contact { scroll-margin-top: 5rem; } /* ID selector */
* { box-sizing: border-box; } /* universal selector */
.profile h2 { margin-top: 2rem; } /* combined/descendant selector */
```

For reusable styling, classes are usually the most flexible default. IDs are useful for unique document targets, form labels and fragment links, but relying on them heavily for styling can make CSS harder to reuse.

## 8. The box model is the foundation of layout

Every normal HTML element is treated like a rectangular box:

```text
margin
┌──────────────────────────────────┐
│ border                           │
│  ┌────────────────────────────┐  │
│  │ padding                    │  │
│  │  ┌──────────────────────┐  │  │
│  │  │ content              │  │  │
│  │  └──────────────────────┘  │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

- **content** is the text, image or child elements;
- **padding** creates space inside the box;
- **border** draws around that padded box;
- **margin** creates space outside the border.

Style the profile card:

```css
.profile {
  width: min(48rem, calc(100% - 2rem));
  margin: 4rem auto;
  padding: 2rem;
  background: #ffffff;
  border: 1px solid #dbe7f1;
  border-radius: 1rem;
  box-shadow: 0 18px 45px rgba(5, 35, 70, 0.08);
}
```

`margin: 4rem auto` gives vertical space and automatically divides the remaining horizontal space equally, centering a block that has a constrained width.

## 9. Fonts, backgrounds and visual hierarchy

A page becomes easier to scan when spacing, type weight and color communicate hierarchy.

```css
h1,
h2 {
  line-height: 1.15;
  color: #04152f;
}

h1 {
  font-size: clamp(2rem, 6vw, 3.4rem);
  margin: 0;
}

h2 {
  margin-top: 2.5rem;
}

a {
  color: #087fc4;
}
```

`clamp()` lets a value stay between a minimum and maximum while changing with the viewport. You do not have to master responsive typography now; just notice that CSS values can be fluid rather than fixed.

## 10. `display`, visibility and positioning

The `display` property controls how an element participates in layout. You will study Flexbox and Grid in later modules, but three ideas are useful now:

```css
.skills {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
```

`visibility: hidden` hides an element visually while preserving its layout space. `display: none` removes it from normal layout entirely. These are different behaviors and can have different accessibility implications.

Positioning changes how an element is placed:

```css
.badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
}
```

An absolutely positioned element is positioned relative to an appropriate positioned ancestor. Do not reach for absolute positioning for ordinary page layout; Flexbox and Grid are usually better tools.

## 11. Build the profile page step by step

Now combine the ideas into one page.

### Step 1 — Add page landmarks

```html
<body>
  <header class="site-header">
    <a href="#main">Saiful</a>
  </header>

  <main id="main" class="profile">
    <!-- profile content -->
  </main>

  <footer class="site-footer">
    <p>Built while learning Software & AI Engineering.</p>
  </footer>
</body>
```

### Step 2 — Add profile content

Add an introduction, About section, Skills list, Projects section and Contact section. Keep headings in a logical order.

### Step 3 — Add reusable classes

Instead of styling every element independently, create reusable classes such as `.section`, `.skills`, `.project-card` and `.contact-form`.

### Step 4 — Open the page in a browser

Save both files, then open `index.html`. Resize the browser window. Use DevTools' Elements panel to select an element and inspect which CSS rule is applied.

### Step 5 — Make one change at a time

Change the background, spacing or font size and observe the effect. Small changes make cause and effect easier to understand than changing twenty declarations at once.

## 12. How HTML and CSS travel through the browser

A useful mental model is:

```text
index.html ──► browser parses HTML ──► DOM tree
     │
     └─► style.css ──► browser parses CSS ──► style rules
                                      │
                         DOM + styles ─┴─► layout ─► paint ─► pixels
```

You do not need to memorize browser-engine internals yet. The important idea is that HTML creates structure and CSS participates in calculating the visual presentation. When you later add JavaScript, JavaScript can inspect or change that document structure.

## 13. Use the practice package as a code trail

The downloadable `web-foundations-starter.zip` is designed to mirror this chapter. Work in this order:

1. open the `starter/` folder;
2. run `index.html` in a browser;
3. add the HTML sections described above;
4. add CSS incrementally rather than pasting everything at once;
5. compare your files with `completed/` after your own attempt;
6. read the package `README.md` to understand the final folder structure.

The goal is not to produce the same colors as the reference. The goal is to understand why every element and CSS rule exists.

## Where this is used professionally

The same fundamentals appear in every frontend stack. A React component ultimately produces elements; a Next.js page still renders HTML; a design system still depends on CSS layout, spacing and visual states. When a framework abstraction fails, developers frequently debug the resulting HTML and CSS directly in browser DevTools.
