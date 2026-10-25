import os, collections, statistics as st
b = os.path.expanduser("~/projects/taxmarker/blast/")
for f in ("senterica.pass", "kpneumoniae.pass"):
    ql = {}
    name = None
    for l in open(b + "queries/" + f + ".fna"):
        if l[0] == ">": name = l[1:].strip(); ql[name] = 0
        else: ql[name] += len(l.strip())
    best = {}
    for l in open(b + "results/" + f + ".tsv"):
        q, s, pid, ln, qc, bs, tx, nm = l.rstrip("\n").split("\t")
        if q not in best or float(bs) > best[q][0]: best[q] = (float(bs), float(pid), float(qc), int(ln), nm)
    weak = [q for q, v in best.items() if not (v[1] >= 97 and v[2] >= 90)]
    strong = [q for q in best if q not in set(weak)]
    for lab, qs in (("weak", weak), ("strong", strong)):
        L = [ql[q] for q in qs]
        print(f, lab, len(qs), "query len median", st.median(L), "min", min(L), "max", max(L),
              "| pident median", round(st.median(best[q][1] for q in qs), 1), "| qcov median", st.median(best[q][2] for q in qs),
              "| aln len median", st.median(best[q][3] for q in qs))
    print("  weak top species:", collections.Counter(best[q][4] for q in weak).most_common(4))
