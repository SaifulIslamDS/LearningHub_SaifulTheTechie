#!/usr/bin/env python3
"""
Create assets/og-image.png — the 1200×630 preview image shown when a page is
shared on LinkedIn, Facebook, X, WhatsApp, Slack and others.

    pip install pillow
    python tools/make_og_image.py

Reads the site name, brand and tagline from site.yml. Run it again after
changing those (the build itself does not need Pillow).
"""
from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SITE = yaml.safe_load((ROOT / "site.yml").read_text(encoding="utf-8"))
W, H = 1200, 630
BG, PANEL, ACCENT, TEXT, MUTED = "#06111f", "#0b1c31", "#27d3ff", "#f5f9ff", "#a8bdd4"

FONT_DIRS = [Path("/usr/share/fonts"), Path("/Library/Fonts"), Path("C:/Windows/Fonts")]


def font(names: list[str], size: int) -> ImageFont.FreeTypeFont:
    for d in FONT_DIRS:
        for n in names:
            hits = list(d.rglob(n)) if d.exists() else []
            if hits:
                return ImageFont.truetype(str(hits[0]), size)
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    bold = ["Inter-Bold.otf", "DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf"]
    regular = ["Inter-Regular.otf", "DejaVuSans.ttf", "arial.ttf", "Arial.ttf"]

    d.rounded_rectangle((48, 48, W - 48, H - 48), radius=36, fill=PANEL, outline="#173654", width=2)
    # Use the approved text-wordmark fallback when the exact circular logo binary is unavailable.
    d.text((104, 106), SITE.get("brand", "Saiful The Techie"), font=font(bold, 34), fill=ACCENT)
    d.text((104, 152), SITE["name"], font=font(bold, 46), fill=TEXT)
    d.text((106, 210), "Deep tutorials · verified examples · hands-on builds", font=font(regular, 24), fill=MUTED)

    y = 286
    for line in wrap(d, SITE["tagline"], font(bold, 44), W - 220)[:3]:
        d.text((104, y), line, font=font(bold, 44), fill=TEXT)
        y += 58

    chips = ["SQL", "Excel", "Power BI", "Python", "Data Engineering", "RAG", "AI Agents"]
    x, y = 104, H - 150
    fc = font(regular, 24)
    for c in chips:
        w = d.textlength(c, font=fc) + 36
        if x + w > W - 104:
            break
        d.rounded_rectangle((x, y, x + w, y + 46), radius=23, fill="#102b47")
        d.text((x + w / 2, y + 23), c, font=fc, fill=ACCENT, anchor="mm")
        x += w + 12

    out = ROOT / "assets" / "og-image.png"
    img.save(out, optimize=True)
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
