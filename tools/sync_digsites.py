#!/usr/bin/env python3
"""Sync dig-site links from the Nephilim Wars Biblical Archaeology Encyclopedia.

The encyclopedia (nephilim-wars.pages.dev/Archaeology/) is the sourced record for each
excavation. The book does not copy those records; it links to them. This writes
data/digsites.json: the names the book's prose may use for each site, and which of the
book's own artifact cards correspond to which site record.

    python3 tools/sync_digsites.py [path/to/sites.json]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/companion/Nephilim-Wars/public/Archaeology/data/sites.json")
BASE = "https://nephilim-wars.pages.dev/Archaeology/"

# Names too bare to auto-link: they name people, books or whole regions far more often
# than the excavation (every "Isaiah" is not the Isaiah Scroll).
STOP = {
    "isaiah", "hezekiah", "nehemiah", "solomon", "david", "pilate", "caiaphas", "cyrus",
    "sennacherib", "merneptah", "nebuchadnezzar", "jehoiachin", "baruch", "erastus", "gallio",
    "sargon", "sargon ii", "xerxes", "ahasuerus", "mesha", "peter", "tobiah", "shalmaneser",
    "tiglath-pileser", "tiglath-pileser iii", "temple", "temple mount", "jerusalem", "babylon",
    "egypt", "israel", "judah", "samaria", "galilee", "ararat", "mount ararat", "nazareth",
    "capernaum", "qumran", "persepolis", "susa", "gezer", "megiddo", "lachish", "siloam",
    "ophel", "city of david", "dead sea scrolls",
}

# Exact names never auto-linked: contested identifications (linking "Sodom" to Tall el-Hammam
# would assert what the record calls disputed), people, and places broader than one dig.
EXCLUDE = {
    "Sodom", "Cities of the Plain", "Eglon", "Shaaraim", "Millo",
    "Pontius Pilate", "Pontius Pilatus", "Shishak", "Shoshenq", "Abdi-Heba", "Garstang", "Kenyon",
    "Zertal", "Sethe", "Balaam son of Beor", "Gedaliah son of Pashhur", "Gemariah son of Shaphan",
    "Hezekiah son of Ahaz", "Joseph son of Caiaphas", "Israel is laid waste",
    "Caesarea", "Ashdod", "Doğubayazıt", "Dogubayazit", "Habiru", "Hurrian", "Nineveh palace reliefs",
}
# A name two records share goes to the main record for that place.
PREFER = {"Hazor": "hazor", "Western Wall": "western-wall", "Great Isaiah Scroll": "isaiah-scroll",
          "Isaiah Scroll": "isaiah-scroll", "Kfar Nahum": "capernaum-synagogue"}

# The book's own artifact cards -> the encyclopedia record for the same find.
ARTIFACTS = {
    "tall-el-hammam": "tall-el-hammam",
    "merneptah-stele": "merneptah-stele",
    "soleb-yhw": "soleb-inscription",
    "jericho-cityiv": "jericho",
    "hazor-destruction": "hazor",
    "tel-dan-stele": "tel-dan-stele",
    "khirbet-qeiyafa": "khirbet-qeiyafa-ostracon",
    "mesha-stele": "mesha-stele",
    "kurkh-monolith": "kurkh-monolith",
    "black-obelisk": "black-obelisk",
    "lachish-siege": "lachish-reliefs",
    "sennacherib-prism": "taylor-prism-sennacherib",
    "hezekiah-tunnel": "hezekiah-tunnel-inscription",
    "hezekiah-bulla": "hezekiah-bulla",
    "ketef-hinnom": "silver-amulets-ketef-hinnom",
    "lachish-letters": "lachish-letters",
    "jehoiachin-tablets": "jehoiachin-rations-tablets",
    "cyrus-cylinder": "cyrus-cylinder",
    "pilate-stone": "pilate-inscription",
    "caiaphas-ossuary": "caiaphas-ossuary",
    "pool-of-bethesda": "bethesda-pool",
    "gallio-inscription": "gallio-inscription",
    "nuzi-tablets": "nuzi-tablets",
    "six-chambered-gates": "gezer-six-chambered-gate",
    # present only if the encyclopedia carries them
    "mt-ebal-altar": "mount-ebal-altar",
    "deir-alla-balaam": "deir-alla-inscription",
    "jeremiah-bullae": "jeremiah-bullae",
    "amarna-letters": "amarna-letters",
    "bubastite-portal": "bubastite-portal",
}


def names_for(site):
    raw = [site["name"], *site.get("aka", []), *site.get("storybook_names", [])]
    # drop parentheticals: "Taylor Prism (Sennacherib's Annals)" -> "Taylor Prism"
    raw += [re.sub(r"\s*\(.*?\)", "", n) for n in raw]
    out = []
    for n in raw:
        n = n.strip(" .,;:")
        if len(n) < 4 or not n[0].isupper() or n.lower() in STOP or n in EXCLUDE or n in out:
            continue
        out.append(n)
    return out


def main():
    db = json.load(open(SRC))
    sites = [{"id": s["id"], "name": s["name"], "url": f"{BASE}{s['id']}.html", "names": names_for(s)}
             for s in db["sites"]]
    ids = {s["id"] for s in sites}
    # a name claimed by two sites links to neither
    seen = {}
    for s in sites:
        for n in s["names"]:
            seen.setdefault(n.lower(), set()).add(s["id"])
    pref = {k.lower(): v for k, v in PREFER.items()}
    for s in sites:
        s["names"] = [n for n in s["names"]
                      if len(seen[n.lower()]) == 1 or pref.get(n.lower()) == s["id"]]
    arts = {a: d for a, d in ARTIFACTS.items() if d in ids}
    out = {"source": "Nephilim Wars Biblical Archaeology Encyclopedia", "base": BASE,
           "checked_through": db.get("checked_through"), "sites": sites, "artifacts": arts}
    path = f"{ROOT}/data/digsites.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    dropped = sorted(n for n, v in seen.items() if len(v) > 1 and n not in pref)
    print(f"WROTE {path}: {len(sites)} sites, {sum(len(s['names']) for s in sites)} names, "
          f"{len(arts)} artifact cards linked; ambiguous names dropped: {dropped or 'none'}")


if __name__ == "__main__":
    main()
