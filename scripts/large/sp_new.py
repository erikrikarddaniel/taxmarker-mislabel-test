import os, collections
H = os.path.expanduser("~/projects/taxmarker/blast/")
A = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1-fixedmodel/"
flag = set()
with open(A + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa":
            flag.add(f[0])
exp = {"ecoli": {"Escherichia", "Shigella"}, "kpneumoniae": {"Klebsiella"}, "saureus": {"Staphylococcus"},
       "senterica": {"Salmonella"}, "paeruginosa": {"Pseudomonas"}}
print("species\tsequences\tflagged in rerun\tunflagged strong hits\texpected genus\t%\tflagged strong hits\texpected genus")
for k, e in exp.items():
    names = set()
    for s in ("pass", "flag"):
        names |= {l[1:].strip() for l in open(H + "queries_orig/%s.%s.fna" % (k, s)) if l[0] == ">"}
    best = {}
    for s in ("pass", "flag"):
        for l in open(H + "results_orig/%s.%s.tsv" % (k, s)):
            q, sid, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
            b = float(bs); g = nm.split()[0].strip("[]")
            if q not in best or b > best[q][0]:
                best[q] = [b, float(pid), float(qc), {g}]
            elif b == best[q][0]:
                best[q][3].add(g)
    strong = {q: v for q, v in best.items() if v[1] >= 97 and v[2] >= 90}
    def cnt(sel):
        t = [q for q in strong if sel(q)]
        return len(t), sum(1 for q in t if strong[q][3] & e)
    nu, ou = cnt(lambda q: q not in flag)
    nf, of = cnt(lambda q: q in flag)
    print(k, len(names), sum(1 for n in names if n in flag), nu, ou, "%.2f" % (100 * ou / nu), nf, of, sep="\t")
