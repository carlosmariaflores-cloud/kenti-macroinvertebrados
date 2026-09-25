(cfg) => {
  const K = window.__K; const {famResolve, FAMDIC, scoreFor, normTax} = K;
  function mulberry32(a){ return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const R = mulberry32(cfg.seed), pick = a => a[Math.floor(R() * a.length)], ri = (a, b) => a + Math.floor(R() * (b - a + 1));
  const cap = w => w[0].toUpperCase() + w.slice(1);
  const fams = FAMDIC.fams.map(f => f[0]);
  // Géneros válidos: se excluyen las grafías alternativas que la lista ya trae como sinónimo (se toma un nombre por familia y letra inicial al azar).
  const gens = Object.entries(FAMDIC.gen).filter(([g, i]) => !Array.isArray(i) && g.length >= 5 && !/idae$/.test(g)).map(([g, i]) => [g, fams[i]]);
  const L = "abcdefghijklmnopqrstuvwxyz";
  function typo(w){
    const t = ri(0, 3), p = ri(1, w.length - 1);            // la primera letra se conserva
    if (t === 0){ let c; do c = pick(L); while (c === w[p]); return w.slice(0, p) + c + w.slice(p + 1); }
    if (t === 1) return w.slice(0, p) + w.slice(p + 1);
    if (t === 2) return w.slice(0, p) + pick(L) + w.slice(p);
    if (p >= w.length - 1) return w.slice(0, p - 1) + w[p] + w[p - 1];
    return w.slice(0, p) + w[p + 1] + w[p] + w.slice(p + 2);
  }
  const out = [];
  const famOk = new Set(fams.map(f => f.toLowerCase()));
  const genSet = new Set(Object.keys(FAMDIC.gen));
  for (const nivel of ["familia", "genero"]){
    for (const k of [0, 1, 2]){
      for (let i = 0; i < cfg.n; i++){
        let truth, w;
        if (nivel === "familia"){ truth = pick(fams); w = truth.toLowerCase(); }
        else { const g = pick(gens); truth = g[1]; w = g[0]; }
        let t = w; for (let j = 0; j < k; j++) t = typo(t);
        const esValido = t !== w && (nivel === "familia" ? famOk.has(t) : genSet.has(t));   // la errata formó otro nombre real
        const name = cap(t) + (nivel === "genero" && R() < 0.5 ? " sp." : "");
        const r = famResolve(name) || {};
        out.push({nivel, k, name, truth, fam: r.fam || "", via: r.via || "", nota: r.nota || "", esValido});
      }
    }
  }
  // Erratas reales de las planillas de la Puna argentina y el Chaco occidental
  const reales = ["Gripopterigidae", "Hydroptylidae", "Simulidae", "Hidracarina", "Hyalella sp.", "limoniidae", "Hydrachnidae", "Beatidae", "Elminthidae", "Andesiop", "Hyallela"].map(n => ({name: n, ...(famResolve(n) || {})}));
  // Errata en la tabla de puntaje: se sigue cruzando
  const tab = {rows: [{name: "Beatidae", score: 7}, {name: "Hydraenidae", score: 5}, {name: "Hydracarina", score: 4}, {name: "Perlidae", score: 10}]};
  const cruce = ["Baetidae", "Hydrachnidae", "Perlodidae"].map(f => { const m = scoreFor(tab, f); return {fam: f, a: m ? m.e.name : null, via: m ? m.via : null}; });
  return {out, reales, cruce};
}
