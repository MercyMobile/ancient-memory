# NASB 1995 and copy-accuracy review

Base: `2062e813f3b55e1787120a059458c52535789e55`. Input: **World-Remembers-Copy-Audit.xlsx**, 115 items. The owner selected **NASB 1995** and authorized appropriate accuracy corrections, without requiring house-style decisions.

## Implemented

All 25 NASB-labelled verbatim source-card quotations were restored from the specifically selected NASB1995 edition, including cards beyond the audit's initial examples. Two closing-argument quotations and the separately labelled Chronicles comparison bring the checked locations to 28. Each restored location has exact verse references, source URLs, and a fingerprint in `scripture-excerpts.json`. Excerpt extraction removes verse numbers, footnote markers, inline formatting, and incidental HTML whitespace; it does not harmonize different translations. Ellipses identify omissions. Full downloaded Bible chapters are not part of the repository or distributed reading editions.

The main repairs include:

- **Judges:** Benjamin rather than Judah in 1:21; Amorites rather than Philistines in 1:34. The card now also quotes 1:18, which records Judah taking Gaza, Ashkelon, and Ekron. The title and explanation no longer say that the cities were never taken.
- **Deuteronomy:** removed invented/garbled wording and the claim that the Edomites were descendants of the Horites. The sons of Esau dispossess the Horites. Emim/Moab, Horites/Seir, and Zamzummin/Ammon are distinguished, as are the prohibited territories and the campaigns against Sihon and Og.
- **Joshua:** restored 10:36–37, 40 and 11:21–22; corrected the card's title and its geographical connections.
- **Samuel/Chronicles:** the Samuel quotation is no longer silently harmonized to Chronicles. Saph/Sippai, Jaare-oregim/Jair, Goliath/Lahmi, and Gob/Gezer remain visible in separately cited passages.
- **Genesis, Job, Psalms, Isaiah, and the other biblical cards:** replaced mixed NIV/NKJV/NASB wording with NASB 1995, retaining LORD and the edition's words. The Genesis 6 quotation now reads Nephilim, not a different translation's giants. The Goliath measurements retain their full verse context.
- **Deuteronomy 32/Psalm 82:** the main quotation follows NASB 1995. Qumran and Greek readings, and the literal alternative in the Psalm's footnote, remain explicitly identified in notes. They are not relabelled NASB quotations.
- **Josephus:** restored “be mistaken” in Antiquities 3.186, fixed misdirected book links, distinguished a report of displayed bones from an explicit claim of personal inspection, and corrected the count of cited books.
- **Other accuracy items:** cherub/cherubim number agreement, xiù spelling, ʻokina in editorial names, filopodial spelling and units, the Enochic adjective, Anishinaabe/Algonquin/Algonquian distinctions, the annual drift comparison, stale corpus counts, and mismatched chapter titles.

## Research citations checked where the audit required them

**Mantle water:** the March 2026 paper is Song et al., *Communications Earth & Environment* **7**, 265, published 25 March 2026, DOI [10.1038/s43247-026-03379-1](https://doi.org/10.1038/s43247-026-03379-1). The earlier “Nature Comm” attribution was incorrect. Both affected cards now identify this paper and distinguish its mineral-storage experiment from claims about a global water inventory or a dated historical discharge. The natural ringwoodite result remains associated with Pearson et al., *Nature* (2014), DOI [10.1038/nature13080](https://doi.org/10.1038/nature13080).

**Antikythera:** [the authors' manuscript, arXiv:2412.07023v3](https://arxiv.org/abs/2412.07023v3), distinguishes the sidereal, synodic, anomalistic, and draconic cycles from the three indicating pointers in the proposed eclipse reconstruction. The text identifies reconstruction of missing gearing as reconstruction, not recovery of a complete original train.

**Daniel:** the note now distinguishes seventy weeks from sixty-nine, identifies the Christian reading, and states the decree/calendar assumptions before calculating dates. Simple elapsed-year arithmetic without a year zero gives 26 CE from 458 BCE and 39 CE from 445 BCE for 483 years. A generic reference to Qumran Daniel manuscripts is no longer presented as proof that a particular fragment contains Daniel 9:24–27. This is not a new adjudication of the book's composition date.

Primary quotation checks:

- [Judges 1, NASB 1995](https://www.biblegateway.com/passage/?search=Judges+1&version=NASB1995)
- [Deuteronomy 2–3, NASB 1995](https://www.biblegateway.com/passage/?search=Deuteronomy+2-3&version=NASB1995)
- [2 Samuel 21, NASB 1995](https://www.biblegateway.com/passage/?search=2+Samuel+21&version=NASB1995)
- [1 Chronicles 20, NASB 1995](https://www.biblegateway.com/passage/?search=1+Chronicles+20&version=NASB1995)
- [Psalm 82, NASB 1995, including footnotes](https://www.biblegateway.com/passage/?search=Psalm+82&version=NASB1995)
- [Greek Deuteronomy 32 (Swete)](https://biblehub.com/sepd/deuteronomy/32.htm)
- [Josephus, Antiquities 3.186, Whiston](https://lexundria.com/j_aj/3.186/wst)

## Scope and preservation

`copy-audit-disposition.json` accounts for all 115 rows: 107 were corrected or addressed by a source-based replacement; eight purely stylistic choices were retained. The original owner's decision cells are not retroactively filled with fabricated approvals. Historical quotation spellings, identifiers, URLs, and the labels on Adams's chronology are not subject to blanket style replacement.

The bibliography and machine summary are generated from current data: 14 chapters, 153 source cards, 112 evidence-lens cards, 41 artifact records, 12 witness profiles, and 32 catalogue entries. The complete text edition now retains source hyperlinks as well as citations. NASB 1995 copyright and edition credits appear in the reading editions and bibliography; a blanket claim that every translation is public domain has been removed.

No artwork, CSS, or JavaScript engine is edited. The mobile page-isolation fix and pop-up timing are protected by file hashes and the existing browser regression test. The atlas data and its historic labels are unchanged.

This pass corrects the supplied copy audit and directly affected claims. It does not certify every archaeological, astronomical, biological, chronological, or theological argument in the book as independently verified, and it does not re-translate every non-biblical source. Sources and interpretations remain inspectable rather than being silently combined.

## Reproduction

```sh
python3 tools/build_reference_docs.py
python3 tools/build_standalone.py
python3 tools/build_text.py
python3 tools/test_copy_accuracy.py
python3 tools/test_mazzaroth.py
node --check js/engine.js
# With Playwright and Chromium installed:
python3 tools/test_page_visibility.py
```

The quote fingerprints are regression checks against the reviewed output, not substitutes for checking a source. `scripture-excerpts.json` records where to inspect those sources.
