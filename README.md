# The World Remembers

An interactive **pop-up storybook** that tells the first history of the world **the way its own authors told it** — as testimony, not as "myth." It lays the oldest texts of many peoples side by side so the shared story becomes visible: the matches aren't identical culture to culture, but enough lines up, from enough peoples who never met, to point back to a common source.

It's built to be **digestible for anyone** (folding paper cut-outs that rise on every page) *and* **honestly sourced** (every account dated, provenanced, and — where reproduced — quoted from public-domain translations; see `SOURCES.md`). Framework and vision drawn from the user's GOD_OS and "World Remembers" work; primary ancient texts are the foundation.

## The eleven chapters (the shared story, in order)
1. **Creation — Out of the Deep** — water, darkness, a formless deep, and a power that divides it.
2. **The Garden** — paradise, a tree of life, a serpent, immortality lost.
3. **The Watchers** — beings descend from the sky; forbidden knowledge; the world corrupted.
4. **The Giants** — the half-breed rulers (Nephilim, Igigi, Si-Te-Cah, Nahullo, Manta…), incl. the Dead Sea Scrolls' **Book of Giants**.
5. **The Flood** — 13 traditions across every inhabited continent.
6. **The Reset** — the ~2200 BCE collapse of four civilizations at once.
7. **The Tower** — one language, a tower to heaven, the scattering of peoples.
8. **The Dragon — The Deep Subdued** — a storm-god or hero fights the great serpent of the sea.
9. **The God Who Returns** — a divine figure goes down into death and comes back.
10. **The World Remembers** — where the texts meet the ground: the archaeological evidence.
11. **The Witnesses** — the libraries, caves, and ancient chroniclers that carried it down.

## Run it
```bash
cd ~/storybook
python3 tools/serve.py            # -> http://127.0.0.1:8080
tailscale serve 8080              # phone / public-on-tailnet
```
Must be **served** (not opened as a file://) because the engine fetches JSON.
Deep-links: `?p=3` (page), `#giants` (chapter id), `?p=7&open=timeline`.

## Build the standalone
```bash
python3 tools/build_standalone.py
```
This generates `the-world-remembers.html`, a self-contained file (CSS, JS, all chapter JSON, and every image inlined as data URIs) that can be opened directly from `file://` or deployed to Cloudflare Pages.

## Add or edit content (no code)
- Chapters: `data/chapters/<id>.json` (copy an existing one as a template), then register in `data/book.json`.
- Each source card carries `traditionEra` + `textRecorded` (two dates) and a `quoteType` of `verbatim` (public-domain quote) or `paraphrase` (honest summary).
- Material evidence: add an artifact to `data/artifacts.json`, then list its id in a chapter's `evidence` array — it renders as a "⛏ The ground confirms" card.
- Science lens: add a `science` object to a chapter (see `data/chapters/flood.json` as an example) for the evidence overlay.
- Backdrops: `python3 tools/gen_art.py "scene" -o name` (local FLUX on the R9700). Cut-outs: hand-authored SVGs in `art/cutouts/`.

## Editorial rule
Present the ancient world's account as its authors recorded it. Use neutral words ("account," "tradition," "testimony"), not "myth/legend." Reproduce only public-domain translations; cite everything. Mark anything uncertain or disputed honestly in the `status`/`notes`.
