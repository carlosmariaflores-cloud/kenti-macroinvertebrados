#!/usr/bin/env python3
"""Runs every check of the paper on the real Kenti page (Chromium + Playwright) and compares it with verif.py.

    cd verificacion && python3 ../scripts/build.py && python3 verificar.py [--rapido]

1. 11 series × 1000 random communities (seeds 20260925–20260935) with three score-table setups:
   a random test BMWP' table, the NOA BMWP' table, and the NOA table completed with BMWP/Bol.
   Kenti and the independent Python implementation must agree on family, BMWP', n, ASPT', ABI and classes.
2. Family assignment with 0, 1 and 2 typos (sim2, seed 20260926) → res2.json.
3. ABI class changes with typos in the 43 real samples, 1000 replicates per rate (sim3, seed 20260927) → res3.json.
4. NOA-only vs completed BMWP' in the 43 real samples (sim4) → bmwp_noa_vs_comp.json.
--rapido: 2 seeds and 100 replicates, to check that everything runs.
"""
import json, re, subprocess, sys, time, pathlib
H = pathlib.Path(__file__).parent
rapido = "--rapido" in sys.argv
srv = subprocess.Popen([sys.executable, "servidor_prueba.py", "web", "47900"], cwd=H)
time.sleep(1.5)
def run(js, cfg, out):
    subprocess.run([sys.executable, "correr.py", js, json.dumps(cfg), out], cwd=H, check=True, stdout=subprocess.DEVNULL)
try:
    total = ok = 0
    seeds = range(20260925, 20260927 if rapido else 20260936)
    for nombre, extra in (("prueba", {}), ("noa", {"real": True}), ("noa+bol", {"real": True, "comp": True})):
        for s in seeds:
            out = f"v_{nombre}_{s}.json"
            run("sim1.js", {"seed": s, "n": 1000, **extra}, out)
            txt = subprocess.run([sys.executable, "verif.py", out], cwd=H, capture_output=True, text=True, check=True).stdout
            got = [tuple(map(int, m)) for m in re.findall(r": (\d+)/(\d+) coinciden", txt)]
            fam = int(re.search(r"familia asignada distinta: (\d+)", txt).group(1))
            good = all(a == b for a, b in got) and fam == 0
            total += 1; ok += good
            print(f"{nombre:8} semilla {s}: {'OK' if good else 'DIFERENCIA'}" + ("" if good else "\n" + txt))
    print(f"\n1) verificación: {ok}/{total} series idénticas ({ok * 1000} comunidades)")
    run("sim2.js", {"seed": 20260926, "n": 1000}, "sim2.json")
    subprocess.run([sys.executable, "anal2.py"], cwd=H, check=True)
    reales = json.load(open(H / "reales.json"))
    subprocess.run([sys.executable, "-c", f"""
import json, sys
from playwright.sync_api import sync_playwright
js = open("sim3.js").read(); data = json.load(open("reales.json"))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto("http://127.0.0.1:47900/"); pg.wait_for_timeout(1500)
    r = pg.evaluate(js, {{"seed": 20260927, "reps": {100 if rapido else 1000}, "rates": [0.1, 0.2, 0.3], "data": data}})
    json.dump(r, open("sim3.json", "w")); b.close()
"""], cwd=H, check=True)
    # anal3 uses the ABI table of one sim1 run
    import shutil; shutil.copy(H / f"v_noa_{seeds[0]}.json", H / "sim1.json")
    subprocess.run([sys.executable, "anal3.py"], cwd=H, check=True)
    res = {}
    for off in (False, True):
        run("sim4.js", {"data": reales, "off": off}, "sim4.json")
        res["noa" if off else "com"] = json.load(open(H / "sim4.json"))
    json.dump(res, open(H / "bmwp_noa_vs_comp.json", "w"), ensure_ascii=False)
    cls = lambda r: r["cB"].split(" ")[0]
    up = sum(cls(a) != cls(b) for a, b in zip(res["noa"], res["com"]))
    print(f"4) BMWP': la clase cambia al completar con BMWP/Bol en {up} de {len(reales)} muestras")
    for f in ("res2.json", "res3.json", "bmwp_noa_vs_comp.json"):
        (H / f).replace(H / "resultados" / f)
    print("resultados/ actualizado")
finally:
    srv.terminate()
