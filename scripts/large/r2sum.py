import os, re, collections
b = os.path.expanduser("~/projects/taxmarker/blast/")
tax = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.tax"
g2p = collections.defaultdict(collections.Counter)
for l in open(tax):
    t = l.rstrip("\n").split("\t")[1].split(";")
    if len(t) >= 6:
        g2p[re.sub(r"_[A-Z]+$", "", t[5][3:])][re.sub(r"_[A-Z]+$", "", t[1][3:])] += 1
phy = lambda l: re.sub(r"_[A-Z]+$", "", l.split(";")[1][3:])
meta = {}
for l in open(b + "rank2all.tsv"):
    s, cat, o, p, lw = l.rstrip("\n").split("\t")
    meta[s] = (cat, phy(o), phy(p))
best = {}
for l in open(b + "results_orig/rank2all.tsv"):
    q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
    bsc = float(bs); g = nm.split()[0].strip("[]")
    if q not in best or bsc > best[q][0]: best[q] = [bsc, float(pid), float(qc), {g}]
    elif bsc == best[q][0]: best[q][3].add(g)
tab = collections.defaultdict(collections.Counter)
for s, (cat, o, p) in meta.items():
    if s not in best: tab[cat]["no hit"] += 1; continue
    bsc, pid, qc, gs = best[s]
    if pid < 97 or qc < 90: tab[cat]["weak hit"] += 1; continue
    ph = {g2p[g].most_common(1)[0][0] for g in gs if g in g2p}
    if not ph: k = "genus unknown"
    elif o in ph and p in ph: k = "both"
    elif o in ph: k = "declared phylum"
    elif p in ph: k = "predicted phylum"
    else: k = "third phylum"
    tab[cat][k] += 1
cols = ["declared phylum", "predicted phylum", "both", "third phylum", "genus unknown", "weak hit", "no hit"]
print("category", *cols, "total", sep="\t")
tot = collections.Counter()
for cat in ["scored+flagged at 0.97", "rep flagged", "rep flagged by raxtax", "scored, not flagged at 0.97", "rep not flagged", "rep removed"]:
    print(cat, *[tab[cat][c] for c in cols], sum(tab[cat].values()), sep="\t")
    tot.update(tab[cat])
print("all", *[tot[c] for c in cols], sum(tot.values()), sep="\t")
