#!/usr/bin/env python3
"""Browser regression test for chapter isolation and mobile navigation.
Install: pip install playwright; python -m playwright install chromium
Run after build_standalone.py: python tools/test_page_visibility.py
Screenshots and JSON are written outside the repository by default.
"""
from __future__ import annotations
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

STATE = """() => [...document.querySelectorAll('#book > .page')].map((p, i) => {
 const s = getComputedStyle(p);
 return {i, current:p.classList.contains('is-current'), inert:p.inert,
   aria:p.getAttribute('aria-hidden'), visibility:s.visibility, opacity:+s.opacity,
   transform:s.transform, pointer:s.pointerEvents, chapter:p._meta?.id || null};
})"""

def check(page, expected: int, flat: bool = True):
    page.wait_for_timeout(450)
    states = page.evaluate(STATE)
    assert len(states) > 10, states
    assert [s['i'] for s in states if s['current']] == [expected], states
    for s in states:
        active = s['i'] == expected
        assert s['inert'] == (not active), s
        assert s['aria'] == str(not active).lower(), s
        if active:
            assert s['visibility'] == 'visible' and s['opacity'] > .99, s
            assert s['pointer'] != 'none', s
            assert s['transform'] == 'none', s
        else:
            assert s['pointer'] == 'none', s
            if flat or s['i'] > expected:
                assert s['visibility'] == 'hidden', s
            if flat:
                assert s['opacity'] == 0 and s['transform'] == 'none', s
    # The visible book must not expose another chapter at hit-test points.
    hits = page.evaluate("""() => {
      const pages=[...document.querySelectorAll('#book > .page')], out=[];
      for(let y=70;y<innerHeight-30;y+=65) for(let x=25;x<innerWidth-20;x+=65){
        const p=document.elementFromPoint(x,y)?.closest('#book > .page');
        if(p) out.push(pages.indexOf(p));
      }
      return [...new Set(out)];
    }""")
    assert hits == [expected], (expected, hits)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
    return states


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--output', default='/tmp/storybook-layout')
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    report = []
    book = json.loads((ROOT / 'data/book.json').read_text())
    mazzaroth = next(i + 1 for i, c in enumerate(book['chapters']) if c['id'] == 'mazzaroth')
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            if args.baseline:
                context = browser.new_context(viewport={'width':412,'height':780}, is_mobile=True, has_touch=True)
                page = context.new_page()
                page.goto(base + '/?p=1', wait_until='networkidle')
                page.wait_for_timeout(2800)
                states = page.evaluate(STATE)
                painted = [s['i'] for s in states if s['visibility'] == 'visible' and s['opacity'] > .99]
                page.screenshot(path=str(output / 'before-mobile-creation.png'))
                (output / 'before-state.json').write_text(json.dumps(states, indent=2))
                assert len(painted) > 1, ('Baseline did not reproduce unread-page visibility', states)
                print('REPRODUCED: mobile Creation leaves these pages paintable:', painted, flush=True)
                browser.close()
                return
            for width, edition in [(360, '/'), (412, '/'), (640, '/'), (412, '/the-world-remembers.html')]:
                context = browser.new_context(viewport={'width':width,'height':780}, is_mobile=True, has_touch=True)
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                label = f'{width}-' + ('offline' if '.html' in edition else 'web')
                try:
                    page.goto(base + edition, wait_until='networkidle')
                    total = page.locator('#book > .page').count()
                    for i in range(total):
                        if i:
                            page.locator('#next').click()
                        check(page, i)
                        if width == 412 and i in (1, 2, mazzaroth):
                            page.wait_for_timeout(2500)
                            page.screenshot(path=str(output / f'after-{label}-page-{i}.png'), animations='disabled')
                    # Backward and rapid navigation must leave one chapter active.
                    page.locator('#prev').click()
                    check(page, total - 2)
                    page.evaluate("document.querySelector('#next').click(); document.querySelector('#prev').click(); document.querySelector('#prev').click();")
                    check(page, total - 3)
                    # Chapter index jump, evidence rebuild, and source drawer.
                    page.locator('#btnIndex').click()
                    page.locator('#index .ix').filter(has_text='Mazzaroth').click()
                    check(page, mazzaroth)
                    page.locator('#btnLens').click()
                    check(page, mazzaroth)
                    if width == 412:
                        page.screenshot(path=str(output / f'after-{label}-mazzaroth-evidence.png'), animations='disabled')
                    page.locator('#btnLens').click()
                    check(page, mazzaroth)
                    page.locator('#book > .page.is-current .card').first.click()
                    assert page.locator('#drawer').evaluate("e => e.classList.contains('open')")
                    page.locator('#drawer .x').click()
                    check(page, mazzaroth)
                    assert not errors, errors
                    report.append({'viewport':width,'edition':edition,'pages':total,'result':'pass'})
                except Exception:
                    page.screenshot(path=str(output / f'failure-{label}.png'))
                    (output / f'failure-{label}.json').write_text(json.dumps(page.evaluate(STATE), indent=2))
                    raise
                finally:
                    context.close()
            # Rotation across the mobile breakpoint and live reduced-motion changes.
            context = browser.new_context(viewport={'width':412,'height':780}, has_touch=True)
            page = context.new_page()
            page.goto(base + '/?p=2', wait_until='networkidle')
            check(page, 2)
            page.set_viewport_size({'width':1280,'height':900})
            page.wait_for_timeout(1000)
            check(page, 2, flat=False)
            page.screenshot(path=str(output / 'after-desktop-garden.png'), animations='disabled')
            page.emulate_media(reduced_motion='reduce')
            check(page, 2)
            page.emulate_media(reduced_motion='no-preference')
            page.wait_for_timeout(1000)
            check(page, 2, flat=False)
            page.set_viewport_size({'width':412,'height':780})
            check(page, 2)
            report.append({'rotation_and_reduced_motion':'pass'})
            context.close()
            browser.close()
        (output / 'results.json').write_text(json.dumps(report, indent=2))
        print('PASS: all chapters, three phone widths, online/offline editions, hit testing, back/rapid navigation, chapter jump, evidence lens, drawer, rotation, and reduced motion.', flush=True)
    finally:
        server.shutdown()

if __name__ == '__main__':
    main()
