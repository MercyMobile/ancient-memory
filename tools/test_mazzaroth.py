#!/usr/bin/env python3
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
assert chapter['sources'][0]['quote'] == '“Can you bind the chains of the Pleiades, Or loose the cords of Orion?”'
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
