#!/usr/bin/env python3
"""Generate storybook backdrops via Novita FLUX.2 Pro (cloud).

Companion to gen_art.py, which uses the local lemonade R9700 pipeline. Same house
style prefix so the plates read as one book. Novita's endpoint is async: POST the
job, poll task-result, then fetch the finished image.

The API key is NOT stored here. Pass it in the environment:

    NOVITA_API_KEY=... python3 tools/gen_art_novita.py "night sky over the wilderness" -o mazzaroth

Files land in art/backdrops/<name>.png at 1216x832, matching the existing plates.
"""
import argparse, base64, io, json, os, re, sys, time, urllib.parse, urllib.request

KEY = os.environ.get("NOVITA_API_KEY", "")
GEN_URL = "https://api.novita.ai/v3/async/flux-2-pro"
TASK_URL = "https://api.novita.ai/v3/async/task-result"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "art", "backdrops")
UA = "Mozilla/5.0 (X11; Linux x86_64)"

# House style. Built from gen_art.py's STYLE (which produced the existing plates)
# plus the aged-plate cues actually visible in them: foxed paper, centre fold,
# sepia/umber wash. "No text" is repeated hard — pseudo-lettering would wreck a
# book whose whole claim is scholarly accuracy.
STYLE = (
    "antique hand-tinted steel engraving, ink-and-wash storybook plate printed on aged "
    "foxed parchment, visible paper grain and browned edges, faint vertical centre fold "
    "crease, muted earthy sepia and umber palette with cold silver highlights, fine "
    "cross-hatched linework, soft painterly atmosphere, cinematic depth, "
    "absolutely no text, no lettering, no letters, no numerals, no captions, no signature, "
    "no inscriptions, no symbols, no writing of any kind, empty of people, "
)


def headers():
    return {"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}


def result_url(out, timeout=300):
    imgs = out.get("images") or []
    if imgs:
        return imgs[0].get("image_url")
    task_id = (out.get("task") or {}).get("task_id") or out.get("task_id")
    if not task_id:
        raise RuntimeError("novita: no images and no task_id: " + json.dumps(out)[:300])
    print(f"    task {task_id} queued; polling…", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(3)
        q = urllib.request.Request(TASK_URL + "?task_id=" + urllib.parse.quote(task_id),
                                   headers={"Authorization": "Bearer " + KEY})
        with urllib.request.urlopen(q, timeout=30) as r:
            res = json.loads(r.read())
        task = res.get("task") or {}
        status = task.get("status", "")
        if status == "TASK_STATUS_SUCCEED":
            ri = res.get("images") or []
            if not ri:
                raise RuntimeError("novita: succeeded but no images")
            return ri[0].get("image_url")
        if status == "TASK_STATUS_FAILED":
            raise RuntimeError("novita task failed: " + str(task.get("reason", "")))
        print(f"    …{status or 'pending'} ({int(deadline - time.time())}s left)", flush=True)
    raise RuntimeError("novita: task timed out")


def generate(prompt, width, height):
    # Novita's flux-2-pro has ignored width/height in testing and returned 1024x1024;
    # aspect_ratio is sent too, and the caller center-crops rather than stretching.
    from math import gcd
    g = gcd(width, height)
    body = json.dumps({"prompt": prompt[:1024], "width": int(width), "height": int(height),
                       "aspect_ratio": f"{width//g}:{height//g}"}).encode()
    req = urllib.request.Request(GEN_URL, data=body, method="POST", headers=headers())
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.loads(r.read())
    url = result_url(out)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
        return r.read()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "backdrop"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("-o", "--out")
    ap.add_argument("-W", "--width", type=int, default=1216)
    ap.add_argument("-H", "--height", type=int, default=832)
    ap.add_argument("--no-style", action="store_true")
    a = ap.parse_args()

    if not KEY:
        sys.exit("ERROR: no NOVITA_API_KEY in environment.")
    os.makedirs(OUT, exist_ok=True)
    full = a.prompt if a.no_style else STYLE + a.prompt
    name = slug(a.out or a.prompt)
    path = os.path.join(OUT, name + ".png")

    print(f"[gen] flux-2-pro {a.width}x{a.height} -> {name}.png", flush=True)
    raw = generate(full, a.width, a.height)

    # Normalize to PNG at the book's exact plate size. NEVER stretch: if the returned
    # aspect differs, center-crop to the target ratio first, then scale. A stretched
    # plate is instantly visible next to the others.
    from PIL import Image
    open(os.path.join(OUT, name + ".raw.png"), "wb").write(raw)
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.size != (a.width, a.height):
        w, h = im.size
        target = a.width / a.height
        if abs(w / h - target) > 1e-3:
            if w / h > target:                      # too wide -> trim sides
                nw = int(round(h * target)); box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
            else:                                   # too tall -> trim top/bottom
                nh = int(round(w / target)); box = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
            print(f"    returned {im.size}; center-cropping to {box[2]-box[0]}x{box[3]-box[1]}")
            im = im.crop(box)
        print(f"    scaling {im.size} -> ({a.width}, {a.height})")
        im = im.resize((a.width, a.height), Image.LANCZOS)
    im.save(path, "PNG")

    print(f"[ok] {path}  ({os.path.getsize(path)//1024} KB)")


if __name__ == "__main__":
    main()
