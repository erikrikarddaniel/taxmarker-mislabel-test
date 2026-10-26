import collections, glob, hashlib, os
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
import sys
A, B = base + sys.argv[1] + "/", base + sys.argv[2] + "/"

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

print("-- trees and models (old md5 | new md5)")
for pat in ("**/*.bestTree", "**/*.bestModel", "**/*.refjson"):
    fa = {os.path.relpath(p, A): p for p in glob.glob(A + pat, recursive=True)}
    fb = {os.path.relpath(p, B): p for p in glob.glob(B + pat, recursive=True)}
    for k in sorted(set(fa) | set(fb)):
        a = md5(fa[k]) if k in fa else "-"
        b = md5(fb[k]) if k in fb else "-"
        print(k, a[:10], b[:10], "SAME" if a == b else "DIFF")

def names(d):
    return {l[1:].split()[0] for l in open(d + "profilecover/user-alignment.covfiltered.fasta") if l[0] == ">"}
def flags(d, method):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == method: o[f[0]] = (int(f[4]), float(f[3]), f[1], f[2])
    return o
sA, sB = names(A), names(B)
print("scored old", len(sA), "new", len(sB), "same set", sA == sB)
fA, fB = flags(A, "sativa"), flags(B, "sativa")
xA, xB = flags(A, "raxtax"), flags(B, "raxtax")
print("raxtax flags old", len(xA), "new", len(xB), "same", set(xA) == set(xB))
print("SATIVA flags old", len(fA), "new", len(fB), "both", len(set(fA) & set(fB)), "only old", len(set(fA) - set(fB)), "only new", len(set(fB) - set(fA)))
print("-- by rank: old | new | both | same predicted taxon (of both) | only old | only new")
for r in range(1, 8):
    a = {n for n, v in fA.items() if v[0] == r}
    b = {n for n, v in fB.items() if v[0] == r}
    both = a & b
    same = sum(1 for n in both if fA[n][3] == fB[n][3])
    print(r, len(a), len(b), len(both), same, len(a - b), len(b - a), sep="\t")
anyboth = set(fA) & set(fB)
print("shared flags with different rank:", sum(1 for n in anyboth if fA[n][0] != fB[n][0]), "different predicted lineage:", sum(1 for n in anyboth if fA[n][3] != fB[n][3]))
def med(x):
    x = sorted(x); return x[len(x) // 2] if x else None
print("median LWR: shared", med([fB[n][1] for n in anyboth]), "only old", med([fA[n][1] for n in set(fA) - set(fB)]), "only new", med([fB[n][1] for n in set(fB) - set(fA)]))
lo = lambda d, s: sum(1 for n in s if d[n][1] < 0.6)
print("LWR < 0.6: shared", lo(fB, anyboth), "of", len(anyboth), "| only old", lo(fA, set(fA) - set(fB)), "of", len(set(fA) - set(fB)), "| only new", lo(fB, set(fB) - set(fA)), "of", len(set(fB) - set(fA)))
