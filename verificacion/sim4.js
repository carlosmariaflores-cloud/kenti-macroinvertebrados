(cfg) => {
  const K = window.__K;
  const C = cfg.data;
  const sites = C.map((_, i) => ({id: "s" + i, code: "S" + i, name: "", estado: "relevado"}));
  const by = new Map();
  C.forEach((c, i) => Object.entries(c.taxa).forEach(([n, v]) => { let sp = by.get(n); if (!sp){ sp = {name: n, family: "", counts: {}}; by.set(n, sp); } sp.counts["s" + i] = v; }));
  K.state = {sites, species: [...by.values()], unit: "individuos", formato: 2, example: false, bio: cfg.off ? {sinComplemento: true} : {}};
  K.famAutoAll();
  return sites.map(st => { const b = K.bioticRow(st); const c = K.classOf(K.BMWP_CLASSES, b.BMWP), a = K.classOf(K.ASPT_CLASSES, b.ASPT);
    return {BMWP: b.BMWP, n: b.bmwp.n, ASPT: b.ASPT, cB: c ? c.cls + " " + c.txt : "", cS: a ? a.cls : "", sin: b.bmwp.unscored, via: b.bmwp.viaGroup, compl: b.bmwp.compl, fromComp: b.bmwp.fromComp}; });
}
