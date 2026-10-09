#!/usr/bin/env python3
"""Static consistency audit for the Saiful The Techie Data, AI & Automation Path.

Runs without the site renderer. It checks curriculum/source integrity and, when docs/
exists, detects stale learner-facing pages such as written lessons that were not built.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "curriculum.yml"
LESSONS = ROOT / "content" / "lessons"
DOWNLOADS = ROOT / "content" / "downloads"
DOCS = ROOT / "docs"
SITE = ROOT / "site.yml"


def frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    _, head, body = text.split("---", 2)
    return yaml.safe_load(head) or {}, body.lstrip("\n")


def lesson_id(path: Path) -> str:
    rel = path.relative_to(LESSONS)
    return "/".join(rel.with_suffix("").parts)


def generated_lesson_path(path: Path) -> Path:
    rel = path.relative_to(LESSONS)
    return DOCS / "learn" / rel.with_suffix(".html")


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []
    data = yaml.safe_load(CURRICULUM.read_text(encoding="utf-8"))
    site = yaml.safe_load(SITE.read_text(encoding="utf-8"))
    phases = data["phases"]

    module_by_key: dict[str, dict[str, Any]] = {}
    phase_by_id = {p["id"]: p for p in phases}
    topic_sets: dict[str, set[str]] = {}
    for ph in phases:
        for mod in ph["modules"]:
            key = f"{ph['id']}/{mod['id']}"
            module_by_key[key] = mod
            topic_sets[key] = set(mod["topics"])

    lesson_paths = sorted(p for p in LESSONS.glob("phase-*/*/*.md") if p.name != "_module.md")
    metas: dict[str, dict[str, Any]] = {}
    paths_by_id: dict[str, Path] = {}
    module_lessons: dict[str, list[str]] = defaultdict(list)
    topic_owner: dict[tuple[str, str], list[str]] = defaultdict(list)
    orders: dict[str, list[int]] = defaultdict(list)

    for path in lesson_paths:
        lid = lesson_id(path)
        meta, _ = frontmatter(path)
        metas[lid] = meta
        paths_by_id[lid] = path
        parts = lid.split("/")
        if len(parts) != 3:
            errors.append(f"Unexpected lesson path: {lid}")
            continue
        key = "/".join(parts[:2])
        module_lessons[key].append(lid)
        if key not in module_by_key:
            errors.append(f"{lid}: module not found in curriculum.yml")
            continue
        if "order" in meta:
            orders[key].append(int(meta["order"]))
        for topic in meta.get("topics", []) or []:
            if topic not in topic_sets[key]:
                errors.append(f"{lid}: topic {topic!r} is not an exact curriculum topic for {key}")
            topic_owner[(key, topic)].append(lid)
        if not (meta.get("resources") or []):
            errors.append(f"{lid}: no curated resources")
        yt = meta.get("youtube")
        if yt:
            required = ["title", "creator", "url", "video_id", "reviewed", "why_recommended"]
            missing = [k for k in required if not yt.get(k)]
            if missing:
                errors.append(f"{lid}: YouTube metadata missing {', '.join(missing)}")
            url = str(yt.get("url", ""))
            if "youtube.com/watch" not in url and "youtu.be/" not in url:
                errors.append(f"{lid}: YouTube URL is not a normal YouTube watch/share URL")

    lesson_ids = set(metas)
    for lid, meta in metas.items():
        for prereq in meta.get("prerequisites", []) or []:
            if prereq not in lesson_ids:
                errors.append(f"{lid}: prerequisite does not resolve: {prereq}")
        for f in meta.get("files", []) or []:
            if not (DOWNLOADS / f).exists():
                errors.append(f"{lid}: referenced practice file missing: {f}")

    for key, vals in orders.items():
        dup = [v for v, c in Counter(vals).items() if c > 1]
        if dup:
            errors.append(f"{key}: duplicate lesson order values: {dup}")

    for (key, topic), owners in topic_owner.items():
        if len(owners) > 1:
            errors.append(f"{key}: topic {topic!r} covered by multiple lessons: {owners}")

    for key, lids in module_lessons.items():
        if lids:
            phase_id, module_id = key.split("/")
            intro = LESSONS / phase_id / module_id / "_module.md"
            if not intro.exists():
                errors.append(f"{key}: written module has no _module.md introduction")

    total_topics = 0
    covered_total = 0
    phase_rows: list[tuple[int, str, int, int, int]] = []
    for ph in phases:
        p_total = sum(len(m["topics"]) for m in ph["modules"])
        p_covered = 0
        p_lessons = 0
        for mod in ph["modules"]:
            key = f"{ph['id']}/{mod['id']}"
            p_lessons += len(module_lessons.get(key, []))
            for topic in mod["topics"]:
                if (key, topic) in topic_owner:
                    p_covered += 1
        total_topics += p_total
        covered_total += p_covered
        phase_rows.append((ph["num"], ph["short"], p_covered, p_total, p_lessons))

    # Learner-facing generated-site checks: these catch the stale-docs defect that
    # v0.9.1 was specifically created to prevent.
    projection_by_phase = {
        "phase-3": "M8 · v0.9.x",
        "phase-5": "M9 · v1.0",
        "phase-6": "M10 · v1.1",
        "phase-4": "M11 · v1.2",
        "phase-7": "M12 · v1.3",
        "phase-8": "M13 · v1.4",
        "phase-9": "M13 · v1.4",
    }
    prompt_pages = 0
    video_pages = 0
    if DOCS.exists():
        for path in lesson_paths:
            out = generated_lesson_path(path)
            if not out.exists():
                errors.append(f"Generated tutorial missing for written source: {lesson_id(path)}")
                continue
            html = out.read_text(encoding="utf-8")
            if 'id="ai-mentor-prompt"' not in html:
                errors.append(f"Generated tutorial has no AI Mentor Prompt: {lesson_id(path)}")
            else:
                prompt_pages += 1
            if "youtube-nocookie.com/embed/" in html:
                video_pages += 1
        # Every uncovered topic in a roadmap-mapped phase must show that phase's projected milestone/version
        # on its generated module page. This is intentionally a topic projection, not a one-topic/one-lesson promise.
        projected_topics = 0
        for ph in phases:
            label = projection_by_phase.get(ph["id"])
            if not label:
                continue
            for mod in ph["modules"]:
                key = f"{ph['id']}/{mod['id']}"
                uncovered = [t for t in mod["topics"] if (key, t) not in topic_owner]
                if not uncovered:
                    continue
                mod_html = DOCS / "learn" / ph["id"] / mod["id"] / "index.html"
                if not mod_html.exists():
                    errors.append(f"Generated module page missing for projected topics: {key}")
                    continue
                html = mod_html.read_text(encoding="utf-8")
                if label not in html:
                    errors.append(f"{key}: projected topics do not show expected milestone/version {label}")
                projected_topics += len(uncovered)
        all_html = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in DOCS.rglob("*.html"))
        if re.search(r"\bcoming soon\b", all_html, flags=re.I):
            errors.append("Generated site still contains an ambiguous 'Coming soon' label")
        notes.append(f"Generated written tutorials with AI Mentor Prompt: {prompt_pages}/{len(lesson_paths)}")
        notes.append(f"Generated tutorials with reviewed YouTube frame: {video_pages}")
        notes.append(f"Uncovered curriculum topics with roadmap projection: {projected_topics}")
    else:
        notes.append("docs/ not present; learner-facing stale-build checks skipped")

    # Current checkpoint expectations. These are intentionally narrow: future-phase
    # uncovered topics are planned work, not audit failures.
    if str(site.get("version")) != "v0.9.1":
        errors.append(f"site.yml version is {site.get('version')!r}; expected v0.9.1 for this correction release")
    p3 = next(row for row in phase_rows if row[0] == 3)
    if (p3[2], p3[3], p3[4]) != (40, 55, 21):
        errors.append(f"Phase 3 checkpoint drift: got {p3[2]}/{p3[3]} topics and {p3[4]} lessons; expected 40/55 and 21")

    print("Saiful The Techie — Data, AI & Automation Path audit")
    print(f"Site version: {site.get('version')}")
    print(f"Written lessons: {len(lesson_paths)}")
    print(f"Curriculum coverage: {covered_total}/{total_topics} topics")
    print("Phase coverage:")
    for num, short, covered, total, lessons in phase_rows:
        print(f"  Phase {num}: {covered:>2}/{total:<2} topics | {lessons:>2} lessons | {short}")
    for note in notes:
        print(note)
    if errors:
        print(f"AUDIT: FAIL ({len(errors)} issue(s))")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
