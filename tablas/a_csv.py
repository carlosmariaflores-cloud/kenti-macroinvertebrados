"""Writes the three transcribed score tables as CSV (UTF-8): family or group, score, order/group, note."""
import csv, pathlib
H = pathlib.Path(__file__).parent
ns = {}
exec((H / "bmwp_noa_1998.py").read_text(encoding="utf-8"), ns)
exec((H / "abi_2009.py").read_text(encoding="utf-8"), ns)
exec((H / "bmwp_bol_2012.py").read_text(encoding="utf-8"), ns)
def w(name, rows):
    with open(H / name, "w", newline="", encoding="utf-8") as f:
        c = csv.writer(f); c.writerow(["familia_o_grupo", "puntaje", "orden_o_grupo", "nota"]); c.writerows(rows)
    print(name, len(rows))
w("bmwp_noa_dominguez_fernandez_1998.csv", [(n, s, "", nota) for s, n, nota in ns["NOA"]])
w("abi_prat_et_al_2009.csv", [(n, s, o, "") for n, s, o in ns["ABI"]])
w("bmwp_bol_mmaya_2012.csv", [(n, s, "", ns["NOTAS"].get(n, "")) for n, s in ns["ROWS"]])
