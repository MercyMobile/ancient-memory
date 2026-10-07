#!/usr/bin/env python3
"""One plain document per chapter: every word of data/chapters/*.json (sources,
quotes, citations, notes, links, physical finds, evidence lens, witnesses) as
ordinary headings and paragraphs. No JSON, no markdown, no web layout.
Picture-placement fields (scene, backdrop, cutouts) are the only things left out.

    python3 tools/build_chapter_docs.py [OUT_DIR]
        -> OUT_DIR (default ~/companion/outputs/storybook-chapters)/NN-<chapter-id>.docx  (+ .pdf via LibreOffice)
"""
import datetime, json, os, subprocess, sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# default lives OUTSIDE the site folder so a deploy never publishes these
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/companion/outputs/storybook-chapters"))
SITE = "https://ancient-memory.pages.dev"

book = json.load(open(f"{ROOT}/data/book.json"))
arts = json.load(open(f"{ROOT}/data/artifacts.json"))["artifacts"]
try:
    digs = json.load(open(f"{ROOT}/data/digsites.json"))
except FileNotFoundError:
    digs = {"sites": [], "artifacts": {}}
dig_by_id = {d["id"]: d for d in digs["sites"]}
cultures = book["cultures"]
NASB = ("Scripture quotations taken from the New American Standard Bible® (NASB 1995), "
        "Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by permission. "
        "https://www.lockman.org/")


def year(y):
    if y is None:
        return None
    return f"about {-y} BCE" if y < 0 else f"about {y} CE"


def new_doc():
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Liberation Serif"
    st.font.size = Pt(11.5)
    st.paragraph_format.space_after = Pt(6)
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(1)
        s.top_margin = s.bottom_margin = Inches(0.9)
    return d


def para(d, text, italic=False, indent=False):
    # keep the source's own paragraph breaks
    for chunk in str(text).split("\n\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        p = d.add_paragraph()
        r = p.add_run(chunk)
        r.italic = italic
        if indent:
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.right_indent = Inches(0.3)


def field(d, label, value):
    if value in (None, "", "—", []):
        return
    p = d.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.add_run(f"{label}: ").bold = True
    p.add_run(str(value))


def build(chm):
    ch = json.load(open(f"{ROOT}/{chm['file']}"))
    n = chm["spinePosition"]
    d = new_doc()

    t = d.add_heading(f"Chapter {n}. {ch.get('motif', chm['motif'])}", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para(d, f"Era: {ch.get('era', chm['era'])}", italic=True)
    para(d, f"From the book: {book['title']}. {book['subtitle']}", italic=True)
    if ch.get("summary"):
        para(d, ch["summary"])
    if ch.get("intro"):
        para(d, ch["intro"])
    if ch.get("exhibit"):
        ex = ch["exhibit"]
        field(d, "Companion exhibit", f"{ex['label']}. {ex.get('blurb', '')} {SITE}{ex['url']}")
    if ch.get("sharedMotifTags"):
        field(d, "Shared story elements tracked in this chapter", "; ".join(ch["sharedMotifTags"]))

    srcs = ch.get("sources", [])
    if srcs:
        d.add_heading(f"The ancient sources ({len(srcs)})", level=1)
        for i, s in enumerate(srcs, 1):
            cu = cultures.get(s["culture"], {})
            who = cu.get("name", s["culture"]) + (f" ({cu['region']})" if cu.get("region") else "")
            d.add_heading(f"{i}. {who}: {s['work']}", level=2)
            field(d, "Central figure", s.get("survivor"))
            field(d, "Tradition era", s.get("traditionEra"))
            field(d, "Text recorded", s.get("textRecorded"))
            if s.get("tYear") is not None or s.get("xYear") is not None:
                parts = []
                if s.get("tYear") is not None:
                    parts.append(f"tradition {year(s['tYear'])}")
                if s.get("xYear") is not None:
                    parts.append(f"written record {year(s['xYear'])}")
                field(d, "Timeline dates used by the book", "; ".join(parts))
            field(d, "Provenance", s.get("provenance"))
            kind = "Verbatim quote" if s.get("quoteType") == "verbatim" else "Faithful summary (paraphrase, not a quote)"
            p = d.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.add_run(f"{kind}:").bold = True
            para(d, s.get("quote", ""), italic=True, indent=True)
            field(d, "Translation", s.get("translation"))
            field(d, "Citation", s.get("citation"))
            field(d, "Shared elements matched", "; ".join(s.get("motifMatches", [])))
            for lk in s.get("links", []):
                field(d, "Source link", f"{lk['label']}: {lk['url']}")
            if s.get("notes"):
                p = d.add_paragraph()
                p.paragraph_format.space_after = Pt(2)
                p.add_run("Notes:").bold = True
                para(d, s["notes"])

    ev = ch.get("evidence", [])
    found = [e for e in ev if e in arts]
    missing = [e for e in ev if e not in arts]
    if ev:
        d.add_heading(f"Physical finds tied to this chapter ({len(found)})", level=1)
        for i, eid in enumerate(found, 1):
            a = arts[eid]
            d.add_heading(f"{i}. {a['name']}", level=2)
            field(d, "Type", a.get("type"))
            field(d, "Period", a.get("period"))
            field(d, "Date", a.get("date"))
            field(d, "Site", a.get("site"))
            field(d, "Confirms", a.get("confirms"))
            if a.get("detail"):
                para(d, a["detail"])
            field(d, "Status", a.get("status"))
            field(d, "Citation", a.get("citation"))
            field(d, "Source link", a.get("url"))
            dig = dig_by_id.get(digs["artifacts"].get(eid))
            if dig:
                field(d, "Dig site record", f"{dig['name']}: {dig['url']}")
        if missing:
            field(d, "Listed in the chapter file but with no record in the artifacts data",
                  ", ".join(missing) + ". The website skips these silently.")

    sci = ch.get("science")
    if sci:
        cards = sci.get("evidence", [])
        d.add_heading(f"The evidence lens ({len(cards)})", level=1)
        if sci.get("intro"):
            para(d, sci["intro"])
        for i, c in enumerate(cards, 1):
            d.add_heading(f"{i}. {c['title']}", level=2)
            field(d, "Observation", c.get("observation"))
            field(d, "What it points to", c.get("tie"))
            if c.get("notes"):
                p = d.add_paragraph()
                p.paragraph_format.space_after = Pt(2)
                p.add_run("Notes:").bold = True
                para(d, c["notes"])
            field(d, "Source", c.get("source"))
            field(d, "Source link", c.get("url"))

    wts = ch.get("witnesses", [])
    if wts:
        d.add_heading(f"Witnesses ({len(wts)})", level=1)
        for i, wt in enumerate(wts, 1):
            d.add_heading(f"{i}. {wt['name']}", level=2)
            field(d, "Place", wt.get("place"))
            field(d, "Era", wt.get("era"))
            field(d, "Kind", wt.get("kind"))
            field(d, "Preserved", wt.get("preserved"))
            if wt.get("story"):
                para(d, wt["story"])
            field(d, "Source link", wt.get("url"))

    d.add_heading("Credits", level=1)
    para(d, NASB)
    para(d, "Other translations and paraphrases are credited per entry; their rights vary by source. "
            "Full bibliography and verification policy: SOURCES.md in the storybook repository.")
    para(d, f"Plain copy made {datetime.date.today().isoformat()} from {chm['file']} "
            f"(the website's data file). Web picture-placement fields were left out; every text field is here.",
         italic=True)

    os.makedirs(OUT, exist_ok=True)
    path = f"{OUT}/{n:02d}-{ch['id']}.docx"
    d.save(path)
    return path, len(srcs), len(found), len(missing), len(sci.get("evidence", [])) if sci else 0, len(wts)


if __name__ == "__main__":
    made = []
    for chm in book["chapters"]:
        path, ns, nf, nm, ne, nw = build(chm)
        made.append(path)
        print(f"{os.path.basename(path):34s} sources {ns:3d}  finds {nf:2d}{f' (+{nm} missing)' if nm else ''}"
              f"  evidence {ne:2d}  witnesses {nw:2d}")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, *made],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\n{len(made)} chapters -> {OUT} (.docx and .pdf)")
