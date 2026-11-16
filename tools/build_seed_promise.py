"""Build the closing exhibit, Following the Seed Promise (exhibits/seed-promise/).

Source of truth: exhibits/seed-promise/content.html — a page fragment (<title>, <style>, body markup, <script>)
with {{BOOK}} standing for the book's root URL.

Writes:
  exhibits/seed-promise/index.html   full document for the site ({{BOOK}} -> ../../)
  --artifact PATH (optional)            fragment copy with absolute links, for the private claude.ai artifact
"""
import argparse, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "exhibits" / "seed-promise"
SITE = "https://ancient-memory.pages.dev/"

DESC = ("The closing exhibit of The World Remembers: following the seed promise of Genesis 3:15 to Jesus of Nazareth through the verifiable evidence — Roman, Jewish and "
        "pagan witnesses, Paul's letters, manuscripts, archaeology, Isaiah 53 and Psalm 22 in copies made before Christ, "
        "and the resurrection evidence, each source cited and objections answered.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact")
    a = ap.parse_args()
    frag = (DIR / "content.html").read_text(encoding="utf-8")
    m = re.match(r"\s*<title>(.*?)</title>\s*", frag, re.S)
    assert m, "content.html must start with <title>"
    body = frag[m.end():]
    page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            "<title>Following the Seed Promise — The World Remembers</title>\n"
            f"<meta name=\"description\" content=\"{DESC}\">\n"
            f"<link rel=\"canonical\" href=\"{SITE}exhibits/seed-promise/\">\n"
            "<style>html{background:#0d0b08}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
            + body.replace("{{BOOK}}", "../../").replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "", 1)
              .replace("</style>", "</style>\n</head>\n<body>", 1)
            + "\n</body>\n</html>\n")
    (DIR / "index.html").write_text(page, encoding="utf-8")
    print("wrote", DIR / "index.html", len(page), "bytes")
    if a.artifact:
        pathlib.Path(a.artifact).write_text(frag.replace("{{BOOK}}", SITE), encoding="utf-8")
        print("wrote", a.artifact)

if __name__ == "__main__":
    main()
