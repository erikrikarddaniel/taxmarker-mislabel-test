import csv, collections, sys
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
import sys
A, B = base + "bac-ssu-r232-1/", base + sys.argv[1] + "/"

def names(d):
    return {l[1:].split()[0] for l in open(d + "profilecover/user-alignment.covfiltered.fasta") if l[0] == ">"}

def flags(d, method=None):
    out = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if method is None or f[5] == method:
                out[f[0]] = int(f[4])
    return out

scoredB = names(B)
flagsA = flags(A, "sativa")
flagsB = flags(B, "sativa")
raxB = flags(B, "raxtax")

seq2key, rep = {}, {}
with open(B + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        c, taxon, name, _, _, _, isrep = l.rstrip("\n").split("\t")
        seq2key[name] = (c, taxon)
        if isrep == "True":
            rep[(c, taxon)] = name

tab = collections.defaultdict(collections.Counter)
for s, r in flagsA.items():
    if s in scoredB:
        cat = "scored, flagged" if s in flagsB else "scored, not flagged"
    else:
        rp = rep[seq2key[s]]
        if rp in scoredB:
            cat = "rep flagged" if rp in flagsB else "rep not flagged"
        elif rp in raxB:
            cat = "rep flagged by raxtax"
        else:
            cat = "rep removed (profile cover/raxtax pass)"
    tab[r][cat] += 1
cats = ["scored, flagged", "scored, not flagged", "rep flagged", "rep flagged by raxtax", "rep not flagged", "rep removed (profile cover/raxtax pass)"]
print("A=240k SATIVA flags:", len(flagsA))
print("rank\t" + "\t".join(cats) + "\ttotal")
tot = collections.Counter()
for r in sorted(tab):
    print(r, *[tab[r][c] for c in cats], sum(tab[r].values()), sep="\t")
    tot.update(tab[r])
print("all", *[tot[c] for c in cats], sum(tot.values()), sep="\t")

caught = ("scored, flagged", "rep flagged", "rep flagged by raxtax")
print("caught (flagged directly, or representative flagged by SATIVA or raxtax): rank, n, pct")
for r in sorted(tab):
    n = sum(tab[r].values()); c = sum(tab[r][k] for k in caught)
    print(r, n, c, "%.0f%%" % (100 * c / n), sep="\t")
print("all", sum(tot.values()), sum(tot[k] for k in caught), "%.0f%%" % (100 * sum(tot[k] for k in caught) / sum(tot.values())), sep="\t")
