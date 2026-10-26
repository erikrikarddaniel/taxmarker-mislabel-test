import collections, sys
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
def flags(d, m):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == m: o[f[0]] = int(f[4])
    return o
fA = flags(base + "bac-ssu-r232-1/", "sativa")
for k in ("0.97", "0.97-fixedmodel", "0.99-fixedmodel"):
    B = base + "bac-ssu-r232-1-" + k + "/"
    fs, fr = flags(B, "sativa"), flags(B, "raxtax")
    seq2key, rep = {}, {}
    with open(B + "clusterselect/user-alignment.selection.tsv") as fh:
        next(fh)
        for l in fh:
            c, t, n, _, _, _, isrep = l.rstrip("\n").split("\t")
            seq2key[n] = (c, t)
            if isrep == "True": rep[(c, t)] = n
    print("==", k, " rank: distinct reps, share of reps flagged (SATIVA or raxtax)")
    for r in (2, 3, 4, 5, 6, 7):
        reps = {rep[seq2key[s]] for s, rr in fA.items() if rr == r and s in seq2key}
        c = sum(1 for x in reps if x in fs or x in fr)
        print(r, len(reps), c, "%.0f%%" % (100 * c / max(1, len(reps))), sep="\t")
