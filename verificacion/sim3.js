(cfg) => {
  const K = window.__K; const {famAutoAll, bioticRow, classOf, abiClasses, abiRef} = K;
  function mulberry32(a){ return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = mulberry32(cfg.seed), pick = a => a[Math.floor(R() * a.length)], ri = (a, b) => a + Math.floor(R() * (b - a + 1));
  const L = "abcdefghijklmnopqrstuvwxyz";
  function typo(name){
    const sp = / sp\.$/.test(name), w = name.replace(/ sp\.$/, "");
    const t = ri(0, 3), p = ri(1, w.length - 1); let o;
    if (t === 0){ let c; do c = pick(L); while (c === w[p]); o = w.slice(0, p) + c + w.slice(p + 1); }
    else if (t === 1) o = w.slice(0, p) + w.slice(p + 1);
    else if (t === 2) o = w.slice(0, p) + pick(L) + w.slice(p);
    else if (p >= w.length - 1) o = w.slice(0, p - 1) + w[p] + w[p - 1];
    else o = w.slice(0, p) + w[p + 1] + w[p] + w.slice(p + 2);
    return o + (sp ? " sp." : "");
  }
  const C = cfg.data, abiC = abiClasses(abiRef());
  function run(namesPerSite){
    const sites = C.map((_, i) => ({id: "s" + i, code: "S" + i, name: "", estado: "relevado"}));
    const by = new Map();
    namesPerSite.forEach((lst, i) => lst.forEach(([n, v]) => { let sp = by.get(n); if (!sp){ sp = {name: n, family: "", counts: {}}; by.set(n, sp); } sp.counts["s" + i] = v; }));
    K.state = {sites, species: [...by.values()], unit: "individuos", formato: 2, example: false, bio: {}};
    famAutoAll();
    return sites.map(st => { const b = bioticRow(st); return [b.ABI, (classOf(abiC, b.ABI) || {}).cls]; });
  }
  const base = run(C.map(c => Object.entries(c.taxa)));
  const reps = [];
  for (const p of cfg.rates){
    for (let r = 0; r < cfg.reps; r++){
      const typed = C.map(c => Object.entries(c.taxa).map(([n, v]) => [R() < p ? typo(n) : n, v]));
      const k = run(typed);
      reps.push({p, names: typed.map(l => l.map(x => x[0])), abi: k.map(x => x[0]), cls: k.map(x => x[1])});
    }
  }
  return {base, reps};
}
