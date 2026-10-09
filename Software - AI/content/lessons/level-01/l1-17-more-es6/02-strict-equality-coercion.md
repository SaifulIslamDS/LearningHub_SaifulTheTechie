---
title: Strict Equality & Coercion Discipline
order: 2
summary: Recognize implicit conversions and prefer explicit type handling.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '17'
source_type: st-recommended
topics: []
prerequisites: []
keywords:
- coercion
- strict equality
reviewed: '2026-10-09'
files: []
resources:
- title: MDN JavaScript Guide
  url: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
  source: MDN
  note: Official browser-oriented JavaScript guide.
- title: MDN JavaScript Reference
  url: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference
  source: MDN
  note: Reference for language syntax and built-ins.
---
## Start here

JavaScript can convert types implicitly in some operations. This can be convenient but can also hide bugs.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>This bridge topic prevents common gaps that appear when tutorial code is moved into real projects.</p></div>

## Core idea

Prefer `===` and `!==` unless you can explain why coercive equality is needed. Convert form/input strings deliberately with `Number`, `String` or parsing.
