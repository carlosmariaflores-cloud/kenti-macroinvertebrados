# Verification / Verificación

Everything runs on **the real Kenti page** (built by `scripts/build.py` into `verificacion/web/`, with a hook,
`gancho.js`, that exposes the page's own functions as `window.__K`), opened in Chromium through Playwright. A small
local server (`servidor_prueba.py`) stands in for the Go launcher. Results are compared with an **independent Python
implementation** (`verif.py`) written from the published tables and rules, not from Kenti's code.

```
pip install playwright && python3 -m playwright install chromium
python3 ../scripts/build.py
python3 verificar.py            # full run (about 15–20 min); --rapido for a quick check
```

| Script | What it does | Result |
|---|---|---|
| `sim1.js` + `verif.py` | 11 × 1000 random communities (seeds 20260925–35): 1–30 taxa, family names, genera and higher groups; random test BMWP' table, NOA table, and NOA + BMWP/Bol | family, BMWP', n, ASPT', ABI and the three classes identical in 11 000/11 000 communities, in each setup |
| `sim2.js` + `anal2.py` | 1000 family names and 1000 genera with 0, 1 and 2 random typos (seed 20260926) | `resultados/res2.json` |
| `sim3.js` + `anal3.py` | The 43 field samples, each name given a typo with probability 0.1, 0.2, 0.3; 1000 replicates (seed 20260927); ABI class with Kenti vs exact name matching | `resultados/res3.json` |
| `sim4.js` | NOA-only vs completed BMWP' in the 43 field samples | `resultados/bmwp_noa_vs_comp.json` |

`reales.json`: the 43 samples (sites numbered, names corrected); raw records in `../datos/`.
`fams_full.json`: family, order and class of the families in the built-in list (used by `verif.py` to map families
to the higher groups the tables score).
