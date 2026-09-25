"""Implementación independiente (Python) de BMWP', ASPT' y ABI para verificar Kenti."""
import json, sys, collections, unicodedata
d = json.load(open(sys.argv[1]))
fams = d["fams"]; gen = d["gen"]
def norm(s): return unicodedata.normalize("NFD", s).encode("ascii","ignore").decode().lower().strip()
GROUPS = {"copepoda":"Copepoda","oligochaeta":"Oligochaeta","hirudinea":"Hirudinea","hydracarina":"Hydracarina","acari":"Hydracarina",
          "turbellaria":"Turbellaria","ostracoda":"Ostracoda","collembola":"Collembola","nematoda":"Nematoda"}
ANCYL = set("ancylus hebetancylus uncancylus gundlachia ferrissia anisancylus laevapex".split())
def resolve(name):
    w = norm(name).replace(" sp.","").split()[0]
    if w in GROUPS: return GROUPS[w]
    if w.endswith("idae"): return w.capitalize()
    if w in ANCYL: return "Ancylidae"
    i = gen.get(w)
    return fams[i] if isinstance(i, int) else ""
# Familias que las tablas puntúan como grupo (clase u orden por encima de familia)
FAM2GROUP = {}
for f, o, c in [(f[0], f[1], f[2]) for f in [[x] + [None, None] for x in []]]: pass
ORDER_CLASS = {}  # se arma con la lista del proyecto
import re
famrows = json.load(open("fams_full.json"))
ORDEN = {f: o for f, o, c in famrows}; VARIAS = set()
for f, o, c in famrows:
    if c == "Clitellata" and o in ("Tubificida","Lumbriculida","Enchytraeida","Haplotaxida","Alluroidida"): FAM2GROUP[f] = "Oligochaeta"
    elif c == "Clitellata": FAM2GROUP[f] = "Hirudinea"
    elif o == "Trombidiformes": FAM2GROUP[f] = "Hydracarina"
    elif o == "Tricladida": FAM2GROUP[f] = "Turbellaria"
    elif c == "Ostracoda": FAM2GROUP[f] = "Ostracoda"
    elif o == "Amphipoda": FAM2GROUP[f] = "Amphipoda"
EQUIV = {"Limoniidae":["Tipulidae"],"Pediciidae":["Tipulidae"],"Cochliopidae":["Hydrobiidae"],"Tateidae":["Hydrobiidae"],
         "Lithoglyphidae":["Hydrobiidae"],"Pomatiopsidae":["Hydrobiidae"],"Micronectidae":["Corixidae"],"Ancylidae":["Planorbidae"],
         "Dugesiidae":["Planariidae"],"Planariidae":["Dugesiidae"],"Naididae":["Tubificidae"],"Tubificidae":["Naididae"],"Crambidae":["Pyralidae"],"Leptohyphidae":["Tricorythidae"]}
def score(tab, fam):
    t = {}
    for r in tab:
        n = r["name"]
        if "varias" in n:
            o = n.split("(")[0].strip(); VARIAS.add(o); t.setdefault(o, r["score"]); continue
        if "rojos" in n: t.setdefault(n, r["score"]); continue
        if "(" in n:   # «Scirtidae (Helodidae)»: vale para los dos nombres
            a, b = n.split("(")[0].strip(), n.split("(")[1].strip(" )")
            t.setdefault(a, r["score"]); t.setdefault(b, r["score"])
        else: t.setdefault(n, r["score"])
    if fam in t: return fam, t[fam]
    for a in EQUIV.get(fam, []):
        if a in t: return a, t[a]
    o = ORDEN.get(fam)          # «Odonata (varias fam.)», «Hemiptera (varias fam.)»: la familia puntúa por su orden
    if o and o in t and o in VARIAS: return o + ':' + fam, t[o]   # cada familia del orden suma por separado
    g = FAM2GROUP.get(fam)
    if g and g in t: return g, t[g]
    return None, None
def bmwp_cls(v): return "Aguas muy limpias" if v>50 else "Aguas no contaminadas" if v>=40 else "Con algún grado de contaminación" if v>=30 else "Aguas contaminadas" if v>=20 else "Aguas muy contaminadas" if v>=10 else "Aguas fuertemente contaminadas"
def aspt_cls(v): return None if v is None else "Muy limpia" if v>=6 else "Buena" if v>=5.4 else "Aceptable" if v>=4.9 else "Dudosa" if v>=4 else "Crítica" if v>=3 else "Muy crítica"
R = d["abiRef"]; L = [round(R*f) for f in (1,.61,.36,.15)]
def abi_cls(v): return "Muy buena" if v>=L[0] else "Buena" if v>=L[1] else "Regular" if v>=L[2] else "Mala" if v>=L[3] else "Muy mala"
diff = collections.Counter(); ex = collections.defaultdict(list); famdiff = collections.Counter(); famex = []
for name, r in d["resolved"].items():
    mine = resolve(name)
    if mine != r["fam"]:
        famdiff[1] += 1
        if len(famex) < 15: famex.append((name, mine, r["fam"], r["via"]))
maxerr = 0.0
for i, (cm, k) in enumerate(zip(d["comms"], d["res"])):
    out = {}
    for tabname, tab in (("B", d["bmwp"]), ("A", d["abi"])):
        seen = {}
        for name, _ in cm:
            f = resolve(name); e, s = score(tab, f)
            if not e and tabname == "B" and d.get("bmwpc"):          # complemento boliviano: sólo lo que el NOA no tiene
                e, s = score(d["bmwpc"], f)
                if e: e = "c:" + e
            if e: seen[e] = s
        out[tabname] = (sum(seen.values()), len(seen), seen)
    B, nB, sB = out["B"]; A, nA, sA = out["A"]
    aspt = B / nB if nB else None
    checks = {"BMWP": B == k["BMWP"], "nB": nB == k["nB"], "ABI": A == k["ABI"], "nA": nA == k["nA"],
              "ASPT": (aspt is None and k["ASPT"] is None) or (aspt is not None and k["ASPT"] is not None and abs(aspt - k["ASPT"]) < 1e-12),
              "cB": bmwp_cls(B) == k["cB"], "cS": aspt_cls(aspt) == k["cS"], "cA": abi_cls(A) == k["cA"]}
    if aspt is not None and k["ASPT"] is not None: maxerr = max(maxerr, abs(aspt - k["ASPT"]))
    for c, ok in checks.items():
        if not ok:
            diff[c] += 1
            if len(ex[c]) < 5: ex[c].append((i, k.get(c), {"B":B,"nB":nB,"A":A,"nA":nA}.get(c), k["viaB"] if "B" in c else k["viaA"]))
n = len(d["res"])
print("comunidades:", n, "| nombres distintos:", len(d["resolved"]))
print("familia asignada distinta:", famdiff[1], famex)
print("máx. diferencia ASPT:", maxerr)
for c in ["BMWP","nB","ASPT","ABI","nA","cB","cS","cA"]:
    print(f"{c}: {n - diff[c]}/{n} coinciden", ex.get(c, ""))
