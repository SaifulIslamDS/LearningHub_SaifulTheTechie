# Validation Report — v0.5.2

**Product:** Saiful The Techie — Software & AI Engineering Learning Hub  
**Release:** v0.5.2 — Navigation, Video & Learning-Path Audit  
**Validated:** 2026-10-09

## Result

**PASS.** The patch corrects the sidebar Level controls, learner-facing module-page duplication/source bookkeeping, direct-file YouTube failure mode, and the roadmap sequencing issue identified by the beginner-to-career audit.

The expected configuration note remains: `site_url` is empty until the live deployment target is chosen, so absolute canonical/share URLs and `sitemap.xml` are intentionally omitted.

## Release size

- **216 generated HTML pages**
- **70 authored tutorials**
- **135 module/roadmap pages**
- **61 video companion pages**
- **70 AI tutor prompts**
- **7 deterministic practice ZIPs**

## UI correction checks

### Collapsible levels

Every normal generated page includes two independent sidebar controls:

- Level 01
- Level 02

`assets/app.js` stores their open/closed state under `stse-levels-v1`.

Structural result:

```text
LEVEL_COLLAPSE_HANDLER True
NORMAL_PAGES_WITH_TWO_LEVEL_TOGGLES PASS
```

### One primary module title

All **135 module pages** were parsed. Every module page contains exactly one `<h1>`.

```text
MODULE_PAGES 135
MODULE_H1_ERRORS 0
```

### Learner-facing source bookkeeping

Generated learner HTML was scanned for the phrases:

- `Source module`
- `Source mapping`

Result:

```text
SOURCE_UI_HITS 0
```

Curriculum traceability remains internal in `curriculum.yml` and lesson metadata.

## YouTube companion fix

The static generator no longer writes YouTube iframe URLs directly into tutorial HTML.

Instead:

- each companion renders metadata + a stable fallback frame;
- `assets/app.js` injects a `youtube-nocookie.com` iframe only when the page is served over `http:` or `https:`;
- direct `file://` use keeps the external Watch on YouTube fallback;
- the iframe retains `strict-origin-when-cross-origin` referrer policy.

This avoids the observed YouTube Error 153 experience in direct-file mode, where the player request may not carry the HTTP Referer/client identity required by YouTube.

Structural result:

```text
VIDEO_COMPANION_PAGES 61
STATIC_YOUTUBE_IFRAME_HTML 0
FILE_PROTOCOL_VIDEO_GUARD True
```

## HTML / build checks

```text
HTML_PAGES 216
DUPLICATE_ID_PAGES 0
Internal links: all OK
```

`python -m py_compile build.py` passed.  
`node --check assets/app.js` passed.

## Deterministic build

The site was built twice and the SHA-256 manifest of the complete `docs/` tree was compared.

```text
DETERMINISM_DIFF_LINES 0
```

Both builds reported:

```text
Built 216 pages: 2 levels, 135 modules, 70 lessons -> docs/
Internal links: all OK
```

## Code regression — RUN-HERE

Re-run successfully:

- all **14** JavaScript foundation programs;
- all **4** framework-independent React logic programs;
- all **5** TypeScript programs with strict compilation, then Node execution;
- all **6** local backend/domain programs.

No tutorial code was changed by this patch; this regression confirms the previous executable baseline remains intact.

## Practice-package validation

All **7** practice ZIPs passed `ZipFile.testzip()` with no corrupt member.

## Learning-path audit

`LEARNING_PATH_AUDIT.md` records the full audit.

Key determination:

- the architecture and complete curriculum can support an **absolute beginner → advanced → career-ready** path;
- the **current v0.5.2 release is not yet career-ready** and must not be described that way;
- the previous roadmap skipped Level 01 Modules 53–67 and failed to explicitly schedule the Level 02 professional/bonus layer;
- the release sequence is corrected before further content expansion.

## Known limits

- Automated screenshot/visual-regression testing is not part of this pass. The user-supplied screenshots were used to identify the UI issues, and the generated HTML/CSS/JS structure was validated after correction.
- The exact approved circular Saiful The Techie logo binary is still unavailable in this runtime; the approved text/wordmark fallback remains in use.

## Next approved milestone

**v0.6.0 — Complete Level 01: Full Stack Project 2 + AI-Assisted Coding (Modules 53–67)**
