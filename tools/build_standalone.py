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
<title>The World Remembers</title>
<meta name="description" content="The first history of the world told through the oldest texts, with a flip to the physical evidence. Interactive pop-up storybook.">
<style>
{css}
</style>
</head>
<body>
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
print(f"WROTE {out}  ({os.path.getsize(out)/1024/1024:.1f} MB, {len(chapters)} chapters, {len(assets)} assets)")
