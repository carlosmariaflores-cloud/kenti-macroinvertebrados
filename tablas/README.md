# Score tables / Tablas de puntaje

Transcribed from the original publications (scanned PDFs, 300 dpi) on 25 September 2026. Spellings of the original
that differ from the current name are kept in the `nota` column. `a_csv.py` writes the CSV files from the Python lists;
the same entries are built into `src/plantilla.html` (`BMWP_KENTI`, `BMWPBOL_KENTI`, `ABI_KENTI`).

| File | Source | Entries |
|---|---|---|
| `bmwp_noa_1998.py` · `bmwp_noa_dominguez_fernandez_1998.csv` | Domínguez, E. & Fernández, H. R. (1998). Calidad de los ríos de la cuenca del Salí (Tucumán, Argentina) medida por un índice biótico. *Serie Conservación de la Naturaleza*, 12. Fundación Miguel Lillo. Table 8, p. 39 (classes: Table 5). | 53 |
| `bmwp_bol_2012.py` · `bmwp_bol_mmaya_2012.csv` | MMAyA (2012), BMWP/Bol, as given in Leaño Sanabria, J. & Pérez Barriga, R. (2020). *Acta Nova*, 9(4), 569–591, Table 1. | 88 |
| `abi_2009.py` · `abi_prat_et_al_2009.csv` | Prat, N., Ríos, B., Acosta, R. & Rieradevall, M. (2009). In Domínguez, E. & Fernández, H. R. (eds.), *Macroinvertebrados bentónicos sudamericanos*. Fundación Miguel Lillo. Table 5, p. 643 (ABI of Ríos-Touma et al. 2014). | 72 |

How Kenti uses them: an exact name first, then nomenclatural equivalents (e.g. Limoniidae → Tipulidae,
Crambidae → Pyralidae, Leptohyphidae → Tricorythidae), then an order entry such as «Odonata (varias fam.)» (each
family of the order counts separately), then the group above family (Oligochaeta, Hirudinea, Hydracarina,
Turbellaria, Ostracoda, Amphipoda). The Bolivian table is used only for families the NOA table does not score.
