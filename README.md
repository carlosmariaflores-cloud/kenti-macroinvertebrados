# Kenti Macroinvertebrados

Free desktop program for benthic macroinvertebrate data from rivers of northwestern Argentina and the Andes.
You paste the sampling table from Excel; Kenti proposes the family of each taxon, computes the biotic indices and
exports an Excel report that records where every family and every score came from.

*[En español, más abajo.](#en-español)*

## What it does

- **Family from the name.** Taxa can be written at whatever level they were identified (species, genus, family or a
  group such as Oligochaeta). Kenti proposes the family from a built-in list of 5802 genera of aquatic
  macroinvertebrates recorded in South America (232 families, GBIF Backbone Taxonomy), works offline, corrects
  spelling mistakes by edit distance and marks every proposal: blue for a proposal, amber for a corrected spelling
  or a genus found in more than one family. What the user types is never changed.
- **Biotic indices**, each with its own table, classes and citation:
  - **BMWP'** for northwestern Argentina (Domínguez & Fernández 1998, Table 8; classes of their Table 5).
    Families missing from that table are completed with the Bolivian **BMWP/Bol** (MMAyA 2012, in Leaño Sanabria &
    Pérez Barriga 2020); the class is still that of the NOA table. The completion can be switched off.
  - **ASPT'** (BMWP' / number of scored families), with the classes of Cammaerts et al. (2008).
  - **ABI**, Andean Biotic Index (Ríos-Touma et al. 2014; table of Prat et al. 2009), with classes computed from the
    basin reference value (96 by default). Sites below 2000 m a.s.l. are flagged.
- Alpha diversity (S, N, Shannon, Simpson, Margalef, Menhinick, Pielou), beta diversity (Jaccard, Morisita-Horn,
  Bray-Curtis, UPGMA), correlation with physicochemical variables and PCA.
- **Excel report** with the data table, the family source of each taxon, all indices and all charts.
- **Spanish and English interface** (ES / EN button at the top right). Numbers follow the language: decimal comma in
  Spanish, decimal point in English.

## Download and use

Download `Kenti-Macroinvertebrados-v0.5-Windows.zip` from [Releases](../../releases), unzip it and double-click
`Kenti Macroinvertebrados.exe`. It opens in its own window (Microsoft Edge or Google Chrome, already on Windows 10/11)
and saves every change to `Documents\Kenti Macroinvertebrados\datos-macroinvertebrados.json`. The first time,
Windows may show "Windows protected your PC" because the program is not digitally signed: click *More info* →
*Run anyway*.

`kenti-macroinvertebrados.html`, also in Releases, is the same program as a single web page: it runs in any modern
browser, on any system, and keeps the data in that browser.

## Build from source

```
python3 scripts/build.py          # dist/kenti-macroinvertebrados.html, launcher/web/ and verificacion/web/
python3 scripts/build.py --exe    # also dist/Kenti Macroinvertebrados.exe and the .zip (Go ≥ 1.22, Pillow)
```

| Folder | Contents |
|---|---|
| `src/` | The page (`plantilla.html`, HTML + JavaScript, no dependencies), module settings (`grupo_macro.json`), genus → family list (`familias_macro.json`), icon and fonts |
| `i18n/` | English dictionary (`en.tsv`): one Spanish phrase and its translation per line |
| `launcher/` | Go launcher (standard library only): serves the page on 127.0.0.1, opens its window and saves the data |
| `tablas/` | The three score tables, transcribed from the original publications (Python and CSV) |
| `verificacion/` | Simulations and the independent Python implementation used to verify the program |
| `datos/` | The 365 records of the 43 field samples used in the paper, with sites numbered |

## Verification

`verificacion/verificar.py` runs the real page in Chromium (Playwright) and compares every result with an independent
implementation in Python (`verif.py`): 11 series of 1000 random communities under three score-table setups, family
assignment with 0–2 typos per name, the effect of typos on the ABI class in the 43 field samples, and the NOA-only vs
completed BMWP'. Seeds are fixed, so the results in `verificacion/resultados/` are reproduced exactly. See
[`verificacion/README.md`](verificacion/README.md).

## How to cite

Please cite the software through its Zenodo DOI (see the badge on the release, or `CITATION.cff`) and the
accompanying paper:

> Flores, C. M., & Rodríguez, G. F. (in preparation). Kenti Macroinvertebrados: automatic family assignment and
> verified computation of the BMWP', ASPT' and ABI biotic indices for rivers of northwestern Argentina. *Limnetica*.

## License

Code: MIT (see `LICENSE`). Fonts: SIL Open Font License 1.1. Genus list derived from the GBIF Backbone Taxonomy
(CC BY 4.0). Field data in `datos/`: CC BY 4.0, Carlos María Flores and Gabriel Federico Rodríguez.

---

## En español

Programa libre de escritorio para datos de macroinvertebrados bentónicos de ríos del noroeste argentino y los Andes.
Se pega la tabla de muestreo desde Excel; Kenti propone la familia de cada taxón, calcula los índices bióticos y
exporta un Excel que registra de dónde salió cada familia y cada puntaje.

- **La familia sale del nombre**: especie, género, familia o grupo (Oligochaeta, Hydracarina…). Lista incorporada de
  5802 géneros sudamericanos (GBIF), sin internet, con corrección de erratas. En azul, propuesta de Kenti; en ámbar,
  grafía corregida o género en más de una familia. Lo que escribe la persona no se toca.
- **BMWP' del NOA** (Domínguez y Fernández 1998), completado con la tabla boliviana **BMWP/Bol** para las familias que
  no están (se puede desactivar); **ASPT'** con las clases de Cammaerts et al. (2008); **ABI** (Ríos-Touma et al.
  2014) con clases según el valor de referencia de la cuenca.
- Diversidad alfa y beta, correlación con fisicoquímicos, PCA y exportación a Excel.
- **Interfaz en español y en inglés** (botón ES / EN arriba a la derecha).

**Descarga**: `Kenti-Macroinvertebrados-v0.5-Windows.zip` en [Releases](../../releases); descomprimir y abrir
`Kenti Macroinvertebrados.exe`. Los datos se guardan solos en `Documentos\Kenti Macroinvertebrados`. Si Windows
muestra «Windows protegió su PC», hacer clic en «Más información» → «Ejecutar de todas formas».

Contacto: Carlos María Flores · cmflores@csnat.unt.edu.ar · Facultad de Ciencias Naturales e Instituto Miguel Lillo,
Universidad Nacional de Tucumán.
