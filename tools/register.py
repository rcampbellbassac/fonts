#!/usr/bin/env python3
"""Add or update a font in the catalog (fonts.json), then rebuild the README table.

  python tools/register.py --id Kamphaeng --name Kamphaeng --native ກຳແພງ --native-lang lo \\
      --category stencil --scripts lo,th,km,latn --status beta --version 0.200 \\
      --description "Heavy stencil display font in the spirit of Black Ops One" \\
      --repo https://github.com/rcampbellbassac/Kamphaeng --made-by "Robert Campbell, Claude"

Only --id is required when updating: other fields keep their current values. Defaults follow the usual
layout of these repos (site = GitHub Pages, woff2 = <site>fonts/<Id>-Regular.woff2, download = latest
release <Id>.zip). `updated` is set to today. `python tools/register.py --check` validates the registry.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "fonts.json"
CATEGORIES = ["script", "handwritten", "painted", "traditional", "fancy", "stencil", "brush", "sans", "serif"]
SCRIPTS = {"lo": "Lao", "th": "Thai", "km": "Khmer", "latn": "Latin"}
STATUSES = ["draft", "beta", "stable", "retired"]
FIELDS = ["id", "name", "native", "native_lang", "category", "scripts", "status", "version", "description",
          "repo", "site", "woff2", "download", "license", "made_by", "updated"]


def load():
    return json.loads(REG.read_text()) if REG.exists() else {"fonts": []}


def save(reg):
    reg["fonts"].sort(key=lambda f: f["name"].lower())
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n")
    readme()


def check(reg) -> list[str]:
    errs, ids = [], set()
    for f in reg["fonts"]:
        w = f"{f.get('id')}: "
        if f.get("id") in ids:
            errs.append(w + "duplicate id")
        ids.add(f.get("id"))
        for k in FIELDS:
            if not f.get(k):
                errs.append(w + f"missing {k}")
        if f.get("category") not in CATEGORIES:
            errs.append(w + f"category must be one of {CATEGORIES}")
        if f.get("status") not in STATUSES:
            errs.append(w + f"status must be one of {STATUSES}")
        if not set(f.get("scripts", [])) <= set(SCRIPTS):
            errs.append(w + f"scripts must be among {list(SCRIPTS)}")
        for k in ("repo", "site", "woff2", "download"):
            if f.get(k) and not f[k].startswith("https://"):
                errs.append(w + f"{k} must be an https URL")
    return errs


def readme():
    reg = load()
    rows = "\n".join(
        f"| [{f['name']}]({f['site']}) | {f['native']} | {f['category']} | "
        f"{', '.join(SCRIPTS[s] for s in f['scripts'])} | {f['version']} {f['status']} | "
        f"[repo]({f['repo']}) · [download]({f['download']}) |" for f in reg["fonts"])
    text = (ROOT / "README.template.md").read_text().replace("{{TABLE}}", rows).replace("{{COUNT}}", str(len(reg["fonts"])))
    (ROOT / "README.md").write_text(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--remove")
    for k in FIELDS:
        if k != "updated":
            ap.add_argument("--" + k.replace("_", "-"))
    a = ap.parse_args()
    reg = load()
    if a.check:
        errs = check(reg)
        print("\n".join(errs) or f"ok: {len(reg['fonts'])} fonts")
        return 1 if errs else 0
    if a.remove:
        reg["fonts"] = [f for f in reg["fonts"] if f["id"] != a.remove]
        save(reg)
        return 0
    if not a.id:
        ap.error("--id is required")
    cur = next((f for f in reg["fonts"] if f["id"] == a.id), None)
    new = dict(cur or {"id": a.id, "license": "OFL-1.1", "status": "beta"})
    for k in FIELDS:
        v = getattr(a, k, None)
        if v is not None:
            new[k] = v.split(",") if k == "scripts" else v
    owner_site = f"https://rcampbellbassac.github.io/{a.id}/"
    new.setdefault("repo", f"https://github.com/rcampbellbassac/{a.id}")
    new.setdefault("site", owner_site)
    new.setdefault("woff2", new["site"].rstrip("/") + f"/fonts/{a.id}-Regular.woff2")
    new.setdefault("download", new["repo"] + f"/releases/latest/download/{a.id}.zip")
    new["updated"] = dt.date.today().isoformat()
    new = {k: new[k] for k in FIELDS if k in new}
    errs = check({"fonts": [new]})
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return 1
    reg["fonts"] = [f for f in reg["fonts"] if f["id"] != a.id] + [new]
    save(reg)
    print(("updated " if cur else "added ") + a.id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
