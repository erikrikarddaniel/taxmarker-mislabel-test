import collections
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/"
lin = {}
for l in open(base + "profilecover/user-alignment.covfiltered.tax"):
    n, _, t = l.rstrip("\n").partition("\t"); lin[n] = t.split(";")
print("scored sequences", len(lin))
for r, name in ((2, "phyla"), (3, "classes"), (4, "orders"), (5, "families"), (6, "genera"), (7, "species")):
    print(name, len({";".join(t[:r]) for t in lin.values() if len(t) >= r}))
flags = collections.Counter(); genera_flagged = set()
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": flags[int(f[4])] += 1
print("SATIVA flags by rank", dict(sorted(flags.items())), "ranks 2-6:", sum(v for k, v in flags.items() if k <= 6))
# genus sizes
g = collections.Counter(";".join(t[:6]) for t in lin.values() if len(t) >= 6)
print("genera with 1 sequence:", sum(1 for v in g.values() if v == 1), " >=10:", sum(1 for v in g.values() if v >= 10), " >=100:", sum(1 for v in g.values() if v >= 100))
# weights
wt = {}
with open(base + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[2] in lin: wt[f[2]] = float(f[4])
print("scored sequences with a weight:", len(wt))
