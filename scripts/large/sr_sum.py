import os, re, collections
b = os.path.expanduser("~/projects/taxmarker/blast/sr/")
tax = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.tax"
strip = lambda x: re.sub(r"_[A-Z]+$", "", x)
def lin(s): return [strip(p[3:]) for p in s.split(";")]
g2l = collections.defaultdict(collections.Counter)
for l in open(tax):
    t = l.rstrip("\n").split("\t")[1]
    p = lin(t)
    if len(p) >= 7: g2l[p[5]][tuple(p)] += 1
g2l = {g: c.most_common(1)[0][0] for g, c in g2l.items()}
meta = {}
for l in open(b + "meta.tsv"):
    n, cat, o, p, r = l.rstrip("\n").split("\t")
    meta[n] = (cat, lin(o), lin(p), int(r))
best = {}
for l in open(b + "res.tsv"):
    q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
    bsc = float(bs); w = nm.replace("[", "").replace("]", "").split()
    g, sp = w[0], " ".join(w[:2])
    if q not in best or bsc > best[q][0]: best[q] = [bsc, float(pid), float(qc), {g}, {sp}]
    elif bsc == best[q][0]: best[q][3].add(g); best[q][4].add(sp)
tab = collections.defaultdict(collections.Counter)
for n, (cat, o, p, r) in meta.items():
    key = (cat, r)
    if n not in best: tab[key]["no hit"] += 1; continue
    bsc, pid, qc, gs, sps = best[n]
    if pid < 97 or qc < 90: tab[key]["weak hit"] += 1; continue
    if r <= 6:
        H = {g2l[g][r - 1] for g in gs if g in g2l}
        d, pr = o[r - 1], p[r - 1]
    else:
        H = {sp for sp in sps}
        d, pr = " ".join(o[6].split()[:2]), " ".join(p[6].split()[:2])
        H = {strip(h.split()[0]) + " " + h.split()[1] if len(h.split()) > 1 else h for h in H}
        d = strip(d.split()[0]) + " " + d.split()[1]; pr = strip(pr.split()[0]) + " " + pr.split()[1]
    if not H: k = "genus unknown"
    elif d in H and pr in H: k = "both"
    elif d in H: k = "declared"
    elif pr in H: k = "predicted"
    else: k = "other"
    tab[key][k] += 1
cols = ["declared", "predicted", "both", "other", "genus unknown", "weak hit", "no hit"]
print("category\trank", *cols, "total", sep="\t")
for cat in ["rax_notflagged", "new_without_rax", "both_sample"]:
    tot = collections.Counter()
    for r in range(2, 8):
        c = tab.get((cat, r))
        if not c: continue
        print(cat, r, *[c[x] for x in cols], sum(c.values()), sep="\t"); tot.update(c)
    print(cat, "all", *[tot[x] for x in cols], sum(tot.values()), sep="\t")
