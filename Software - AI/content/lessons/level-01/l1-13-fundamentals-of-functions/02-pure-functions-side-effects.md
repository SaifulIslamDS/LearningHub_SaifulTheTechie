---
title: Pure Functions & Side Effects
order: 2
summary: Recognize predictable computation and controlled effects.
level: Beginner
time: 45–60 min
curriculum_level: Level 01
source_module: '13'
source_type: st-recommended
topics: []
prerequisites: []
keywords:
- pure functions
- side effects
reviewed: '2026-10-09'
files: []
resources:
- title: MDN JavaScript Guide
  url: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
  source: MDN
  note: Official browser-oriented JavaScript guide.
---
## Start here

A pure function returns the same result for the same inputs and does not change outside state.

<div class="admonition job"><p class="admonition-title">Why it matters at work</p><p>This bridge topic prevents common gaps that appear when tutorial code is moved into real projects.</p></div>

## Core idea

Pure functions are easier to test. Real programs still need effects such as network requests or storage; keep those boundaries visible and controlled.
