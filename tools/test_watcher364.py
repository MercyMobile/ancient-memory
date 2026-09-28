#!/usr/bin/env python3
"""Regression checks for the Watcher 364 exhibit and its links into the book."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[1]
page = (ROOT / 'exhibits/watcher-364/index.html').read_text(encoding='utf-8')
assert page.startswith('<!doctype html>') and '<title>Watcher 364' in page
assert 'root.WATCHER_CORPUS = [' in page and 'root.Watcher364 = api' in page
assert page.count("\n    {\n      family:") == 43, 'corpus record count changed'
assert 'https://ancient-memory.pages.dev/#' not in page and 'href="../../#watchers"' in page
for removed in ('not a claim that either date', 'not an attempt to prove a historical theory'):
    assert removed not in page, removed
for kept in ('id="reckoning"', '107,016', '107,015.96', '1,732,112', '1,733,204', 'doi.org/10.1038/306743a0', 'La date de la Cène', 'always a Tuesday'):
    assert kept in page, kept
assert (ROOT / 'exhibits/watcher-364/SOURCE_MATRIX.md').read_text(encoding='utf-8').count('## The reckoning, tested') == 1
# arithmetic the page claims
def jdn(y, m, d):
    a = (14 - m) // 12; yy = y + 4800 - a; mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083
assert jdn(30, 4, 7) == 1732112 and jdn(33, 4, 3) == 1733204 and jdn(33, 4, 3) - jdn(30, 4, 7) == 1092
assert jdn(30, 4, 7) % 7 == 4 and jdn(33, 4, 3) % 7 == 4  # Friday (0 = Monday)
assert 294 * 364 == 107016 and abs(293 * 365.2422 - 107016) < 0.05
assert 6 * 52 * 7 // 7 == 312 and 312 % 24 == 0 and 294 * 52 == 15288 and 15288 % 24 == 0
# links from the book
url = 'https://ancient-memory.pages.dev/exhibits/watcher-364/'
mz = json.loads((ROOT / 'data/chapters/mazzaroth.json').read_text(encoding='utf-8'))
assert mz['science']['evidence'][6]['url'] == url and '107,016' in mz['science']['evidence'][6]['observation']
assert any(l['url'] == url for l in mz['sources'][8]['links']) and any(l['url'] == url for l in mz['sources'][11]['links'])
dr = json.loads((ROOT / 'data/chapters/dying-rising.json').read_text(encoding='utf-8'))
assert sum(e['url'] == url for e in dr['science']['evidence']) == 1
for f in ('index.html', 'llms.txt', 'sitemap.xml', 'SOURCES.md'):
    assert 'exhibits/watcher-364/' in (ROOT / f).read_text(encoding='utf-8'), f
index = (ROOT / 'index.html').read_text(encoding='utf-8')
assert 'class="bar-link exhibit-link" href="/exhibits/watcher-364/"' in index, 'top-bar door missing'
book = json.loads((ROOT / 'data/book.json').read_text(encoding='utf-8'))
assert book['cover']['exhibit']['url'] == '/exhibits/watcher-364/'
for cid in ('mazzaroth', 'watchers', 'dying-rising'):
    ch = json.loads((ROOT / f'data/chapters/{cid}.json').read_text(encoding='utf-8'))
    assert ch['exhibit']['url'] == '/exhibits/watcher-364/', cid
engine = (ROOT / 'js/engine.js').read_text(encoding='utf-8')
for hook in ('BOOK.cover.exhibit', 'exhibit-pill', 'exhibit-callout'):
    assert hook in engine, hook
assert '**Companion exhibit:**' in (ROOT / 'llms-full.txt').read_text(encoding='utf-8')
# complications on the dial
for kept in ('var Chrono', 'id="dayTicks"', 'id="dayHand"', 'id="moonDisc"', 'id="dwDoy"', 'id="complications"', 'id="scaleGrid"', 'id="markerRail"', 'Absent · no inspected text', 'Seder Olam'):
    assert kept in page, kept
assert page.count('<script>') == 4
assert '## The complications on the dial' in (ROOT / 'exhibits/watcher-364/SOURCE_MATRIX.md').read_text(encoding='utf-8')
import shutil, subprocess
if shutil.which('node'):
    scripts = re.findall(r'<script>([\s\S]*?)</script>', page)
    chrono = next(sc for sc in scripts if 'var Chrono' in sc)
    probe = chrono + """
const g=(y,m,d)=>Chrono.gregorianToJdn(y,m,d);
const r=Chrono.readingAt(g(2026,8,31)); const s=Chrono.scalesAt(r.enoch.yearAbsolute,r.enoch.doy);
const c=Chrono.scalesAt(1,1); const x=Chrono.readingAt(Chrono.julianToJdn(33,4,3)); const t=Chrono.readingAt(Chrono.julianToJdn(30,4,7));
const portals=[1,31,61,92,122,152,183,213,243,274,304,334].map(d=>Chrono.portalAt(d).portal).join('');
const courses=[4,18,25,32].map(d=>Chrono.scalesAt(1,d).course).join(',');
const feasts=Chrono.APPOINTED.map(a=>a.doy).join(',');
console.log(JSON.stringify([portals,courses,feasts,Chrono.scalesAt(x.enoch.yearAbsolute,x.enoch.doy).writtenDay,Chrono.CREATION_JDN%7,Chrono.scalesAt(1,1).signCourse,Chrono.scalesAt(1,166).signCourse]));
console.log(JSON.stringify([r.enoch.yearInEpoch,r.enoch.doy,r.enoch.remainingYears,r.enoch.remainingDays,r.sinceCrucifixion.years,r.sinceCrucifixion.days,c.writtenDay,c.course,c.portal.portal,x.enoch.doy,t.enoch.doy,Chrono.CREATION_JDN,Chrono.NISAN_14_33-Chrono.NISAN_14_30,Chrono.scalesAt(1,14).writtenDay,Chrono.portalAt(91).portal,Chrono.portalAt(273).dayParts]));
"""
    out = subprocess.run(['node', '-e', probe], capture_output=True, text=True, check=True).stdout.strip()
    first, out = out.split('\n')
    # 1 Enoch 72 portal sequence; 4Q325 Sabbath courses; 5/3 = 124 and 6/22 = 173; 3 Apr 33 is a sixth day on the written week; anchor is a Wednesday (JDN mod 7 == 2); the 4Q319 sign is the year-head week only
    assert json.loads(first) == ['456654321123', 'Delaiah,Jehoiarib,Jedaiah,Harim', '14,15,26,75,124,173,183,192,197,204', 'Sixth', 2, True, False], first
    assert json.loads(out) == [5806, 265, 194, 100, 2000, 80, 'Fourth', 'Gamul', 4, 185, 185, 348000, 1092, 'Third', 6, 6], out
print('PASS: exhibit assembled, disclaimers gone, reckoning present, arithmetic exact, book links in place.')
