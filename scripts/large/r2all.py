import os, collections
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
A, B = base + "bac-ssu-r232-1/", base + "bac-ssu-r232-1-0.97/"
out = os.path.expanduser("~/projects/taxmarker/blast/")
def names(d):
    return {l[1:].split()[0] for l in open(d + "profilecover/user-alignment.covfiltered.fasta") if l[0] == ">"}
def flags(d, method):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == method: o[f[0]] = f
    return o
scB = names(B)
fA, fB, xB = flags(A, "sativa"), flags(B, "sativa"), flags(B, "raxtax")
seq2key, rep = {}, {}
with open(B + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        c, t, n, _, _, _, r = l.rstrip("\n").split("\t")
        seq2key[n] = (c, t)
        if r == "True": rep[(c, t)] = n
rows = []
for s, f in fA.items():
    if f[4] != "2": continue
    if s in scB: cat = "scored+flagged at 0.97" if s in fB else "scored, not flagged at 0.97"
    else:
        rp = rep[seq2key[s]]
        if rp in scB: cat = "rep flagged" if rp in fB else "rep not flagged"
        elif rp in xB: cat = "rep flagged by raxtax"
        else: cat = "rep removed"
    rows.append((s, cat, f[1], f[2], f[3]))
with open(out + "rank2all.tsv", "w") as fh:
    for r in rows: fh.write("\t".join(r) + "\n")
print(len(rows), collections.Counter(r[1] for r in rows))
want = {r[0] for r in rows}
w = False
with open(out + "queries_orig/rank2all.fna", "w") as fo:
    for l in open(A + "weightfilter/user-alignment.weightfiltered.ungapped.fasta"):
        if l[0] == ">":
            n = l[1:].split()[0]; w = n in want
            if w: fo.write(">" + n + "\n")
        elif w: fo.write(l)
