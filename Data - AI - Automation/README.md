# Data, AI & Automation Path

**Version v0.7** · [Roadmap](ROADMAP.md) · [Changelog](CHANGELOG.md)

A free, text-first tutorial website for the **Integrated Data, AI & Automation Engineering Curriculum**. It runs from basics to job-ready across 10 phases, from Excel and SQL to RAG, AI agents and LLMOps.

- **Works offline:** open `index.html` (or `docs/index.html`) in any browser.
- **GitHub Pages ready:** the finished website is in `docs/`.
- **Features:** toggleable curriculum menu, light/dark mode, offline search, progress tracking, scored quizzes, a glossary linked from every lesson, copyable code and hand-picked free resources.
- **Practice files:** every lesson lists the data, workbooks, scripts and answer keys it uses. The **Practice files** page lists them all, with a one-click bundle.

## Quick start (no install)

Unzip the package, then double-click **`index.html`** in the main folder.

| Key | Action |
|---|---|
| ☰ button or `M` | Show / hide the curriculum menu (it stays open as you move between lessons) |
| `/` | Search |
| `Esc` | Close search results |

---

## Go live on GitHub (first time, about 10 minutes)

You need a free GitHub account. Choose **Option A** (no command line) or **Option B** (command line).

### Option A: GitHub Desktop (no command line)

1. Install **GitHub Desktop** from <https://desktop.github.com> and sign in.
2. Unzip the package. Rename the folder from `data-ai-automation-path-v0.7` to **`data-ai-automation-path`**.
3. In GitHub Desktop, choose **File → Add local repository**, pick the folder, and click **create a repository** when asked.
4. Click **Publish repository**.
   - Name: `data-ai-automation-path`
   - **Untick "Keep this code private"**, because GitHub Pages is free for public repositories.
5. Continue with **Turn on GitHub Pages** below.

### Option B: command line

First create an **empty public** repository named `data-ai-automation-path` on github.com, with no README and no licence. Then run:

```bash
cd data-ai-automation-path        # the unzipped folder, renamed without the version
git init
git add .
git commit -m "Release v0.7: Phase 2 Data Science"
git branch -M main
git remote add origin https://github.com/<your-username>/data-ai-automation-path.git
git push -u origin main
git tag v0.7 && git push origin v0.7
```

### Turn on GitHub Pages

1. On your repository page, open **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Choose branch **`main`** and folder **`/docs`**, then click **Save**.
4. After 1–2 minutes the site is live at `https://<your-username>.github.io/data-ai-automation-path/`.

### Finish (one time)

In `site.yml`, set these two lines, then rebuild and push (see *Edit or add content* below):

```yaml
site_url: "https://<your-username>.github.io/data-ai-automation-path/"
github_repo: "https://github.com/<your-username>/data-ai-automation-path"
```

This makes the 404 page link home correctly, adds a **Suggest an edit** link to every lesson, and switches on the search and sharing features:

- `sitemap.xml` (every page, with last-reviewed dates) and a `Sitemap:` line in `robots.txt`.
- Canonical links and absolute `og:url` / `og:image` tags, so LinkedIn, WhatsApp, Facebook and X show a preview card with the image `assets/og-image.png`.

The build prints `Sitemap: N URLs` when this is on. A GitHub Pages *project* site lives in a sub-folder, so search engines don't read its `robots.txt`: submit `https://<your-username>.github.io/data-ai-automation-path/sitemap.xml` once in [Google Search Console](https://search.google.com/search-console) (and Bing Webmaster Tools) instead.

### Check the live site

- [ ] The home page opens, and the version **v0.7** shows under the site name.
- [ ] The ☰ menu, search, dark mode and a lesson page all work.
- [ ] A made-up address (e.g. `/nothing.html`) shows the "Page not found" page.
- [ ] The **Actions** tab shows a green **Build check**.
- [ ] `…/sitemap.xml` opens, and pasting a lesson link into LinkedIn's [Post Inspector](https://www.linkedin.com/post-inspector/) shows the preview card.
- [ ] In **Actions → External link check**, click **Run workflow** once. Broken links (if any) appear in an issue labelled `broken-links`.

---

## Updating to a new version

Each release comes as a zip named `data-ai-automation-path-vX.Y`.

1. Unzip it.
2. Copy **everything inside** the folder into your existing `data-ai-automation-path` repository folder, replacing the old files. Keep the hidden `.git` folder.
3. Commit with the message `Release vX.Y`, then push. With the command line, also run `git tag vX.Y && git push origin vX.Y`.
4. GitHub Pages updates on its own within a minute or two.

---

## Edit or add content

```bash
pip install -r requirements.txt
python build.py          # rebuilds docs/ and checks internal links
```

| Edit this | To change |
|---|---|
| `site.yml` | Site name, **version**, author, live address |
| `curriculum.yml` | Phases, modules, planned topics, role tracks |
| `content/lessons/<phase>/<module>/*.md` | Lessons (start from `content/_templates/lesson-template.md`) |
| `content/lessons/<phase>/<module>/_module.md` | Optional module introduction |
| `content/pages/*.md` | About, How to learn and other pages |
| `content/projects/<phase-id>.md` | Optional milestone project brief for a phase |
| `content/downloads/` | Practice files (CSV, SQL, Excel, zips …) |
| `content/glossary.yml` | Glossary terms (shown on the Glossary page, in search and as "Key terms" in lessons) |
| `content/downloads/files.yml` | Practice-file catalogue: group and description of every file |
| `examples/` | Source of the Phase 0 and Phase 2 code zips and lesson charts (rebuild with `python tools/package_examples.py`) |
| `tools/` | `make_practice_files.py` (Excel workbooks), `make_phase2_data.py` (Phase 2 datasets, fixed seed), `package_examples.py` (example zips + charts), `make_og_image.py` (share image, needs Pillow) |
| `content/curriculum-map.html` | The one-page curriculum map |
| `assets/style.css`, `assets/app.js` | Design and behaviour |

**Never edit `docs/` by hand.** It is deleted and rebuilt on every build. Always commit the rebuilt `docs/` with your changes. The **Build check** workflow fails if you forget.

## Repository structure

```
index.html            opens the site offline (redirects to docs/)
build.py              generator: Markdown -> static HTML
site.yml              site settings (name, version, links)
curriculum.yml        the curriculum map (phases, modules, topics)
content/              lessons, pages, downloads, templates, project briefs
examples/             Phase 0 and Phase 2 example projects (zipped into content/downloads/)
tools/                scripts that regenerate practice files
assets/               CSS + JS
docs/                 generated website (served by GitHub Pages)
.github/              CI build check, weekly link check, issue templates
ROADMAP.md            development milestones
CHANGELOG.md          what changed in each version
CONTRIBUTING.md       how to add or fix a lesson
LICENSE               MIT, for the code
LICENSE-CONTENT.md    CC BY-NC-SA 4.0, for the lesson content
```

## Licence

- **Lesson content** (`content/` and the generated lesson pages): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md). Free to share and adapt with credit, non-commercially, under the same licence.
- **Code** (`build.py`, `assets/`, workflows): [MIT](LICENSE).
