import os, re, collections
b = os.path.expanduser("~/projects/taxmarker/blast/")
tax = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.tax"
g2p = collections.defaultdict(collections.Counter)
for l in open(tax):
    t = l.rstrip("\n").split("\t")[1].split(";")
    if len(t) >= 6:
        g = re.sub(r"_[A-Z]+$", "", t[5][3:])
        g2p[g][re.sub(r"_[A-Z]+$", "", t[1][3:])] += 1
def phy(l): return re.sub(r"_[A-Z]+$", "", l.split(";")[1][3:])
meta = {}
for l in open(b + "rank2miss.tsv"):
    s, rp, o, p, lw = l.rstrip("\n").split("\t")
    meta[s] = (phy(o), phy(p), float(lw))
best = {}
for l in open(b + "results_orig/rank2miss.tsv"):
    q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
    bsc = float(bs)
    g = nm.split()[0].strip("[]")
    if q not in best or bsc > best[q][0]: best[q] = [bsc, float(pid), float(qc), {g}]
    elif bsc == best[q][0]: best[q][3].add(g)
res = collections.Counter()
for s, (o, p, lw) in meta.items():
    if s not in best: res["no hit"] += 1; continue
    bsc, pid, qc, gs = best[s]
    if pid < 97 or qc < 90: res["weak hit (<97% id or <90% cov)"] += 1; continue
    phys = set()
    for g in gs:
        if g in g2p: phys.add(g2p[g].most_common(1)[0][0])
    if not phys: res["strong hit, genus unknown in GTDB map"] += 1
    elif o in phys and p in phys: res["strong hit, both phyla"] += 1
    elif o in phys: res["strong hit: declared phylum (%s)" % "flag looks wrong"] += 1
    elif p in phys: res["strong hit: predicted phylum (flag looks right)"] += 1
    else: res["strong hit: a third phylum"] += 1
for k, v in res.most_common(): print(v, k)
