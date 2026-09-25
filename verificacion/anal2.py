"""Summary of sim2 (family assignment with typos): correct, no family (with warning), other family."""
import json, collections
d = json.load(open("sim2.json"))
KNOWN = {f for f, o, c in json.load(open("fams_full.json"))}
t = collections.defaultdict(collections.Counter)
for r in d["out"]:
    k = f'{r["nivel"]}_{r["k"]}'
    # correct: the true family (ancylid genera go to Ancylidae on purpose, as the indices score them);
    # other: a different real family; warns: no usable family (empty, or the misspelt name kept with a warning).
    if r["fam"] == r["truth"] or (r["fam"] == "Ancylidae" and r["truth"] == "Planorbidae"): c = "correcta"
    elif r["fam"] in KNOWN or r["via"] == "corregido": c = "otra"
    else: c = "avisa"
    t[k][c] += 1
out = {"tabla": {k: dict(v) for k, v in sorted(t.items())}, "reales": d["reales"], "cruce": d["cruce"]}
for k, v in sorted(t.items()): print(k, dict(v))
json.dump(out, open("res2.json", "w"), ensure_ascii=False)
