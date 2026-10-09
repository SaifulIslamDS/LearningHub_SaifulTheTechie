#!/usr/bin/env python3
"""
Build the static tutorial site.

    python build.py            # writes the finished site into ./docs

Source files (edit these):
    site.yml                       site name, author, links
    curriculum.yml                 phases, modules, planned topics
    content/lessons/<phase>/<module>/<lesson>.md   lesson pages
    content/pages/<page>.md        extra pages (about, how to learn ...)
    content/curriculum-map.html    the one-page curriculum, copied as-is
    content/downloads/             practice files (CSV, SQL ...) + files.yml catalogue
    content/images/                charts and screenshots used in lessons (copied to docs/images/)
    content/glossary.yml           glossary terms (linked from lessons as "Key terms")
    assets/                        CSS + JS

Output (do not edit by hand, it is rebuilt every time):
    docs/                          open docs/index.html offline, or serve with GitHub Pages
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

try:
    import markdown
    import yaml
except ImportError:
    sys.exit("Missing packages. Run:  pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUT = ROOT / "docs"

SITE = yaml.safe_load((ROOT / "site.yml").read_text(encoding="utf-8"))
CURR = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
PHASES = CURR["phases"]
TRACKS = CURR.get("tracks", [])

esc = html.escape
MD_EXT = ["extra", "admonition", "sane_lists", "toc", "codehilite"]
MD_CFG = {
    "codehilite": {"guess_lang": False, "css_class": "codehilite", "pygments_lang_class": True},
    "toc": {"toc_depth": "2-3"},
}

warnings: list[str] = []
notes: list[str] = []


# ------------------------------------------------------------------ helpers
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def read_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            meta = yaml.safe_load(text[3:end]) or {}
            return meta, text[end + 4:].lstrip("\n")
    return {}, text


def render_md(text: str) -> tuple[str, list]:
    md = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_CFG)
    body = md.convert(text)
    return body, getattr(md, "toc_tokens", [])


def strip_tags(s: str) -> str:
    s = re.sub(r"<pre.*?</pre>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def rel(depth: int) -> str:
    return "../" * depth if depth else "./"


# ------------------------------------------------------------------ load lessons
LESSONS: list[dict] = []          # every written lesson, curriculum order
by_module: dict[str, list] = {}   # "phase-1/analytical-sql" -> lessons

for ph in PHASES:
    for mod in ph["modules"]:
        key = f"{ph['id']}/{mod['id']}"
        folder = CONTENT / "lessons" / ph["id"] / mod["id"]
        items = []
        if folder.is_dir():
            for f in sorted(folder.glob("*.md")):
                if f.name.startswith("_"):      # _module.md = module intro, not a lesson
                    continue
                meta, body = read_front_matter(f)
                if meta.get("draft"):
                    continue
                slug = f.stem
                items.append({
                    "id": f"{key}/{slug}",
                    "slug": slug,
                    "phase": ph,
                    "module": mod,
                    "meta": meta,
                    "source": body,
                    "file": f,
                    "title": meta.get("title", slug.replace("-", " ").title()),
                    "order": meta.get("order", 999),
                })
            items.sort(key=lambda x: (x["order"], x["slug"]))
            topic_names = set(mod["topics"])
            for it in items:
                for t in it["meta"].get("topics", []) or []:
                    if t not in topic_names:
                        warnings.append(f"{it['file'].relative_to(ROOT)}: topic '{t}' is not in curriculum.yml for {key}")
        by_module[key] = items
        LESSONS.extend(items)

LESSON_BY_ID = {l["id"]: l for l in LESSONS}
for i, l in enumerate(LESSONS):
    l["prev"] = LESSONS[i - 1] if i > 0 else None
    l["next"] = LESSONS[i + 1] if i + 1 < len(LESSONS) else None


def phase_lesson_count(ph) -> int:
    return sum(len(by_module[f"{ph['id']}/{m['id']}"]) for m in ph["modules"])


# URL helpers (relative to site root; always explicit index.html so file:// works)
def u_phase(ph): return f"learn/{ph['id']}/index.html"
def u_module(ph, m): return f"learn/{ph['id']}/{m['id']}/index.html"
def u_lesson(l): return f"learn/{l['phase']['id']}/{l['module']['id']}/{l['slug']}.html"
def u_project(ph): return f"learn/{ph['id']}/project.html"


# Optional milestone project brief per phase: content/projects/<phase-id>.md
PROJECTS = {ph["id"]: CONTENT / "projects" / f"{ph['id']}.md" for ph in PHASES
            if (CONTENT / "projects" / f"{ph['id']}.md").exists()}


# ------------------------------------------------------------------ practice files
DL = CONTENT / "downloads"
_manifest = yaml.safe_load((DL / "files.yml").read_text(encoding="utf-8")) if (DL / "files.yml").exists() else {"files": []}
FILES = {f["path"]: f for f in _manifest.get("files", [])}
FILE_GROUPS = _manifest.get("groups", [])
BUNDLE = "practice-files.zip"


def human_size(n: int) -> str:
    return f"{n} B" if n < 1024 else (f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB")


def file_size(path: str) -> str:
    fp = DL / path
    return human_size(fp.stat().st_size) if fp.exists() else "missing"


def files_box(r: str, paths: list, where: str) -> str:
    """Download box shown at the top of lessons, modules and project pages."""
    if not paths:
        return ""
    items = []
    for pth in paths:
        if pth not in FILES:
            warnings.append(f"{where}: practice file '{pth}' is not listed in content/downloads/files.yml")
        if not (DL / pth).exists():
            warnings.append(f"{where}: practice file '{pth}' does not exist in content/downloads/")
            continue
        info = FILES.get(pth, {})
        items.append(f'<li><a href="{r}downloads/{esc(pth)}" download>{esc(pth.split("/")[-1])}</a>'
                     f'<span class="f-desc">{esc(info.get("description", ""))} · {file_size(pth)}</span></li>')
    return (f'<div class="files-box"><div class="files-head"><b>Practice files for this page</b>'
            f'<a href="{r}practice-files.html">All practice files →</a></div><ul>{"".join(items)}</ul></div>')


# ------------------------------------------------------------------ glossary
_gloss = yaml.safe_load((CONTENT / "glossary.yml").read_text(encoding="utf-8")) if (CONTENT / "glossary.yml").exists() else {}
GLOSS_CATS = _gloss.get("categories", [])
GLOSSARY = sorted(_gloss.get("terms", []), key=lambda t: t["term"].lower().lstrip("."))


def _norm(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


_gloss_ids = set()
for _t in GLOSSARY:
    gid = slugify(_t["term"]) or "term"
    while gid in _gloss_ids:
        gid += "-2"
    _gloss_ids.add(gid)
    _t["id"] = gid
    _t["names"] = {_norm(_t["term"])} | {_norm(a) for a in (_t.get("aka") or [])}
    if _t.get("cat") not in GLOSS_CATS:
        warnings.append(f"glossary: '{_t['term']}' has unknown category '{_t.get('cat')}'")


def gloss_target(t):
    """(url, label) for where a glossary term is taught: lesson, project, module or phase."""
    see = str(t.get("see", "")).strip("/")
    if see in LESSON_BY_ID:
        return u_lesson(LESSON_BY_ID[see]), LESSON_BY_ID[see]["title"]
    parts = see.split("/")
    ph = next((x for x in PHASES if x["id"] == parts[0]), None)
    if ph is None:
        if see:
            warnings.append(f"glossary: '{t['term']}' points at unknown '{see}'")
        return None, None
    if len(parts) == 2 and parts[1] == "project" and ph["id"] in PROJECTS:
        return u_project(ph), f"Phase {ph['num']} milestone project"
    if len(parts) == 2:
        m = next((x for x in ph["modules"] if x["id"] == parts[1]), None)
        if m:
            written = bool(by_module[f"{ph['id']}/{m['id']}"])
            return u_module(ph, m), f"{m['title']} (Phase {ph['num']}{'' if written else ', coming soon'})"
        warnings.append(f"glossary: '{t['term']}' points at unknown module '{see}'")
    return u_phase(ph), f"Phase {ph['num']}: {ph['short']}" + ("" if phase_lesson_count(ph) else " (coming soon)")


def lesson_terms(l) -> list:
    """Glossary terms for a lesson: taught here (see:) or named in its keywords."""
    kws = {_norm(k) for k in (l["meta"].get("keywords") or [])} | {_norm(k) for k in (l["meta"].get("terms") or [])}
    return [t for t in GLOSSARY if str(t.get("see", "")).strip("/") == l["id"] or (t["names"] & kws)]


def terms_box(r: str, terms: list) -> str:
    if not terms:
        return ""
    chips = "".join(f'<a class="term-chip" href="{r}glossary.html#{t["id"]}" title="{esc(t["def"])}">{esc(t["term"])}</a>'
                    for t in terms)
    return (f'<div class="terms-box"><div class="files-head"><b>Key terms in this lesson</b>'
            f'<a href="{r}glossary.html">Glossary →</a></div><div class="term-chips">{chips}</div></div>')


def youtube_box(meta: dict) -> str:
    """Optional, curated YouTube companion from lesson front matter."""
    y = meta.get("youtube") or {}
    if not isinstance(y, dict) or not y.get("url"):
        return ""
    title = esc(str(y.get("title") or "Video companion"))
    creator = esc(str(y.get("creator") or ""))
    why = esc(str(y.get("why_recommended") or ""))
    duration = esc(str(y.get("duration") or ""))
    level = esc(str(y.get("level") or ""))
    url = esc(str(y["url"]))
    vid = str(y.get("video_id") or "").strip()
    meta_bits = " · ".join(x for x in [creator, duration, level] if x)
    player = (f'<div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/{esc(vid)}" '
              f'title="{title}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
              f'allowfullscreen></iframe></div>') if vid else ""
    why_html = f'<p>{why}</p>' if why else ""
    meta_html = f'<p class="video-meta">{meta_bits}</p>' if meta_bits else ""
    return (f'<section class="video-companion"><h2 id="video-companion">Video companion</h2>'
            f'{player}<h3>{title}</h3>{why_html}{meta_html}<p><a href="{url}">Watch on YouTube ↗</a></p></section>')


# ------------------------------------------------------------------ quizzes
QUIZ_RE = re.compile(r'<div class="quiz-q">(.*?)</div>', re.S)
LETTERS = "ABCDEFGH"


def mark_quizzes(body_html: str, where: str) -> tuple[str, int]:
    """Add data-answer="<index>" to every quiz question, read from the bolded letter in its answer."""
    count = 0

    def fix(mo):
        nonlocal count
        inner = mo.group(1)
        ans = re.search(r"<summary>[^<]*</summary>\s*<p><strong>\s*([A-H])\b", inner)
        n_opts = len(re.findall(r"<li>", inner.split("<details", 1)[0]))
        if not ans or n_opts < 2 or LETTERS.index(ans.group(1)) >= n_opts:
            warnings.append(f"{where}: quiz question {count + 1} has no readable answer letter")
            return mo.group(0)
        count += 1
        return f'<div class="quiz-q" data-answer="{LETTERS.index(ans.group(1))}">{inner}</div>'

    return QUIZ_RE.sub(fix, body_html), count


# ------------------------------------------------------------------ SEO: social tags + sitemap
SITE_URL = (SITE.get("site_url") or "").strip()
if SITE_URL and not SITE_URL.endswith("/"):
    SITE_URL += "/"
SITEMAP: list[tuple[str, str]] = []           # (path, lastmod)
RELEASE_DATE = str(SITE.get("release_date") or date.today().isoformat())


def tag_html(tag):
    if not tag:
        return ""
    label = {"new": "New", "updated": "Updated"}.get(tag, tag)
    return f'<span class="tag {esc(tag)}">{esc(label)}</span>'


# ------------------------------------------------------------------ layout pieces
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICON_MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
ICON_SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

THEME_BOOT = """<script>(function(){var t=null;try{t=localStorage.getItem('daa-theme')}catch(e){}
if(!t)t=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';
document.documentElement.setAttribute('data-theme',t);
var n=null;try{n=localStorage.getItem('daa-nav')}catch(e){}
if(n==='open'&&window.matchMedia&&matchMedia('(min-width: 961px)').matches)document.documentElement.setAttribute('data-nav','open');
document.documentElement.classList.add('no-anim')})();</script>"""


def sidebar(r: str, cur_phase=None, cur_module=None, cur_lesson=None) -> str:
    out = [
           f'<div class="side-progress"><div class="bar" data-progress-scope="all" data-total="{len(LESSONS)}"><i></i></div>'
           f'<span class="bar-label" data-progress-label></span></div>']
    for ph in PHASES:
        is_cur = cur_phase is ph
        cls = "nav-phase" + (" current open" if is_cur else "")
        aria = ' aria-current="page"' if is_cur and not cur_module else ""
        out.append(f'<div class="{cls}"><a href="{r}{u_phase(ph)}"{aria}>'
                   f'<span class="nav-num">{ph["num"]}</span>{esc(ph["short"])}</a>')
        if is_cur:
            out.append('<ul class="nav-modules">')
            for m in ph["modules"]:
                mcur = cur_module is m
                out.append(f'<li><a class="{"current" if mcur else ""}" href="{r}{u_module(ph, m)}">{esc(m["title"])}</a>')
                lessons = by_module[f"{ph['id']}/{m['id']}"]
                if mcur and lessons:
                    out.append('<ul class="nav-lessons">')
                    for l in lessons:
                        c = "current" if l is cur_lesson else ""
                        out.append(f'<li><a class="{c}" data-lesson="{l["id"]}" href="{r}{u_lesson(l)}">{esc(l["title"])}</a></li>')
                    out.append("</ul>")
                out.append("</li>")
            if ph["id"] in PROJECTS:
                pc = "current" if cur_module == "project" else ""
                out.append(f'<li><a class="nav-project {pc}" href="{r}{u_project(ph)}">★ Milestone project</a></li>')
            out.append("</ul>")
        out.append("</div>")
    out.append(f'<div class="side-extra"><a href="{r}index.html">Home</a><a href="{r}curriculum.html">Full curriculum map</a><a href="{r}practice-files.html">Practice files</a><a href="{r}glossary.html">Glossary</a>'
               f'<a href="{r}how-to-learn.html">How to learn here</a><a href="{r}about.html">About &amp; contributing</a></div>')
    return "\n".join(out)


def page(*, title: str, depth: int, body: str, side: str | None, toc: list | None = None,
         description: str = "", active: str = "", wide_content: bool = False, extra_attrs: str = "",
         og_type: str = "website") -> str:
    r = rel(depth)
    full_title = f"{title} — {SITE['name']}" if title != SITE["name"] else title
    toc_html = ""
    if toc:
        links = "".join(f'<a href="#{esc(t["id"])}">{esc(t["name"])}</a>' for t in toc)
        toc_html = f'<aside class="toc" aria-label="On this page"><h4>On this page</h4>{links}</aside>'
    layout_cls = "layout wide" if toc_html else "layout"
    nav = lambda key, href, label: f'<a href="{r}{href}" class="{"active" if active == key else ""}">{label}</a>'
    logo_asset = str(SITE.get("logo_asset") or "").strip()
    logo_html = f'<img class="brand-logo" src="{r}{esc(logo_asset)}" alt="">' if logo_asset else ""
    favicon_html = f'<link rel="icon" href="{r}{esc(logo_asset)}">' if logo_asset else ""
    return f"""<!DOCTYPE html>
<html lang="{SITE.get('language', 'en')}" data-root="{r}"{extra_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description or SITE['tagline'])}">
<meta property="og:type" content="{'article' if og_type == 'article' else 'website'}">
<meta property="og:site_name" content="{esc(SITE.get('brand', SITE['name']))}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description or SITE['tagline'])}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<!--PAGE-URL-->
{THEME_BOOT}
<link rel="stylesheet" href="{r}assets/style.css">
{favicon_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <button class="icon-btn menu-toggle" id="menuBtn" aria-label="Open curriculum menu" title="Curriculum menu (press M)" aria-controls="sidebar" aria-expanded="false"><span class="ico-menu">{ICON_MENU}</span><span class="ico-close">{ICON_CLOSE}</span></button>
  <a class="brand" href="{r}index.html">{logo_html}<span class="brand-text"><span class="brand-name">{esc(SITE.get('brand', SITE['name']))}</span><span class="brand-version">{esc(SITE['name'])} · {esc(SITE.get('version', ''))}</span></span></a>
  <nav class="top-links" aria-label="Main">
    {nav('home', 'index.html', 'Home')}{nav('map', 'curriculum.html', 'Curriculum')}{nav('files', 'practice-files.html', 'Practice files')}{nav('glossary', 'glossary.html', 'Glossary')}{nav('how', 'how-to-learn.html', 'How to learn')}{nav('about', 'about.html', 'About')}
  </nav>
  <div class="top-spacer"></div>
  <div class="search" role="search">
    {ICON_SEARCH}
    <input id="searchInput" type="search" placeholder="Search lessons, tools, topics" aria-label="Search" autocomplete="off">
    <kbd>/</kbd>
    <div class="search-results" id="searchResults" role="listbox"></div>
  </div>
  <button class="icon-btn theme-toggle" id="themeBtn" aria-label="Toggle light or dark mode" title="Light / dark">{ICON_MOON}{ICON_SUN}</button>
</header>
<div class="{layout_cls}">
  <nav class="sidebar" id="sidebar" aria-label="Curriculum">
    <div class="side-title">Curriculum</div>
    {side or sidebar(r)}</nav>
  <main class="main" id="main"><div class="content{' full' if wide_content else ''}">
{body}
  </div></main>
  {toc_html}
</div>
<footer class="site"><b>{esc(SITE.get('brand', SITE['name']))}</b> · {esc(SITE['name'])} {esc(SITE.get('version', ''))} · Updated {esc(SITE['updated'])}<br>
Lesson text: <a href="{r}license.html">CC BY-NC-SA 4.0</a> · Code: <a href="{r}license.html#code-mit-license">MIT</a> · Free external resources belong to their respective owners.</footer>
<script src="{r}search-index.js"></script>
<script src="{r}assets/app.js"></script>
</body>
</html>
"""


def crumbs(r: str, items: list[tuple[str, str | None]]) -> str:
    parts = []
    for label, href in items:
        parts.append(f'<a href="{r}{href}">{esc(label)}</a>' if href else f"<span>{esc(label)}</span>")
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


def progress_block(scope: str, total: int) -> str:
    return (f'<div><div class="bar" data-progress-scope="{scope}" data-total="{total}"><i></i></div>'
            f'<span class="bar-label" data-progress-label></span></div>')


# ------------------------------------------------------------------ writers
search_index: list[dict] = []


def write(rel_path: str, content: str, lastmod: str | None = None):
    if "<!--PAGE-URL-->" in content:
        tags = ""
        if SITE_URL:
            url = SITE_URL + rel_path.removesuffix("index.html")
            tags = (f'<link rel="canonical" href="{esc(url)}">\n<meta property="og:url" content="{esc(url)}">\n'
                    f'<meta property="og:image" content="{esc(SITE_URL)}assets/og-image.png">\n'
                    f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                    f'<meta property="og:image:alt" content="{esc(SITE["name"])}: {esc(SITE["tagline"])}">\n'
                    f'<meta name="twitter:image" content="{esc(SITE_URL)}assets/og-image.png">')
        content = content.replace("<!--PAGE-URL-->", tags)
        if rel_path != "404.html":
            SITEMAP.append((rel_path, lastmod or RELEASE_DATE))
    p = OUT / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def build_home():
    r = rel(0)
    first = LESSONS[0] if LESSONS else None
    start_btn = (f'<a class="btn" href="{r}{u_lesson(first)}">Start with a lesson</a>' if first else "")
    phase_tiles = []
    for ph in PHASES:
        n = phase_lesson_count(ph)
        phase_tiles.append(f"""<a class="card phase-tile" href="{r}{u_phase(ph)}">
  <div class="row"><h3>Phase {ph['num']} — {esc(ph['title'])}</h3><span class="big-num">{ph['num']}</span></div>
  <p>{esc(ph['summary'])}</p>
  <p class="bar-label">{len(ph['modules'])} modules · {n} lesson{'s' if n != 1 else ''} written</p>
  {progress_block(ph['id'], n)}
</a>""")
    tracks = "".join(
        f'<div class="card track"><h4>{esc(t["title"])}</h4><div class="ph">Phases {" · ".join(str(p) for p in t["phases"])}</div>'
        f'<p>{esc(t["focus"])}</p></div>' for t in TRACKS)
    latest = "".join(
        f'<li class="lesson-row" data-lesson="{l["id"]}"><span class="n">{l["phase"]["num"]}</span><span>'
        f'<a href="{r}{u_lesson(l)}">{esc(l["title"])}</a><span class="desc">{esc(l["module"]["title"])} · '
        f'{esc(l["meta"].get("summary", ""))}</span></span><span class="lesson-state"></span></li>' for l in LESSONS)
    body = f"""
<section class="card hero">
  <span class="eyebrow">{esc(SITE.get('brand', ''))} · Learn · Build · Explain · Share</span>
  <h1>{esc(SITE['name'])}</h1>
  <p class="brand-line">{esc(SITE.get('brand_line', ''))}</p>
  <p>{esc(SITE['tagline'])} Every tutorial builds a mental model, demonstrates real code or data, explains verified output, and connects the skill to a practical build and curated resources.</p>
  <div class="hero-actions">{start_btn}<a class="btn ghost" href="{r}curriculum.html">See the full curriculum</a><a class="btn ghost" href="{r}how-to-learn.html">How to learn here</a></div>
</section>

<div class="grid cols-3">
  <div class="card how"><b>Learn in order, or skip</b><span>Ten phases from foundations to career. Skip what you already know.</span></div>
  <div class="card how"><b>Every lesson is practical</b><span>Deep explanations, verified examples, step-by-step builds and synchronized practice files.</span></div>
  <div class="card how"><b>Progress saved in your browser</b><span>Mark lessons complete. Nothing is sent anywhere.</span></div>
</div>

<div class="section-head"><h2>Your progress</h2><p>{len(LESSONS)} lessons written so far. New lessons are added phase by phase.</p></div>
<div class="card how">{progress_block('all', len(LESSONS))}<p style="margin:10px 0 0"><button class="btn ghost" id="resetProgress" type="button">Reset progress</button></p></div>

<div class="section-head"><h2>Curriculum phases</h2><p>Open a phase to see its modules, lessons and milestone project.</p></div>
<div class="grid cols-2">{''.join(phase_tiles)}</div>

<div class="section-head"><h2>Target role tracks</h2><p>Pick one job target. The phases listed are your priority path.</p></div>
<div class="grid cols-5">{tracks}</div>

<div class="section-head"><h2>Written lessons</h2><p>Everything you can read today.</p></div>
<ul class="lesson-list">{latest or '<li class="lesson-row planned">First lessons coming soon.</li>'}</ul>
"""
    write("index.html", page(title=SITE["name"], depth=0, body=body, side=None, active="home", wide_content=True))
    search_index.append({"t": "Home", "p": SITE["name"], "u": "index.html", "k": "Page", "x": SITE["tagline"]})


def build_phase(ph):
    depth = 2
    r = rel(depth)
    project_link = (f' <a class="milestone-link" href="{r}{u_project(ph)}">Open the project brief →</a>'
                    if ph["id"] in PROJECTS else "")
    tiles = []
    for m in ph["modules"]:
        n = len(by_module[f"{ph['id']}/{m['id']}"])
        status = f"{n} lesson{'s' if n != 1 else ''} written" if n else "Coming soon"
        tiles.append(f"""<a class="card module-tile" href="{r}{u_module(ph, m)}">
  <h3>{esc(m['title'])}{tag_html(m.get('tag'))}</h3>
  <p>{esc(', '.join(m['topics']))}</p>
  <span class="count">{status}</span>
</a>""")
        search_index.append({"t": m["title"], "p": f"Phase {ph['num']} · {ph['short']}", "u": u_module(ph, m),
                             "k": "Module", "x": " ".join(m["topics"])})
    cert = f'<p><b>Optional certification:</b> {esc(ph["cert"])}.</p>' if ph.get("cert") else ""
    n = phase_lesson_count(ph)
    idx = PHASES.index(ph)
    prev_ph = PHASES[idx - 1] if idx > 0 else None
    next_ph = PHASES[idx + 1] if idx + 1 < len(PHASES) else None
    pager = '<nav class="pager">'
    if prev_ph:
        pager += f'<a class="prev" href="{r}{u_phase(prev_ph)}"><small>← Previous phase</small>Phase {prev_ph["num"]} — {esc(prev_ph["short"])}</a>'
    if next_ph:
        pager += f'<a class="next" href="{r}{u_phase(next_ph)}"><small>Next phase →</small>Phase {next_ph["num"]} — {esc(next_ph["short"])}</a>'
    pager += "</nav>"
    body = f"""{crumbs(r, [('Home', 'index.html'), (f"Phase {ph['num']}", None)])}
<h1>Phase {ph['num']} — {esc(ph['title'])}</h1>
<p class="lead">{esc(ph['summary'])}</p>
<div class="meta"><span class="pill"><b>{len(ph['modules'])}</b> modules</span><span class="pill"><b>{n}</b> lessons written</span></div>
{progress_block(ph['id'], n)}
<div class="milestone"><strong>{esc(ph['milestone']['label'])}:</strong> {esc(ph['milestone']['text'])}{project_link}</div>
{cert}
<div class="section-head"><h2>Modules</h2></div>
<div class="grid cols-2">{''.join(tiles)}</div>
{pager}
"""
    write(u_phase(ph), page(title=f"Phase {ph['num']}: {ph['title']}", depth=depth, body=body,
                            side=sidebar(r, ph), description=ph["summary"], wide_content=True))
    search_index.append({"t": f"Phase {ph['num']} — {ph['title']}", "p": "Curriculum", "u": u_phase(ph),
                         "k": "Phase", "x": ph["summary"] + " " + ph["milestone"]["text"]})


def build_module(ph, m):
    depth = 3
    r = rel(depth)
    key = f"{ph['id']}/{m['id']}"
    lessons = by_module[key]
    covered = {t for l in lessons for t in (l["meta"].get("topics") or [])}
    rows = []
    for i, l in enumerate(lessons, 1):
        rows.append(f'<li class="lesson-row" data-lesson="{l["id"]}"><span class="n">{i}</span><span>'
                    f'<a href="{r}{u_lesson(l)}">{esc(l["title"])}</a>'
                    f'<span class="desc">{esc(l["meta"].get("summary", ""))}</span></span>'
                    f'<span class="lesson-state">{esc(l["meta"].get("time", ""))}</span></li>')
    planned = [t for t in m["topics"] if t not in covered]
    for j, t in enumerate(planned, len(lessons) + 1):
        rows.append(f'<li class="lesson-row planned"><span class="n">{j}</span><span>{esc(t)}'
                    f'<span class="desc">Planned lesson</span></span><span class="lesson-state"><span class="tag soon">Coming soon</span></span></li>')
        search_index.append({"t": t, "p": f"Planned · {m['title']} · Phase {ph['num']}", "u": u_module(ph, m),
                             "k": "Planned", "x": ""})
    mods = ph["modules"]
    i = mods.index(m)
    pager = '<nav class="pager">'
    if i > 0:
        pager += f'<a class="prev" href="{r}{u_module(ph, mods[i-1])}"><small>← Previous module</small>{esc(mods[i-1]["title"])}</a>'
    if i + 1 < len(mods):
        pager += f'<a class="next" href="{r}{u_module(ph, mods[i+1])}"><small>Next module →</small>{esc(mods[i+1]["title"])}</a>'
    pager += "</nav>"
    intro_file = CONTENT / "lessons" / ph["id"] / m["id"] / "_module.md"
    intro = render_md(intro_file.read_text(encoding="utf-8"))[0] if intro_file.exists() else ""
    module_files = []
    for l in lessons:
        for fpath in (l["meta"].get("files") or []):
            if fpath not in module_files:
                module_files.append(fpath)
    topic_chips = "".join(f'<span class="term-chip">{esc(t)}</span>' for t in m["topics"])
    body = f"""{crumbs(r, [('Home', 'index.html'), (f"Phase {ph['num']}", u_phase(ph)), (m['title'], None)])}
<span class="eyebrow">Phase {ph['num']} · {esc(ph['short'])}</span>
<h1>{esc(m['title'])}{tag_html(m.get('tag'))}</h1>
<p class="lead">{esc(ph['summary'])}</p>
{intro}
<div class="module-topics"><b>Curriculum coverage</b><div class="term-chips">{topic_chips}</div></div>
{files_box(r, module_files, key)}
<div class="section-head"><h2>Tutorials</h2><p>{len(lessons)} ready · {len(planned)} planned</p></div>
<ul class="lesson-list">{''.join(rows)}</ul>
{pager}
"""
    write(u_module(ph, m), page(title=m["title"], depth=depth, body=body, side=sidebar(r, ph, m),
                                description=f"{m['title']}: {', '.join(m['topics'])}"))


def build_lesson(l):
    depth = 3
    r = rel(depth)
    ph, m, meta = l["phase"], l["module"], l["meta"]
    body_html, toc_tokens = render_md(l["source"])
    body_html, n_quiz = mark_quizzes(body_html, l["id"])
    l["quiz_count"] = n_quiz
    terms = lesson_terms(l)
    l["terms"] = terms

    # free resources from front matter
    if (meta.get("youtube") or {}).get("url"):
        toc_tokens = list(toc_tokens) + [{"id": "video-companion", "name": "Video companion"}]

    res = meta.get("resources") or []
    res_html = ""
    if res:
        items = "".join(
            f'<li><a href="{esc(x["url"])}">{esc(x["title"])}</a>'
            f'<span class="r-meta">{esc(x.get("source", ""))}{" · " if x.get("source") and x.get("note") else ""}{esc(x.get("note", ""))}</span></li>'
            for x in res)
        res_html = f'<h2 id="free-resources">Free resources to go deeper</h2><ul class="resources">{items}</ul>'
        toc_tokens = list(toc_tokens) + [{"id": "free-resources", "name": "Free resources"}]

    # prerequisites
    pre_html = ""
    pre = meta.get("prerequisites") or []
    if pre:
        links = []
        for pid in pre:
            target = LESSON_BY_ID.get(pid)
            if target:
                links.append(f'<a href="{r}{u_lesson(target)}">{esc(target["title"])}</a>')
            else:
                links.append(esc(str(pid)))
        pre_html = f'<div class="admonition note"><p class="admonition-title">Before you start</p><p>{" · ".join(links)}</p></div>'

    pills = [f'<span class="pill">Phase <b>{ph["num"]}</b> · {esc(ph["short"])}</span>']
    if meta.get("level"):
        pills.append(f'<span class="pill">Level <b>{esc(meta["level"])}</b></span>')
    if meta.get("time"):
        pills.append(f'<span class="pill">Time <b>{esc(meta["time"])}</b></span>')

    pager = '<nav class="pager">'
    if l["prev"]:
        pager += f'<a class="prev" href="{r}{u_lesson(l["prev"])}"><small>← Previous</small>{esc(l["prev"]["title"])}</a>'
    if l["next"]:
        pager += f'<a class="next" href="{r}{u_lesson(l["next"])}"><small>Next →</small>{esc(l["next"]["title"])}</a>'
    else:
        pager += f'<a class="next" href="{r}{u_module(ph, m)}"><small>Back to module →</small>{esc(m["title"])}</a>'
    pager += "</nav>"

    edit = ""
    if SITE.get("github_repo"):
        src = l["file"].relative_to(ROOT).as_posix()
        edit = f' · <a href="{esc(SITE["github_repo"].rstrip("/"))}/edit/main/{src}">Suggest an edit</a>'
    reviewed = meta.get("reviewed", "")

    body = f"""{crumbs(r, [('Home', 'index.html'), (f"Phase {ph['num']}", u_phase(ph)), (m['title'], u_module(ph, m)), (l['title'], None)])}
<h1>{esc(l['title'])}</h1>
<p class="lead">{esc(meta.get('summary', ''))}</p>
<div class="meta">{''.join(pills)}</div>
{pre_html}
{files_box(r, meta.get('files') or [], l['id'])}
{body_html}
{youtube_box(meta)}
{terms_box(r, terms)}
{res_html}
<div class="complete-bar"><span>Finished reading and did the exercise?</span>
<button class="btn" id="completeBtn" type="button" data-id="{l['id']}">Mark lesson as complete</button></div>
{pager}
<p class="reviewed">Last reviewed: {esc(str(reviewed))}{edit}</p>
"""
    toc = [{"id": t["id"], "name": t["name"]} for t in toc_tokens]
    write(u_lesson(l), page(title=l["title"], depth=depth, body=body, side=sidebar(r, ph, m, l),
                            toc=toc, description=meta.get("summary", ""), og_type="article"),
          lastmod=str(reviewed) if reviewed else None)
    search_index.append({"t": l["title"], "p": f"Phase {ph['num']} · {m['title']}", "u": u_lesson(l), "k": "Lesson",
                         "x": (meta.get("summary", "") + " " + " ".join(str(k) for k in (meta.get("keywords") or [])) + " " +
                               strip_tags(body_html))[:1500]})


def build_project(ph):
    depth = 2
    r = rel(depth)
    meta, src = read_front_matter(PROJECTS[ph["id"]])
    body_html, toc_tokens = render_md(src)
    title = meta.get("title", f"Phase {ph['num']} Milestone Project")
    pills = [f'<span class="pill">Phase <b>{ph["num"]}</b> · {esc(ph["short"])}</span>']
    if meta.get("time"):
        pills.append(f'<span class="pill">Effort <b>{esc(meta["time"])}</b></span>')
    if meta.get("level"):
        pills.append(f'<span class="pill">Level <b>{esc(meta["level"])}</b></span>')
    body = f"""{crumbs(r, [('Home', 'index.html'), (f"Phase {ph['num']}", u_phase(ph)), ('Milestone project', None)])}
<span class="eyebrow">★ Milestone project</span>
<h1>{esc(title)}</h1>
<p class="lead">{esc(meta.get('summary', ''))}</p>
<div class="meta">{''.join(pills)}</div>
{files_box(r, meta.get('files') or [], 'project ' + ph['id'])}
{body_html}
<nav class="pager"><a class="prev" href="{r}{u_phase(ph)}"><small>← Back to phase</small>Phase {ph['num']} — {esc(ph['short'])}</a></nav>
<p class="reviewed">Last reviewed: {esc(str(meta.get('reviewed', '')))}</p>"""
    toc = [{"id": t["id"], "name": t["name"]} for t in toc_tokens]
    write(u_project(ph), page(title=title, depth=depth, body=body, side=sidebar(r, ph, "project"),
                              toc=toc, description=meta.get("summary", "")))
    search_index.append({"t": title, "p": f"Phase {ph['num']} · Milestone project", "u": u_project(ph), "k": "Project",
                         "x": (meta.get("summary", "") + " " + strip_tags(body_html))[:1500]})


def build_pages():
    folder = CONTENT / "pages"
    for f in sorted(folder.glob("*.md")):
        meta, src = read_front_matter(f)
        body_html, toc_tokens = render_md(src)
        title = meta.get("title", f.stem.replace("-", " ").title())
        body = f"""{crumbs('./', [('Home', 'index.html'), (title, None)])}
<h1>{esc(title)}</h1>
<p class="lead">{esc(meta.get('summary', ''))}</p>
{body_html}"""
        toc = [{"id": t["id"], "name": t["name"]} for t in toc_tokens]
        write(f"{f.stem}.html", page(title=title, depth=0, body=body, side=None, toc=toc,
                                     description=meta.get("summary", ""), active=meta.get("nav", "")))
        search_index.append({"t": title, "p": "Page", "u": f"{f.stem}.html", "k": "Page",
                             "x": (meta.get("summary", "") + " " + strip_tags(body_html))[:1200]})


def build_license_page():
    code = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
    content_md = (ROOT / "LICENSE-CONTENT.md").read_text(encoding="utf-8") if (ROOT / "LICENSE-CONTENT.md").exists() else ""
    if not code and not content_md:
        warnings.append("LICENSE files missing — license.html not built")
        return
    content_html, _ = render_md(re.sub(r"^# .*\n", "", content_md, count=1))
    body = f"""{crumbs('./', [('Home', 'index.html'), ('Licence', None)])}
<h1>Licence</h1>
<p class="lead">This project uses two licences: one for the lesson text, one for the code that builds the site.</p>
<h2 id="lesson-content-cc-by-nc-sa-40">Lesson content — CC BY-NC-SA 4.0</h2>
{content_html}
<h2 id="code-mit-license">Code — MIT License</h2>
<pre><code>{esc(code)}</code></pre>"""
    write("license.html", page(title="Licence", depth=0, body=body, side=None,
                               toc=[{"id": "lesson-content-cc-by-nc-sa-40", "name": "Lesson content"},
                                    {"id": "code-mit-license", "name": "Code"}],
                               description="Licences for the lesson content and the site code."))


def build_404():
    """GitHub Pages shows 404.html for unknown addresses. Links are worked out in the browser,
    because the page can be shown at any depth."""
    home = SITE.get("site_url") or ""
    html_404 = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found — {esc(SITE['name'])}</title>
<style>
:root{{--bg:#f3f1ea;--panel:#fbfaf6;--text:#24312c;--muted:#5f6d66;--accent:#3f7d6a;--line:rgba(36,49,44,.12)}}
@media (prefers-color-scheme:dark){{:root{{--bg:#131b19;--panel:#1a2421;--text:#e2e9e4;--muted:#9caca4;--accent:#7cc0a8;--line:rgba(255,255,255,.08)}}}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;padding:16px}}
.box{{max-width:460px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:28px}}
h1{{margin:0 0 8px}} p{{color:var(--muted)}} a{{color:var(--accent);font-weight:600}}
</style></head>
<body><div class="box"><h1>Page not found</h1>
<p>This page does not exist (yet). Lessons are added phase by phase, so it may be coming soon.</p>
<p><a id="home" href="{esc(home) or 'index.html'}">Go to the home page →</a></p></div>
<script>(function(){{var h={json.dumps(home)};if(!h){{var seg=location.pathname.split('/').filter(Boolean);
h=(location.hostname.endsWith('github.io')&&seg.length)?'/'+seg[0]+'/':'/';}}
document.getElementById('home').href=h;}})();</script></body></html>
"""
    write("404.html", html_404)


def build_downloads_page():
    """Practice files page (grouped) + one zip bundle with every file."""
    used = {}
    for l in LESSONS:
        for fpath in (l["meta"].get("files") or []):
            used.setdefault(fpath, []).append(l)
    on_disk = sorted(p.relative_to(DL).as_posix() for p in DL.rglob("*") if p.is_file() and p.name != "files.yml")
    for pth in on_disk:
        if pth not in FILES:
            warnings.append(f"content/downloads/{pth} is not listed in files.yml")
    groups = FILE_GROUPS or sorted({f.get("group", "Other") for f in FILES.values()})
    sections = []
    for g in groups:
        rows = []
        for pth, info in FILES.items():
            if info.get("group", "Other") != g:
                continue
            lessons = used.get(pth, [])
            uses = ", ".join(f'<a href="{u_lesson(x)}">{esc(x["title"].split(":")[0])}</a>' for x in lessons[:4])
            if len(lessons) > 4:
                uses += f" +{len(lessons) - 4} more"
            rows.append(f'<tr><td><a href="downloads/{esc(pth)}" download><code>{esc(pth)}</code></a></td>'
                        f'<td>{esc(info.get("description", ""))}</td><td>{file_size(pth)}</td>'
                        f'<td>{uses or esc(info.get("used_in", ""))}</td></tr>')
        if rows:
            sections.append(f'<h2 id="{slugify(g)}">{esc(g)}</h2><table><thead><tr><th>File</th><th>What it is</th>'
                            f'<th>Size</th><th>Used in</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')
    # deterministic bundle (fixed timestamps, sorted names) so CI's "docs up to date" check stays stable
    bundle_path = OUT / "downloads" / BUNDLE
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for pth in on_disk:
            zi = zipfile.ZipInfo(f"practice-files/{pth}", date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, (DL / pth).read_bytes())
    body = f"""{crumbs('./', [('Home', 'index.html'), ('Practice files', None)])}
<h1>Practice files</h1>
<p class="lead">Every dataset, workbook, script, template and answer key used in the lessons. All files use the same small sales data, so results match across SQL, Excel, Power BI and Python.</p>
<div class="files-box"><div class="files-head"><b>Download everything at once</b></div>
<ul><li><a href="downloads/{BUNDLE}" download>{BUNDLE}</a><span class="f-desc">All {len(on_disk)} practice files in one zip · {human_size(bundle_path.stat().st_size)}</span></li></ul></div>
<div class="admonition tip"><p class="admonition-title">How to use them</p>
<p>Save the files in one folder (for example <code>C:\\Practice\\</code> or <code>~/practice/</code>). Lessons tell you which file to open. Files called <em>solutions</em> contain worked answers: try the exercise first. Each lesson also has its own download box at the top.</p></div>
{"".join(sections)}"""
    toc = [{"id": slugify(g), "name": g} for g in groups if any(i.get("group", "Other") == g for i in FILES.values())]
    write("practice-files.html", page(title="Practice files", depth=0, body=body, side=None, toc=toc,
                                      active="files", description="Download the practice datasets, workbooks and scripts."))
    search_index.append({"t": "Practice files", "p": "Downloads", "u": "practice-files.html", "k": "Page",
                         "x": "download practice files dataset workbook xlsx csv sql zip " + " ".join(FILES)})


def build_glossary():
    used: dict[str, list] = {}
    for l in LESSONS:
        for t in l.get("terms", []):
            used.setdefault(t["id"], []).append(l)
    letters = sorted({(t["term"].lstrip(".")[:1] or "#").upper() for t in GLOSSARY})
    entries, cur = [], None
    for t in GLOSSARY:
        letter = (t["term"].lstrip(".")[:1] or "#").upper()
        if letter != cur:
            if cur is not None:
                entries.append("</dl></section>")
            entries.append(f'<section class="g-letter" id="letter-{letter.lower()}"><h2>{esc(letter)}</h2><dl>')
            cur = letter
        url, label = gloss_target(t)
        learn = f'<a href="{url}">{esc(label)}</a>' if url else ""
        others = [x for x in used.get(t["id"], []) if u_lesson(x) != url]
        also = ", ".join(f'<a href="{u_lesson(x)}">{esc(x["title"].split(":")[0])}</a>' for x in others[:5])
        if len(others) > 5:
            also += f" +{len(others) - 5} more"
        aka = [a for a in (t.get("aka") or []) if _norm(a) != _norm(t["term"])]
        aka_html = f'<span class="g-aka">Also: {esc(", ".join(aka[:4]))}</span>' if aka else ""
        search_text = " ".join([t["term"], *aka, t["def"], t.get("cat", "")]).lower()
        entries.append(
            f'<div class="g-entry" id="{t["id"]}" data-cat="{esc(t.get("cat", ""))}" data-text="{esc(search_text)}">'
            f'<dt><a class="g-anchor" href="#{t["id"]}">{esc(t["term"])}</a><span class="g-cat">{esc(t.get("cat", ""))}</span></dt>'
            f'<dd><p>{esc(t["def"])}</p>{aka_html}'
            f'<p class="g-links">{"<b>Learn it:</b> " + learn if learn else ""}'
            f'{" · <b>Also used in:</b> " + also if also else ""}</p></dd></div>')
        search_index.append({"t": t["term"], "p": f"Glossary · {t.get('cat', '')}", "u": f"glossary.html#{t['id']}",
                             "k": "Term", "x": " ".join(aka) + " " + t["def"]})
    if cur is not None:
        entries.append("</dl></section>")
    letter_nav = "".join(f'<a href="#letter-{x.lower()}">{esc(x)}</a>' for x in letters)
    cats = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in GLOSS_CATS)
    body = f"""{crumbs('./', [('Home', 'index.html'), ('Glossary', None)])}
<h1>Glossary</h1>
<p class="lead">{len(GLOSSARY)} key terms in plain English, from SQL and DAX to RAG and AI agents. Each term links to the lesson where it is taught, and lessons link back here under <b>Key terms</b>.</p>
<div class="g-tools">
  <input type="search" id="glossFilter" placeholder="Filter terms, e.g. join, DAX, RAG" aria-label="Filter glossary terms" autocomplete="off">
  <select id="glossCat" aria-label="Filter by category"><option value="">All categories</option>{cats}</select>
  <span id="glossCount" class="g-count" aria-live="polite"></span>
</div>
<nav class="g-az" aria-label="Jump to letter">{letter_nav}</nav>
{"".join(entries)}
<p class="g-empty" id="glossEmpty" hidden>No terms match. Try a shorter word, or <a href="about.html">suggest a new term</a>.</p>"""
    write("glossary.html", page(title="Glossary", depth=0, body=body, side=None, active="glossary",
                                description=f"{len(GLOSSARY)} data, BI, engineering and AI terms explained in plain English."))
    search_index.append({"t": "Glossary", "p": "Page", "u": "glossary.html", "k": "Page",
                         "x": "glossary terms definitions dictionary jargon"})


def build_sitemap():
    """sitemap.xml + robots.txt. A sitemap needs absolute URLs, so it is only written when site_url is set."""
    robots = "User-agent: *\nAllow: /\n"
    if SITE_URL:
        rows = []
        for path, lastmod in sorted(SITEMAP):
            loc = SITE_URL + path.removesuffix("index.html")
            rows.append(f"  <url><loc>{html.escape(loc)}</loc><lastmod>{lastmod}</lastmod></url>")
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n",
            encoding="utf-8")
        robots += f"Sitemap: {SITE_URL}sitemap.xml\n"
    else:
        notes.append("site_url is empty in site.yml, so sitemap.xml and absolute share links (og:url, og:image) "
                     "were skipped. Set it once the site is live.")
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")


def check_links():
    """Report internal links that point at files that do not exist."""
    bad = []
    for p in OUT.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        for href in re.findall(r'(?:href|src)="([^"#?]+)', text):
            if href.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            if not (p.parent / href).resolve().exists():
                bad.append(f"{p.relative_to(OUT)} -> {href}")
    return bad


# ------------------------------------------------------------------ main
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    if (CONTENT / "downloads").is_dir():
        shutil.copytree(CONTENT / "downloads", OUT / "downloads", ignore=shutil.ignore_patterns("files.yml"))
    if (CONTENT / "images").is_dir():                       # charts and screenshots used in lessons
        shutil.copytree(CONTENT / "images", OUT / "images")
    if (CONTENT / "curriculum-map.html").exists():
        shutil.copy(CONTENT / "curriculum-map.html", OUT / "curriculum.html")
        SITEMAP.append(("curriculum.html", RELEASE_DATE))
    else:
        warnings.append("content/curriculum-map.html missing — the Curriculum link will be broken")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: serve files as-is

    build_home()
    for ph in PHASES:
        build_phase(ph)
        for m in ph["modules"]:
            build_module(ph, m)
    for l in LESSONS:
        build_lesson(l)
    for ph in PHASES:
        if ph["id"] in PROJECTS:
            build_project(ph)
    build_pages()
    build_license_page()
    build_404()
    build_downloads_page()
    build_glossary()
    build_sitemap()

    (OUT / "search-index.js").write_text(
        "window.SEARCH_INDEX=" + json.dumps(search_index, ensure_ascii=False, separators=(",", ":")) + ";",
        encoding="utf-8")

    bad = check_links()
    pages = len(list(OUT.rglob("*.html")))
    modules = sum(len(ph["modules"]) for ph in PHASES)
    print(f"Built {pages} pages: {len(PHASES)} phases, {modules} modules, {len(LESSONS)} lessons -> {OUT.relative_to(ROOT)}/")
    for w in warnings:
        print("WARNING:", w)
    for n in notes:
        print("NOTE:", n)
    if SITE_URL:
        print(f"Sitemap: {len(SITEMAP)} URLs")
    if bad:
        print(f"BROKEN LINKS ({len(bad)}):")
        for b in bad:
            print("  ", b)
        sys.exit(1)
    print("Internal links: all OK")


if __name__ == "__main__":
    main()
