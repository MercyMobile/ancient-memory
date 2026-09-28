#!/usr/bin/env python3
"""Derive the presence matrix (story chapters × cultures) from the source cards.

The matrix is EVIDENCE ABOUT THE BOOK, not about the cultures: a cell says what cards this book holds
for that people on that motif. It is regenerated from data/chapters/*.json on every build and checked by
tools/test_matrix.py, so it can never drift from the sources.

Cell rule (printed on the page):
  strong  — at least one card from that culture in that chapter is a verbatim quotation sharing two or
            more of the chapter's motifs, or any card sharing three or more.
  weak    — the culture has a card in the chapter, but only a paraphrase or a single shared motif.
  absent  — this book holds no card from that culture in that chapter.
"""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
RULE = ("Strong: at least one card from that people in that chapter is a verbatim quotation sharing two or more "
        "of the chapter's motifs, or any card sharing three or more. Weak: the people has a card there, but only a "
        "paraphrase or a single shared motif. Empty: this book holds no card from that people on that motif — which "
        "says nothing about what that people has or has not preserved.")
ROUTES = {
    'same-world': 'Same world as the Hebrew record — the Near East; contact is constant.',
    'route': 'A documented route to the Near East (trade, conquest, script or religion) existed before the text was written down.',
    'late': 'A route existed only late: the text was written down after Christian or Islamic contact, so transmission is possible and has to be weighed.',
    'none': 'No route to the Near East is known before European contact; the text was written down after that contact, by or through outsiders.',
    'catalogue': 'A comparative catalogue, not a people.',
}

def cell_strength(cards):
    best = 0
    for s in cards:
        m = len(s.get('motifMatches') or [])
        strong = (s.get('quoteType') == 'verbatim' and m >= 2) or m >= 3
        best = max(best, 2 if strong else 1)
    return best

def build():
    book = json.loads((ROOT / 'data/book.json').read_text(encoding='utf-8'))
    cults = book['cultures']
    chapters = []
    cells = {}
    detail = {}
    per_culture = collections.defaultdict(lambda: {'cards': 0, 'chapters': set(), 'earliest': None})
    for meta in book['chapters']:
        data = json.loads((ROOT / meta['file']).read_text(encoding='utf-8'))
        srcs = data.get('sources') or []
        if not srcs:
            continue  # the Witnesses chapter carries no source cards
        chapters.append({'id': meta['id'], 'motif': meta['motif'], 'spinePosition': meta.get('spinePosition'), 'tags': data.get('sharedMotifTags', [])})
        by_c = collections.defaultdict(list)
        for s in srcs:
            by_c[s['culture']].append(s)
            pc = per_culture[s['culture']]
            pc['cards'] += 1; pc['chapters'].add(meta['id'])
            x = s.get('xYear')
            if isinstance(x, (int, float)) and (pc['earliest'] is None or x < pc['earliest']):
                pc['earliest'] = int(x)
        row = {}
        for c, cards in by_c.items():
            row[c] = cell_strength(cards)
            detail[f"{meta['id']}|{c}"] = {
                'cards': len(cards),
                'verbatim': sum(1 for s in cards if s.get('quoteType') == 'verbatim'),
                'motifs': max(len(s.get('motifMatches') or []) for s in cards),
                'works': [s.get('work', '') for s in cards][:3],
            }
        cells[meta['id']] = row
    for key, c in cults.items():
        assert c.get('route') in ROUTES, f"culture {key} needs a route in {sorted(ROUTES)}"
    order = sorted(cults, key=lambda k: (-per_culture[k]['cards'], cults[k]['name']))
    cultures = [{
        'key': k, 'name': cults[k]['name'], 'region': cults[k].get('region', ''), 'color': cults[k].get('color', ''),
        'route': cults[k]['route'], 'routeNote': cults[k].get('routeNote', ''),
        'cards': per_culture[k]['cards'], 'chapters': sorted(per_culture[k]['chapters']),
        'earliestRecorded': per_culture[k]['earliest'],
    } for k in order]
    n_cells = len(chapters) * len(cultures)
    strong = sum(1 for r in cells.values() for v in r.values() if v == 2)
    weak = sum(1 for r in cells.values() for v in r.values() if v == 1)
    singles = [c['name'] for c in cultures if c['cards'] == 1]
    reach = {ch['id']: len(cells[ch['id']]) for ch in chapters}
    widest = max(reach, key=reach.get)
    only_here = [c['name'] for c in cultures if c['chapters'] == [widest]]
    summary = {
        'cells': n_cells, 'strong': strong, 'weak': weak, 'absent': n_cells - strong - weak,
        'cultures': len(cultures), 'chapters': len(chapters), 'cards': sum(c['cards'] for c in cultures),
        'singleCardCultures': singles, 'reach': reach, 'widestChapter': widest, 'onlyInWidest': only_here,
        'routeCounts': dict(collections.Counter(c['route'] for c in cultures)),
    }
    return {'title': 'Presence matrix', 'rule': RULE, 'routes': ROUTES, 'chapters': chapters, 'cultures': cultures,
            'cells': cells, 'detail': detail, 'summary': summary}

if __name__ == '__main__':
    m = build()
    (ROOT / 'data/matrix.json').write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    s = m['summary']
    print(f"data/matrix.json: {s['chapters']} chapters × {s['cultures']} cultures = {s['cells']} cells; "
          f"strong {s['strong']}, weak {s['weak']}, empty {s['absent']} ({s['absent']/s['cells']:.0%}); "
          f"{len(s['singleCardCultures'])} single-card cultures; widest reach: {s['widestChapter']} ({s['reach'][s['widestChapter']]} cultures)")
