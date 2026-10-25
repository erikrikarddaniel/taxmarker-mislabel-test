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
scA, scB = names(A), names(B)
fA, fB = flags(A, "sativa"), flags(B, "sativa")
seq2key, rep = {}, {}
with open(B + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        c, t, n, _, _, _, r = l.rstrip("\n").split("\t")
        seq2key[n] = (c, t)
        if r == "True": rep[(c, t)] = n
miss = []
for s, f in fA.items():
    if f[4] == "2" and s not in scB:
        rp = rep[seq2key[s]]
        if rp in scB and rp not in fB:
            miss.append((s, rp))
print("misses:", len(miss))
repflagA = sum(1 for s, rp in miss if rp in fA)
repscoredA = sum(1 for s, rp in miss if rp in scA)
print("rep scored in A:", repscoredA, " rep flagged in A (any rank):", repflagA)
lw = sorted(float(fA[s][3]) for s, _ in miss)
print("A lwr: min %.2f median %.2f max %.2f" % (lw[0], lw[len(lw)//2], lw[-1]))
def phy(l): return l.split(";")[1] if ";" in l else l
pairs = collections.Counter((phy(fA[s][1]), phy(fA[s][2])) for s, _ in miss)
for (a, b), n in pairs.most_common(10): print(n, a, "->", b)
with open(out + "rank2miss.tsv", "w") as fh:
    for s, rp in miss: fh.write("\t".join([s, rp, fA[s][1], fA[s][2], fA[s][3]]) + "\n")
want = {s for s, _ in miss}
w = None
with open(out + "queries_orig/rank2miss.fna", "w") as fo:
    for l in open(base + "bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.ungapped.fasta"):
        if l[0] == ">":
            n = l[1:].split()[0]
            w = n in want
        if w: fo.write(l if l[0] != ">" else ">" + n + "\n")
