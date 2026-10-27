import os, re, collections
exec(open(os.path.expanduser("~/projects/taxmarker/dnc_cmp.py")).read().split('print("parts done')[0])
b = os.path.expanduser("~/projects/taxmarker/blast/")
g2p = collections.defaultdict(collections.Counter)
for l in open("/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1-fixedmodel/weightfilter/user-alignment.weightfiltered.tax"):
    t = l.rstrip("\n").split("\t")[1].split(";")
    if len(t) >= 6: g2p[re.sub(r"_[A-Z]+$", "", t[5][3:])][re.sub(r"_[A-Z]+$", "", t[1][3:])] += 1
ph = lambda l: re.sub(r"_[A-Z]+$", "", l.split(";")[1][3:])
meta = {}
for l in open(b + "rank2all_new.tsv"):
    s, cat, o, p, lw = l.rstrip("\n").split("\t"); meta[s] = (ph(o), ph(p))
best = {}
for l in [x for f in ("results_orig/rank2all.tsv", "results_new/rank2new.tsv") for x in open(b + f)]:
    q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
    bsc = float(bs); g = nm.split()[0].strip("[]")
    if q not in best or bsc > best[q][0]: best[q] = [bsc, float(pid), float(qc), {g}]
    elif bsc == best[q][0]: best[q][3].add(g)
def cl(s):
    o, p = meta[s]
    if s not in best: return "no hit"
    bsc, pid, qc, gs = best[s]
    if pid < 97 or qc < 90: return "weak"
    phs = {g2p[g].most_common(1)[0][0] for g in gs if g in g2p}
    if not phs: return "unknown"
    return "both" if o in phs and p in phs else "declared (flag wrong)" if o in phs else "predicted (flag right)" if p in phs else "third"
tab = collections.defaultdict(collections.Counter)
for n, v in w.items():
    if v[0] == 2 and n in meta: tab["part flags it" if n in part else "part does not flag"][cl(n)] += 1
for k, c in tab.items(): print(k, sum(c.values()), dict(c))
