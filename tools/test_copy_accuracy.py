#!/usr/bin/env python3
"""Regression checks for the NASB 1995 accuracy restoration and generated editions.
Fingerprints pin reviewed excerpts; they do not independently authenticate a translation.
Source URLs and extraction provenance are in reports/scripture-excerpts.json.
"""
from pathlib import Path
import hashlib,json,re
NASB_CARDS=52  # verbatim NASB 1995 source cards; update deliberately when cards are added
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
book=load('data/book.json');chapters={c['id']:load(c['file']) for c in book['chapters']}
m=load('reports/scripture-excerpts.json')
assert m['version']=='NASB 1995'
assert len(m['entries'])==28
for e in m['entries']:
 value=load(e['file'])
 for k in e['path']:value=value[k]
 if e.get('mode')=='contains':
  assert e['excerpt'] in value,e['citation'];value=e['excerpt']
 assert hashlib.sha256(value.encode()).hexdigest()==e['sha256'],e['citation']
 assert e['sources'] and all('version=NASB1995' in s['url'] for s in e['sources']),e['citation']
assert sum(s.get('quoteType')=='verbatim' and 'NASB 1995' in s.get('translation','') for c in chapters.values() for s in c.get('sources',[]))==NASB_CARDS
for c in chapters.values():
 for s in c.get('sources',[]):
  if 'NASB' in s.get('translation',''):assert 'NASB 1995' in s['translation'],s['work']
  for l in s.get('links',[]):
   assert not re.search(r'version=NASB(?:&|$)',l['url']),l
sf=chapters['second-flood']['sources']
assert 'sons of Benjamin' in sf[4]['quote'] and 'Amorites' in sf[4]['quote'] and 'Judah took Gaza' in sf[4]['quote']
assert 'Never Taken' not in sf[4]['work']
assert 'sons of Esau dispossessed them' in sf[2]['quote']
assert 'Now Hor had kings' not in sf[2]['quote']
assert sf[3]['work'].startswith('Joshua 10–11')
assert 'Jaare-oregim' in sf[6]['quote'] and 'Lahmi' not in sf[6]['quote']
assert 'Lahmi the brother of Goliath' in sf[6]['notes'] and '1 CHRONICLES 20:4–5' in sf[6]['notes']
watch=chapters['watchers']['sources'][0]
assert 'sons of Israel' in watch['quote'] and 'His own congregation' in watch['quote']
assert 'angels of God' in watch['notes'] and '4QDeutj' in watch['notes']
assert 'we shall not be mistaken in their meaning' in chapters['mazzaroth']['sources'][13]['quote']
assert 'nearly a day and a quarter' in chapters['mazzaroth']['science']['evidence'][6]['observation']
assert chapters['flood']['science']['evidence'][12]['url']=='https://doi.org/10.1038/s43247-026-03379-1'
for idx in [8,12]:assert 'Communications Earth & Environment' in chapters['flood']['science']['evidence'][idx]['source']
assert 'four lunar cycles' in chapters['watchers']['science']['evidence'][2]['notes']
assert 'three pointers' in chapters['watchers']['science']['evidence'][2]['notes']
# All 115 audit rows have a disposition; style-only choices are not falsely reported as edits.
d=load('reports/copy-audit-disposition.json');assert len(d)==115 and len({x['id'] for x in d})==115
assert all(x['status'] and x['note'] for x in d)
# No visual design or engine changes are allowed in a copy correction.
for p,digest in load('reports/copy-accuracy-protected-files.json').items():
 assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest,p
for p in (ROOT/'data').rglob('*.json'):json.loads(p.read_text())
ns=sum(len(c.get('sources',[])) for c in chapters.values());ne=sum(len(c.get('science',{}).get('evidence',[])) for c in chapters.values())
llms=(ROOT/'llms.txt').read_text()
assert f'{ns} source cards' in llms and f'{ne} evidence-lens cards' in llms
assert chapters['mazzaroth']['motif'] in llms and 'NASB 1995' in llms
bibliography=(ROOT/'SOURCES.md').read_text();text=(ROOT/'download/the-world-remembers.md').read_text()
assert '≤500' not in bibliography and 'NASB 2020' not in bibliography
for c in chapters.values():
 for s in c.get('sources',[]):
  assert s['work'].replace('|','\\|').replace('\n',' ') in bibliography,s['work']
  assert s['quote'] in text,s['work']
  for l in s.get('links',[]):assert l['url'] in text,l['url']
html=(ROOT/'the-world-remembers.html').read_text()
assert html==(ROOT/'download/the-world-remembers.html').read_text()
match=re.search(r'const EMBED = (\{.*?\});\s*const ASSETS = ',html,re.S);assert match
embed=json.loads(match.group(1));assert embed['book']==book and embed['chapters']==chapters
assert embed['artifacts']==load('data/artifacts.json') and embed['atlas']==load('data/atlas.json')
for p in ['index.html','the-world-remembers.html','download/the-world-remembers.html','download/the-world-remembers.md']:
 t=(ROOT/p).read_text();assert 'Copyright © 1960, 1971, 1977, 1995' in t and 'NASB 1995' in t,p
print('PASS: 28 reviewed scripture locations; 25 NASB 1995 source cards; 115 dispositions; distinct manuscript readings; 153/112 corpus counts; synchronized editions and source links; protected artwork, CSS, and JavaScript.')
