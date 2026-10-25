import os, collections
H = os.path.expanduser("~/projects/taxmarker/")
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/"
whole = {}
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": whole[f[0]] = (int(f[4]), f[2])
for d in ("dnc", "dnc50"):
    O = H + d + "/"
    part = set()
    for l in open(O + "res/job_462/job_462.mis") if False else []: pass
    tab = collections.defaultdict(collections.Counter)
    for l in open(O + "sample.tsv"):
        j = l.split()[0]
        own = {x.strip() for x in open(O + "jobs/" + j + ".own")}
        tx = {}
        for x in open(O + "jobs/" + j + ".tax"):
            n, _, t = x.rstrip("\n").partition("\t"); tx[n] = t
        lineages = collections.defaultdict(set)   # rank -> set of lineage prefixes in the part
        for n, t in tx.items():
            p = t.split(";")
            for r in range(1, len(p) + 1): lineages[r].add(";".join(p[:r]))
        flagged = {}
        mis = O + "res/" + j + "/" + j + ".mis"
        for x in open(mis):
            if x.strip() and x[0] != ";":
                f = x.split("\t")
                if float(f[4]) >= 0.5: flagged[f[0]] = 1
        for n in own:
            if n in whole:
                r, pred = whole[n]
                present = ";".join(pred.split(";")[:r]) in lineages[r]
                tab[r][("predicted taxon present in part" if present else "absent from part", "part flags" if n in flagged else "part silent")] += 1
    print("##", d)
    for r in (2, 5, 6, 7):
        t = tab[r]
        pres = t[("predicted taxon present in part", "part flags")] + t[("predicted taxon present in part", "part silent")]
        ab = t[("absent from part", "part flags")] + t[("absent from part", "part silent")]
        print("rank", r, "whole flags", pres + ab, "| predicted taxon present in part:", pres, "(part flags %d)" % t[("predicted taxon present in part", "part flags")], "| absent:", ab, "(part flags %d)" % t[("absent from part", "part flags")])
