#!/usr/bin/env python3
"""Keep the bibliography and machine-readable corpus summary synchronized with data.
Run before build_standalone.py and build_text.py. Does not change content JSON.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
book=json.loads((ROOT/'data/book.json').read_text())
chapters=[json.loads((ROOT/c['file']).read_text()) for c in book['chapters']]
arts=json.loads((ROOT/'data/artifacts.json').read_text())['artifacts']
counts=dict(chapters=len(chapters),sources=sum(len(c.get('sources',[])) for c in chapters),evidence=sum(len(c.get('science',{}).get('evidence',[])) for c in chapters),artifacts=len(arts),witnesses=sum(len(c.get('witnesses',[])) for c in chapters),cultures=len(book['cultures']))
p=ROOT/'llms.txt';s=p.read_text()
line=f"The book has {counts['chapters']} chapters, {counts['sources']} source cards, {counts['artifacts']} artifact records, {counts['evidence']} evidence-lens cards, and {counts['witnesses']} manuscript-witness profiles across {counts['cultures']} catalogued cultures."
s,n=re.subn(r'The book has .*? catalogued cultures\.',line,s);assert n==1,'Corpus statement missing'
order='## Reading order\n\n'+'\n'.join(f"{i+1}. {c['motif']}" for i,c in enumerate(chapters))+'\n\n'
s,n=re.subn(r'## Reading order\n.*?(?=## World atlas)',lambda _:order,s,flags=re.S);assert n==1
edition='Biblical quotations use NASB 1995. Other textual witnesses and translation variants are identified separately; they are not silently substituted into a NASB quotation.'
if edition not in s:s=s.replace('## Reading and citation policy\n','## Reading and citation policy\n\n'+edition+'\n')
p.write_text(s)
# Preserve the existing atlas-method section and the detailed Mazzaroth references.
p=ROOT/'SOURCES.md';old=p.read_text()
atlas=re.search(r'## World atlas: date sources\n.*?(?=\n## )',old,re.S)
maz=re.search(r'## Mazzaroth revision — bonds, measure, and appointed times\n.*',old,re.S)
def cell(x):return str(x or '').replace('|','\\|').replace('\n',' ')
def links(xs):return '; '.join(f"[{cell(x['label'])}]({x['url']})" for x in xs if x.get('url'))
L=['# The World Remembers — Sources & Bibliography','',
'Generated from the current chapter and artifact data by `tools/build_reference_docs.py`. This is a source inventory, not a claim that every interpretation or scientific conclusion has received a new independent audit.','',
'## Translation and quotation policy','',
'Scripture quotations taken from the New American Standard Bible® (NASB 1995), Copyright © 1960, 1971, 1977, 1995 by The Lockman Foundation. Used by permission. [The Lockman Foundation](https://www.lockman.org/).','',
'NASB 1995 is copyrighted, not public domain. Each card identifies its translation or labels its summary as a paraphrase. Ellipses mark omitted text. Footnote markers, verse numbers, and typographic italics are not reproduced in the excerpt fields. Different manuscript readings are discussed separately from the main quotation. Other translations retain their individual credits and rights notices; this inventory does not grant a blanket license.','',
f"**Corpus:** {counts['chapters']} chapters; {counts['sources']} source cards; {counts['evidence']} evidence-lens cards; {counts['artifacts']} artifact records; {counts['witnesses']} witness profiles; {counts['cultures']} catalogued cultures.",'']
if atlas:L += [atlas.group(0).strip(),'']
for c in chapters:
 L += ['## '+c['motif'],'']
 if c.get('sources'):
  L += ['### Texts','', '| Voice | Work | Type | Translation | Citation and links |','|---|---|---|---|---|']
  for s in c['sources']:
   vals=[book['cultures'].get(s['culture'],{}).get('name',s['culture']),s['work'],'quoted' if s.get('quoteType')=='verbatim' else 'summary',s.get('translation',''),s.get('citation','')+' '+links(s.get('links',[]))]
   L += ['| '+' | '.join(cell(x) for x in vals)+' |']
  L += ['']
 if c.get('science',{}).get('evidence'):
  L += ['### Evidence lens','', '| Finding | Source | Link |','|---|---|---|']
  for e in c['science']['evidence']:L += ['| '+' | '.join(cell(x) for x in [e['title'],e.get('source',''),e.get('url','')])+' |']
  L += ['']
 for w in c.get('witnesses',[]): L += ['**'+w['name']+'** — '+w.get('place','')+'; '+w.get('era','')+'. '+w.get('preserved',''),'']
L += ['## Artifact records','', '| Object | Citation | Link |','|---|---|---|']
for a in arts.values():L += ['| '+' | '.join(cell(x) for x in [a['name'],a.get('citation',''),a.get('url','')])+' |']
L += ['','## Accuracy review','', 'The NASB 1995 restoration and all 115 copy-audit dispositions are recorded in `reports/copy-accuracy-review.md`, `reports/copy-audit-disposition.json`, and `reports/scripture-excerpts.json`. The review does not silently equate a paraphrase with an exact quotation.','']
if maz:L += [maz.group(0).replace('NASB 2020','NASB 1995').replace('version=NASB)','version=NASB1995)').replace('version=NASB]','version=NASB1995]').replace('&version=NASB)', '&version=NASB1995)').strip(),'']
p.write_text('\n'.join(L).rstrip()+'\n')
print('Reference documents synchronized:',counts)
