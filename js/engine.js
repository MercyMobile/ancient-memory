/* The First History — engine.
   Data-driven: book.json defines chapters; each chapter file holds the sources.
   Pages are stacked; the "current" page sits on top of the unread (right) pile,
   read pages flip to the left. Pop-up cut-outs rise when a page becomes active. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const el = (t, c, html) => { const e = document.createElement(t); if (c) e.className = c; if (html != null) e.innerHTML = html; return e; };
  // Make a div/span keyboard-activatable: tabindex, role, Enter/Space.
  const activable = (node, handler) => {
    if (!node) return node;
    node.setAttribute('tabindex', '0');
    node.setAttribute('role', 'button');
    node.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handler(); }
    });
    return node;
  };
  const REDUCED = matchMedia('(prefers-reduced-motion:reduce)').matches;
  // Keep the page-state model in sync with the flat mobile/reduced-motion CSS.
  const FLAT_BOOK = matchMedia('(max-width:640px), (prefers-reduced-motion:reduce)');

  let BOOK, CULT, ART = {}, ATLAS = null, DIG = null, pages = [], current = 0, lens = 'texts', CHAPTERS = [];
  let atlasView = 'world';
  let lastFocus = null; // Store focus for overlay restoration
  let popupTimers = []; // Cancel delayed rises when navigating again
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
    try { ATLAS = await (await fetch('data/atlas.json')).json(); } catch (e) { ATLAS = null; }
    try { loadDigs(await (await fetch('data/digsites.json')).json()); } catch (e) { DIG = null; }
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
    if (q.get('lens') === 'science') {
      lens = 'science';
      renderBook();
      document.body.classList.add('sci-lens');
      const b = $('#btnLens');
      if (b) {
        b.textContent = '📜 Texts';
        b.classList.add('on');
        b.setAttribute('aria-pressed', 'true');
      }
    }
    if (q.has('p')) current = Math.max(0, Math.min(pages.length - 1, +q.get('p') || 0));
    else if (location.hash) { const i = BOOK.chapters.findIndex(c => c.id === location.hash.slice(1)); if (i >= 0) current = i + pageOffset(); }
    updatePages();
    wire();
    // a chapter link inside the book (#the-kinds) turns the page instead of opening a new tab
    window.addEventListener('hashchange', () => {
      const i = BOOK.chapters.findIndex(c => c.id === location.hash.slice(1));
      if (i < 0) return;
      closeDrawer(); closeTimeline(false); closeIndex();
      go(i + pageOffset());
    });
    // shareable view deep-links: ?open=atlas, ?open=timeline, or ?open=card&i=0
    const open = q.get('open');
    if (open === 'atlas' || open === 'timeline') {
      atlasView = open === 'timeline' ? 'chapter' : 'world';
      setTimeout(toggleTimeline, 600);
    }
    else if (open === 'chapters') setTimeout(() => buildIndexState(true), 400);
    else if (open === 'card') { const p = pages[current]; const c = p && p.querySelectorAll('.card')[+(q.get('i') || 0)]; if (c) setTimeout(() => c.click(), 600); }
  }

  function renderBook() {
    const book = $('#book'); book.innerHTML = ''; pages = [];
    pages.push(makeCover());
    if (BOOK.prologue) pages.push(makeSpine(BOOK.prologue, 'prologue'));
    CHAPTERS.forEach((c, i) => pages.push(makeChapter(c.meta, c.data, i + 1)));
    if (BOOK.spine) pages.push(makeSpine(BOOK.spine));
    pages.forEach(p => { const u = el('div', 'underside', '<span>· ' + BOOK.title + ' ·</span>'); p.appendChild(u); book.appendChild(p); });
  }

  function toggleLens() {
    lens = lens === 'science' ? 'texts' : 'science';
    const cur = current; renderBook(); current = Math.min(cur, pages.length - 1);
    const b = $('#btnLens');
    if (b) {
      b.textContent = lens === 'science' ? '📜 Texts' : '🔬 Evidence';
      b.classList.toggle('on', lens === 'science');
      b.setAttribute('aria-pressed', lens === 'science');
    }
    document.body.classList.toggle('sci-lens', lens === 'science');
    closeDrawer();
    updatePages();
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
         ${BOOK.cover.exhibit ? `<a class="exhibit" href="${esc(BOOK.cover.exhibit.url)}">${esc(BOOK.cover.exhibit.label)} ›</a>` : ''}
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
       <div class="motiftitle">${esc(meta.motif)}</div>
       ${data.exhibit ? `<a class="exhibit-pill" href="${esc(data.exhibit.url)}">✦ ${esc(data.exhibit.label)}</a>` : ''}`;
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


  // chapter i lives at page i + 1, or i + 2 when the book opens with a prologue page
  const pageOffset = () => (BOOK.prologue ? 2 : 1);

  /* ---------- the spine pages: the prologue before the chapters, the closing argument after ---------- */
  function makeSpine(sp, kind) {
    const p = el('div', 'page spinepage' + (kind ? ' ' + kind : ''));
    const pin = el('div', 'pin');

    const scene = el('div', 'scene');
    scene.innerHTML =
      `<img class="backdrop" src="${asset(sp.backdrop || BOOK.cover.backdrop)}" alt="">
       <div class="vignette"></div>
       <div class="eyebrow">${esc(sp.eyebrow || '')}</div>
       <div class="motiftitle">${esc(sp.title)}</div>`;
    pin.appendChild(scene);

    const low = el('div', 'lower spinelower'), seen = new Set();
    let h = `<p class="spinesub">${esc(sp.subtitle || '')}</p>
             <p class="summary">${digs(sp.lede || '', seen)}</p>`;

    (sp.movements || []).forEach(m => {
      h += `<section class="mvt${m.break ? ' brk' : ''}">
              <p class="mstamp">${esc(m.stamp)}</p>
              <h3>${esc(m.title)}</h3>`;
      (m.body || []).forEach(t => { h += `<p>${digs(t, seen)}</p>`; });
      if (m.quote) h += `<blockquote>${esc(m.quote.text)}<cite>${esc(m.quote.cite)}</cite></blockquote>`;
      if (m.note) h += `<p class="mnote">${digs(m.note, seen)}</p>`;
      h += `</section>`;
      if (m.stamp && /Flood/.test(m.stamp) && sp.figure) h += spineFigure(sp.figure);
    });

    if ((sp.closing || []).length) {
      h += `<section class="mvt closing"><h3>${esc(sp.closingTitle || 'What the picture is')}</h3>`;
      sp.closing.forEach(t => { h += `<p>${digs(t, seen)}</p>`; });
      h += `</section>`;
    }

    if ((sp.open || []).length) {
      h += `<section class="mvt open"><h3>Still to recover</h3><ul>`;
      sp.open.forEach(t => { h += `<li>${esc(t)}</li>`; });
      h += `</ul></section>`;
    }
    low.innerHTML = h;
    pin.appendChild(low);
    p.appendChild(pin);
    p._meta = { motif: sp.title, spinePosition: 'spine' };
    p._data = {};
    return p;
  }

  /* lifespan plot + the same numbers in a table, since the numbers are the point */
  function spineFigure(f) {
    const all = f.pre.concat(f.post), n = all.length;
    const W = 880, H = 380, L = 64, R = 24, T = 26, B = 54;
    const X = i => L + i * ((W - L - R) / (n - 1));
    const Y = a => H - B - (a / 1000) * (H - T - B);
    const pts = arr => arr.map(([, a], i) => `${X(i + (arr === f.post ? f.pre.length : 0)).toFixed(1)},${Y(a).toFixed(1)}`).join(' ');
    const floodX = ((X(f.pre.length - 1) + X(f.pre.length)) / 2).toFixed(1);
    const mi = f.post.findIndex(r => r[0] === f.mark);
    const mX = X(f.pre.length + mi).toFixed(1), mY = Y(f.post[mi][1]).toFixed(1);
    const grid = [1000, 750, 500, 250, 0].map(v =>
      `<line x1="${L}" y1="${Y(v).toFixed(1)}" x2="${W - R}" y2="${Y(v).toFixed(1)}"/>`).join('');
    const gtxt = [1000, 750, 500, 250, 0].map(v =>
      `<text x="${L - 8}" y="${(Y(v) + 4).toFixed(1)}">${v}</text>`).join('');
    const dots = all.map(([, a], i) =>
      `<circle cx="${X(i).toFixed(1)}" cy="${Y(a).toFixed(1)}" r="3"/>`).join('');
    const names = all.map(([nm], i) => (i % 2 === 0)
      ? `<text x="${X(i).toFixed(1)}" y="${H - 36}">${esc(nm.slice(0, 7))}</text>` : '').join('');

    let rows = '', prev = null;
    f.post.forEach(([nm, a]) => {
      const d = prev === null ? '—' : (a - prev > 0 ? '+' : '') + (a - prev);
      rows += `<tr${nm === f.mark ? ' class="mark"' : ''}><td>${esc(nm)}</td><td class="n">${a}</td><td class="d">${d}</td></tr>`;
      prev = a;
    });

    return `<figure class="spinefig">
      <figcaption class="fhd">${esc(f.title)}</figcaption>
      <div class="fscroll">
        <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(f.caption)}">
          <g class="grid">${grid}</g>
          <g class="glab">${gtxt}</g>
          <line class="brkline" x1="${floodX}" y1="${T}" x2="${floodX}" y2="${Y(0).toFixed(1)}"/>
          <text class="brklab" x="${(+floodX + 6)}" y="${T + 14}">THE FLOOD</text>
          <line class="brkline" x1="${mX}" y1="${T}" x2="${mX}" y2="${Y(0).toFixed(1)}"/>
          <text class="brklab" x="${(+mX + 6)}" y="${T + 14}">BABEL</text>
          <polyline class="ln" points="${pts(f.pre)}"/>
          <polyline class="ln" points="${pts(f.post)}"/>
          <g class="dot">${dots}</g>
          <circle class="markdot" cx="${mX}" cy="${mY}" r="5.5"/>
          <g class="nlab">${names}</g>
          <text class="marklab" x="${mX}" y="${H - 10}">${esc(f.mark)} · ${f.post[mi][1]}</text>
        </svg>
      </div>
      <p class="fcap">${esc(f.caption)}</p>
      <div class="fscroll">
        <table class="ftab"><thead><tr><th>Generation</th><th class="n">Years</th><th class="d">Change</th></tr></thead>
        <tbody>${rows}</tbody></table>
      </div>
    </figure>`;
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
    activable(c, () => openWitness(wt));
    return c;
  }
  function openWitness(wt) {
    const d = $('#drawer');
    // Store current focus before opening drawer
    lastFocus = document.activeElement;
    const icon = wt.kind === 'person' ? '✍' : '📜';
    const link = wt.url ? `<a href="${wt.url}" target="_blank" rel="noopener">more ↗</a>` : '';
    d.innerHTML =
      `<button class="x" aria-label="close drawer">×</button>
       <div class="dcult" style="color:#b5862f">${icon} ${esc(wt.place || '')}${wt.era ? ' · ' + esc(wt.era) : ''}</div>
       <h2>${esc(wt.name)}</h2>
       <blockquote>${esc(wt.story || '')}</blockquote>
       <div class="meta">
         <div><b>What it preserved</b>${esc(wt.preserved || '')}</div>
         ${link ? `<div><b>See more</b>${link}</div>` : ''}
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
    // Move focus to close button for accessibility
    setTimeout(() => {
      const closeBtn = d.querySelector('.x');
      if (closeBtn) closeBtn.focus();
    }, 50);
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
      `<span class="cult" style="color:#3f7d8c">🔬 Evidence</span>
       <span class="surv">${esc(ev.title)}</span>
       <span class="snip">${esc(ev.observation)}</span>`;
    c.onclick = () => openScience(ev);
    activable(c, () => openScience(ev));
    return c;
  }
  function openScience(ev) {
    const d = $('#drawer'), seen = new Set();
    // Store current focus before opening drawer
    lastFocus = document.activeElement;
    const link = ev.url ? `<a href="${ev.url}" target="_blank" rel="noopener">source ↗</a>` : '';
    d.innerHTML =
      `<button class="x" aria-label="close drawer">×</button>
       <div class="dcult" style="color:#3f7d8c">🔬 Physical evidence</div>
       <h2>${esc(ev.title)}</h2>
       <blockquote>${digs(ev.observation, seen)}</blockquote>
        <div class="meta">
          <div><b>What it points to</b>${digs(ev.tie || '', seen)}</div>
          ${ev.notes ? `<div><b>2026 update</b>${digs(ev.notes, seen)}</div>` : ''}
          <div><b>Source</b>${esc(ev.source || '—')}${link ? ' · ' + link : ''}</div>
        </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
    // Move focus to close button for accessibility
    setTimeout(() => {
      const closeBtn = d.querySelector('.x');
      if (closeBtn) closeBtn.focus();
    }, 50);
  }

  function makePopup(s) {
    const d = el('div', 'popup');
    d.style.left = s.x + '%';
    d.style.bottom = (100 - s.y) + '%';
    d.style.width = (s.scale * 26) + '%';
    // Leave room for the scene title at every placement, including raised figures.
    d.style.setProperty('--popup-height', Math.max(10, Math.min(38, s.y * .44 - 6)) + 'vh');
    d.style.zIndex = s.z || 1;
    d.dataset.delay = s.delay || 0;
    d.innerHTML = `<img src="${asset('art/cutouts/' + s.cutout + '.webp')}" alt="">`;
    if (s.flipX) d.querySelector('img').style.transform = 'scaleX(-1)';
    return d;
  }

  /* ---------- lower region (full chapter) ---------- */
  function makeLower(meta, data) {
    const low = el('div', 'lower');
    low.appendChild(el('p', 'summary', digs(data.summary, new Set())));
    if (data.exhibit) low.appendChild(el('a', 'exhibit-callout', `<b>✦ ${esc(data.exhibit.label)}</b> ${esc(data.exhibit.blurb || '')} <span>Open the exhibit ›</span>`)).href = data.exhibit.url;

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
          activable(chip, () => toggleMotif(low, t, chip));
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
    card.onclick = () => openArtifact(id, a);
    activable(card, () => openArtifact(id, a));
    return card;
  }

  function openArtifact(id, a) {
    const d = $('#drawer'), seen = new Set();
    const dig = DIG && DIG.sites[DIG.byArtifact[id]];
    if (dig) seen.add(dig.id);
    // Store current focus before opening drawer
    lastFocus = document.activeElement;
    const links = a.url ? `<a href="${a.url}" target="_blank" rel="noopener">source ↗</a>` : '';
    d.innerHTML =
      `<button class="x" aria-label="close drawer">×</button>
       <div class="dcult" style="color:#9a6a2a">&#9935; ${esc(a.type || 'Artifact')}${a.period ? ' · ' + esc(a.period) : ''}</div>
       <h2>${esc(a.name)}</h2>
       <div class="dwork">${esc(a.site || '')}${a.date ? ' · ' + esc(a.date) : ''}</div>
       <blockquote>${digs(a.detail || '', seen)}</blockquote>
       <div class="meta">
         <div><b>Confirms</b>${digs(a.confirms || '—', seen)}</div>
         <div><b>Scholarly status</b>${digs(a.status || '—', seen)}</div>
         <div><b>Citation</b>${esc(a.citation || '—')}</div>
         ${links ? `<div><b>Source</b>${links}</div>` : ''}
         ${dig ? `<div><b>Dig site record</b><a class="dig" href="${esc(dig.url)}" target="_blank" rel="noopener">${esc(dig.name)} ↗</a></div>` : ''}
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
    // Move focus to close button for accessibility
    setTimeout(() => {
      const closeBtn = d.querySelector('.x');
      if (closeBtn) closeBtn.focus();
    }, 50);
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
    activable(card, () => openDrawer(src));
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
    const c = cult(src.culture), d = $('#drawer'), seen = new Set();
    // Store current focus before opening drawer
    lastFocus = document.activeElement;
    const chips = (src.motifMatches || []).map(t => `<span class="chip hot">${esc(t)}</span>`).join('');
    const links = (src.links || []).map(l => String(l.url).startsWith('#')
      ? `<a href="${esc(l.url)}" class="inbook">${esc(l.label)} ›</a>`
      : `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)} ↗</a>`).join(' · ');
    d.innerHTML =
      `<button class="x" aria-label="close drawer">×</button>
       <div class="dcult" style="color:${c.color}">${esc(c.name)}${c.region ? ' · ' + esc(c.region) : ''}</div>
       <h2>${esc(src.survivor || c.name)}</h2>
       <div class="dwork">${esc(src.work || '')}</div>
       <span class="qtag ${src.quoteType || 'paraphrase'}">${src.quoteType === 'verbatim' ? 'Verbatim quotation' : 'Summary / paraphrase'}</span>
       <blockquote>${esc(src.quote || '')}</blockquote>
       <div class="dchips">${chips}</div>
       <div class="meta">
         <div><b>Tradition era</b>${esc(src.traditionEra || '—')}</div>
         <div><b>Text recorded</b>${esc(src.textRecorded || '—')}</div>
         <div><b>Provenance</b>${digs(src.provenance || '—', seen)}</div>
         <div><b>Translation</b>${esc(src.translation || '—')}</div>
         <div><b>Citation</b>${esc(src.citation || '—')}</div>
         ${src.notes ? `<div><b>Why it matters</b>${digs(src.notes, seen)}</div>` : ''}
         ${links ? `<div><b>Sources</b>${links}</div>` : ''}
       </div>`;
    d.querySelector('.x').onclick = closeDrawer;
    d.classList.add('open'); $('#scrim').classList.add('open');
    // Move focus to close button for accessibility
    setTimeout(() => {
      const closeBtn = d.querySelector('.x');
      if (closeBtn) closeBtn.focus();
    }, 50);
  }

  function closeDrawer() {
    if (!$('#drawer').classList.contains('open')) return;
    $('#drawer').classList.remove('open');
    $('#scrim').classList.remove('open');
    // Capture target now; callers may clear lastFocus before the timeout fires.
    const target = lastFocus;
    if (target && target !== document.body) {
      setTimeout(() => { try { target.focus(); } catch (_) {} }, 50);
    }
    lastFocus = null;
  }

  /* ---------- timeline ---------- */
  function buildTimeline() {
    const tl = $('#timeline');
    const world = atlasView === 'world';
    tl.innerHTML = `<div class="atlas-shell">
      <div class="atlas-toolbar"><span class="atlas-kicker">THE WORLD REMEMBERS · SOURCES IN TIME</span><button class="atlas-close" type="button" aria-label="Close atlas">Close ×</button></div>
      <div class="atlas-tabs" role="tablist" aria-label="Time views">
        <button type="button" role="tab" data-view="world" aria-selected="${world}" class="${world ? 'active' : ''}">World atlas</button>
        <button type="button" role="tab" data-view="chapter" aria-selected="${!world}" class="${!world ? 'active' : ''}">This chapter’s sources</button>
      </div>
      ${world ? buildWorldAtlas() : buildChapterTimeline()}
    </div>`;
    tl.querySelector('.atlas-close').onclick = () => closeTimeline();
    tl.querySelectorAll('.atlas-tabs button').forEach(button => {
      button.onclick = () => {
        atlasView = button.dataset.view;
        buildTimeline();
        tl.querySelector(`[data-view="${atlasView}"]`).focus();
      };
    });
    tl.querySelectorAll('[data-chapter]').forEach(button => {
      button.onclick = () => {
        const idx = BOOK.chapters.findIndex(c => c.id === button.dataset.chapter);
        if (idx < 0) return;
        closeTimeline(false);
        go(idx + pageOffset());
        $('#btnTime').focus();
      };
    });
  }

  function buildWorldAtlas() {
    if (!ATLAS) return '<h2>World atlas</h2><p class="tsub">The atlas data could not be loaded.</p>';
    const w = ATLAS.window;
    const pos = y => ((Math.max(w.from, Math.min(w.to, y)) - w.from) / (w.to - w.from)) * 100;
    const anchor = pos(w.adamsAnchor);
    const sourceLink = item => `<a href="${esc(item.sourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(item.sourceLabel)} ↗</a>`;
    const chapterButton = item => item.chapter ? `<button type="button" data-chapter="${esc(item.chapter)}">Read the chapter ›</button>` : '';
    const milestones = ATLAS.chronology.map(item => `<article class="atlas-milestone ${item.kind === 'horizon' ? 'horizon' : ''}">
      <span class="atlas-year">${esc(item.date)}</span>
      <h3>${esc(item.label)}</h3>
      <p>${esc(item.detail)}</p>
      <div class="atlas-cardfoot">${sourceLink(item)}${chapterButton(item)}</div>
    </article>`).join('');
    const ticks = w.ticks.map(y => `<span class="atlas-tick" style="left:${pos(y)}%">${-y}</span>`).join('');
    const rows = w.rows.map(item => `<article class="atlas-row ${item.kind === 'climate' ? 'climate' : ''}">
      <div class="atlas-rowhead"><span class="atlas-region">${esc(item.region)}</span><h4>${esc(item.title)}</h4><span class="atlas-date">${esc(item.date)}</span></div>
      <div class="atlas-plot" role="img" aria-label="${esc(item.title)}: ${esc(item.date)}">
        <span class="atlas-reference" style="left:${anchor}%"></span>
        <span class="atlas-range" style="left:${pos(item.start)}%;width:${pos(item.end) - pos(item.start)}%"></span>
        ${item.kind === 'climate' ? `<span class="atlas-climate-point" style="left:${pos(w.scienceMarker)}%" title="4.2 ka formal boundary · approximately 2250 BCE"></span>` : ''}
      </div>
      <div class="atlas-rowfoot">${esc(item.basis)} <span>· ${sourceLink(item)}</span></div>
    </article>`).join('');
    const early = ATLAS.outsideWindow;
    return `<header class="atlas-hero">
        <span class="atlas-eyebrow">ANCIENT ACCOUNTS · DATED OBJECTS · EARTH RECORD</span>
        <h2>A world at the same time</h2>
        <p>Follow the book’s ancient voices, then place each written source and physical trace on its own clock. This first comparison leaf opens around the Tower and Reset chapters.</p>
        <div class="atlas-duo">
          <div><span>ADAMS’S 1881 CHART</span><strong>2247 BC</strong><p>“Confusion of Tongues” and dispersion, dated by Adams’s Ussher-based chronology.</p></div>
          <div><span>MEGHALAYAN BOUNDARY</span><strong>c. 2250 BCE</strong><p>The 4.2 ka formal marker, selected as a modeled midpoint in a much longer Mawmluh Cave record.</p></div>
        </div>
        <p class="atlas-hero-note">The printed years are nominally three years apart. They use different dating methods; the cave signal spans centuries.</p>
        <div class="atlas-actions"><button type="button" data-chapter="reset">Read the Reset ›</button><button type="button" data-chapter="tower">Read the Tower ›</button><a class="atlas-exhibit" href="/exhibits/adams-chart/">Open Adams’s chart, sheet by sheet ›</a></div>
      </header>
      <section class="atlas-section" aria-labelledby="atlas-chron-title">
        <div class="atlas-sectionhead"><span>01 · THE STORY AXIS</span><h3 id="atlas-chron-title">Adams’s dates, in their proper frame</h3><p>These are the chart’s placements, not dates printed in Genesis. The 70 CE endpoint is this book’s editorial boundary.</p></div>
        <div class="atlas-milestones">${milestones}</div>
      </section>
      <section class="atlas-section" aria-labelledby="atlas-window-title">
        <div class="atlas-sectionhead"><span>02 · PARALLEL PLACES</span><h3 id="atlas-window-title">Around 2250 BCE, across the world</h3><p>Each band shows a documented occupation, historical period, building phase, or local proxy. The gold rule marks Adams’s 2247 BC label.</p></div>
        <div class="atlas-chart">
          <div class="atlas-axis"><span class="atlas-axis-label">APPROXIMATE YEARS BCE →</span><div class="atlas-axis-track">${ticks}<span class="atlas-reference" style="left:${anchor}%"></span></div></div>
          ${rows}
        </div>
        <div class="atlas-chartlegend"><span class="atlas-legend-rule"></span> Adams’s 2247 BC label <span class="atlas-legend-range"></span> dated regional interval <span class="atlas-legend-point"></span> 4.2 ka formal marker</div>
      </section>
      <section class="atlas-section atlas-ending" aria-labelledby="atlas-early-title">
        <div><span class="atlas-eyebrow">EARLIER ON THE PHYSICAL TIMELINE</span><h3 id="atlas-early-title">${esc(early.place)}</h3><strong>${esc(early.date)}</strong><p>${esc(early.detail)}</p>${sourceLink(early)}</div>
        <div><span class="atlas-eyebrow">HOW TO READ THIS LEAF</span><p>${esc(ATLAS.method)}</p><p>For the account itself, open the relevant chapter. Its source card gives the surviving text’s recorded date and provenance.</p></div>
      </section>
      <p class="atlas-edition">${esc(ATLAS.edition)}</p>`;
  }

  // Witness eras: a bare four-digit year with no BCE marker is CE ("found 1928", "copied c. 1701").
  function eraYear(str) {
    if (!str) return null;
    if (!/bce/i.test(str)) { const m = str.match(/\b(1\d{3}|20\d{2})\b/); if (m) return +m[1]; }
    return parseYear(str);
  }
  // "Qumran — the Dead Sea Scrolls" -> "Qumran"; "Berossus & Manetho (the Greek copyists)" -> "Berossus & Manetho"
  const shortName = n => String(n || '').split(' — ')[0].replace(/\s*\(.*\)\s*$/, '').trim();

  function buildChapterTimeline() {
    const page = pages[current];
    const data = page && page._data;
    const here = page && page._meta && page._meta.motif ? page._meta.motif : 'the cover';
    const chapterList = `<div class="atlas-actions tchapters">${BOOK.chapters.map(c => `<button type="button" data-chapter="${esc(c.id)}">${esc(c.motif)} ›</button>`).join('')}</div>`;
    if (!data || !data.sources) {
      return `<h2>Chapter source dates</h2>
        <div class="tsub">This tab shows the sources of the chapter the book is open to. The book is open at ${esc(here)}, which has no source cards. Open a chapter:</div>${chapterList}`;
    }
    const MIN = -3500, MAX = 2000, span = MAX - MIN;
    const pos = y => ((Math.max(MIN, Math.min(MAX, y)) - MIN) / span) * 100;
    const witnessMode = !data.sources.length && Array.isArray(data.witnesses) && data.witnesses.length > 0;
    let html = `<h2>${esc(page._meta.motif)} — ${witnessMode ? 'the witnesses in time' : 'source dates'}</h2>
      <div class="tsub">Showing the chapter the book is open to (${esc(page._meta.motif)}). Turn the page and reopen the atlas for another chapter.</div>
      <div class="tsub">${witnessMode
        ? 'Solid dot = the date of the manuscript, library or writer that carried the accounts down. Each row also prints its date.'
        : 'Hollow ring = the source card’s proposed tradition era · solid dot = recorded text date. The eras are approximate; an undated oral tradition has no ring. Each row also prints its dates.'}</div>
      <div class="axis">`;
    [-3500, -2500, -1500, -500, 500, 1500, 2000].forEach(y => {
      html += `<span class="tick" style="left:${pos(y)}%">${y < 0 ? (-y) + ' BCE' : (y === 0 ? '1 CE' : y + ' CE')}</span>`;
    });
    html += `</div>`;
    if (witnessMode) {
      data.witnesses.forEach(wt => {
        const y = eraYear(wt.era);
        const px = y != null ? pos(y) : null;
        const era = wt.era || 'undated';
        let row = `<div class="trow" role="listitem" aria-label="${esc(wt.name)}: ${esc(era)}"><span class="lbl">${esc(shortName(wt.name))}</span><span class="tdate">${esc(era)}</span>`;
        if (px != null) row += `<span class="tmark text" title="${esc(era)}" style="left:${px}%"></span>`;
        row += `</div>`;
        html += row;
      });
    } else if (!data.sources.length) {
      html += `<div class="tsub">This chapter has no dated source cards yet.</div>${chapterList}`;
    } else data.sources.forEach(s => {
      const c = cult(s.culture);
      const hasEraDate = /\d/.test(s.traditionEra || '');
      const yt = hasEraDate ? (s.tYear != null ? s.tYear : parseYear(s.traditionEra)) : null;
      const yx = s.xYear != null ? s.xYear : parseYear(s.textRecorded);
      const pt = yt != null ? pos(yt) : null;
      const px = yx != null ? pos(yx) : null;
      const dates = `${s.traditionEra || 'tradition undated'} · ${s.textRecorded || 'text undated'}`;
      let row = `<div class="trow" role="listitem" aria-label="${esc(c.name)}, ${esc(s.work || '')}: ${esc(dates)}"><span class="lbl" style="color:${c.color}">${esc(c.name)}</span><span class="tdate">${esc(dates)}</span>`;
      if (pt != null && px != null) {
        const a = Math.min(pt, px), b = Math.max(pt, px);
        row += `<span class="tline" style="left:${a}%;width:${b - a}%"></span>`;
      }
      if (pt != null) row += `<span class="tmark tradition" title="tradition: ${esc(s.traditionEra)}" style="left:${pt}%;border-color:${c.color}"></span>`;
      if (px != null) row += `<span class="tmark text" title="recorded: ${esc(s.textRecorded)}" style="left:${px}%;background:${c.color}"></span>`;
      row += `</div>`;
      html += row;
    });
    html += witnessMode
      ? `<div class="tlegend"><span><span class="d2"></span> witness dated</span></div>`
      : `<div class="tlegend"><span><span class="d1"></span> proposed tradition era</span><span><span class="d2"></span> text recorded</span></div>`;
    return html;
  }

  /* ---------- index ---------- */
  function buildIndex(chapters) {
    const grid = $('#index .grid');
    chapters.sort((a, b) => (a.meta.spinePosition || 0) - (b.meta.spinePosition || 0));
    chapters.forEach(c => {
      const pageIdx = BOOK.chapters.findIndex(x => x.id === c.meta.id) + pageOffset();
      const ix = el('div', 'ix');
      ix.innerHTML = `<div class="n">${spineLabel(c.meta.spinePosition)}</div>
        <h3>${esc(c.meta.motif)}</h3>
        <p>${esc(c.meta.teaser || '')}</p>
        <div class="st ${c.meta.status}">${c.meta.status === 'complete' ? '✦ Complete' : 'In research'}</div>`;
      const goChapter = () => { closeIndex(); go(pageIdx); };
      ix.onclick = goChapter;
      activable(ix, goChapter);
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
      p.classList.toggle('is-current', i === current);
      p.inert = i !== current;
      p.setAttribute('aria-hidden', String(i !== current));
      if (FLAT_BOOK.matches) {
        // Phones and reduced-motion layouts paint only the active chapter.
        // Explicitly hide unread pages; z-index alone does not isolate them.
        p.style.transform = 'none';
        p.style.opacity = (i === current) ? '1' : '0';
        p.style.pointerEvents = (i === current) ? '' : 'none';
        p.style.visibility = (i === current) ? 'visible' : 'hidden';
      } else {
        // The CURRENT page carries NO transform — so (a) mobile can scroll its
        // cards/content (you can't scroll inside a 3D-transformed element) and
        // (b) the first paint doesn't animate (no flash on load/refresh).
        // Pages not yet reached are hidden so they can't bleed through the
        // current one (z-index is unreliable inside a preserve-3d context).
        // Only flipped-away pages get a transform, for the page-turn animation.
        p.style.opacity = '';
        p.style.pointerEvents = (i === current) ? '' : 'none';
        p.style.visibility = (i > current) ? 'hidden' : '';
        p.style.transform = flipped ? 'rotateY(-178deg)' : 'none';
      }
    });
    // Reset the paper layers and cancel rises scheduled for an earlier page.
    popupTimers.forEach(clearTimeout);
    popupTimers = [];
    pages.forEach(p => p.querySelectorAll('.popup').forEach(u => u.classList.remove('up')));
    const active = pages[current];
    if (active) {
      const pops = active.querySelectorAll('.popup');
      pops.forEach(u => {
        const delay = REDUCED ? 0 : (+u.dataset.delay || 0) + 820; // rise as the page finishes opening
        popupTimers.push(setTimeout(() => u.classList.add('up'), delay));
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
  function closeIndex() {
    if (!$('#index').classList.contains('open')) return;
    $('#index').classList.remove('open');
    // Capture target now; callers may clear lastFocus before the timeout fires.
    const target = lastFocus;
    if (target && target !== document.body) {
      setTimeout(() => { try { target.focus(); } catch (_) {} }, 50);
    }
    lastFocus = null;
  }

  function toggleTimeline() {
    const t = $('#timeline'), open = !t.classList.contains('open');
    if (!open) { closeTimeline(); return; }
    closeDrawer();
    closeIndex();
    lastFocus = document.activeElement;
    buildTimeline();
    t.classList.add('open');
    document.querySelectorAll('#bar,#stage,#prev,#next,#foot,#index,#scrim,#drawer').forEach(node => { node.inert = true; });
    setTimeout(() => { const firstTab = t.querySelector('.atlas-tabs button.active'); if (firstTab) firstTab.focus(); }, 50);
    const btnTime = $('#btnTime');
    if (btnTime) {
      btnTime.classList.add('on');
      btnTime.setAttribute('aria-pressed', 'true');
    }
  }

  function closeTimeline(restoreFocus = true) {
    const t = $('#timeline');
    if (!t.classList.contains('open')) return;
    t.classList.remove('open');
    document.querySelectorAll('#bar,#stage,#prev,#next,#foot,#index,#scrim,#drawer').forEach(node => { node.inert = false; });
    const btnTime = $('#btnTime');
    if (btnTime) { btnTime.classList.remove('on'); btnTime.setAttribute('aria-pressed', 'false'); }
    const target = lastFocus;
    lastFocus = null;
    if (restoreFocus && target && target !== document.body) {
      setTimeout(() => { try { target.focus(); } catch (_) {} }, 50);
    }
  }

  /* ---------- wiring ---------- */
  function wire() {
    // Reapply page isolation when rotating a phone or changing motion settings.
    FLAT_BOOK.addEventListener('change', updatePages);
    $('#next').onclick = next; $('#prev').onclick = prev;
    const lb = $('#btnLens'); if (lb) lb.onclick = toggleLens;
    $('#scrim').onclick = closeDrawer;
    $('#btnIndex').onclick = () => {
      closeTimeline(false);
      const o = !$('#index').classList.contains('open');
      if (o) {
        // Store current focus before opening index
        lastFocus = document.activeElement;
        // Move focus to first index item for accessibility
        setTimeout(() => {
          const firstIx = $('#index .ix');
          if (firstIx) {
            firstIx.setAttribute('tabindex', '-1');
            firstIx.focus();
          }
        }, 50);
      }
      buildIndexState(o);
    };
    $('#btnTime').onclick = toggleTimeline;
    $('#timeline').addEventListener('keydown', e => {
      if (e.key !== 'Tab') return;
      const focusable = [...$('#timeline').querySelectorAll('button, a[href]')];
      if (!focusable.length) return;
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    document.addEventListener('keydown', e => {
      const overlayOpen = $('#timeline').classList.contains('open') || $('#index').classList.contains('open') || $('#drawer').classList.contains('open');
      if (e.key === 'ArrowRight' && !overlayOpen) next();
      else if (e.key === 'ArrowLeft' && !overlayOpen) prev();
      else if (e.key === 'Escape') {
        closeDrawer();
        closeIndex();
        closeTimeline();
      }
    });
    // swipe to turn pages — but NOT when the swipe starts in the lower/card area
    // (so the horizontal tile row scrolls on its own without flipping the chapter)
    let x0 = null, y0 = null, fromLower = false;
    const stage = $('#stage');
    stage.addEventListener('touchstart', e => {
      const t = e.touches[0]; x0 = t.clientX; y0 = t.clientY;
      fromLower = !!(e.target.closest && e.target.closest('.lower'));
    }, { passive: true });
    stage.addEventListener('touchend', e => {
      if (x0 == null) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      x0 = null;
      if (fromLower) return;                                   // tiles/text: let them scroll
      if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return; // need a clear horizontal swipe
      if (dx < 0) next(); else prev();
    }, { passive: true });

    // drag-to-scroll for the horizontal tile rows (mouse + touch, via Pointer Events).
    // On phones the rows set touch-action:none, so the browser never claims the
    // gesture (mobile GPUs break native panning inside/after the 3D page stack);
    // this handler drives it instead: horizontal drags scroll the row (with a
    // momentum fling), vertical drags scroll the surrounding text panel.
    let dsRow = null, dsLower = null, dsX = 0, dsY = 0, dsLeft = 0, dsTop = 0,
        dsAxis = null, dsMoved = false, suppressClick = false,
        dsVel = 0, dsLastX = 0, dsLastT = 0, dsFling = null;
    stage.addEventListener('pointerdown', e => {
      const row = e.target.closest && e.target.closest('.cards');
      if (!row) { dsRow = null; return; }
      if (dsFling) { cancelAnimationFrame(dsFling); dsFling = null; }
      dsRow = row; dsLower = row.closest('.lower');
      dsX = dsLastX = e.clientX; dsY = e.clientY;
      dsLeft = row.scrollLeft; dsTop = dsLower ? dsLower.scrollTop : 0;
      dsAxis = null; dsMoved = false; dsVel = 0; dsLastT = performance.now();
    }, true);
    stage.addEventListener('pointermove', e => {
      if (!dsRow) return;
      const dx = e.clientX - dsX, dy = e.clientY - dsY;
      if (!dsAxis) {
        if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
        dsAxis = Math.abs(dx) >= Math.abs(dy) ? 'x' : 'y';
        dsMoved = true;
      }
      if (dsAxis === 'x') {
        dsRow.scrollLeft = dsLeft - dx;
        const now = performance.now(), dt = now - dsLastT;
        if (dt > 0) { dsVel = (e.clientX - dsLastX) / dt; dsLastX = e.clientX; dsLastT = now; }
      } else if (dsLower) {
        dsLower.scrollTop = dsTop - dy;
      }
    }, true);
    stage.addEventListener('pointerup', () => {
      if (dsRow && dsMoved) {
        suppressClick = true; setTimeout(() => { suppressClick = false; }, 0);
        if (dsAxis === 'x' && Math.abs(dsVel) > 0.25) {          // momentum fling
          let v = -dsVel, row = dsRow, last = performance.now();
          const step = now => {
            const dt = now - last; last = now;
            row.scrollLeft += v * dt;
            v *= Math.pow(0.94, dt / 16);
            if (Math.abs(v) > 0.02) dsFling = requestAnimationFrame(step);
            else dsFling = null;
          };
          dsFling = requestAnimationFrame(step);
        }
      }
      dsRow = null; dsAxis = null;
    }, true);
    stage.addEventListener('pointercancel', () => { dsRow = null; dsAxis = null; }, true);
    stage.addEventListener('click', e => {
      if (suppressClick) { e.stopPropagation(); e.preventDefault(); }
    }, true);
    // mouse wheel over a tile row scrolls it horizontally
    stage.addEventListener('wheel', e => {
      const row = e.target.closest && e.target.closest('.cards');
      if (!row || row.scrollWidth <= row.clientWidth) return;
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      row.scrollLeft += e.deltaY;
      e.preventDefault();
    }, { passive: false });
  }

  /* ---------- helpers ---------- */
  function spineLabel(n) { return ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV'][n] || ''; }
  // Dig sites: a named excavation in the prose links to its record in the Nephilim Wars
  // archaeology encyclopedia (data/digsites.json, synced by tools/sync_digsites.py).
  // Only the first mention per pane is linked; ancient quotations are never touched.
  function loadDigs(dj) {
    const byName = {}, names = [];
    (dj.sites || []).forEach(site => (site.names || []).forEach(n => { const k = esc(n); if (!byName[k]) { byName[k] = site; names.push(k); } }));
    names.sort((a, b) => b.length - a.length);
    const alt = names.map(n => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
    DIG = { byName, byArtifact: dj.artifacts || {}, sites: Object.fromEntries((dj.sites || []).map(x => [x.id, x])),
            re: alt ? new RegExp(`(?<![\\p{L}\\p{N}])(?:${alt})(?![\\p{L}\\p{N}])`, 'gu') : null };
  }
  function digs(text, seen) {
    const h = esc(text);
    if (!DIG || !DIG.re) return h;
    return h.replace(DIG.re, m => {
      const site = DIG.byName[m];
      if (!site || seen.has(site.id)) return m;
      seen.add(site.id);
      return `<a class="dig" href="${esc(site.url)}" target="_blank" rel="noopener" title="Dig site record: ${esc(site.name)}">${m}</a>`;
    });
  }
  function esc(s) { return (s == null ? '' : String(s)).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m])); }
  function cssEsc(s) { return s.replace(/"/g, '\\"'); }

  load().catch(e => { document.body.innerHTML = '<p style="color:#e8dcc0;padding:40px;font-family:sans-serif">Could not load the book — be sure you are running it through a server (python3 tools/serve.py), not opening the file directly.<br><br>' + esc(e.message) + '</p>'; });
})();
