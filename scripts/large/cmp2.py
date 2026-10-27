import os, sys, collections, re
# usage: cmp2.py DIR  (dnc or dnc50)
H = os.path.expanduser("~/projects/taxmarker/")
O = H + sys.argv[1] + "/"
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/" + __import__("os").environ.get("BENCH", "bac-ssu-r232-1") + "/"
whole = {}
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": whole[f[0]] = (int(f[4]), float(f[3]), f[1], f[2])
def parse(path):
    o = {}
    for l in open(path):
        if not l.strip() or l[0] == ";": continue
        f = l.rstrip("\n").split("\t")
        op, pp = f[5].split(";"), f[6].split(";")
        r = next((i + 1 for i, (a, b) in enumerate(zip(op, pp)) if a != b), None)
        if r is None and len(op) != len(pp): r = min(len(op), len(pp)) + 1
        if float(f[4]) >= 0.5: o[f[0]] = (r, float(f[4]), f[5], f[6])
    return o
done = [l.split()[0] for l in open(O + "dnc.log") if l.startswith("job_")]
size = {l.split()[0]: int(l.split()[3]) for l in open(O + "sample.tsv")}
part, own_all, nparts = {}, set(), 0
for j in done:
    p = O + "res/" + j + "/" + j + ".mis"
    if not os.path.exists(p): continue
    nparts += 1
    own = {l.strip() for l in open(O + "jobs/" + j + ".own")}
    own_all |= own
    for n, v in parse(p).items():
        if n in own: part[n] = v
w = {n: v for n, v in whole.items() if n in own_all}
print("##", sys.argv[1], "parts with .mis:", nparts, "of", len(done), "own tips:", len(own_all))
print("whole-tree flags", len(w), " part-wise flags", len(part), " both", sum(1 for n in part if n in w), " only part-wise", sum(1 for n in part if n not in w))
print("rank\twhole\talso part (recall)\tpart\talso whole\tonly part-wise")
for r in range(2, 8):
    a = [n for n, v in w.items() if v[0] == r]; b = [n for n, v in part.items() if v[0] == r]
    print(r, len(a), "%d (%.0f%%)" % (sum(1 for n in a if n in part), 100 * sum(1 for n in a if n in part) / max(1, len(a))), len(b), sum(1 for n in b if n in w), sum(1 for n in b if n not in w), sep="\t")
ex = {n: v for n, v in part.items() if n not in w}
print("-- only part-wise flags: LWR median %.2f; predicted-label genus in whole-tree prediction? n/a" % sorted(v[1] for v in ex.values())[len(ex) // 2] if ex else "no extras")
# extras: are they in the 240k-scored set but unflagged there? (all own tips are scored in the whole tree)
import json
tab = collections.Counter((v[0]) for v in ex.values())
print("extras by rank:", dict(sorted(tab.items())))
# for extras at ranks 2-5: genus-level BLAST not available; list a few
for n, v in list(ex.items())[:0]: pass
open(O + "extras.tsv", "w").write("".join("%s\t%s\t%s\t%s\t%s\n" % (n, v[0], v[1], v[2], v[3]) for n, v in ex.items()))
