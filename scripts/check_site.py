from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://akhilalladi-code.github.io/telugu-bhakti/"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.title = False
        self.lang = False
        self.viewport = False
        self.description = False
        self.canonical = False
        self.noindex = False
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("a", "link") and attrs.get("href"):
            self.links.append((attrs["href"], tag))
        if tag in ("script", "img", "source") and attrs.get("src"):
            self.links.append((attrs["src"], tag))
        if tag == "html" and attrs.get("lang"):
            self.lang = True
        if tag == "meta":
            name = (attrs.get("name") or "").lower()
            prop = (attrs.get("property") or "").lower()
            self.viewport |= name == "viewport"
            self.description |= name == "description" and bool(attrs.get("content"))
            self.noindex |= name == "robots" and "noindex" in attrs.get("content", "").lower()
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = bool(attrs.get("href"))
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.title = True

errors = []
html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
for page in html_files:
    parser = PageParser()
    parser.feed(page.read_text(encoding="utf-8"))
    relative = page.relative_to(ROOT)
    if not parser.title:
        errors.append(f"{relative}: missing title")
    if not parser.lang:
        errors.append(f"{relative}: missing html lang")
    if not parser.viewport:
        errors.append(f"{relative}: missing viewport meta")
    if not parser.noindex and not parser.description:
        errors.append(f"{relative}: missing meta description")
    if not parser.noindex and not parser.canonical:
        errors.append(f"{relative}: missing canonical URL")

    for raw, tag in parser.links:
        if raw.startswith(("#", "http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")):
            if raw.startswith("#") and raw[1:] and unquote(raw[1:]) not in parser.ids:
                errors.append(f"{relative}: missing in-page anchor {raw}")
            continue
        parsed = urlparse(raw)
        target_path = unquote(parsed.path)
        if not target_path:
            continue
        target = (page.parent / target_path).resolve()
        if not target.is_relative_to(ROOT):
            errors.append(f"{relative}: link escapes repository: {raw}")
            continue
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{relative}: broken local {tag} reference: {raw}")

songs_path = ROOT / "data" / "songs.json"
songs = json.loads(songs_path.read_text(encoding="utf-8"))
seen = set()
for song in songs:
    for field in ("id", "titleTe", "href"):
        if not song.get(field):
            errors.append(f"songs.json: entry missing {field}")
    if song.get("id") in seen:
        errors.append(f"songs.json: duplicate id {song.get('id')}")
    seen.add(song.get("id"))
    target = (ROOT / song.get("href", "")).resolve()
    if not target.is_relative_to(ROOT) or not target.is_file():
        errors.append(f"songs.json: invalid or missing song page for {song.get('id')}")

sitemap_path = ROOT / "sitemap.xml"
try:
    sitemap = ET.parse(sitemap_path).getroot()
    locs = {node.text for node in sitemap.iter() if node.tag.endswith("loc") and node.text}
    for page in html_files:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if parser.noindex:
            continue
        rel = page.relative_to(ROOT).as_posix()
        suffix = "" if rel == "index.html" else rel[:-10] if rel.endswith("index.html") else rel
        expected = BASE + suffix
        if expected not in locs:
            errors.append(f"sitemap.xml: missing {expected}")
except (ET.ParseError, OSError) as exc:
    errors.append(f"sitemap.xml: invalid XML: {exc}")

if errors:
    print("Site checks failed:")
    print("\n".join(f"- {item}" for item in errors))
    sys.exit(1)

print(f"Site checks passed: {len(html_files)} HTML pages, {len(songs)} indexed songs, local links and sitemap verified.")
