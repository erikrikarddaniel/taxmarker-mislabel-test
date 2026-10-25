import csv, collections, sys
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
A, B = base + "bac-ssu-r232-1/", base + "bac-ssu-r232-1-0.97/"

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
        cat = "scored at 0.97 (counted before)"
    else:
        rp = rep[seq2key[s]]
        if rp in scoredB:
            cat = "rep flagged" if rp in flagsB else "rep not flagged"
        elif rp in raxB:
            cat = "rep flagged by raxtax"
        else:
            cat = "rep removed (profile cover/raxtax pass)"
    tab[r][cat] += 1
cats = ["scored at 0.97 (counted before)", "rep flagged", "rep flagged by raxtax", "rep not flagged", "rep removed (profile cover/raxtax pass)"]
print("A=240k SATIVA flags:", len(flagsA))
print("rank\t" + "\t".join(cats) + "\ttotal")
tot = collections.Counter()
for r in sorted(tab):
    print(r, *[tab[r][c] for c in cats], sum(tab[r].values()), sep="\t")
    tot.update(tab[r])
print("all", *[tot[c] for c in cats], sum(tot.values()), sep="\t")
