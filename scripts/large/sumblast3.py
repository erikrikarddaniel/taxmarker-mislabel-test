import sys, os, collections
d = os.path.expanduser("~/projects/taxmarker/blast/results_orig/")
exp = {"ecoli": {"Escherichia", "Shigella"}, "kpneumoniae": {"Klebsiella"}, "saureus": {"Staphylococcus"},
       "senterica": {"Salmonella"}, "paeruginosa": {"Pseudomonas"}}
for f in sys.argv[1:]:
    e = exp[f.split(".")[0]]
    best = {}
    for l in open(d + f + ".tsv"):
        q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
        b, pid, qc = float(bs), float(pid), float(qc)
        g = nm.split()[0].strip("[]")
        if q not in best or b > best[q][0]:
            best[q] = [b, pid, qc, {g}]
        elif b == best[q][0]:
            best[q][3].add(g)
    nq = len(best)
    inf = {q: v for q, v in best.items() if v[1] >= 97 and v[2] >= 90}
    ok = sum(1 for v in inf.values() if v[3] & e)
    off = collections.Counter()
    for q, v in inf.items():
        if not (v[3] & e):
            off["/".join(sorted(v[3]))] += 1
    weak_ok = sum(1 for q, v in best.items() if q not in inf and v[3] & e)
    print(f"== {f}: with hits {nq}; strong hits (>=97% id, >=90% cov) {len(inf)}: expected genus among top {ok}, other {len(inf)-ok}; weak hits {nq-len(inf)}: expected genus among top {weak_ok}")
    print("   other (strong):", off.most_common(5))
