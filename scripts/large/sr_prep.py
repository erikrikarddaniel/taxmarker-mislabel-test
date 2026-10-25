import os, random
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
A, B = base + "bac-ssu-r232-1-0.97/", base + "bac-ssu-r232-1-0.97-skip_raxtax/"
out = os.path.expanduser("~/projects/taxmarker/blast/sr/")
os.makedirs(out, exist_ok=True)
def names(d): return {l[1:].split()[0] for l in open(d + "profilecover/user-alignment.covfiltered.fasta") if l[0] == ">"}
def flags(d, method):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == method: o[f[0]] = f
    return o
sA, sB = names(A), names(B)
fA, xA, fB = flags(A, "sativa"), flags(A, "raxtax"), flags(B, "sativa")
common = sA & sB
rows = []
for n, f in xA.items():
    if n in sB and n not in fB: rows.append((n, "rax_notflagged", f[1], f[2], f[4]))
ca = {n for n in fA if n in common}; cb = {n for n in fB if n in common}
for n in cb - ca: rows.append((n, "new_without_rax", fB[n][1], fB[n][2], fB[n][4]))
random.seed(1)
both = sorted(n for n in ca & cb if fB[n][4] in "23456")
for n in random.sample(both, 1500): rows.append((n, "both_sample", fB[n][1], fB[n][2], fB[n][4]))
with open(out + "meta.tsv", "w") as fh:
    for r in rows: fh.write("\t".join(r) + "\n")
import collections
print(collections.Counter(r[1] for r in rows))
print("rax_notflagged expected 1845, new 3622")
want = {r[0] for r in rows}
w = False; got = set()
with open(out + "q.fna", "w") as fo:
    for l in open(base + "bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.ungapped.fasta"):
        if l[0] == ">":
            n = l[1:].split()[0]; w = n in want
            if w: fo.write(">" + n + "\n"); got.add(n)
        elif w: fo.write(l)
print("queries written", len(got), "missing", len(want - got))
