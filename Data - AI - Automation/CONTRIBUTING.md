# Contributing

Thank you for helping improve the lessons.

## Report a mistake or suggest a lesson

Open an issue and use the **Content error** or **Lesson request** template.

## Add or edit a lesson

1. Install the build tools once: `pip install -r requirements.txt`
2. Copy `content/_templates/lesson-template.md` into `content/lessons/<phase-id>/<module-id>/` with a name like `03-case-expressions.md`.
3. Fill in the front matter (title, order, summary, level, time, `topics`).
   - `topics` must use the exact topic text from `curriculum.yml`.
4. Write the lesson. Follow the **Definition of done** in [ROADMAP.md](ROADMAP.md).
   - **Quiz:** each question is a `<div class="quiz-q" markdown="1">` with a numbered option list and an answer that starts with the bold letter, e.g. `**B.**` or `**B — because…**`. The build reads that letter to score the quiz, and warns if it can't.
   - **Key terms:** words in your `keywords` that match a glossary term (or one of its `aka` names) appear automatically under "Key terms". To force a term, add `terms: [Star schema]` to the front matter.
   - **Practice files:** list them in `files:` and catalogue new ones in `content/downloads/files.yml`.
5. Run `python build.py` and fix any warnings or broken links.
6. Open `docs/index.html` and check the page in light and dark mode.
7. Commit **both** your Markdown file **and** the rebuilt `docs/` folder, then open a pull request.

## Add or edit a glossary term

Edit `content/glossary.yml`: `term`, optional `aka` (other names), `cat` (one of the listed categories), `def` (1–2 plain sentences) and `see` (the lesson, module or phase where it is taught). Run `python build.py`: the term appears on the Glossary page, in search and under "Key terms" in matching lessons.

## Rules

- Write original text. Never copy text from other tutorial sites.
- Run every example. Paste real results only.
- Link only to free resources, and check that each link works.
- Never edit files in `docs/` by hand. They are rebuilt every time.
