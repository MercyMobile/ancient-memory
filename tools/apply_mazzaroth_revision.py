#!/usr/bin/env python3
"""Apply the approved, source-backed Mazzaroth revision on its review branch."""
from __future__ import annotations
import copy
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / 'data/chapters/mazzaroth.json'
BOOK = ROOT / 'data/book.json'
TEST = ROOT / 'tools/test_mazzaroth.py'
TITLE = 'Mazzaroth — Bonds, Measure, and Appointed Times'
INTERNAL_WORK = 'Job alone — weight, measure, binding, and release'
PLEIADES_TITLE = 'The Pleiades — a measured gravitationally bound core'
ORION_TITLE = 'Orion — measured expansion in named stellar associations'


def link(label: str, url: str) -> dict[str, str]:
    return {'label': label, 'url': url}


def write_json(path: Path, value: object) -> None:
    original = path.read_text(encoding='utf-8')
    match = re.search(r'\n( +)"', original)
    indent = len(match.group(1)) if match else 1
    path.write_text(json.dumps(value, ensure_ascii=False, indent=indent) + '\n', encoding='utf-8')


raw = CHAPTER.read_bytes()
blob = subprocess.check_output(['git', 'hash-object', str(CHAPTER)], text=True).strip()
if blob != '104c123a8a90bd7d560ecb7ee572b57f8a06347c':
    raise SystemExit('The reviewed chapter has changed; reconcile before applying this revision.')
if TEST.exists():
    raise SystemExit('Existing tools/test_mazzaroth.py will not be overwritten.')
chapter = json.loads(raw)
old = copy.deepcopy(chapter)
book = json.loads(BOOK.read_text(encoding='utf-8'))
old_book = copy.deepcopy(book)
assert chapter['id'] == 'mazzaroth'
assert chapter['sources'][0]['work'] == 'Mazzaroth — Job 38:31–33'
assert chapter['science']['evidence'][0]['title'] == 'The Pleiades really are bound together. Orion is not.'

chapter['motif'] = TITLE
chapter['summary'] = (
    'Job names the Pleiades and Orion, then asks about binding and loosening. '
    'The next questions concern Mazzaroth at its appointed time, the guidance of another celestial formation, '
    'and the ordinances of the heavens with their rule over Earth. Elsewhere in the same book, the wind has '
    'weight, the waters have measure, and rain and sea have prescribed limits. The recurring vocabulary is '
    'concrete: measure, limits, binding, release, timing, and governance. Follow the Hebrew words through Job, '
    'check the ancient Greek translation, then place the wording beside measurements of the Pleiades and '
    'named stellar populations in Orion. The text, the proposed etymologies, and the astronomical measurements '
    'are presented separately so each connection can be inspected.'
)
first = chapter['sources'][0]
first['quote'] = '“Can you tie up the chains of the Pleiades, Or untie the cords of Orion?”'
first['translation'] = (
    'New American Standard Bible, 2020 text (NASB), © The Lockman Foundation. '
    'The quotation is Job 38:31; the following verses are summarized in the notes. '
    'NASB translates Mazzaroth in 38:32 as a constellation and identifies the Hebrew term in its footnote.'
)
first['citation'] = 'Job 38:31 (NASB 2020); context: Job 38:31–33. Hebrew text, BDB/NAS lexical entries, and Greek Job are linked below.'
first['notes'] = '''THE HEBREW RECORD
הַתְקַשֵּׁר מַעֲדַנּוֹת כִּימָה אוֹ־מֹשְׁכוֹת כְּסִיל תְּפַתֵּחַ
Job 38:31 pairs an action of binding with Kimah, identified as the Pleiades, and an action of opening or loosening with Kesil, identified as Orion. These remain questions about what the addressee can do; the grammar does not state that either group is presently contracting or dispersing.

BINDING AND RELEASE — THE WORDS
• הַתְקַשֵּׁר — hateqashsher, from קשר (qashar): bind or tie. BDB describes the Piel use here as binding fast.
• מַעֲדַנּוֹת — maʿadannot: bonds or bands in this construction. BDB proposes a connection with ענד (ʿanad, bind) through a transposition of consonants or a textual error. That derivation is proposed, rather than as secure as the binding verb itself.
• מֹשְׁכוֹת — moshekhot: cords. The NAS lexical entry derives the noun from משך (mashakh), draw or pull. The noun denotes cords; its relationship to a drawing verb is lexical evidence, not a technical definition of gravitational attraction.
• תְּפַתֵּחַ — tefatteah, from פתח (pataḥ): open; with cords as its object, loosen or release.

THE SAME ROOTS INSIDE JOB
Job 39:5 uses pataḥ for releasing a wild donkey's bonds. Job 41:1 uses mashakh for drawing Leviathan out with a fishhook. The latter is Job 40:25 in Masoretic Hebrew numbering; references in the chapter otherwise follow NASB/English numbering. These uses check the meanings of opening and drawing within the same book. They do not make an animal's harness and a celestial relationship the same mechanism.

THE ANCIENT GREEK WITNESS
Greek Job 38:31, in Swete's edition, reads: συνῆκας δὲ δεσμὸν Πλειάδος, καὶ φραγμὸν Ὠρίωνος ἤνοιξας;
It asks about understanding the Pleiades' bond (desmos) and opening Orion's enclosure or barrier (phragmos). The first action differs from the Hebrew binding question, but the constellation identifications and the language of bond and restraint are present in the ancient translation tradition. This is a translation witness, not a second astronomical observation.

MAZZAROTH — TIMING FIRST, ETYMOLOGY SECOND
Job 38:32 places מַזָּרוֹת (Mazzaroth) with בְּעִתּוֹ (beʿitto), in its time, rendered seasonally in the NASB. Bringing it forth at that time is explicit in the sentence.
The NAS lexicon lists the word's derivation as uncertain. BDB proposes that it corresponds to מַזָּלוֹת (mazzalot) in 2 Kings 23:5; BDB in turn proposes an Akkadian/Assyrian loan behind that related form, manzaltu or mazaltu, station or abode. These are successive lexical proposals. They should not be compressed into an certain assertion that Mazzaroth literally means stations, nor used by themselves to establish the date or direction of astronomical knowledge transmission.
The Greek text retains Μαζουρὼθ in 38:32. Transliteration alone does not establish why a translator retained a term or how much the translator knew. Job does not enumerate twelve signs or equal thirty-degree divisions in these verses.

THE SEQUENCE IN THE TEXT
38:31 — binding and release.
38:32 — appointed time and guidance.
38:33 — heavenly ordinances and their rule over Earth.
The sequence and the vocabulary can be documented without assigning a modern physical mechanism to every word. The accompanying evidence cards identify the measured stellar populations precisely.

LEXICAL SOURCES
The linked BDB and NAS Exhaustive Concordance entries supply the lexical evidence. Their entries are distinguished from the separate devotional Topical Lexicon material on the same hosting pages.'''.replace('an certain', 'a certain')
first['links'] = [
    link('Job 38:31–33 — NASB 2020', 'https://www.biblegateway.com/passage/?search=Job%2038%3A31-33&version=NASB'),
    link('Job 38:31 — Hebrew text', 'https://biblehub.com/text/job/38-31.htm'),
    link('Qashar — BDB and NAS lexical entries', 'https://biblehub.com/hebrew/7194.htm'),
    link('Maʿadannot — BDB proposed derivation', 'https://biblehub.com/hebrew/4575.htm'),
    link('Moshekhot — BDB and NAS lexical entries', 'https://biblehub.com/hebrew/4189.htm'),
    link('Pataḥ — BDB and NAS lexical entries', 'https://biblehub.com/hebrew/6605.htm'),
    link('Mazzaroth — BDB and NAS entries', 'https://biblehub.com/hebrew/4216.htm'),
    link('Mazzalot — BDB proposed Akkadian connection', 'https://biblehub.com/hebrew/4208.htm'),
    link('Greek Job 38 — Swete text', 'https://biblehub.com/sepd/job/38.htm'),
]

internal = {
    'culture': 'hebrew', 'work': INTERNAL_WORK, 'survivor': 'Job',
    'traditionEra': first['traditionEra'], 'textRecorded': first['textRecorded'],
    'provenance': 'The Hebrew text of Job. This card compares vocabulary within the same book; it does not add an independent witness.',
    'quoteType': 'paraphrase',
    'quote': (
        'Job 28:25 speaks of assigning weight to the wind and measuring the waters. '
        'The next verse assigns a prescription to rain; Job 38:10 sets a boundary for the sea. '
        'Job 38:31–33 moves from binding and release to appointed time, guidance, and heavenly ordinances. '
        'Job 39:5 uses the opening verb for releasing an animal’s bonds; Job 41:1 uses the drawing verb with a fishhook.'
    ),
    'translation': 'Faithful summary of the cited Hebrew passages, checked against the NASB. Not a verbatim quotation.',
    'citation': 'Job 28:25–26; 38:10, 31–33; 39:5; 41:1 (NASB/English numbering; the last is Hebrew Job 40:25).',
    'motifMatches': ['the heavens are bound / held by something', 'the stations rise in their appointed season'],
    'notes': '''WEIGHT AND MEASURE
Job 28:25 uses מִשְׁקָל (mishqal), weight, with the wind, and מִדָּה (middah), measure, with the waters. These are the terms in the Hebrew text; no modern account of atmospheric pressure is supplied by the verse.

PRESCRIBED LIMITS AND ORDINANCES
Job 28:26 uses חֹק (ḥoq), a prescription or prescribed limit, concerning rain. Job 38:10 uses חֻקִּי (ḥuqqi), the noun with a first-person suffix, for the sea's boundary. Job 38:33 uses the related חֻקּוֹת (ḥuqqot), ordinances, for the heavens. The relationship is in the Hebrew word family, not just in similar English translations.

DRAWING AND OPENING
The root משך (mashakh) behind Orion's cords also occurs in drawing with a fishhook in Job 41:1. The root פתח (pataḥ) behind loosening Orion's cords also occurs in opening the donkey's bonds in Job 39:5. The nouns for the cords/bonds in the two passages are not identical; the repeated element in that comparison is the verb.

DOCUMENTED PATTERN
Weight and measure; prescribed limits; binding and release; appointed time; heavenly ordinances. Each item has a verse-level reference. This card records vocabulary and its uses rather than reconstructing the author's unrecorded explanation of a physical mechanism.''',
    'links': [
        link('Job 28:25 — weight and measure', 'https://biblehub.com/text/job/28-25.htm'),
        link('Job 28:26 — prescribed limit', 'https://biblehub.com/text/job/28-26.htm'),
        link('Job 38:10 — the sea’s boundary', 'https://biblehub.com/text/job/38-10.htm'),
        link('Job 38:33 — heavenly ordinances', 'https://biblehub.com/text/job/38-33.htm'),
        link('Job 39:5 — releasing bonds', 'https://biblehub.com/text/job/39-5.htm'),
        link('Job 41:1 — drawing with a fishhook', 'https://biblehub.com/text/job/41-1.htm'),
    ],
    'cutouts': copy.deepcopy(first.get('cutouts', [])),
    'tYear': first['tYear'], 'xYear': first['xYear'],
}
chapter['sources'].insert(1, internal)
chapter['science']['intro'] = (
    'First establish the wording: binding and release, appointed time, and heavenly ordinances. '
    'Then identify the observed populations and the measurements. The Pleiades study concerns a bound cluster core '
    'within a larger dispersing complex; the Orion study concerns named stellar associations, not an undifferentiated '
    'constellation. Their results are set beside Job 38:31 without turning a lexical meaning into a measured force.'
)
pleiades = {
    'title': PLEIADES_TITLE,
    'observation': (
        'Boyle, Bouma and Mann (2025) identify the Pleiades as the bound core of a larger, coeval stellar complex. '
        'Their analysis combines TESS rotation measurements with Gaia motions, and checks elemental abundances '
        'and reconstructed trajectories to investigate the stars’ shared origin.'
    ),
    'tie': 'Job 38:31 pairs the Pleiades with a binding action. The measured bound core supplies a specific physical relationship to compare with that wording.',
    'source': 'A. W. Boyle, L. G. Bouma and A. W. Mann, “Lost Sisters Found: TESS and Gaia Reveal a Dissolving Pleiades Complex,” The Astrophysical Journal 994, 24 (2025), doi:10.3847/1538-4357/ae0724; arXiv:2511.07533.',
    'url': 'https://arxiv.org/abs/2511.07533',
    'notes': (
        'MEASUREMENT: the bound Pleiades core and the extended Greater Pleiades Complex are distinct scales in the study. '
        'The larger population is dispersing; bound does not mean every member remains permanently fixed relative to every other.\n\n'
        'TEXTUAL COMPARISON: the verse uses a binding question. The physical finding and the ancient wording can be displayed together; '
        'the paper does not investigate Job or establish the author’s intended mechanism.'
    ),
}
orion = {
    'title': ORION_TITLE,
    'observation': (
        'Sánchez-Sanjuán and colleagues (2024) analysed young populations in the Orion star-forming complex using '
        'Gaia DR3 positions, parallaxes and proper motions, supplemented by APOGEE-2 and GALAH DR3 radial velocities. '
        'They found evidence of general expansion in Orion OB1 around a common centre and projected ballistic '
        'expansion in the Lambda Orionis association.'
    ),
    'tie': 'Job 38:31 pairs Orion with opening or loosening cords. Measured expansion in named Orion populations is the comparison to inspect, rather than stopping at the constellation’s visible outline.',
    'source': 'S. Sánchez-Sanjuán et al., “Kinematic study of the Orion Complex: analysing the young stellar clusters from big and small structures,” Monthly Notices of the Royal Astronomical Society 534, 2566–2584 (2024), doi:10.1093/mnras/stae2157.',
    'url': 'https://doi.org/10.1093/mnras/stae2157',
    'notes': (
        'MEASUREMENT SCOPE: Orion OB1 and Lambda Orionis are identified stellar populations. The study’s expansion '
        'results must not be silently relabelled as a measurement of the entire classical constellation or specifically '
        'of its three Belt stars.\n\n'
        'TEXTUAL COMPARISON: the Hebrew is a question about loosening, not a declaration of a measured expansion rate. '
        'Connecting Kesil’s cords to one of these particular populations requires an identification in addition to the '
        'lexical and astronomical evidence presented here.'
    ),
}
chapter['science']['evidence'] = [pleiades, orion] + old['science']['evidence'][1:]

meta = [item for item in book['chapters'] if item['id'] == 'mazzaroth']
assert len(meta) == 1
meta[0]['motif'] = TITLE
meta[0]['teaser'] = (
    'Job’s Hebrew vocabulary of binding, release, measure, limits, and appointed time, '
    'checked within the book and beside an ancient Greek translation, a bound Pleiades core, '
    'and measured expansion in named Orion populations.'
)

# Limit the edit to the approved section and preserve all unrelated data and art.
for key in old:
    if key not in {'motif', 'summary', 'sources', 'science'}:
        assert chapter[key] == old[key], key
assert chapter['sources'][2:] == old['sources'][1:]
assert chapter['science']['evidence'][2:] == old['science']['evidence'][1:]
assert chapter['science']['backdrop'] == old['science']['backdrop']
for key in old_book:
    if key != 'chapters':
        assert book[key] == old_book[key], key
for before, after in zip(old_book['chapters'], book['chapters']):
    if before['id'] != 'mazzaroth':
        assert before == after
    else:
        assert {k: v for k, v in before.items() if k not in {'motif', 'teaser'}} == {k: v for k, v in after.items() if k not in {'motif', 'teaser'}}

bibliography = '''

## Mazzaroth revision — bonds, measure, and appointed times

This revision separates the Hebrew wording, proposed lexical derivations, ancient translation evidence, and modern measurements. The intra-Job card compares passages within one work; the Greek translation is a textual witness, not an independent astronomical observation. Existing comparative-cultural cards are retained.

### Text and lexicons

- **Job 38:31–33, NASB 2020.** The displayed quotation is verse 31; context is summarized. [Read the passage](https://www.biblegateway.com/passage/?search=Job%2038%3A31-33&version=NASB). Scripture copyright remains with The Lockman Foundation.
- **Hebrew Job 38:31.** [Verse-level text](https://biblehub.com/text/job/38-31.htm).
- **Brown–Driver–Briggs and NAS Exhaustive Concordance entries:** [qashar, H7194](https://biblehub.com/hebrew/7194.htm); [maʿadannot, H4575](https://biblehub.com/hebrew/4575.htm); [moshekhot, H4189](https://biblehub.com/hebrew/4189.htm); [pataḥ, H6605](https://biblehub.com/hebrew/6605.htm). BDB’s proposed derivation for maʿadannot remains a proposal; the cord noun’s drawing-root derivation is not a technical definition of gravity.
- **Mazzaroth and mazzalot:** [H4216](https://biblehub.com/hebrew/4216.htm) and [H4208](https://biblehub.com/hebrew/4208.htm). BDB proposes a relationship between the two forms and an Akkadian/Assyrian loan behind the latter. NAS lists Mazzaroth’s derivation as uncertain. The appointed-time phrase is direct textual evidence, independent of that proposed etymological chain.
- **Greek Job 38:31–32, Swete edition.** [Greek text](https://biblehub.com/sepd/job/38.htm). Bond/enclosure vocabulary and Greek constellation names are evidence of the translation tradition; retaining Mazzaroth in Greek letters does not establish the translator’s reason for doing so.
- **Internal vocabulary checks:** [Job 28:25](https://biblehub.com/text/job/28-25.htm), [28:26](https://biblehub.com/text/job/28-26.htm), [38:10](https://biblehub.com/text/job/38-10.htm), [38:33](https://biblehub.com/text/job/38-33.htm), [39:5](https://biblehub.com/text/job/39-5.htm), [41:1](https://biblehub.com/text/job/41-1.htm). References follow NASB/English numbering; Job 41:1 is Hebrew Job 40:25.

Lexical references above are to the named BDB/NAS entries, not the separate devotional Topical Lexicon sections on the hosting pages. Short glosses and passage summaries are identified as such rather than presented as verbatim NASB quotations.

### Astronomical measurements

- **Boyle, Andrew W.; Bouma, Luke G.; Mann, Andrew W. (2025).** “Lost Sisters Found: TESS and Gaia Reveal a Dissolving Pleiades Complex.” *The Astrophysical Journal* **994**, 24. [doi:10.3847/1538-4357/ae0724](https://doi.org/10.3847/1538-4357/ae0724); [open manuscript, arXiv:2511.07533](https://arxiv.org/abs/2511.07533). The bound core and the extended complex are kept distinct.
- **Sánchez-Sanjuán, Sergio, et al. (2024).** “Kinematic study of the Orion Complex: analysing the young stellar clusters from big and small structures.” *Monthly Notices of the Royal Astronomical Society* **534**, 2566–2584. [doi:10.1093/mnras/stae2157](https://doi.org/10.1093/mnras/stae2157); [open article](https://academic.oup.com/mnras/article/534/3/2566/7760396). The named associations are not substituted for the entire constellation or its Belt.

The papers establish measured stellar relationships, not what Job’s author knew. The text’s binding/loosening questions are preserved as questions. No date of Job, gravitational equation, or route of knowledge transmission is inferred from their juxtaposition.
'''
sources_path = ROOT / 'SOURCES.md'
sources_text = sources_path.read_text(encoding='utf-8')
assert '## Mazzaroth revision — bonds, measure, and appointed times' not in sources_text

TEST_TEXT = r'''#!/usr/bin/env python3
"""Regression checks for Mazzaroth data and the generated reading editions.
Run after tools/build_standalone.py and tools/build_text.py.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
chapter = json.loads((ROOT / 'data/chapters/mazzaroth.json').read_text(encoding='utf-8'))
book = json.loads((ROOT / 'data/book.json').read_text(encoding='utf-8'))
assert chapter['id'] == 'mazzaroth'
assert chapter['motif'] == 'Mazzaroth — Bonds, Measure, and Appointed Times'
meta = next(item for item in book['chapters'] if item['id'] == 'mazzaroth')
assert meta['motif'] == chapter['motif']
assert 'Job’s Hebrew vocabulary' in meta['teaser']
assert sum(s['work'] == 'Job alone — weight, measure, binding, and release' for s in chapter['sources']) == 1
notes = chapter['sources'][0]['notes']
for token in ('קשר', 'מַעֲדַנּוֹת', 'משך', 'פתח', 'בְּעִתּוֹ', 'δεσμὸν', 'φραγμὸν', 'proposed', 'Job 40:25'):
    assert token in notes, token
assert chapter['sources'][0]['quote'] == '“Can you tie up the chains of the Pleiades, Or untie the cords of Orion?”'
assert chapter['sources'][1]['quoteType'] == 'paraphrase'
for token in ('מִשְׁקָל', 'מִדָּה', 'חֹק', 'חֻקִּי', 'חֻקּוֹת'):
    assert token in chapter['sources'][1]['notes'], token
astro = chapter['science']['evidence'][:2]
assert astro[0]['url'] == 'https://arxiv.org/abs/2511.07533'
assert astro[1]['url'] == 'https://doi.org/10.1093/mnras/stae2157'
assert 'bound core' in astro[0]['observation']
assert 'Orion OB1' in astro[1]['observation'] and 'Lambda Orionis' in astro[1]['observation']
assert 'three Belt stars' in astro[1]['notes']
changed_section = '\n'.join((chapter['summary'], notes, chapter['science']['intro'], *(c['notes'] for c in astro)))
for removed in ('THIS CARD EXISTS TO STOP A BAD ARGUMENT', 'AND THE TRANSLATORS DIDN\'T KNOW EITHER', 'the other is a trick of perspective'):
    assert removed not in changed_section, removed
for source in chapter['sources'][:2]:
    assert source['citation'] and source['provenance']
    assert source['links'] and all(x['url'].startswith('https://') for x in source['links'])
for path in (ROOT / 'data').rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8'))
html = (ROOT / 'the-world-remembers.html').read_text(encoding='utf-8')
download_html = (ROOT / 'download/the-world-remembers.html').read_text(encoding='utf-8')
assert html == download_html, 'Offline HTML copies differ'
match = re.search(r'const EMBED = (\{.*?\});\s*const ASSETS = ', html, re.S)
assert match, 'Embedded JSON not found'
embed = json.loads(match.group(1))
assert embed['chapters']['mazzaroth'] == chapter, 'Bundled chapter is stale'
assert embed['book'] == book, 'Bundled metadata is stale'
assert len(embed['chapters']) == len(book['chapters'])
assets_match = re.search(r'const ASSETS = (\{.*?\});\s*</script>', html, re.S)
assert assets_match, 'Embedded artwork map not found'
assets = json.loads(assets_match.group(1))
assert assets[chapter['backdrop']].startswith('data:image/')
assert assets[chapter['science']['backdrop']].startswith('data:image/')
for item in chapter['scene']:
    assert 'art/cutouts/' + item['cutout'] + '.webp' in assets
text = (ROOT / 'download/the-world-remembers.md').read_text(encoding='utf-8')
for token in (chapter['motif'], chapter['summary'], notes, chapter['sources'][1]['notes'], astro[0]['title'], astro[1]['title']):
    assert token in text, 'Text edition is missing revised content'
index = (ROOT / 'index.html').read_text(encoding='utf-8')
assert chapter['motif'] in index and meta['teaser'] in index
assert '<script src="js/engine.js"></script>' in index
assert len(index) < 200_000
assert '## Mazzaroth revision — bonds, measure, and appointed times' in (ROOT / 'SOURCES.md').read_text(encoding='utf-8')
print('PASS: Hebrew and Greek evidence, internal Job references, exact study populations, source links, JSON, metadata, both HTML copies, embedded assets, and complete text edition.')
'''
compile(TEST_TEXT, str(TEST), 'exec')
write_json(CHAPTER, chapter)
write_json(BOOK, book)
sources_path.write_text(sources_text.rstrip() + bibliography + '\n', encoding='utf-8')
TEST.write_text(TEST_TEXT, encoding='utf-8')
print('Applied Mazzaroth revision; unrelated chapters, art, animation, and closing argument preserved.')
