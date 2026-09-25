import json, collections, sys
sys.argv=["x","sim1.json"]   # any sim1 output: only its ABI table and reference are used
exec(open("verif.py").read().split("diff = collections.Counter()")[0])   # resolve(), score(), abi_cls()
d3=json.load(open("sim3.json")); C=json.load(open("reales.json"))
abi=d["abi"]
def naive(names):
    seen={}
    for n in names:
        e,s=score(abi, resolve(n))
        if e: seen[e]=s
    return sum(seen.values())
base=[b[0] for b in d3["base"]]; bcls=[b[1] for b in d3["base"]]
# comprobación: base Kenti == implementación independiente sin erratas
indep=[naive(list(c["taxa"])) for c in C]
print("base Kenti = independiente:", base==indep, sum(a!=b for a,b in zip(base,indep)))
out={}
for p in (0.1,0.2,0.3):
    R=[r for r in d3["reps"] if r["p"]==p]
    ck=cn=tot=0; dk=[]; dn=[]
    for r in R:
        for i,(names,a,c) in enumerate(zip(r["names"],r["abi"],r["cls"])):
            nv=naive(names); tot+=1
            ck+= c!=bcls[i]; cn+= abi_cls(nv)!=bcls[i]
            dk.append(a-base[i]); dn.append(nv-base[i])
    import statistics as st
    out[p]=dict(muestras=tot, cambio_clase_kenti=ck/tot, cambio_clase_sin_correccion=cn/tot,
               sesgo_kenti=st.mean(dk), sesgo_sin=st.mean(dn), exacto_kenti=sum(x==0 for x in dk)/tot, exacto_sin=sum(x==0 for x in dn)/tot)
    print(p, {k:(round(v,4) if isinstance(v,float) else v) for k,v in out[p].items()})
json.dump(out,open("res3.json","w"))
