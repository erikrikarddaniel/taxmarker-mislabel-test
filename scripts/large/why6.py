import collections
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
A = base + "bac-ssu-r232-1/"
def flags(d):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == "sativa": o[f[0]] = int(f[4])
    return o
fA = {n: r for n, r in flags(A).items() if r == 6}
dirs = {k: base + "bac-ssu-r232-1-" + k + "/" for k in ("0.97", "0.97-fixedmodel", "0.99-fixedmodel")}
sel = dirs["0.97"] + "clusterselect/user-alignment.selection.tsv"
seq2key, rep = {}, {}
with open(sel) as fh:
    next(fh)
    for l in fh:
        c, t, n, _, _, _, isrep = l.rstrip("\n").split("\t")
        seq2key[n] = (c, t)
        if isrep == "True": rep[(c, t)] = n
cnt = collections.Counter(rep[seq2key[s]] for s in fA if s in seq2key and (seq2key[s] in rep) and True)
print("rank-6 1.0 flags", len(fA), "distinct reps at 0.97", len(cnt), "top 10 reps carry", sum(v for _, v in cnt.most_common(10)))
fl = {k: flags(d) for k, d in dirs.items()}
for r, v in cnt.most_common(8):
    print(r, v, {k: fl[k].get(r) for k in fl})
