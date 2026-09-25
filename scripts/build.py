#!/usr/bin/env python3
"""Build Kenti Macroinvertebrados from source.

    python3 scripts/build.py          # dist/kenti-macroinvertebrados.html + launcher/web/ + verificacion/web/
    python3 scripts/build.py --exe    # also the Windows .exe and its .zip (needs Go ≥ 1.22)

Steps: fill src/plantilla.html with src/grupo_macro.json and the genus → family list
(src/familias_macro.json), insert the English dictionary (i18n/en.tsv), check the script,
and copy the page with its icon and fonts into launcher/web/, which the Go launcher embeds.
"""
import json, os, re, shutil, subprocess, sys, zipfile
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parent.parent
DIST = R / "dist"


def dictionary():
    """i18n/en.tsv → {Spanish: English}. Lines: Spanish TAB English; {0}, {#0} (number), {t0} (a name) mark variable parts."""
    d, errs = {}, []
    for i, line in enumerate((R / "i18n/en.tsv").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            errs.append(f"en.tsv:{i}: expected 2 columns, found {len(parts)}"); continue
        es, en = (re.sub(r"\s+", " ", x).strip() for x in parts)
        ph_es = sorted(set(re.findall(r"\{[#t]?(\d+)\}", es))); ph_en = sorted(set(re.findall(r"\{(\d+)\}", en)))
        if ph_es != ph_en:
            errs.append(f"en.tsv:{i}: placeholders differ {ph_es} / {ph_en}")
        if ph_es and not re.search(r"[A-Za-zÁÉÍÓÚáéíóúñ]{2,}", re.sub(r"\{[#t]?\d+\}", "", es)):
            errs.append(f"en.tsv:{i}: a pattern needs some fixed text")
        if es in d and d[es] != en:
            errs.append(f"en.tsv:{i}: repeated with a different translation")
        d[es] = en
    # Continuations that start with «· » also work on their own, once split off.
    for es, en in list(d.items()):
        if es.startswith("· ") and en.startswith("· ") and es[2:] not in d:
            d[es[2:]] = en[2:]
    if errs:
        sys.exit("\n".join(errs))
    return d


def render():
    cfg = json.loads((R / "src/grupo_macro.json").read_text(encoding="utf-8"))
    s = (R / "src/plantilla.html").read_text(encoding="utf-8")
    vals = {k: v for k, v in cfg.items() if k != "GROUP"}
    vals["GROUP_JSON"] = json.dumps(cfg["GROUP"], ensure_ascii=False, separators=(",", ":"))
    vals["FAM_JSON"] = (R / "src/familias_macro.json").read_text(encoding="utf-8").strip()
    s = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: vals[m.group(1)], s)
    js = "const I18N_EN = " + json.dumps(dictionary(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"
    s, n = re.subn(r"/\*I18N-EN-BEGIN\*/.*?/\*I18N-EN-END\*/", lambda m: "/*I18N-EN-BEGIN*/" + js + "/*I18N-EN-END*/", s, flags=re.S)
    assert n == 1, "I18N block not found"
    script = s[s.rindex("<script>"):]
    names = re.findall(r"^\s*function ([A-Za-z0-9_$]+)\s*\(", script, re.M)
    dup = sorted(k for k, v in Counter(names).items() if v > 1)
    assert not dup, "repeated functions: " + ", ".join(dup)
    return s, cfg


def main():
    html, cfg = render()
    DIST.mkdir(exist_ok=True)
    (DIST / "kenti-macroinvertebrados.html").write_text(html, encoding="utf-8")
    web = R / "launcher/web"
    if web.exists():
        shutil.rmtree(web)
    shutil.copytree(R / "src/web", web)
    (web / "index.html").write_text(html, encoding="utf-8")
    print(f"dist/kenti-macroinvertebrados.html · {len(html)//1024} KB")
    # Test page for verificacion/: the same page plus a hook (window.__K) that exposes the real functions.
    hook = (R / "verificacion/gancho.js").read_text(encoding="utf-8")
    assert html.count("\nboot();\n") == 1
    t = R / "verificacion/web"
    t.mkdir(exist_ok=True)
    (t / "index.html").write_text(html.replace("\nboot();\n", "\n" + hook + "boot();\n"), encoding="utf-8")
    if "--exe" not in sys.argv:
        return
    ver = cfg["VERSION"]
    sys.path.insert(0, str(R / "scripts"))
    from icono import escribir_syso
    escribir_syso(R / "src/web/icono.png", R / "launcher/rsrc_windows_amd64.syso")
    exe = DIST / "Kenti Macroinvertebrados.exe"
    env = dict(os.environ, CGO_ENABLED="0", GOOS="windows", GOARCH="amd64")
    subprocess.run(["go", "build", "-trimpath", "-ldflags", "-H windowsgui -s -w", "-o", str(exe), "."],
                   cwd=R / "launcher", env=env, check=True)
    z = DIST / f"Kenti-Macroinvertebrados-v{ver}-Windows.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(exe, exe.name)
        for name in ("LEEME.txt", "README.txt"):
            t = (R / "docs" / name).read_text(encoding="utf-8").replace("\n", "\r\n")
            zf.writestr(name, "﻿" + t)
    print(f"{exe.name} {exe.stat().st_size//1024} KB · {z.name} {z.stat().st_size//1024} KB")


if __name__ == "__main__":
    main()
