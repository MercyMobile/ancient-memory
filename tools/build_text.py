#!/usr/bin/env python3
"""Build the model-readable text edition: every word of the book (chapters,
source cards, quotes, citations, notes, evidence lenses, finds, witnesses)
as one markdown file with no images — small enough to upload to an AI.

    python3 tools/build_text.py   ->  download/the-world-remembers.md
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
book = json.load(open(f"{ROOT}/data/book.json"))
arts = json.load(open(f"{ROOT}/data/artifacts.json"))["artifacts"]
atlas = json.load(open(f"{ROOT}/data/atlas.json"))
cultures = book["cultures"]

L = []
w = L.append
w(f"# {book['title']}")
w(f"*{book['subtitle']}*\n")
w(book["intro"] + "\n")
w(f"**How to read the sources:** {book['motifKey']}\n")

for chm in book["chapters"]:
    ch = json.load(open(f"{ROOT}/{chm['file']}"))
    w(f"\n---\n\n# {chm['spinePosition']}. {ch.get('motif', chm['motif'])}  ({chm['era']})\n")
    if ch.get("summary"):
        w(ch["summary"] + "\n")
    if ch.get("intro"):
        w(ch["intro"] + "\n")
    if ch.get("exhibit"):
        w(f"**Companion exhibit:** [{ch['exhibit']['label']}](https://ancient-memory.pages.dev{ch['exhibit']['url']}) — {ch['exhibit'].get('blurb','')}\n")
    tags = ch.get("sharedMotifTags") or []
    if tags:
        w("**Shared story-elements tracked in this chapter:** " + "; ".join(tags) + "\n")

    for s in ch.get("sources", []):
        cu = cultures.get(s["culture"], {})
        w(f"\n## {cu.get('name', s['culture'])} ({cu.get('region','')}) — {s['work']}")
        if s.get("survivor") and s["survivor"] != "—":
            w(f"**Central figure:** {s['survivor']}  ")
        w(f"**Tradition era:** {s.get('traditionEra','?')} · **Text recorded:** {s.get('textRecorded','?')}  ")
        if s.get("provenance"):
            w(f"**Provenance:** {s['provenance']}  ")
        kind = "VERBATIM QUOTE" if s.get("quoteType") == "verbatim" else "FAITHFUL SUMMARY (paraphrase)"
        w(f"\n> [{kind}] {s.get('quote','')}\n")
        if s.get("translation"):
            w(f"**Translation:** {s['translation']}  ")
        if s.get("citation"):
            w(f"**Citation:** {s['citation']}  ")
        if s.get("motifMatches"):
            w(f"**Shared elements matched:** {'; '.join(s['motifMatches'])}  ")
        for source_link in s.get("links", []):
            w(f"[Source: {source_link['label']}]({source_link['url']})  ")
        if s.get("notes"):
            w(f"**Notes:** {s['notes']}")

    ev = [e for e in ch.get("evidence", []) if e in arts]
    if ev:
        w(f"\n### ⛏ The ground confirms — physical finds tied to this chapter\n")
        for eid in ev:
            a = arts[eid]
            w(f"- **{a['name']}** ({a['date']}; {a['site']}) — confirms: {a['confirms']}. "
              f"{a['detail']} *Status:* {a['status']} *Citation:* {a['citation']}")

    sci = ch.get("science")
    if sci:
        w(f"\n### 🔬 The evidence lens\n")
        w(sci.get("intro", "") + "\n")
        for c in sci.get("evidence", []):
            w(f"**{c['title']}**  ")
            w(f"Observation: {c['observation']}  ")
            if c.get("tie"):   w(f"What it points to: {c['tie']}  ")
            if c.get("notes"): w(f"Notes: {c['notes']}  ")
            if c.get("source"): w(f"Source: {c['source']}")
            if c.get("url"): w(f"[Research source]({c['url']})")
            w("")

    for wt in ch.get("witnesses", []):
        w(f"\n## Witness: {wt['name']} ({wt.get('place','')}; {wt.get('era','')})")
        w(f"**Preserved:** {wt.get('preserved','')}  ")
        w(wt.get("story", ""))

w("\n---\n\n*Full bibliography, translation licensing, and verification policy: SOURCES.md in the project repository. "
  "Scripture quotations taken from the New American Standard Bible® (NASB 1995), Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by permission. https://www.lockman.org/. "
  "Other translations and paraphrases are credited per entry; their rights vary by source.*")

# ---- the spine: the closing argument, after every chapter ----
sp = book.get("spine")
if sp:
    w("\n---\n")
    w(f"# {sp['title']}")
    w(f"*{sp.get('subtitle','')}* — {sp.get('eyebrow','')}\n")
    w(sp.get("lede", "") + "\n")
    for m in sp.get("movements", []):
        w(f"## {m['stamp']} — {m['title']}\n")
        for para in m.get("body", []):
            w(para + "\n")
        if m.get("quote"):
            w(f"> {m['quote']['text']}\n>\n> — {m['quote']['cite']}\n")
        if m.get("note"):
            w(f"**Note:** {m['note']}\n")
    fig = sp.get("figure")
    if fig:
        w(f"### {fig['title']}\n")
        w(fig.get("caption", "") + "\n")
        w("| Generation | Years | Change |")
        w("|---|---:|---:|")
        prev = None
        for nm, age in fig["pre"] + fig["post"]:
            delta = "—" if prev is None else ("+" if age - prev > 0 else "") + str(age - prev)
            w(f"| {nm} | {age} | {delta} |")
            prev = age
        w("")
    w("## What the picture is\n")
    for para in sp.get("closing", []):
        w(para + "\n")
    w("## Still to recover\n")
    for para in sp.get("open", []):
        w(f"- {para}")
    w("")

# ---- global atlas: keep chronology and measured ranges visibly distinct ----
w("\n---\n")
w("# World atlas — sources in time\n")
w("Adams's named biblical chronology is shown beside independently dated places and measurements. The 70 CE endpoint is this book's story horizon; later source copies retain their own provenance dates.\n")
w("## Adams's chronology and the story endpoint\n")
for item in atlas["chronology"]:
    w(f"- **{item['date']} — {item['label']}.** {item['detail']} [Source: {item['sourceLabel']}]({item['sourceUrl']})")
w("\n## Around 2250 BCE in parallel places\n")
w("The gold line in the interactive chart marks Adams's 2247 BC label. The 4.2 ka formal boundary is approximately 2250 BCE; the local Mawmluh Cave signal spans centuries.\n")
for item in atlas["window"]["rows"]:
    w(f"- **{item['region']} · {item['title']} ({item['date']}).** {item['basis']} [Source: {item['sourceLabel']}]({item['sourceUrl']})")
early = atlas["outsideWindow"]
w(f"\n**Earlier:** {early['place']} ({early['date']}). {early['detail']} [Source: {early['sourceLabel']}]({early['sourceUrl']})\n")
w(f"**How to read the atlas:** {atlas['method']}\n")

text = "\n".join(L) + "\n"
os.makedirs(f"{ROOT}/download", exist_ok=True)
out = f"{ROOT}/download/the-world-remembers.md"
open(out, "w").write(text)

# A conventional, non-download plain-text corpus for LLMs and a normal HTML
# reading route for agents/browsers that neither execute the book JS nor open
# Content-Disposition: attachment resources.
full_text = f"{ROOT}/llms-full.txt"
open(full_text, "w").write(text)
read_dir = f"{ROOT}/read"
os.makedirs(read_dir, exist_ok=True)
read_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The World Remembers — Complete Text Edition</title>
<meta name="description" content="The complete text, sources, citations, evidence notes, and world atlas from The World Remembers. No JavaScript required.">
<meta name="robots" content="index, follow, max-snippet:-1">
<link rel="canonical" href="https://ancient-memory.pages.dev/read/">
<link rel="alternate" type="text/plain" href="https://ancient-memory.pages.dev/llms-full.txt">
<style>
:root{{color-scheme:light}} body{{margin:0;background:#eee5d2;color:#241b12;font:18px/1.6 Georgia,serif}}
main{{max-width:980px;margin:auto;padding:24px}} nav{{display:flex;gap:18px;flex-wrap:wrap;padding:12px 0 24px}}
a{{color:#68420d}} article{{background:#fffaf0;padding:clamp(20px,5vw,64px);box-shadow:0 8px 30px #503b241f}}
pre{{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}} @media print{{body{{background:white}}article{{box-shadow:none}}}}
</style>
</head>
<body><main>
<nav aria-label="Editions"><a href="/">Interactive storybook</a><a href="/llms-full.txt">Plain text</a><a href="/SOURCES.md">Bibliography</a></nav>
<article aria-label="Complete text of The World Remembers"><pre>{html.escape(text)}</pre></article>
</main></body>
</html>
"""
read_out = f"{read_dir}/index.html"
open(read_out, "w").write(read_html)
print(f"WROTE {out}, {full_text}, and {read_out}  ({len(text)/1024:.0f} KB text)")
