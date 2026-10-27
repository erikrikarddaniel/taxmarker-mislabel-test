import re, collections
exec(open("r2sum_new.py").read().split("tab = collections.defaultdict")[0])
newq = {l[1:].strip() for l in open(b + "queries_new/rank2new.fna") if l[0] == ">"}
def cl(s):
    cat, o, p = meta[s]
    if s not in best: return "no hit"
    bsc, pid, qc, gs = best[s]
    if pid < 97 or qc < 90: return "weak hit"
    ph = {g2p[g].most_common(1)[0][0] for g in gs if g in g2p}
    if not ph: return "genus unknown"
    return "both" if o in ph and p in ph else "declared phylum" if o in ph else "predicted phylum" if p in ph else "third phylum"
c = collections.Counter(cl(s) for s in newq)
print("706 new phylum flags:", sum(c.values()), dict(c))
c2 = collections.Counter(meta[s][0] for s in newq)
print("by category:", dict(c2))
# reps of 'rep not flagged' flagged in the 1.0 rerun?
A = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1-fixedmodel/"
C = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1-0.97-fixedmodel/"
fl = set()
with open(A + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": fl.add(f[0])
seq2key, rep = {}, {}
with open(C + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        cc, t, n, _, _, _, isrep = l.rstrip("\n").split("\t")
        seq2key[n] = (cc, t)
        if isrep == "True": rep[(cc, t)] = n
rnf = [s for s, (cat, o, p) in meta.items() if cat == "rep not flagged"]
print("rep not flagged:", len(rnf), "their representative flagged in the 1.0 rerun:", sum(1 for s in rnf if rep[seq2key[s]] in fl))
