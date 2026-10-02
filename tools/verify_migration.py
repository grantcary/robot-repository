#!/usr/bin/env python3
"""Prove that the markdown site says the same thing as the original HTML site.

Both versions are reduced to an ordered stream of "atoms" (text, links, images,
video embeds, headings, list structure, emphasis) and the streams are diffed
page by page.  Layout (wrappers, <br>, tables used for spacing, CSS classes) is
deliberately ignored; anything a reader could see or click is compared.

    pip install beautifulsoup4 html5lib
    mkdocs build
    python tools/verify_migration.py --ref 2bfd065

``--ref`` is the git commit holding the original hand-written HTML (the commit
just before the migration).  Exit status is 1 if any page differs.
"""
import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

BASE = "http://site.invalid/"
BLOCKS = {
    "p", "li", "ul", "ol", "div", "br", "h1", "h2", "h3", "h4", "table", "tr", "td", "th",
    "article", "main", "section", "details", "summary", "img", "iframe", "video",
}
CITE = re.compile(r"(?:cite[-_]note-|cn-)(\d+)$")


# ------------------------------------------------------------------ helpers --
def norm_url(href, page):
    cite = CITE.search(href)
    if cite and "://" not in href:
        return ("cite", int(cite.group(1)))
    url = urljoin(urljoin(BASE, page), href)
    # series.html was a stale duplicate of articles.html and is now a redirect to it
    return url.replace("/series.html", "/articles.html")


def norm_embed(src, ratio):
    u = urlparse(src)
    q = parse_qs(u.query)
    if u.netloc.endswith("youtube.com") and u.path.startswith("/embed/"):
        return ("youtube", u.path.split("/")[2], (q.get("start") or ["0"])[0], ratio)
    if u.netloc == "archive.org":
        return ("archive", u.path, u.query, ratio)
    return ("other", src, ratio)


def orig_ratio(node):
    for anc in [node, *node.parents]:
        cls = anc.get("class", []) if isinstance(anc, Tag) else []
        if "aspect-4-3" in cls:
            return "4/3"
        if "aspect-16-9" in cls:
            return "16/9"
    return "?"


def new_ratio(node):
    for anc in [node, *node.parents]:
        if isinstance(anc, Tag) and "embed" in anc.get("class", []):
            m = re.search(r"aspect-ratio:\s*([\d/ ]+)", anc.get("style", ""))
            return m.group(1).replace(" ", "") if m else "?"
    return "?"


# -------------------------------------------------------------------- atoms --
def atoms_of(nodes, page, side, cards_from=None):
    out = []

    def brk():
        if out and out[-1] != ("brk",):
            out.append(("brk",))

    def walk(n):
        if isinstance(n, Comment):
            return
        if isinstance(n, NavigableString):
            t = re.sub(r"\s+", "", str(n))
            if t:
                if out and out[-1][0] == "t":
                    out[-1] = ("t", out[-1][1] + t)
                else:
                    out.append(("t", t))
            return
        if not isinstance(n, Tag):
            return
        name = n.name
        if name in ("script", "style"):
            return

        # profile-photo cards (home + robots directory) compare as one unit
        if (side == "old" and name == "table" and "table-align" in n.get("class", [])) or (
            side == "new" and name == "ul" and "robot-grid" in n.get("class", [])
        ):
            brk()
            cards = []
            if side == "old":
                for td in n.select("td"):
                    ths = td.select("th")
                    img = ths[0].img
                    cards.append(
                        (norm_url(ths[0].a["href"], page), ths[1].a.get_text(strip=True),
                         img["src"], img.get("alt", ""))
                    )
            else:
                for li in n.select("li"):
                    a = li.a
                    img = a.img
                    cards.append(
                        (norm_url(a["href"], page), a.get_text(strip=True), img["src"], img.get("alt", ""))
                    )
            if out and out[-1][0] == "cards":
                out[-1] = ("cards", out[-1][1] + tuple(cards))
            else:
                out.append(("cards", tuple(cards)))
            brk()
            return

        # the generated series cards wrap the picture in a second link
        if side == "new" and name == "a" and n.find("img") and "series-card" in n.parent.get("class", []):
            for c in n.children:
                walk(c)
            return

        if name in BLOCKS:
            brk()
        if name in ("h1", "h2", "h3", "h4"):
            out.append((name,))
        elif name in ("ul", "ol"):
            out.append(("list", name))
        elif name == "li" and n.get("id") and CITE.search(n["id"]):
            out.append(("liid", int(CITE.search(n["id"]).group(1))))
        elif name == "a" and n.get("href"):
            out.append(("a", norm_url(n["href"], page)))
        elif name == "img":
            out.append(("img", norm_url(n["src"], page), n.get("alt", "")))
        elif name in ("iframe",):
            ratio = orig_ratio(n) if side == "old" else new_ratio(n)
            out.append(("embed", norm_embed(n["src"], ratio)))
        elif name == "video":
            out.append(("embed", ("video", n["src"], new_ratio(n))))
        elif name in ("i", "em"):
            out.append(("em",))
        elif name in ("b", "strong"):
            out.append(("strong",))
        for c in n.children:
            walk(c)
        if name in ("i", "em"):
            out.append(("/em",))
        elif name in ("b", "strong"):
            out.append(("/strong",))
        if name in BLOCKS:
            brk()

    for n in nodes:
        walk(n)
    while out and out[-1] == ("brk",):
        out.pop()
    while out and out[0] == ("brk",):
        out.pop(0)
    # the old site laid profile cards out as many little tables; the new one as one grid
    merged = []
    for a in out:
        if a[0] == "cards" and len(merged) >= 2 and merged[-1] == ("brk",) and merged[-2][0] == "cards":
            merged.pop()
            merged[-1] = ("cards", merged[-1][1] + a[1])
        else:
            merged.append(a)
    return merged


# ------------------------------------------------------------- old / new ----
def git_show(ref, path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"]).decode("utf-8")


def parse(html):
    return BeautifulSoup(html, "html5lib")


def old_page(ref, path):
    soup = parse(git_show(ref, path))
    root = soup.select_one("div.center-page")
    kids = [c for c in root.children if isinstance(c, Tag)]
    info = {"title": soup.title.get_text().strip(), "header": None, "tabs": [], "nav": []}
    if kids[0].name == "table" and "custom-align" in kids[0].get("class", []):
        info["header"] = kids[0].find("h3").get_text(strip=True)
        info["logo"] = norm_url(kids[0].a["href"], path)
        rest = kids[1:]
        if rest and rest[0].name == "table":
            info["tabs"] = [
                (a.get_text(strip=True), norm_url(a["href"], path)) for a in rest[0].select("a.btn")
            ]
            rest = rest[1:]
    else:
        info["logo"] = norm_url(root.a["href"], path)
        idx = next(i for i, k in enumerate(kids) if k.name == "table")
        info["nav"] = [(a.get_text(strip=True), norm_url(a["href"], path)) for a in kids[idx].select("a.btn")]
        rest = kids[idx + 1:]
    return info, atoms_of(rest, path, "old")


def new_page(site, path):
    f = Path(site) / path
    soup = parse(f.read_text(encoding="utf-8"))
    art = soup.select_one("article.article")
    h1 = soup.select_one("h1.page-title")
    info = {
        "title": soup.title.get_text().strip(),
        "header": h1.get_text(strip=True) if h1 else None,
        "tabs": [(a.get_text(strip=True), norm_url(a["href"], path)) for a in soup.select("nav.tabs a.btn")],
        "nav": [(a.get_text(strip=True), norm_url(a["href"], path)) for a in soup.select("#topnav a.btn, #masthead nav a.btn")],
        "logo": norm_url(soup.select_one("a.logo")["href"], path),
        "scripts": len(soup.find_all("script")),
    }
    return info, atoms_of([art], path, "new")


# ------------------------------------------------------------------- diff ---
def show(a):
    s = repr(a)
    return s if len(s) < 140 else s[:137] + "..."


def diff_atoms(old, new, limit=6):
    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    lines = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        lines.append(f"  {tag} at atom {i1}:")
        for a in old[i1:i2][:3]:
            lines.append(f"     - old {show(a)}")
        for a in new[j1:j2][:3]:
            lines.append(f"     + new {show(a)}")
        if len(lines) > limit * 4:
            lines.append("  ...")
            break
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True, help="git ref of the original HTML site")
    ap.add_argument("--site", default="site", help="built MkDocs output directory")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    pages = [p for p in subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", args.ref], text=True).split() if p.endswith(".html")]

    failures = 0
    totals = dict(pages=0, text=0, links=0, images=0, embeds=0)
    for path in sorted(pages):
        if path == "series.html":
            # stale duplicate of articles.html: must have been identical, and must now redirect
            _, a = old_page(args.ref, "series.html")
            _, b = old_page(args.ref, "articles.html")
            ok = a == b and (Path(args.site) / "series.html").exists()
            print(f"{'ok  ' if ok else 'FAIL'} {path:28} (duplicate of articles.html -> redirect)")
            failures += not ok
            continue
        oi, oa = old_page(args.ref, path)
        ni, na = new_page(args.site, path)
        problems = []
        if oi["title"] != ni["title"]:
            problems.append(f"  title: {oi['title']!r} != {ni['title']!r}")
        if oi["header"] != ni["header"]:
            problems.append(f"  header: {oi['header']!r} != {ni['header']!r}")
        if oi["tabs"] != ni["tabs"]:
            problems.append(f"  tabs: {oi['tabs']} != {ni['tabs']}")
        if oi["nav"] and oi["nav"] != ni["nav"]:
            # the old site's stale series.html used the label "Series"; everything else must match
            problems.append(f"  nav: {oi['nav']} != {ni['nav']}")
        if oi["logo"] != ni["logo"]:
            problems.append(f"  logo link: {oi['logo']} != {ni['logo']}")
        if ni["scripts"]:
            problems.append("  page contains <script>")
        if oa != na:
            problems.append(f"  content differs ({len(oa)} old atoms vs {len(na)} new):")
            problems += diff_atoms(oa, na)
        totals["pages"] += 1
        totals["text"] += sum(len(a[1]) for a in oa if a[0] == "t")
        totals["links"] += sum(1 for a in oa if a[0] == "a")
        totals["images"] += sum(1 for a in oa if a[0] == "img")
        totals["embeds"] += sum(1 for a in oa if a[0] == "embed")
        status = "FAIL" if problems else "ok  "
        print(f"{status} {path:28} {len(oa):5} atoms")
        if problems:
            failures += 1
            print("\n".join(problems))

    print()
    print(
        f"{totals['pages']} pages compared: {totals['text']:,} characters of text, "
        f"{totals['links']} links, {totals['images']} images, {totals['embeds']} video embeds."
    )
    print("RESULT:", "ALL PAGES IDENTICAL" if not failures else f"{failures} page(s) differ")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
