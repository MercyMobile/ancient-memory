#!/usr/bin/env python3
"""The presence matrix must be exactly what the source cards say — never hand-edited, never stale."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_matrix import build, ROUTES

m = json.loads((ROOT / 'data/matrix.json').read_text(encoding='utf-8'))
fresh = build()
assert m['cells'] == fresh['cells'] and m['summary'] == fresh['summary'] and m['detail'] == fresh['detail'], \
    'data/matrix.json is stale: run python3 tools/build_matrix.py'
book = json.loads((ROOT / 'data/book.json').read_text(encoding='utf-8'))
assert m['summary']['cultures'] == len(book['cultures']), 'every culture must appear as a row'
for c in m['cultures']:
    assert c['route'] in ROUTES and c['routeNote'], f"{c['key']} lacks a route or a route note"
    assert c['cards'] >= 1, f"{c['key']} is defined but never quoted"
S = m['summary']
assert S['strong'] + S['weak'] + S['absent'] == S['cells'] == S['chapters'] * S['cultures']
html = (ROOT / 'the-world-remembers.html').read_text(encoding='utf-8')
assert m['rule'][:60] in html and '"matrix":' in html and 'Presence matrix' in html, 'matrix not embedded in the standalone book'
plain = (ROOT / 'llms-full.txt').read_text(encoding='utf-8')
assert '# Presence matrix — which people, which motif' in plain and m['rule'][:60] in plain, 'matrix missing from the text edition'
assert all(f"| {c['name']} | {c['route']} |" in plain for c in m['cultures']), 'text-edition matrix rows incomplete'
print(f"PASS: matrix matches the cards ({S['cells']} cells: {S['strong']} strong, {S['weak']} weak, {S['absent']} empty); "
      f"{S['cultures']} peoples routed; embedded in the book and the text edition.")
