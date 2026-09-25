// Se ejecuta dentro de la página de Kenti (código real). Devuelve comunidades y resultados.
(cfg) => {
  const K = window.__K; const {famAutoAll, FAM_ATTR, bioticRow, classOf, BMWP_CLASSES, ASPT_CLASSES, abiClasses, abiRef, ABI_KENTI, FAMDIC} = K;
  function mulberry32(a){ return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = mulberry32(cfg.seed), ri = (a, b) => a + Math.floor(R() * (b - a + 1)), pick = a => a[Math.floor(R() * a.length)];
  const cap = w => w[0].toUpperCase() + w.slice(1);
  const fams = FAMDIC.fams.map(f => f[0]);
  const genOk = Object.entries(FAMDIC.gen).filter(([g, i]) => !Array.isArray(i) && g.length >= 4 && !/idae$/.test(g)).map(([g, i]) => [g, fams[i]]);
  const grupos = ["Copepoda", "Oligochaeta", "Hirudinea", "Hydracarina", "Acari", "Turbellaria", "Ostracoda", "Collembola", "Nematoda"];
  // Tabla BMWP de prueba (puntajes al azar 1-10): la verificación del cálculo no depende de los valores.
  const bmwpRows = [...fams, "Oligochaeta", "Hirudinea", "Hydracarina", "Turbellaria", "Ostracoda"].filter(() => R() < 0.6).map(n => ({name: n, score: ri(1, 10), orden: ""}));
  const TAB = {rows: bmwpRows, archivo: "prueba"};
  const comms = [];
  for (let c = 0; c < cfg.n; c++){
    const S = ri(1, 30), names = new Set();
    while (names.size < S){
      const u = R();
      if (u < 0.6) names.add(pick(fams));
      else if (u < 0.85){ const [g] = pick(genOk); names.add(cap(g) + (R() < 0.5 ? " sp." : "")); }
      else names.add(pick(grupos));
    }
    comms.push([...names].map(n => [n, ri(1, 500)]));
  }
  const allNames = [...new Set(comms.flat().map(x => x[0]))];
  const sites = comms.map((_, i) => ({id: "s" + i, code: "C" + (i + 1), name: "", estado: "relevado"}));
  const species = allNames.map(n => ({name: n, family: "", counts: {}}));
  const byName = new Map(species.map(sp => [sp.name, sp]));
  comms.forEach((cm, i) => cm.forEach(([n, v]) => { byName.get(n).counts["s" + i] = v; }));
  K.state = {sites, species, unit: "individuos", formato: 2, example: false, bio: Object.assign(cfg.real ? {} : {tablas: {bmwp: TAB}}, cfg.comp ? {} : {sinComplemento: true})};
  famAutoAll();
  const fa = FAM_ATTR();
  const resolved = Object.fromEntries(species.map(sp => [sp.name, {fam: sp[fa.key] || "", via: (sp.famAuto || {}).via || ""}]));
  const abiC = abiClasses(abiRef());
  const res = sites.map(st => {
    const b = bioticRow(st);
    return {BMWP: b.BMWP, nB: b.bmwp.n, ASPT: b.ASPT, ABI: b.ABI, nA: b.abi.n,
      cB: (classOf(BMWP_CLASSES, b.BMWP) || {}).txt, cS: (classOf(ASPT_CLASSES, b.ASPT) || {}).cls, cA: (classOf(abiC, b.ABI) || {}).cls,
      viaB: b.bmwp.viaGroup, viaA: b.abi.viaGroup};
  });
  return {comms, resolved, res, bmwp: cfg.real ? K.BMWP_KENTI.rows : bmwpRows, bmwpc: cfg.comp ? K.BMWPBOL_KENTI.rows : null, abi: ABI_KENTI.rows, fams, gen: FAMDIC.gen, abiRef: abiRef()};
}
