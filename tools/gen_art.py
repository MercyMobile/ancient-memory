#!/usr/bin/env python3
"""Generate atmospheric backdrops for the storybook via local lemonade FLUX.

Hits the OpenAI-style images endpoint on the R9700 (Flux-2-Klein-4B). A fixed
style prefix keeps every backdrop visually consistent so they read as one book.
Generation is serialized on the GPU by lemonade itself; run prompts one at a time.

    python3 tools/gen_art.py "the great deluge, rain-lashed flood waters"
    python3 tools/gen_art.py "stormy primordial sea" -o deluge -s 1216x832

Files land in art/backdrops/<name>.png. Use --no-style to skip the style prefix.
"""
import argparse, base64, json, os, re, sys, urllib.request, urllib.error

LEMON = os.environ.get("LEMON_URL", "http://127.0.0.1:13305")
MODEL = os.environ.get("FLUX_MODEL", "Flux-2-Klein-4B")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "art", "backdrops")

# One house style for the whole book: aged illustrated plate, no text, no people-focus
# (people are the folding SVG cut-outs; backdrops are atmosphere/landscape only).
STYLE = ("antique hand-tinted engraving, ink-and-wash storybook plate on aged "
         "parchment, muted earthy palette, soft painterly atmosphere, cinematic "
         "depth, no text, no lettering, no borders, empty landscape, ")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "backdrop"


def generate(prompt, size):
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": size, "n": 1}).encode()
    req = urllib.request.Request(LEMON + "/api/v1/images/generations", data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.load(r)
    item = data["data"][0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as r:
            return r.read()
    raise RuntimeError("no image payload in response: " + json.dumps(item)[:200])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("-o", "--out", help="output name (default: from prompt)")
    ap.add_argument("-s", "--size", default="1216x832")
    ap.add_argument("--no-style", action="store_true")
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    full = a.prompt if a.no_style else STYLE + a.prompt
    name = slug(a.out or a.prompt)
    path = os.path.join(OUT, name + ".png")

    print(f"[gen] model={MODEL} size={a.size}\n[gen] {full[:90]}...")
    try:
        png = generate(full, a.size)
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: cannot reach lemonade at {LEMON} ({e}). Is the daemon up?")
    with open(path, "wb") as f:
        f.write(png)
    print(f"[ok] wrote {path} ({len(png)//1024} KB)")
    print("     (optional upscale: RealESRGAN-x4plus via lemonade if needed)")


if __name__ == "__main__":
    main()
