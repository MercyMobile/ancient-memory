/* The First History — engine.
   Data-driven: book.json defines chapters; each chapter file holds the sources.
   Pages are stacked; the "current" page sits on top of the unread (right) pile,
   read pages flip to the left. Pop-up cut-outs rise when a page becomes active. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const el = (t, c, html) => { const e = document.createElement(t); if (c) e.className = c; if (html != null) e.innerHTML = html; return e; };
  const REDUCED = matchMedia('(prefers-reduced-motion:reduce)').matches;

  let BOOK, CULT, ART = {}, pages = [], current = 0, lens = 'texts', CHAPTERS = [];
  const asset = p => (typeof ASSETS !== 'undefined' && ASSETS && ASSETS[p]) ? ASSETS[p] : p;

  /* ---------- approximate year for the timeline ---------- */
  function parseYear(str) {
    if (!str) return null;
    str = str.toLowerCase();
    const ce = /\bce\b/.test(str) && !/bce/.test(str);
    const bce = /bce/.test(str);
    let m;
    if ((m = str.match(/(\d+)(?:st|nd|rd|th)?\s*millennium/))) { const n = +m[1]; return bce ? -(n * 1000 - 500) : (n * 1000 - 500); }
    if ((m = str.match(/(\d+)(?:st|nd|rd|th)?\s*c(?:entury|\.)/))) { const n = +m[1]; return bce ? -(n * 100 - 50) : (n * 100 - 50); }
    if ((m = str.match(/(\d{1,4})/))) { const n = +m[1]; return bce ? -n : (ce ? n : -n); }
    return null;
  }

  /* ---------- load ---------- */
  async function load() {
    BOOK = await (await fetch('data/book.json')).json();
    CULT = BOOK.cultures || {};
    try { ART = (await (await fetch('data/artifacts.json')).json()).artifacts || {}; } catch (e) { ART = {}; }
    const chapters = await Promise.all(BOOK.chapters.map(async c => {
      try { return { meta: c, data: await (await fetch(c.file)).json() }; }
      catch (e) { return { meta: c, data: { error: true } }; }
    }));
    build(chapters);
  }

  function cult(id) { return CULT[id] || { name: id ? id[0].toUpperCase() + id.slice(1) : 'Source', region: '', color: '#8a7a4a' }; }

  /* ---------- build all pages ---------- */
  function build(chapters) {
    CHAPTERS = chapters;
    document.title = BOOK.title + ' — ' + BOOK.subtitle;
    const bt = $('#bar .title'); if (bt) bt.textContent = BOOK.title;
    renderBook();
    buildIndex(chapters);
    // deep-link: ?p=2 (page index) or #flood (chapter id) for sharing
    const q = new URLSearchParams(location.search);
    if (q.get('lens') === 'science') { lens = 'science'; renderBook(); document.body.classList.add('sci-lens'); const b = $('#btnLens'); if (b) { b.textContent = '📜 Texts'; b.classList.add('on'); } }
    if (q.has('p')) current = Math.max(0, Math.min(pages.length - 1, +q.get('p') || 0));
    else if (location.hash) { const i = BOOK.chapters.findIndex(c => c.id === location.hash.slice(1)); if (i >= 0) current = i + 1; }
    updatePages();
    wire();
    // shareable view deep-links: ?open=timeline  or  ?open=card&i=0
    const open = q.get('open');
    if (open === 'timeline') setTimeout(toggleTimeline, 600);
    else if (open === 'chapters') setTimeout(() => buildIndexState(true), 400);
    else if (open === 'card') { const p = pages[current]; const c = p && p.querySelectorAll('.card')[+(q.get('i') || 0)]; if (c) setTimeout(() => c.click(), 600); }
  }

  function renderBook() {
    const book = $('#book'); book.innerHTML = ''; pages = [];
    pages.push(makeCover());
    CHAPTERS.forEach((c, i) => pages.push(makeChapter(c.meta, c.data, i + 1)));
    pages.forEach(p => { const u = el('div', 'underside', '<span>· ' + BOOK.title + ' ·</span>'); p.appendChild(u); book.appendChild(p); });
  }

  function toggleLens() {
    lens = lens === 'science' ? 'texts' : 'science';
    const cur = current; renderBook(); current = Math.min(cur, pages.length - 1);
    const b = $('#btnLens'); if (b) { b.textContent = lens === 'science' ? '📜 Texts' : '🔬 Evidence'; b.classList.toggle('on', lens === 'science'); }
    document.body.classList.toggle('sci-lens', lens === 'science');
    closeDrawer(); updatePages();
  }

  /* ---------- cover ---------- */
  function makeCover() {
    const p = el('div', 'page');
    const c = el('div', 'cover');
    c.innerHTML =
      `<img class="bg" src="${asset(BOOK.cover.backdrop)}" alt="">
       <div class="frame"></div>
       <div class="ctext">
         <div class="eyebrow">${esc(BOOK.cover.tagline || '')}</div>
         <h1>${esc(BOOK.title)}</h1>
         <div class="sub">${esc(BOOK.subtitle)}</div>
         <button class="open">Open the book ›</button>
       </div>`;
    c.querySelector('.open').onclick = () => go(1);
    p.appendChild(c);
    return p;
  }

  /* ---------- a chapter page ---------- */
  function makeChapter(meta, data, idx) {
    const p = el('div', 'page');
    const pin = el('div', 'pin');
    const sci = lens === 'science' && data.science;

    // scene (pop-up stage)
    const scene = el('div', 'scene');
    const backdrop = sci ? (data.science.backdrop || data.backdrop) : (data.backdrop || BOOK.cover.backdrop);
    scene.innerHTML =
      `<img class="backdrop" src="${asset(backdrop)}" alt="">
       <div class="vignette"></div>
       <div class="eyebrow">${sci ? '🔬 Through the evidence' : spineLabel(meta.spinePosition) + (meta.era ? ' · ' + esc(meta.era) : '')}</div>
       <div class="motiftitle">${esc(meta.motif)}</div>`;
    if (!sci) (data.scene || []).forEach(s => scene.appendChild(makePopup(s)));
    pin.appendChild(scene);

    if (data.witnesses) pin.appendChild(makeWitnessLower(meta, data));
    else if (sci) pin.appendChild(makeScienceLower(meta, data));
    else if (data.status === 'stub' || data.error) pin.appendChild(makeStub(meta, data));
    else if (lens === 'science' && !data.science && (data.sources && data.sources.length)) pin.appendChild(el('div', 'lower', '<p class="summary">The evidence lens for this chapter is still being assembled. Flip back to <b>📜 Texts</b> to read it.</p>'));
    else pin.appendChild(makeLower(meta, data));
    p.appendChild(pin);
    p._meta = meta; p._data = data;
    return p;
  }

  /* ---------- the witnesses (source libraries) ---------- */
  function makeWitnessLower(meta, data) {
    const low = el('div', 'lower');
    low.appendChild(el('p', 'summary', esc(data.intro || '')));
    const cards = el('div', 'cards');
    (data.witnesses || []).forEach(wt => cards.appendChild(makeWitnessCard(wt)));
    low.appendChild(cards);
    return low;
  }
  function makeWitnessCard(wt) {
    const c = el('div', 'card witness');
    const icon = wt.kind === 'person' ? '✍' : '📜';
    c.innerHTML =
      `<span class="cult" style="color:#b5862f">${icon} ${esc(wt.place || '')}</span>
       <span class="surv">${esc(wt.name)}</span>
       <span class="work">${esc(wt.era || '')}</span>
       <span class="snip">${esc(wt.preserved || '')}</span>`;
    c.onclick = () => openWitness(wt);
    return c;
  }
  function openWitness(wt) {
    const d = $('#drawer');
    const icon = wt.kind === 'person' ? '✍' : '📜';
    const link = wt.url ? `<a href="${wt.url}" target="_blank" rel="noopener">more ↗</a>` : '';
    d.innerHTML =
      `<button class="x" aria-label="close">×</button>
       <div class="dcult" style="color:#b5862f">${icon} ${esc(wt.place || '')}${wt.era ? ' · ' + esc(wt.era) : ''}</div>
       <h2>${esc(wt.name)}</h2>
       <blockquote>${esc(wt.story || '')}</blockquote>
       <div class="meta">
         <div><b>What it preserved</b>${esc(wt.preserved || '')}</div>
         ${link ? `<div><b>See more</b>${link}</div>` : ''}
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
  }

  /* ---------- science lens (the evidence) ---------- */
  function makeScienceLower(meta, data) {
    const low = el('div', 'lower');
    low.appendChild(el('p', 'summary', esc(data.science.intro || '')));
    const cards = el('div', 'cards');
    (data.science.evidence || []).forEach(ev => cards.appendChild(makeScienceCard(ev)));
    low.appendChild(cards);
    return low;
  }
  function makeScienceCard(ev) {
    const c = el('div', 'card sci');
    c.innerHTML =
      `<span class="pq sci ${(ev.strength || '').toLowerCase()}">${esc(ev.strength || '')}</span>
       <span class="cult" style="color:#3f7d8c">🔬 Evidence</span>
       <span class="surv">${esc(ev.title)}</span>
       <span class="snip">${esc(ev.observation)}</span>`;
    c.onclick = () => openScience(ev);
    return c;
  }
  function openScience(ev) {
    const d = $('#drawer');
    const link = ev.url ? `<a href="${ev.url}" target="_blank" rel="noopener">source ↗</a>` : '';
    d.innerHTML =
      `<button class="x" aria-label="close">×</button>
       <div class="dcult" style="color:#3f7d8c">🔬 Physical evidence · ${esc(ev.strength || '')}</div>
       <h2>${esc(ev.title)}</h2>
       <blockquote>${esc(ev.observation)}</blockquote>
       <div class="meta">
         <div><b>What it points to</b>${esc(ev.tie || '')}</div>
         <div><b>Source</b>${esc(ev.source || '—')}${link ? ' · ' + link : ''}</div>
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
  }

  function makePopup(s) {
    const d = el('div', 'popup');
    d.style.left = s.x + '%';
    d.style.bottom = (100 - s.y) + '%';
    d.style.width = (s.scale * 26) + '%';
    d.style.zIndex = s.z || 1;
    d.dataset.delay = s.delay || 0;
    d.innerHTML = `<img src="${asset('art/cutouts/' + s.cutout + '.svg')}" alt="">`;
    return d;
  }

  /* ---------- lower region (full chapter) ---------- */
  function makeLower(meta, data) {
    const low = el('div', 'lower');
    low.appendChild(el('p', 'summary', esc(data.summary)));

    const tags = data.sharedMotifTags || [];
    const sources = data.sources || [];
    if (sources.length) {
      const cards = el('div', 'cards');
      sources.forEach(src => cards.appendChild(makeCard(src, tags)));
      low.appendChild(cards);
      if (tags.length) {
        const leg = el('div', 'legend');
        tags.forEach(t => {
          const chip = el('span', 'chip', esc(t));
          chip.onclick = () => toggleMotif(low, t, chip);
          leg.appendChild(chip);
        });
        low.appendChild(leg);
      }
    }
    // folded-in material evidence (artifacts that confirm the texts)
    const ev = (data.evidence || []).map(id => ART[id]).filter(Boolean);
    if (ev.length) {
      low.appendChild(el('div', 'evhead', '&#9935; The ground confirms — tap a find'));
      const erow = el('div', 'cards evcards');
      (data.evidence || []).forEach(id => { if (ART[id]) erow.appendChild(makeArtifactCard(id, ART[id])); });
      low.appendChild(erow);
    }
    return low;
  }

  function makeArtifactCard(id, a) {
    const card = el('div', 'card artifact');
    card.innerHTML =
      `<span class="cult" style="color:#9a6a2a">${esc(a.type || 'Artifact')}</span>
       <span class="surv">${esc(a.name)}</span>
       <span class="work">${esc(a.site || '')}${a.date ? ' · ' + esc(a.date) : ''}</span>
       <span class="snip">${esc(a.confirms || a.detail || '')}</span>`;
    card.onclick = () => openArtifact(a);
    return card;
  }

  function openArtifact(a) {
    const d = $('#drawer');
    const links = a.url ? `<a href="${a.url}" target="_blank" rel="noopener">source ↗</a>` : '';
    d.innerHTML =
      `<button class="x" aria-label="close">×</button>
       <div class="dcult" style="color:#9a6a2a">&#9935; ${esc(a.type || 'Artifact')}${a.period ? ' · ' + esc(a.period) : ''}</div>
       <h2>${esc(a.name)}</h2>
       <div class="dwork">${esc(a.site || '')}${a.date ? ' · ' + esc(a.date) : ''}</div>
       <blockquote>${esc(a.detail || '')}</blockquote>
       <div class="meta">
         <div><b>Confirms</b>${esc(a.confirms || '—')}</div>
         <div><b>Scholarly status</b>${esc(a.status || '—')}</div>
         <div><b>Citation</b>${esc(a.citation || '—')}</div>
         ${links ? `<div><b>Source</b>${links}</div>` : ''}
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
  }

  function makeCard(src, tags) {
    const c = cult(src.culture);
    const card = el('div', 'card');
    card.style.borderTop = '3px solid ' + c.color;
    const strips = tags.map(t =>
      `<span class="strip ${(src.motifMatches || []).includes(t) ? 'has' : ''}" data-tag="${esc(t)}"></span>`).join('');
    card.innerHTML =
      `<span class="pq ${src.quoteType || 'paraphrase'}">${src.quoteType === 'verbatim' ? 'quoted' : 'summary'}</span>
       <span class="cult" style="color:${c.color}">${esc(c.name)}</span>
       <span class="surv">${esc(src.survivor || c.name)}</span>
       <span class="work">${esc(src.work || '')}</span>
       <span class="snip">${esc(src.quote || '')}</span>
       <span class="dates">${esc(src.textRecorded || src.traditionEra || '')}</span>
       <span class="strips">${strips}</span>`;
    card.onclick = () => openDrawer(src);
    return card;
  }

  /* ---------- stub region ---------- */
  function makeStub(meta, data) {
    const s = el('div', 'stub');
    s.innerHTML = `<div class="tag">Chapter in research</div>
      <p class="summary">${esc(data.summary || meta.teaser || '')}</p>
      <h3>Sources this chapter will draw on:</h3>`;
    const ul = el('ul');
    (data.plannedSources || []).forEach(ps => {
      const li = el('li');
      li.innerHTML = `<b>${esc(cult(ps.culture).name)}</b>${esc(ps.work)}`;
      ul.appendChild(li);
    });
    s.appendChild(ul);
    if (data.sharedMotifTags) {
      const leg = el('div', 'legend');
      data.sharedMotifTags.forEach(t => leg.appendChild(el('span', 'chip', esc(t))));
      s.appendChild(leg);
    }
    return s;
  }

  /* ---------- motif highlight ---------- */
  function toggleMotif(scope, tag, chip) {
    const on = !chip.classList.contains('hot');
    scope.querySelectorAll('.chip').forEach(c => c.classList.remove('hot'));
    scope.querySelectorAll('.strip').forEach(s => s.classList.remove('hot'));
    scope.querySelectorAll('.card').forEach(c => c.style.opacity = '1');
    if (on) {
      chip.classList.add('hot');
      scope.querySelectorAll(`.strip[data-tag="${cssEsc(tag)}"]`).forEach(s => {
        if (s.classList.contains('has')) s.classList.add('hot');
      });
      scope.querySelectorAll('.card').forEach(card => {
        const hit = [...card.querySelectorAll('.strip.has')].some(s => s.dataset.tag === tag);
        card.style.opacity = hit ? '1' : '.4';
      });
    }
  }

  /* ---------- scholarly drawer ---------- */
  function openDrawer(src) {
    const c = cult(src.culture), d = $('#drawer');
    const chips = (src.motifMatches || []).map(t => `<span class="chip hot">${esc(t)}</span>`).join('');
    const links = (src.links || []).map(l => `<a href="${l.url}" target="_blank" rel="noopener">${esc(l.label)} ↗</a>`).join(' · ');
    d.innerHTML =
      `<button class="x" aria-label="close">×</button>
       <div class="dcult" style="color:${c.color}">${esc(c.name)}${c.region ? ' · ' + esc(c.region) : ''}</div>
       <h2>${esc(src.survivor || c.name)}</h2>
       <div class="dwork">${esc(src.work || '')}</div>
       <span class="qtag ${src.quoteType || 'paraphrase'}">${src.quoteType === 'verbatim' ? 'Verbatim — public-domain translation' : 'Summary / paraphrase'}</span>
       <blockquote>${esc(src.quote || '')}</blockquote>
       <div class="dchips">${chips}</div>
       <div class="meta">
         <div><b>Tradition era</b>${esc(src.traditionEra || '—')}</div>
         <div><b>Text recorded</b>${esc(src.textRecorded || '—')}</div>
         <div><b>Provenance</b>${esc(src.provenance || '—')}</div>
         <div><b>Translation</b>${esc(src.translation || '—')}</div>
         <div><b>Citation</b>${esc(src.citation || '—')}</div>
         ${src.notes ? `<div><b>Why it matters</b>${esc(src.notes)}</div>` : ''}
         ${links ? `<div><b>Sources</b>${links}</div>` : ''}
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
  }
  function closeDrawer() { $('#drawer').classList.remove('open'); $('#scrim').classList.remove('open'); }

  /* ---------- timeline ---------- */
  function buildTimeline() {
    const page = pages[current];
    const tl = $('#timeline');
    const data = page && page._data;
    if (!data || !data.sources) { tl.innerHTML = '<h2>Timeline</h2><p class="tsub">Open a completed chapter to see its sources placed in time.</p>'; return; }
    const MIN = -3500, MAX = 1700, span = MAX - MIN;
    const pos = y => ((Math.max(MIN, Math.min(MAX, y)) - MIN) / span) * 100;
    let html = `<h2>${esc(page._meta.motif)} — in time</h2>
      <div class="tsub">Hollow ring = age of the living tradition · solid dot = when it was written down. The long connectors are the point: many traditions are far older than the ink that preserves them.</div>
      <div class="axis">`;
    [-3500, -3000, -2500, -2000, -1500, -1000, -500, 0, 500, 1000, 1500].forEach(y => {
      html += `<span class="tick" style="left:${pos(y)}%">${y < 0 ? (-y) + ' BCE' : (y === 0 ? '1 CE' : y + ' CE')}</span>`;
    });
    // fall of Rome reference line (~400 CE) — the project's notional horizon
    html += `<span class="rome" style="left:${pos(400)}%"><span>400 CE · fall of Rome</span></span>`;
    html += `</div>`;
    data.sources.forEach(s => {
      const c = cult(s.culture);
      const yt = s.tYear != null ? s.tYear : parseYear(s.traditionEra);
      const yx = s.xYear != null ? s.xYear : parseYear(s.textRecorded);
      const pt = yt != null ? pos(yt) : null;
      const px = yx != null ? pos(yx) : null;
      let row = `<div class="trow"><span class="lbl" style="color:${c.color}">${esc(c.name)}</span>`;
      if (pt != null && px != null) {
        const a = Math.min(pt, px), b = Math.max(pt, px);
        row += `<span class="tline" style="left:${a}%;width:${b - a}%"></span>`;
      }
      if (pt != null) row += `<span class="tmark tradition" title="tradition: ${esc(s.traditionEra)}" style="left:${pt}%;border-color:${c.color}"></span>`;
      if (px != null) row += `<span class="tmark text" title="recorded: ${esc(s.textRecorded)}" style="left:${px}%;background:${c.color}"></span>`;
      row += `</div>`;
      html += row;
    });
    html += `<div class="tlegend"><span><span class="d1"></span> living tradition</span><span><span class="d2"></span> written down</span></div>`;
    tl.innerHTML = html;
  }

  /* ---------- index ---------- */
  function buildIndex(chapters) {
    const grid = $('#index .grid');
    chapters.sort((a, b) => (a.meta.spinePosition || 0) - (b.meta.spinePosition || 0));
    chapters.forEach(c => {
      const pageIdx = BOOK.chapters.findIndex(x => x.id === c.meta.id) + 1;
      const ix = el('div', 'ix');
      ix.innerHTML = `<div class="n">${spineLabel(c.meta.spinePosition)}</div>
        <h3>${esc(c.meta.motif)}</h3>
        <p>${esc(c.meta.teaser || '')}</p>
        <div class="st ${c.meta.status}">${c.meta.status === 'complete' ? '✦ Complete' : 'In research'}</div>`;
      ix.onclick = () => { closeIndex(); go(pageIdx); };
      grid.appendChild(ix);
    });
  }

  /* ---------- navigation + pop-up firing ---------- */
  function updatePages() {
    const N = pages.length;
    pages.forEach((p, i) => {
      const flipped = i < current;
      p.classList.toggle('flipped', flipped);
      p.style.zIndex = flipped ? i : (N - i);
    });
    // reset popups everywhere, fire on the active page
    pages.forEach(p => p.querySelectorAll('.popup').forEach(u => u.classList.remove('up')));
    const active = pages[current];
    if (active) {
      const pops = active.querySelectorAll('.popup');
      pops.forEach(u => {
        const delay = REDUCED ? 0 : (+u.dataset.delay || 0) + 450; // wait for page turn
        setTimeout(() => u.classList.add('up'), delay);
      });
    }
    $('#prev').disabled = current === 0;
    $('#next').disabled = current === N - 1;
    $('#foot').textContent = current === 0 ? '' : `${current} / ${N - 1}`;
    if ($('#timeline').classList.contains('open')) buildTimeline();
  }

  function go(i) {
    i = Math.max(0, Math.min(pages.length - 1, i));
    if (i === current) return;
    current = i; closeDrawer(); updatePages();
  }
  const next = () => go(current + 1), prev = () => go(current - 1);

  function openIndex() { buildIndexState(true); }
  function buildIndexState(o) { $('#index').classList.toggle('open', o); }
  function closeIndex() { $('#index').classList.remove('open'); }

  function toggleTimeline() {
    const t = $('#timeline'), open = !t.classList.contains('open');
    closeIndex();
    if (open) buildTimeline();
    t.classList.toggle('open', open);
    $('#btnTime').classList.toggle('on', open);
  }

  /* ---------- wiring ---------- */
  function wire() {
    $('#next').onclick = next; $('#prev').onclick = prev;
    const lb = $('#btnLens'); if (lb) lb.onclick = toggleLens;
    $('#scrim').onclick = closeDrawer;
    $('#btnIndex').onclick = () => { const o = !$('#index').classList.contains('open'); $('#timeline').classList.remove('open'); $('#btnTime').classList.remove('on'); buildIndexState(o); };
    $('#btnTime').onclick = toggleTimeline;
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') next();
      else if (e.key === 'ArrowLeft') prev();
      else if (e.key === 'Escape') { closeDrawer(); closeIndex(); $('#timeline').classList.remove('open'); $('#btnTime').classList.remove('on'); }
    });
    // swipe
    let x0 = null;
    const stage = $('#stage');
    stage.addEventListener('touchstart', e => x0 = e.touches[0].clientX, { passive: true });
    stage.addEventListener('touchend', e => {
      if (x0 == null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (dx < -50) next(); else if (dx > 50) prev();
      x0 = null;
    }, { passive: true });
  }

  /* ---------- helpers ---------- */
  function spineLabel(n) { return ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'][n] || ''; }
  function esc(s) { return (s == null ? '' : String(s)).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m])); }
  function cssEsc(s) { return s.replace(/"/g, '\\"'); }

  load().catch(e => { document.body.innerHTML = '<p style="color:#e8dcc0;padding:40px;font-family:sans-serif">Could not load the book — be sure you are running it through a server (python3 tools/serve.py), not opening the file directly.<br><br>' + esc(e.message) + '</p>'; });
})();
