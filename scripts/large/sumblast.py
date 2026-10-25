import sys, os, collections
d = os.path.expanduser("~/projects/taxmarker/blast/results/")
for f in sys.argv[1:]:
    best = {}
    for l in open(d + f + ".tsv"):
        q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
        b = float(bs)
        if q not in best or b > best[q][0]:
            best[q] = (b, float(pid), float(qc), nm, {nm})
        elif b == best[q][0]:
            best[q][4].add(nm)
    n = len(best)
    gen = collections.Counter(); sp = collections.Counter()
    lowid = 0
    for q, (b, pid, qc, nm, names) in best.items():
        g = nm.split()[0]
        gen[g] += 1; sp[nm] += 1
        if pid < 97 or qc < 80: lowid += 1
    print("==", f, "queries with hits:", n, " top hit <97% id or <80% cov:", lowid)
    print("  genus:", gen.most_common(6))
    print("  species:", sp.most_common(6))
