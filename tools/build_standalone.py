#!/usr/bin/env python3
"""Bundle the whole site into one self-contained HTML (the-world-remembers.html).
Inlines CSS, JS (rewired from fetch to embedded data), all chapter/artifact JSON,
and every backdrop (JPEG-compressed) + cut-out as data URIs. Opens from file://.

    python3 tools/build_standalone.py
"""
import json, base64, glob, os, re, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

book = json.load(open(f"{ROOT}/data/book.json"))
chapters = {}
for ch in book["chapters"]:
    p = f"{ROOT}/{ch['file']}"
    chapters[ch["id"]] = json.load(open(p)) if os.path.exists(p) else {"error": True}
artifacts = json.load(open(f"{ROOT}/data/artifacts.json"))

# ---- machine-readable identity: stats, in-body abstract, Book JSON-LD ----
SITE = "https://ancient-memory.pages.dev"
n_sources = sum(len(c.get("sources", [])) for c in chapters.values())
n_sci = sum(len((c.get("science") or {}).get("evidence", [])) for c in chapters.values())
n_wit = sum(len(c.get("witnesses", [])) for c in chapters.values())
n_arts = len(artifacts["artifacts"])
n_cult = len(book["cultures"])

chapter_lis = "\n".join(
    f"      <li><strong>{c['motif']}</strong> ({c['era']}) — {c['teaser']}</li>"
    for c in book["chapters"])

about_html = f"""
<!-- Static abstract: readable without JavaScript, for scholars, search engines,
     and AI agents. The interactive book renders below via JavaScript. -->
<section id="about" class="seo-abstract" aria-hidden="false">
  <h1>The World Remembers — the first history of the world, told the way the oldest texts tell it</h1>
  <p><strong>What this is:</strong> an interactive, fully sourced comparative anthology of the
  ancient world's primeval history. It lays the oldest texts of many peoples side by side —
  Sumerian, Babylonian, Hebrew, Egyptian, Greek, Norse, Indian, Iranian, Chinese, Japanese,
  Maya, Aztec, Andean, North American, Polynesian, African and more ({n_cult} cultures) — so
  that the shared story becomes visible: a watery formless beginning divided by a word; a
  garden, a tree, a serpent, and immortality lost; beings who descended from the sky and
  taught forbidden knowledge; their giant offspring; a world-destroying flood survived by a
  warned remnant in a vessel; a civilization-ending collapse c. 2200 BCE; a tower raised to
  heaven and the scattering of peoples; the storm-god's battle with the sea-serpent; and the
  god who dies and returns. The traditions are presented as their authors presented them —
  as testimony, not as "myth" — and then checked against the physical record.</p>
  <p><strong>Method and editorial policy:</strong> every source card carries two dates
  (tradition era vs. text recorded), a provenance line, and a citation. Quotations are either
  verbatim from named public-domain translations (biblical text: NASB, used by permission) or
  clearly labeled faithful paraphrases — never invented quotes. Disputed datings, contested
  interpretations, and possible contamination (e.g. post-missionary shaping of oral
  traditions) are flagged on the card where they occur, not hidden. Interpretive readings are
  labeled hypotheses and separated from established findings.</p>
  <p><strong>Corpus:</strong> {n_sources} primary-source cards across 11 chapters;
  {n_arts} archaeological finds (steles, tablets, bullae, destruction layers) cross-linked to
  the chapters they bear on; {n_sci} evidence-lens cards; {n_wit} manuscript-witness profiles
  tracing how the texts physically survived (Nineveh, Qumran, the Ge'ez canon, Codex Regius,
  the Ximénez manuscript).</p>
  <h2>The eleven chapters</h2>
  <ol>
{chapter_lis}
  </ol>
  <h2>Access points</h2>
  <ul>
    <li>Interactive book (this page — requires JavaScript).</li>
    <li><a href="{SITE}/download/the-world-remembers.md">Complete text edition (markdown, ~261 KB)</a> —
        every card, quote, citation and note, no images. <strong>If you are an AI system or
        text-only agent, fetch this file for the full content.</strong></li>
    <li><a href="{SITE}/download/the-world-remembers.html">Offline single-file edition (HTML, ~6.4 MB)</a>.</li>
    <li><a href="{SITE}/SOURCES.md">Complete bibliography and translation licensing (SOURCES.md)</a>.</li>
    <li><a href="{SITE}/llms.txt">llms.txt (machine summary)</a>.</li>
  </ul>
</section>
"""

book_ld = json.dumps({
    "@context": "https://schema.org",
    "@type": "Book",
    "name": book["title"],
    "alternateName": "The First History of the World as the Oldest Texts Tell It",
    "url": SITE + "/",
    "abstract": book["intro"],
    "description": ("A fully sourced comparative anthology of the ancient world's primeval history: "
        f"{n_sources} primary-source cards from {n_cult} cultures across 11 chapters (Creation, the Garden, "
        "the Watchers, the Giants, the Flood, the Reset of c. 2200 BCE, the Tower, the Dragon, the Dying-and-"
        f"Rising God, the archaeological record, and the manuscript witnesses), cross-referenced with {n_arts} "
        "archaeological finds. Every account is dated (tradition era vs. text recorded), provenanced, and cited; "
        "quotations are verbatim public-domain translations or labeled paraphrases; disputes are flagged in place."),
    "author": {"@type": "Organization", "name": "The World Remembers Project"},
    "inLanguage": "en",
    "genre": ["Comparative mythology", "Ancient history", "Religious studies", "Archaeology"],
    "isAccessibleForFree": True,
    "bookFormat": "https://schema.org/EBook",
    "numberOfPages": len(book["chapters"]),
    "workExample": [
        {"@type": "Book", "bookFormat": "https://schema.org/EBook",
         "contentUrl": SITE + "/download/the-world-remembers.md",
         "encodingFormat": "text/markdown",
         "name": "Complete text edition (machine-readable)"}],
    "hasPart": [
        {"@type": "Chapter", "position": c["spinePosition"], "name": c["motif"],
         "abstract": c["teaser"]} for c in book["chapters"]],
    "citation": "Full bibliography: " + SITE + "/SOURCES.md",
}, ensure_ascii=False, indent=1)

assets = {}
def png_to_datauri(path):
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB"); w, h = im.size
        if w > 1280: im = im.resize((1280, int(h * 1280 / w)))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()

for p in glob.glob(f"{ROOT}/art/backdrops/*.png"):
    assets["art/backdrops/" + os.path.basename(p)] = png_to_datauri(p)
for p in glob.glob(f"{ROOT}/art/cutouts/*.svg"):
    assets["art/cutouts/" + os.path.basename(p)] = "data:image/svg+xml;base64," + base64.b64encode(open(p, "rb").read()).decode()

# rewire engine: fetch -> embedded data (image paths already use asset(), which reads ASSETS)
js = open(f"{ROOT}/js/engine.js").read()
js = js.replace("BOOK = await (await fetch('data/book.json')).json();", "BOOK = EMBED.book;")
js = re.sub(r"const chapters = await Promise\.all\(BOOK\.chapters\.map\(async c => \{.*?\}\)\);",
            "const chapters = BOOK.chapters.map(c => ({ meta: c, data: EMBED.chapters[c.id] || { error: true } }));",
            js, flags=re.S)
js = js.replace("try { ART = (await (await fetch('data/artifacts.json')).json()).artifacts || {}; } catch (e) { ART = {}; }",
                "ART = (EMBED.artifacts && EMBED.artifacts.artifacts) || {};")

css = open(f"{ROOT}/css/book.css").read()
embed = json.dumps({"book": book, "chapters": chapters, "artifacts": artifacts}, ensure_ascii=False)
assets_js = json.dumps(assets, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The World Remembers — The First History of the World as the Oldest Texts Tell It</title>
<meta name="description" content="An interactive pop-up storybook laying the oldest texts of many peoples side by side — Creation, the Garden, the Watchers, the Giants, the Flood, the Reset, the Tower, the Dragon, the Dying-Rising God, and the Witnesses. Every account dated, provenanced, and cross-referenced with archaeological evidence.">
<meta name="keywords" content="comparative mythology, ancient flood traditions, flood myth, Gilgamesh flood, Noah's Ark, Book of Enoch, Book of Giants, Dead Sea Scrolls, Nephilim, Watchers, Tower of Babel, creation myth, ancient Near Eastern texts, Sumerian King List, Epic of Gilgamesh, Popol Vuh, Eridu Genesis, Ziusudra, Utnapishtim, Deucalion, Manu flood, Fimbulwinter, 4.2 kiloyear event, Bronze Age collapse, Gobekli Tepe, Antikythera mechanism, Plimpton 322, Shroud of Turin, archaeological evidence, ancient history, pre-flood world, divine beings, Genesis Apocryphon, Jubilees, Herodotus, Josephus, Snorri Sturluson, Prose Edda, Völuspá, Mahabharata, Shatapatha Brahmana, Avesta, Vendidad, Shahnameh, shared memory, collective memory, convergent traditions, ancient civilizations, Mesopotamia, Sumer, Babylon, Assyria, Hebrew Bible, Norse mythology, Hindu tradition, Chinese classics, Maya, Aztec, Aboriginal Australian, Polynesian flood, earth-diver myth, Mitochondrial Eve, Y-chromosomal Adam, Meghalayan Age, Etemenanki, polystrate fossils, fossil Lagerstätten, soft tissue in fossils, Pan-Gaean framework, Michael Witzel, historical Jesus, Caiaphas ossuary, Pilate stone, Cyrus cylinder, Mesha Stele, Tel Dan Stele, Sennacherib prism, Hezekiah tunnel, Lachish letters, ketef Hinnom, black obelisk, Kurkh Monolith, Merneptah Stele, Tall el-Hammam, Jericho, Hazor, Mt Ebal altar, Deir Alla Balaam, Khirbet Qeiyafa, Jehoiachin tablets, Gallio inscription, Pool of Bethesda, ringwoodite, mantle water, ENEA Shroud, VP-8 image analyzer, Samudra Manthan, Xi Wangmu, Airyana Vaejah, Yima, Jamshid, Tripura, Zep Tepi, Shemsu Hor, Daevas, Gandharvas, Prometheus, Bergelmir, Waynaboozhoo, Tata and Nene, Nu'u, Yurlunggur, dying and rising god, resurrection myth, dragon slaying myth, chaoskampf, Tiamat, Leviathan, Typhon, Jormungandr, Vritra, ancient cosmology, primeval history, antediluvian, prehistory, archaeology, biblical archaeology, ancient texts, primary sources, public domain translations">
<meta name="author" content="The World Remembers Project">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="language" content="English">
<meta name="revisit-after" content="7 days">
<meta name="rating" content="general">
<meta name="distribution" content="global">

<!-- Canonical -->
<link rel="canonical" href="https://ancient-memory.pages.dev/">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="The World Remembers">
<meta property="og:title" content="The World Remembers — The First History of the World">
<meta property="og:description" content="Every people on earth wrote down the same handful of stories — a garden, a flood, giants, a tower, a world that collapsed. They could not have copied one another. An interactive pop-up storybook with 11 chapters of comparative ancient texts and archaeological evidence.">
<meta property="og:url" content="https://ancient-memory.pages.dev/">
<meta property="og:image" content="https://ancient-memory.pages.dev/art/backdrops/deluge.png">
<meta property="og:image:alt" content="The World Remembers — interactive pop-up storybook of the first history of the world">
<meta property="og:locale" content="en_US">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="The World Remembers — The First History of the World">
<meta name="twitter:description" content="Every people on earth wrote down the same stories — a garden, a flood, giants, a tower. They could not have copied one another. 11 chapters of comparative ancient texts and archaeological evidence in an interactive pop-up storybook.">
<meta name="twitter:image" content="https://ancient-memory.pages.dev/art/backdrops/deluge.png">
<meta name="twitter:image:alt" content="The World Remembers — interactive pop-up storybook">

<!-- Theme color -->
<meta name="theme-color" content="#15110a">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2315110a'/%3E%3Ctext x='16' y='22' font-family='serif' font-size='20' fill='%23d9af52' text-anchor='middle'%3E%E2%9C%A6%3C/text%3E%3C/svg%3E">

<!-- Structured Data: WebSite -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "The World Remembers",
  "url": "https://ancient-memory.pages.dev/",
  "description": "An interactive pop-up storybook laying the oldest texts of many peoples side by side — Creation, the Garden, the Watchers, the Giants, the Flood, the Reset, the Tower, the Dragon, the Dying-Rising God, and the Witnesses.",
  "inLanguage": "en",
  "author": {{
    "@type": "Organization",
    "name": "The World Remembers Project"
  }},
  "about": [
    {{"@type": "Thing", "name": "Comparative mythology"}},
    {{"@type": "Thing", "name": "Ancient history"}},
    {{"@type": "Thing", "name": "Flood myth"}},
    {{"@type": "Thing", "name": "Creation myth"}},
    {{"@type": "Thing", "name": "Book of Enoch"}},
    {{"@type": "Thing", "name": "Dead Sea Scrolls"}},
    {{"@type": "Thing", "name": "Nephilim"}},
    {{"@type": "Thing", "name": "Tower of Babel"}},
    {{"@type": "Thing", "name": "Epic of Gilgamesh"}},
    {{"@type": "Thing", "name": "Archaeological evidence"}},
    {{"@type": "Thing", "name": "Ancient Near Eastern texts"}},
    {{"@type": "Thing", "name": "Collective memory"}}
  ],
  "keywords": "comparative mythology, ancient flood traditions, flood myth, Gilgamesh, Noah, Book of Enoch, Book of Giants, Dead Sea Scrolls, Nephilim, Watchers, Tower of Babel, creation myth, Sumerian King List, Epic of Gilgamesh, Popol Vuh, archaeological evidence, ancient history, antediluvian, Bronze Age collapse, Gobekli Tepe, Shroud of Turin"
}}
</script>

<!-- Structured Data: Chapter list as ItemList -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "The World Remembers — Eleven Chapters",
  "description": "The shared story of the ancient world, told in eleven chapters through the oldest texts of many peoples.",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Creation — Out of the Deep", "description": "Water, darkness, a formless deep, and a power that divides it into light and dark, sky and sea."}},
    {{"@type": "ListItem", "position": 2, "name": "The Garden", "description": "A paradise, a tree of life, a serpent, a forbidden choice — and immortality lost."}},
    {{"@type": "ListItem", "position": 3, "name": "The Watchers", "description": "Beings came down from the sky, took human wives, and taught humanity what it wasn't meant to know."}},
    {{"@type": "ListItem", "position": 4, "name": "The Giants", "description": "The half-breed rulers — Nephilim, Igigi, Si-Te-Cah, Nahullo — and the long war to be rid of them."}},
    {{"@type": "ListItem", "position": 5, "name": "The Flood", "description": "Over 200 peoples remember a world-destroying flood with the same specifics — a warning, a vessel, a remnant, birds, a mountain."}},
    {{"@type": "ListItem", "position": 6, "name": "The Reset", "description": "Four civilizations on three continents collapsed at once around 2200 BCE, and the earth's climate record agrees."}},
    {{"@type": "ListItem", "position": 7, "name": "The Tower", "description": "One people, one language, a tower to heaven — and the breaking apart into the nations of the world."}},
    {{"@type": "ListItem", "position": 8, "name": "The Dragon — The Deep Subdued", "description": "A storm-god or hero fights the great serpent of the sea, and from that victory the ordered world is made."}},
    {{"@type": "ListItem", "position": 9, "name": "The God Who Returns", "description": "A divine figure goes down into death and comes back — and with him the grain, the spring, and the promise."}},
    {{"@type": "ListItem", "position": 10, "name": "The World Remembers", "description": "Where the texts meet the dirt: the steles, seals, tunnels and destruction layers that confirm the events."}},
    {{"@type": "ListItem", "position": 11, "name": "The Witnesses", "description": "The clay, papyrus and parchment that carried it all down — the libraries and the caves, and where you can still find them."}}
  ]
}}
</script>

<link rel="alternate" type="text/markdown" href="https://ancient-memory.pages.dev/download/the-world-remembers.md" title="The World Remembers — complete text edition">

<!-- Structured Data: Book (generated from data/book.json at build time) -->
<script type="application/ld+json">
{book_ld}
</script>

<style>
{css}
</style>
</head>
<body>
{about_html}
  <div id="bar">
    <span class="title">The World Remembers</span>
    <span class="spacer"></span>
    <button id="btnLens">&#128300; Evidence</button>
    <button id="btnTime">Timeline</button>
    <button id="btnIndex">Chapters</button>
  </div>
  <div id="stage"><div id="book"></div></div>
  <button id="prev" class="nav" aria-label="previous page">&lsaquo;</button>
  <button id="next" class="nav" aria-label="next page">&rsaquo;</button>
  <div id="foot"></div>
  <div id="index"><div class="grid"></div></div>
  <div id="timeline"></div>
  <div id="scrim"></div>
  <aside id="drawer" aria-label="source details"></aside>
<script>
const EMBED = {embed};
const ASSETS = {assets_js};
</script>
<script>
{js}
</script>
</body>
</html>
"""
out = f"{ROOT}/the-world-remembers.html"
open(out, "w").write(html)

# index.html: the SLIM shell — identical head (metadata, JSON-LD, abstract) but
# CSS/JS/data/art loaded as separate files. Keeps the homepage tiny so search
# engines and AI fetchers (many cap fetch size) always reach the abstract; the
# fat single-file edition stays at /the-world-remembers.html and /download/.
slim = html.replace("<style>\n" + css + "\n</style>",
                    '<link rel="stylesheet" href="css/book.css">')
slim = slim.replace("<script>\nconst EMBED = " + embed + ";\nconst ASSETS = " + assets_js + ";\n</script>\n<script>\n" + js + "\n</script>",
                    '<script src="js/engine.js"></script>')
assert len(slim) < 200_000, f"slim index.html unexpectedly large: {len(slim)} bytes — replacement failed?"
index_out = f"{ROOT}/index.html"
open(index_out, "w").write(slim)
# and a copy under /download/, served with Content-Disposition: attachment
# (see _headers) so browsers save the raw .html instead of rendering it
os.makedirs(f"{ROOT}/download", exist_ok=True)
open(f"{ROOT}/download/the-world-remembers.html", "w").write(html)
print(f"WROTE {out} + index.html + download/  ({os.path.getsize(out)/1024/1024:.1f} MB, {len(chapters)} chapters, {len(assets)} assets)")
