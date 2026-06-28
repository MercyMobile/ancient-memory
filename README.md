# The World Remembers

An interactive **pop-up storybook** that tells the first history of the world **the way its own authors told it** — as testimony, not as "myth." It lays the oldest texts of many peoples side by side so the shared story becomes visible: the matches aren't identical culture to culture, but enough lines up, from enough peoples who never met, to point back to a common source.

It's built to be **digestible for anyone** (folding paper cut-outs that rise on every page) *and* **honestly sourced** (every account dated, provenanced, and — where reproduced — quoted from public-domain translations; see `SOURCES.md`). Framework and vision drawn from the user's GOD_OS and "World Remembers" work; primary ancient texts are the foundation.

## The seven chapters (the shared story, in order)
1. **The Garden** — paradise, a tree of life, a serpent, immortality lost.
2. **The Watchers** — beings descend from the sky; forbidden knowledge; the world corrupted.
3. **The Giants** — the half-breed rulers (Nephilim, Igigi, Si-Te-Cah, Nahullo, Manta…), incl. the Dead Sea Scrolls' **Book of Giants**.
4. **The Flood** — 13 traditions across every inhabited continent.
5. **The Reset** — the ~2200 BCE collapse of four civilizations at once.
6. **The Tower** — one language, a tower to heaven, the scattering of peoples.
7. **The World Remembers** — where the texts meet the ground: the archaeological evidence.

## Run it
```bash
cd ~/storybook
python3 tools/serve.py            # -> http://127.0.0.1:8080
tailscale serve 8080              # phone / public-on-tailnet
```
Must be **served** (not opened as a file://) because the engine fetches JSON.
Deep-links: `?p=3` (page), `#giants` (chapter id), `?p=7&open=timeline`.

## Add or edit content (no code)
- Chapters: `data/chapters/<id>.json` (copy an existing one as a template), then register in `data/book.json`.
- Each source card carries `traditionEra` + `textRecorded` (two dates) and a `quoteType` of `verbatim` (public-domain quote) or `paraphrase` (honest summary).
- Material evidence: add an artifact to `data/artifacts.json`, then list its id in a chapter's `evidence` array — it renders as a "⛏ The ground confirms" card.
- Backdrops: `python3 tools/gen_art.py "scene" -o name` (local FLUX on the R9700). Cut-outs: hand-authored SVGs in `art/cutouts/`.

## Editorial rule
Present the ancient world's account as its authors recorded it. Use neutral words ("account," "tradition," "testimony"), not "myth/legend." Reproduce only public-domain translations; cite everything. Mark anything uncertain or disputed honestly in the `status`/`notes`.
