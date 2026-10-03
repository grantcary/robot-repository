# Robot Repository

Archiving robotic history, mostly between the 90s and 2000s: [robotrepository.com](https://www.robotrepository.com)

The site is a folder of markdown files built into plain HTML + CSS with
[MkDocs](https://www.mkdocs.org). The built site has **no JavaScript**.

## Writing

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # once
.venv/bin/mkdocs serve                                               # http://127.0.0.1:8000, reloads on save
```

Every page is a file in `docs/`, and its path is its URL (`docs/asimo/2000.md` →
`/asimo/2000.html`). Push to `main` and GitHub Actions builds and publishes it.

### Article syntax

````markdown
---
title: "ASIMO 2000"          # browser tab: "robot repository - ASIMO 2000"
series: asimo                # which tab row this page belongs to (see "Adding things" below)
robot:                       # optional: lists the page in the Robots directory
  name: "ASIMO 2000"
  thumbnail: https://i.imgur.com/EHNFHNu.jpeg
  letter: A                  # optional: defaults to the first letter of the name
toc: false                   # optional: hide the Contents box
---

## 2000 (Version 1)

![](https://i.imgur.com/cWxMXts.jpeg)

![](https://i.imgur.com/aaa.jpeg) ![](https://i.imgur.com/bbb.jpeg)

ASIMO is an acronym.[^1] It could also walk.[^2]

https://www.youtube.com/watch?v=82JFCciO3E4

https://youtu.be/JdoHz4D3y8Q?t=398 4:3

https://archive.org/details/asimo-2005-media-kit-videos/01.dv

### Hardware

#### A sub-section

### References

1. [First source](https://example.com/one)
2. [Second source](https://example.com/two)
````

- **Headings:** `##` for the article title, `###` for sections, `####` for sub-sections.
  A "Contents" box is generated from them.
- **Citations:** `[^3]` shows `[3]` and links to item 3 of the list under the `### References` heading.
  The number is the *position in that list*, and you number them yourself, same as before.
- **Videos:** any YouTube link (`watch`, `youtu.be`, `shorts`, with `t=`/`start=` timestamps),
  any `archive.org/details/…` or `archive.org/embed/…` item, or a direct `.mp4`/`.webm` link
  (including `web.archive.org/web/…/clip.mp4` captures). The URL must be alone on its own line,
  an optional ratio like `4:3` or `9:16` can follow it. A URL inside a sentence stays a normal link.
  Anything else (other iframes, etc.) can still be pasted as raw HTML.
- **Links to other pages:** `[ASIMO 2005](asimo/2005.md)`, relative to the current file.
- Standard markdown otherwise: `*italic*`, `**bold**`, lists, tables.

### Adding things

| I want to… | Do this |
| --- | --- |
| add a new year/model to an existing series | create the `.md`, then add one line to that series' `pages:` in `mkdocs.yml` |
| add a robot to the **Robots** directory | give the page a `robot:` block (above). It appears automatically, ordered by series, grouped by letter |
| add a whole new series | add an entry under `extra.series` in `mkdocs.yml` (`title`, `image` for the Articles page, `pages`). It appears on the Articles page automatically |
| change the home page | edit `docs/index.md` (`{{robots\|asimo/2000.md\|…}}` picks the highlighted robots) |
| add a top-level page | create it, then add it to `nav:` in `mkdocs.yml` |

## How it's put together

| Path | What |
| --- | --- |
| `docs/` | all content (markdown, images, `CNAME`, `favicon.ico`) |
| `mkdocs.yml` | site settings, top navigation, and the series (tab rows) |
| `theme/` | the look: `main.html` (page template) and `css/wiki.css` |
| `hooks/robotrepo.py` | video embeds, citations, image layout, robot/series directories |
| `.github/workflows/deploy.yml` | builds with `mkdocs build --strict` and publishes to GitHub Pages |
| `tools/verify_migration.py` | checks the markdown site says exactly what the old HTML site said |

Hosting: in the repo's **Settings → Pages**, set *Source* to **GitHub Actions**.

`mkdocs build --strict` fails on broken internal links, so a typo in a link is
caught before it goes live.

## Known quirks carried over from the old site

These were in the original HTML and are kept exactly as they were, because the
migration was not allowed to change article content:

- `<title>` of every Atlas page reads "Atlas - PetProto", and `sdr-3x` reads "Sony SDR-3". Change `title:` in each page's front matter.
- `qrio/sdr-4xii.md`: the reference list is displayed as 1–2 while the in-text markers say [3] and [4]. See the comment in the file for how to fix it.
- `p-series/p4.md`: reference 1 links to `web.archive.org/…` without `https://`, so it is a broken relative link.
- The P1–P3 tabs link to the home page until those pages exist.
- `atlas/petproto.md` is not linked from the Atlas tabs (it has its own tab row, `atlas-petproto` in `mkdocs.yml`).
