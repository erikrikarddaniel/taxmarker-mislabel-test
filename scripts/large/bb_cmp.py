import os, collections
H = os.path.expanduser("~/projects/taxmarker/")
O = H + "bb/"
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/"
whole = {}
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": whole[f[0]] = (int(f[4]), float(f[3]), f[2])
role = dict(l.rstrip("\n").split("\t") for l in open(O + "backbone.tsv"))
bb = {}
for l in open(O + "res/bb.mis"):
    if not l.strip() or l[0] == ";": continue
    f = l.rstrip("\n").split("\t")
    if float(f[4]) < 0.5: continue
    op, pp = f[5].split(";"), f[6].split(";")
    r = next((i + 1 for i, (a, b) in enumerate(zip(op, pp)) if a != b), None)
    if r is None and len(op) != len(pp): r = min(len(op), len(pp)) + 1
    bb[f[0]] = (r, float(f[4]), f[6])
cnt = collections.Counter(role.values())
print("tips", dict(cnt), " flags in backbone run:", len(bb), "by role", dict(collections.Counter(role.get(n, "?") for n in bb)))
print("candidates (whole-tree flags ranks 2-6): rank, n, flagged again (any rank), same rank, same predicted taxon at that rank")
for r in range(2, 7):
    c = [n for n, v in whole.items() if v[0] == r and role.get(n) == "candidate"]
    again = [n for n in c if n in bb]
    same = [n for n in again if bb[n][0] == r]
    agree = [n for n in again if bb[n][0] == r and ";".join(bb[n][2].split(";")[:r]) == ";".join(whole[n][2].split(";")[:r])]
    print(r, len(c), "%d (%.0f%%)" % (len(again), 100 * len(again) / max(1, len(c))), len(same), len(agree), sep="\t")
ctl = [n for n, v in role.items() if v == "control"]
cf = [n for n in ctl if n in bb]
print("controls (unflagged in whole tree): n", len(ctl), "flagged in backbone run", len(cf), "by rank", dict(sorted(collections.Counter(bb[n][0] for n in cf).items())))
b_f = [n for n, v in role.items() if v == "backbone" and n in bb]
print("backbone reps flagged:", len(b_f))
open(O + "extras_controls.tsv", "w").write("".join("%s\t%s\t%s\t%s\n" % (n, bb[n][0], bb[n][1], bb[n][2]) for n in cf))
