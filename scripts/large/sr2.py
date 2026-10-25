import collections
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
A, B = base + "bac-ssu-r232-1-0.97/", base + "bac-ssu-r232-1-0.97-skip_raxtax/"
def names(d): return {l[1:].split()[0] for l in open(d + "profilecover/user-alignment.covfiltered.fasta") if l[0] == ">"}
def flags(d, method):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == method: o[f[0]] = (int(f[4]), float(f[3]), f[1], f[2])
    return o
sA, sB = names(A), names(B)
fA, xA, fB = flags(A, "sativa"), flags(A, "raxtax"), flags(B, "sativa")
common = sA & sB
print("scored: with raxtax", len(sA), " without", len(sB), " common", len(common), " only without", len(sB - sA), " only with", len(sA - sB))
print("raxtax flags (0.97 run):", len(xA), " of which scored in the skip run:", len(set(xA) & sB), " = only-without set:", len((sB - sA) == (set(xA) & sB)) if False else ((sB - sA) <= set(xA)))
print("SATIVA flags: with raxtax", len(fA), " without", len(fB))
print("-- sequences scored in both: flags by rank (with raxtax | without | both)")
for r in range(2, 8):
    a = {n for n, v in fA.items() if n in common and v[0] == r}
    b = {n for n, v in fB.items() if n in common and v[0] == r}
    print(r, len(a), len(b), len(a & b), sep="\t")
ca = {n for n in fA if n in common}; cb = {n for n in fB if n in common}
print("total on common:", len(ca), len(cb), "both", len(ca & cb), "only with", len(ca - cb), "only without", len(cb - ca))
ox = set(xA) & sB
print("-- raxtax-flagged sequences that pass profile cover (scored in skip run):", len(ox), " flagged by SATIVA there:", sum(1 for n in ox if n in fB))
print("by raxtax rank (all 6?):", collections.Counter(v[0] for v in xA.values()))
print("SATIVA flag rank of those:", dict(sorted(collections.Counter(fB[n][0] for n in ox if n in fB).items())))
lost = set(xA) - sB
print("raxtax-flagged sequences removed by profile cover (not scored in skip run):", len(lost))
# agreement of predicted taxon at the raxtax mismatch rank
agree = sum(1 for n in ox if n in fB and ";".join(fB[n][3].split(";")[:7]) == ";".join(xA[n][3].split(";")[:7]))
print("same full predicted lineage as raxtax:", agree)
for sp in ("Staphylococcus aureus", "Escherichia coli", "Klebsiella pneumoniae", "Salmonella enterica", "Pseudomonas aeruginosa"):
    s = ";s__" + sp
    xr = [n for n, v in xA.items() if v[2].endswith(s)]
    print(sp, "raxtax flags", len(xr), "scored in skip run", sum(1 for n in xr if n in sB), "flagged by SATIVA there", sum(1 for n in xr if n in fB))
