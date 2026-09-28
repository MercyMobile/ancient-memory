#!/usr/bin/env python3
"""Regression checks for crawler, LLM, and no-JavaScript reading paths."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


class BookFallbackParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.in_book = False
        self.text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "div" and values.get("id") == "book":
            self.in_book = True
            self.depth = 1
            return
        if self.in_book:
            self.depth += 1
            if tag == "a" and values.get("href"):
                self.links.append(values["href"])

    def handle_endtag(self, tag):
        if self.in_book:
            self.depth -= 1
            if self.depth == 0:
                self.in_book = False

    def handle_data(self, data):
        if self.in_book:
            self.text.append(data)


index = (ROOT / "index.html").read_text()
parser = BookFallbackParser()
parser.feed(index)
visible_fallback = " ".join(" ".join(parser.text).split())
assert "The World Remembers" in visible_fallback
assert "Every people on earth" in visible_fallback
assert "Interactive sourced storybook" in visible_fallback
assert "https://ancient-memory.pages.dev/read/" in parser.links
assert "https://ancient-memory.pages.dev/llms-full.txt" in parser.links
assert 'data-static-fallback' in index

for mime, url in [
    ("text/plain", "https://ancient-memory.pages.dev/llms-full.txt"),
    ("text/html", "https://ancient-memory.pages.dev/read/"),
    ("text/markdown", "https://ancient-memory.pages.dev/download/the-world-remembers.md"),
]:
    assert f'type="{mime}" href="{url}"' in index

for block in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', index, re.S):
    json.loads(block)

markdown = (ROOT / "download/the-world-remembers.md").read_text()
plain = (ROOT / "llms-full.txt").read_text()
read_html = (ROOT / "read/index.html").read_text()
assert plain == markdown and len(plain) > 250_000
book_n=len(json.loads((ROOT / "data/book.json").read_text())["chapters"])
assert f"# {book_n}. The Witnesses" in plain and "# World atlas — sources in time" in plain
assert "<script" not in read_html.lower()
assert "Complete text of The World Remembers" in read_html
assert f"# {book_n}. The Witnesses" in read_html

sitemap = (ROOT / "sitemap.xml").read_text()
for url in [
    "https://ancient-memory.pages.dev/",
    "https://ancient-memory.pages.dev/llms.txt",
    "https://ancient-memory.pages.dev/llms-full.txt",
    "https://ancient-memory.pages.dev/read/",
    "https://ancient-memory.pages.dev/exhibits/watcher-364/",
    "https://ancient-memory.pages.dev/exhibits/adams-chart/",
]:
    assert f"<loc>{url}</loc>" in sitemap

robots = (ROOT / "robots.txt").read_text()
assert "User-agent: *" in robots and "Allow: /" in robots
print("PASS: visible no-JS homepage fallback, valid JSON-LD, complete plain-text and HTML editions, sitemap, and crawler access.")
