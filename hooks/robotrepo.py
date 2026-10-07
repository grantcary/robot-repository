"""Site logic for the robot repository, kept in one file on purpose.

Everything here exists so that article markdown can stay plain:

  * a bare video URL on its own line becomes an embed (YouTube, archive.org,
    or a direct video file)
  * ``[^3]`` becomes a numbered citation that links to reference 3
  * a list can start right under a line of text, without a blank line first
  * images on their own line are centred; several on one line sit side by side,
    scaled to one shared height (each image's shape is measured at build time
    and cached in ``hooks/image-sizes.json``)
  * ``{{robots}}`` / ``{{series}}`` build the robot directory and the Articles
    page from the front matter of the pages themselves
  * tab rows for a series come from ``extra.series`` in mkdocs.yml

Markdown features are in ``RobotRepoExtension``; the MkDocs hooks (bottom of
file) wire it in and supply the data the theme needs.
"""
import json
import logging
import re
import urllib.request
import xml.etree.ElementTree as etree
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import ImageFile
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from mkdocs.exceptions import PluginError
from mkdocs.utils import get_relative_url
from mkdocs.utils.meta import get_data

log = logging.getLogger("mkdocs.hooks.robotrepo")

# --------------------------------------------------------------------------
# Video embeds
# --------------------------------------------------------------------------

YOUTUBE_ALLOW = (
    "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; "
    "picture-in-picture; web-share"
)
VIDEO_FILE = re.compile(r"\.(mp4|m4v|webm|ogv|mov)$", re.I)
EMBED_LINE = re.compile(r"^[ \t]*(https?://\S+)(?:[ \t]+(\d+):(\d+))?[ \t]*$")


def _seconds(value):
    """'398', '398s', '1m30s' -> 398 / 398 / 90"""
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s?)?", value or "")
    if not m or not any(m.groups()):
        return None
    h, mi, s = (int(g or 0) for g in m.groups())
    return h * 3600 + mi * 60 + s


def resolve_embed(url):
    """Return a dict describing how to embed ``url``, or None if it isn't a
    recognised video URL (in which case the line is left alone)."""
    u = urlparse(url)
    host = u.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    q = parse_qs(u.query)
    path = u.path

    # YouTube -----------------------------------------------------------
    video_id = None
    if host in ("youtube.com", "m.youtube.com", "youtube-nocookie.com"):
        if path == "/watch":
            video_id = (q.get("v") or [None])[0]
        else:
            m = re.match(r"^/(?:embed|shorts|live|v)/([\w-]+)", path)
            video_id = m.group(1) if m else None
    elif host == "youtu.be":
        video_id = path.strip("/") or None
    if video_id:
        params = []
        start = _seconds((q.get("t") or q.get("start") or [""])[0])
        if start:
            params.append(f"start={start}")
        end = _seconds((q.get("end") or [""])[0])
        if end:
            params.append(f"end={end}")
        if q.get("list"):
            params.append(f"list={q['list'][0]}")
        src = f"https://www.youtube.com/embed/{video_id}"
        if params:
            src += "?" + "&".join(params)
        return {
            "kind": "iframe",
            "src": src,
            "attrs": {
                "title": "YouTube video player",
                "allow": YOUTUBE_ALLOW,
                "referrerpolicy": "strict-origin-when-cross-origin",
            },
        }

    # Internet Archive items (also what the Wayback Machine's video player is)
    if host == "archive.org":
        m = re.match(r"^/(?:details|embed)/(.+)$", path)
        if m:
            src = f"https://archive.org/embed/{m.group(1)}"
            if u.query:
                src += "?" + u.query
            return {
                "kind": "iframe",
                "src": src,
                "attrs": {
                    "title": "Internet Archive video player",
                    "webkitallowfullscreen": "true",
                    "mozallowfullscreen": "true",
                },
            }

    # Plain video files, including captures like web.archive.org/web/…/x.mp4
    if VIDEO_FILE.search(path):
        return {"kind": "video", "src": url, "attrs": {}}

    return None


class EmbedProcessor(BlockProcessor):
    """A paragraph that is just a video URL (optionally followed by ``4:3``)."""

    def test(self, parent, block):
        m = EMBED_LINE.match(block)
        return bool(m) and resolve_embed(m.group(1)) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = EMBED_LINE.match(block)
        spec = resolve_embed(m.group(1))
        ratio = f"{m.group(2)}/{m.group(3)}" if m.group(2) else "16/9"

        wrap = etree.SubElement(parent, "div")
        wrap.set("class", "embed")
        wrap.set("style", f"aspect-ratio: {ratio}")
        if spec["kind"] == "iframe":
            el = etree.SubElement(wrap, "iframe")
            el.set("src", spec["src"])
            el.set("loading", "lazy")
            el.set("frameborder", "0")
            el.set("allowfullscreen", "allowfullscreen")
        else:
            el = etree.SubElement(wrap, "video")
            el.set("src", spec["src"])
            el.set("controls", "controls")
            el.set("preload", "metadata")
        for k, v in spec["attrs"].items():
            el.set(k, v)
        return True


# --------------------------------------------------------------------------
# Citations:  [^3]  ->  superscript [3] linking to reference 3
# --------------------------------------------------------------------------


class CiteInline(InlineProcessor):
    def handleMatch(self, m, data):
        n = int(m.group(1))
        sup = etree.Element("sup")
        sup.set("class", "cite")
        a = etree.SubElement(sup, "a")
        a.set("href", f"#cite_note-{n:02d}")
        a.text = f"[{n}]"
        return sup, m.start(0), m.end(0)


# --------------------------------------------------------------------------
# Lists right under a line of text
# --------------------------------------------------------------------------

# Python-Markdown only starts a list after a blank line, so "The plug-ins are:"
# followed directly by "+ HUMANOID" would read as one paragraph. Add the blank
# line for it, like GitHub does. Only top-level bullets ("- ", "* ", "+ ") and
# lists numbered from "1." count, so a wrapped line that happens to begin with
# a number isn't turned into a list.
LIST_START = re.compile(r"^(?:[-*+]|1[.)])[ \t]+\S")
LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]+")
FENCE = re.compile(r"^[ \t]*(```|~~~)")


class ListAfterText(Preprocessor):
    def run(self, lines):
        out, fenced, prev = [], False, ""
        for line in lines:
            if FENCE.match(line):
                fenced = not fenced
            elif (
                not fenced
                and LIST_START.match(line)
                and prev.strip()
                and not prev[0].isspace()
                and not LIST_ITEM.match(prev)
                and not prev.lstrip().startswith(("|", ">", "<"))
            ):
                out.append("")
            out.append(line)
            prev = line
        return out


# --------------------------------------------------------------------------
# Tidy-ups on the parsed tree
# --------------------------------------------------------------------------


# Image sizes, so side-by-side images can share a height without JavaScript.
# Remote images are measured once by downloading just enough of the file to
# read its header, then remembered in image-sizes.json (commit that file, so
# builds don't re-download).

SIZES_FILE = Path(__file__).with_name("image-sizes.json")
_SIZES = None
_SIZES_CHANGED = False


def _load_sizes():
    global _SIZES
    if _SIZES is None:
        try:
            _SIZES = json.loads(SIZES_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _SIZES = {}
    return _SIZES


def _fetch_size(url):
    req = urllib.request.Request(url, headers={"User-Agent": "robotrepository-build"})
    parser = ImageFile.Parser()
    with urllib.request.urlopen(req, timeout=20) as resp:
        for _ in range(256):  # at most 1 MB of header
            chunk = resp.read(4096)
            if not chunk:
                break
            parser.feed(chunk)
            if parser.image:
                return list(parser.image.size)
    return None


def image_size(src):
    """(width, height) of a remote image, or None if it can't be measured."""
    global _SIZES_CHANGED
    if not src.startswith(("http://", "https://")):
        return None
    sizes = _load_sizes()
    if src not in sizes:
        try:
            size = _fetch_size(src)
        except Exception as e:  # network trouble shouldn't break the build
            log.info("Could not measure image %s: %s", src, e)
            return None
        if not size:
            return None
        sizes[src] = size
        _SIZES_CHANGED = True
    return tuple(sizes[src])


def _save_sizes():
    global _SIZES_CHANGED
    if _SIZES_CHANGED:
        SIZES_FILE.write_text(
            json.dumps(dict(sorted(_SIZES.items())), indent=1) + "\n", encoding="utf-8"
        )
        _SIZES_CHANGED = False


def _is_image(el):
    if el.tag == "img":
        return True
    return el.tag == "a" and len(el) == 1 and el[0].tag == "img" and not (el.text or "").strip()


class TidyTree(Treeprocessor):
    def run(self, root):
        # Image-only paragraphs: one image is a centred figure, several sit
        # side by side as a gallery.
        for p in root.iter("p"):
            kids = list(p)
            if (
                kids
                and all(_is_image(k) for k in kids)
                and not (p.text or "").strip()
                and all(not (k.tail or "").strip() for k in kids)
            ):
                p.set("class", "gallery" if len(kids) > 1 else "figure")
                if len(kids) > 1:
                    self._share_height(kids)

        for img in root.iter("img"):
            img.set("loading", "lazy")

        # The list under a "References" heading is the target of [^n] markers.
        heading = None
        for el in root.iter():
            if el.tag in ("h2", "h3", "h4"):
                heading = "".join(el.itertext()).strip().lower()
            elif el.tag == "ol" and heading == "references":
                el.set("class", "references")
                for i, li in enumerate(el.findall("li"), 1):
                    li.set("id", f"cite_note-{i:02d}")
                heading = None

    @staticmethod
    def _share_height(kids):
        # Each image gets width in proportion to its aspect ratio, so every
        # image in the row ends up the same height. If any image can't be
        # measured the row keeps equal widths (undistorted, just not
        # height-matched).
        imgs = [k if k.tag == "img" else k[0] for k in kids]
        sizes = [image_size(img.get("src", "")) for img in imgs]
        if not all(sizes):
            return
        for k, img, (w, h) in zip(kids, imgs, sizes):
            img.set("width", str(w))
            img.set("height", str(h))
            # x100 keeps the total above 1; below that, flex leaves a gap
            k.set("style", f"flex-grow: {100 * w / h:.2f}")


class RobotRepoExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(ListAfterText(md), "list_after_text", 25)
        md.parser.blockprocessors.register(EmbedProcessor(md.parser), "embed", 18)
        md.inlinePatterns.register(CiteInline(r"\[\^(\d+)\]", md), "cite", 175)
        md.treeprocessors.register(TidyTree(md), "robotrepo_tidy", 15)


# --------------------------------------------------------------------------
# Site data: front matter registry, series, directives
# --------------------------------------------------------------------------

REGISTRY = {}  # src_uri -> front matter dict
SERIES = []  # extra.series from mkdocs.yml
SERIES_BY_ID = {}

DIRECTIVE = re.compile(r"^\{\{\s*(robots|series)\s*((?:\|[^}\n]*)?)\}\}[ \t]*$", re.M)


def _link(src_uri_from, src_uri_to):
    """Relative URL from one page to another, given their docs-relative paths."""
    to = _FILES.get_file_from_path(src_uri_to)
    frm = _FILES.get_file_from_path(src_uri_from)
    if to is None:
        raise PluginError(f"{src_uri_from}: no such page '{src_uri_to}'")
    return get_relative_url(to.url, frm.url)


_FILES = None


def on_config(config):
    config.markdown_extensions.append(RobotRepoExtension())
    SERIES[:] = config.extra.get("series", [])
    SERIES_BY_ID.clear()
    SERIES_BY_ID.update({s["id"]: s for s in SERIES})
    return config


def on_files(files, config):
    global _FILES
    _FILES = files
    REGISTRY.clear()
    for f in files.documentation_pages():
        text = Path(f.abs_src_path).read_text(encoding="utf-8")
        _, meta = get_data(text)
        REGISTRY[f.src_uri] = meta

    for s in SERIES:
        for p in s["pages"]:
            if files.get_file_from_path(p["page"]) is None:
                raise PluginError(f"series '{s['id']}' lists missing page {p['page']}")
    for src, meta in REGISTRY.items():
        sid = meta.get("series")
        if sid and sid not in SERIES_BY_ID:
            raise PluginError(f"{src}: unknown series '{sid}'")
    return files


def _robot_entries():
    """Pages with a ``robot:`` block, in catalogue order: series order first,
    then anything not in a series (alphabetical)."""
    seen, ordered = set(), []
    for s in SERIES:
        for p in s["pages"]:
            src = p["page"]
            if src not in seen and "robot" in REGISTRY.get(src, {}):
                seen.add(src)
                ordered.append(src)
    loose = sorted(
        (src for src, m in REGISTRY.items() if "robot" in m and src not in seen),
        key=lambda src: REGISTRY[src]["robot"]["name"].lower(),
    )
    return ordered + loose


def _robot_card(page_src, target_src):
    r = REGISTRY[target_src]["robot"]
    name = escape(r["name"])
    href = escape(_link(page_src, target_src))
    thumb = escape(str(r["thumbnail"]))
    return (
        f'<li><a href="{href}"><img src="{thumb}" alt="{name} Profile Photo" '
        f'class="profile-image" width="50" height="50" loading="lazy">'
        f'<span class="profile-name">{name}</span></a></li>'
    )


def _robots_html(page_src, args):
    if args:  # {{robots|a.md|b.md}}  -> just those, in that order
        for a in args:
            if "robot" not in REGISTRY.get(a, {}):
                raise PluginError(f"{page_src}: {{{{robots}}}} lists '{a}', which has no robot: front matter")
        cards = "".join(_robot_card(page_src, a) for a in args)
        return f'<ul class="robot-grid">{cards}</ul>'

    groups = {}
    for src in _robot_entries():
        r = REGISTRY[src]["robot"]
        letter = str(r.get("letter") or r["name"][0]).upper()
        groups.setdefault(letter, []).append(src)
    out = []
    for letter in sorted(groups):
        cards = "".join(_robot_card(page_src, s) for s in groups[letter])
        out.append(f'<h3 id="robots-{letter.lower()}">{letter}</h3>')
        out.append(f'<ul class="robot-grid">{cards}</ul>')
    return "\n\n".join(out)


def _series_html(page_src):
    out = []
    for s in SERIES:
        if s.get("hidden"):
            continue
        start = s.get("start") or s["pages"][0]["page"]
        href = escape(_link(page_src, start))
        title = escape(s["title"])
        out.append(
            '<div class="series-card">'
            f'<div class="headrow"><h3>{title}</h3><a href="{href}">Read more</a></div>'
            f'<a href="{href}"><img src="{escape(s["image"])}" alt="" loading="lazy"></a>'
            "</div>"
        )
    return "\n\n".join(out)


def on_page_markdown(markdown, page, config, files):
    def expand(m):
        kind = m.group(1)
        args = [a.strip() for a in m.group(2).split("|") if a.strip()]
        if kind == "robots":
            return _robots_html(page.file.src_uri, args)
        return _series_html(page.file.src_uri)

    return DIRECTIVE.sub(expand, markdown)


def _count_toc(items):
    return sum(1 + _count_toc(i.children) for i in items)


def on_page_context(context, page, config, nav):
    src = page.file.src_uri
    meta = page.meta
    header, tabs = meta.get("header"), []
    sid = meta.get("series")
    if sid:
        s = SERIES_BY_ID[sid]
        header = s["title"]
        for t in s["pages"]:
            tabs.append(
                {
                    "label": str(t["label"]),
                    "url": _link(src, t["page"]),
                    "active": t["page"] == src,
                }
            )
    context["page_header"] = header
    context["series_tabs"] = tabs
    context["toc_count"] = _count_toc(page.toc)
    context["page_history_url"] = f"{config.repo_url}/commits/main/docs/{src}"
    return context


REDIRECT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>robot repository</title>
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{canonical}">
</head>
<body>
<p>This page has moved to <a href="{target}">{target}</a>.</p>
</body>
</html>
"""


def on_post_build(config):
    _save_sizes()
    base = config.site_url or ""
    for old, new in (config.extra.get("redirects") or {}).items():
        dest = Path(config.site_dir) / old
        dest.parent.mkdir(parents=True, exist_ok=True)
        rel = get_relative_url(new, old)
        dest.write_text(
            REDIRECT_HTML.format(target=escape(rel), canonical=escape(base + new)),
            encoding="utf-8",
        )
