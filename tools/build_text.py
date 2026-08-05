#!/usr/bin/env python3
"""Build the model-readable text edition: every word of the book (chapters,
source cards, quotes, citations, notes, evidence lenses, finds, witnesses)
as one markdown file with no images — small enough to upload to an AI.

    python3 tools/build_text.py   ->  download/the-world-remembers.md
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
book = json.load(open(f"{ROOT}/data/book.json"))
arts = json.load(open(f"{ROOT}/data/artifacts.json"))["artifacts"]
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
            w("")

    for wt in ch.get("witnesses", []):
        w(f"\n## Witness: {wt['name']} ({wt.get('place','')}; {wt.get('era','')})")
        w(f"**Preserved:** {wt.get('preserved','')}  ")
        w(wt.get("story", ""))

w("\n---\n\n*Full bibliography, translation licensing, and verification policy: SOURCES.md in the project repository. "
  "Scripture quotations are from the New American Standard Bible (NASB), © The Lockman Foundation, used by permission; "
  "all other verbatim quotations are from public-domain translations named per entry.*")

os.makedirs(f"{ROOT}/download", exist_ok=True)
out = f"{ROOT}/download/the-world-remembers.md"
open(out, "w").write("\n".join(L) + "\n")
print(f"WROTE {out}  ({os.path.getsize(out)/1024:.0f} KB)")
