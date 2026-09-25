# Changelog

## 0.5 — 2026-09-25
- Spanish and English interface (ES / EN button). Numbers, messages, charts, the Excel report and copied tables follow
  the language; pasted tables are also recognised with English headers (Family, Taxon, Genus, Order, Total…).
- Built-in score tables: NOA BMWP' (Domínguez & Fernández 1998), completed with the Bolivian BMWP/Bol for families it
  does not score (can be switched off), and ABI (Prat et al. 2009). ASPT' classes of Cammaerts et al. (2008).
- Family assignment: typos in the family ending are corrected («Planorbiae» → Planorbidae); a table name is matched by
  similarity only when it is not a known family (Hydrachnidae no longer took the score of Hydraenidae).
- Fixes: «Copy table for Excel» in the alpha-diversity tab failed; the Excel report showed «Invalid Date» for
  built-in tables; chart labels were repeated in their accessible name.

## 0.4 — 2026-09-24
- Automatic family from genus or species (built-in list of South American genera from GBIF, GBIF online for the rest).
