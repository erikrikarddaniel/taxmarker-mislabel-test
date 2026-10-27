import os, collections
O = os.path.expanduser("~/projects/taxmarker/dnc/")
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/" + __import__("os").environ.get("BENCH", "bac-ssu-r232-1") + "/"
whole = {}
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": whole[f[0]] = (int(f[4]), float(f[3]))
def parse(path):
    o = {}
    for l in open(path):
        if not l.strip() or l[0] == ";": continue
        f = l.rstrip("\n").split("\t")
        name, conf, op, pp = f[0], float(f[4]), f[5].split(";"), f[6].split(";")
        r = next((i + 1 for i, (a, b) in enumerate(zip(op, pp)) if a != b), None)
        if r is None and len(op) != len(pp): r = min(len(op), len(pp)) + 1
        if conf >= 0.5: o[name] = (r, conf)
    return o
done = [l.split()[0] for l in open(O + "dnc.log") if l.startswith("job_")]
sizes = {l.split("\t")[0]: int(l.split("\t")[4]) for l in open(O + "sample.tsv")}
part = {}; own_all = set(); ok = 0
for j in done:
    p = O + "res/" + j + "/" + j + ".mis"
    if not os.path.exists(p): continue
    ok += 1
    own = {l.strip() for l in open(O + "jobs/" + j + ".own")}
    own_all |= own
    for n, v in parse(p).items():
        if n in own: part[n] = v
w = {n: v for n, v in whole.items() if n in own_all}
print("parts done with .mis:", ok, "of", len(done), "; own tips:", len(own_all))
print("flags among these tips: whole-tree", len(w), " part-wise", len(part), " both", sum(1 for n in part if n in w))
print("rank\twhole\talso part\tpart\talso whole")
for r in range(1, 8):
    a = [n for n, v in w.items() if v[0] == r]; b = [n for n, v in part.items() if v[0] == r]
    print(r, len(a), sum(1 for n in a if n in part), len(b), sum(1 for n in b if n in w), sep="\t")

print("--- by part size (own tips)")
cls = lambda n: "<100" if n < 100 else ("100-499" if n < 500 else ">=500")
tips = collections.defaultdict(set)
for j in done:
    for l in open(O + "jobs/" + j + ".own"): tips[cls(sizes[j])].add(l.strip())
for c in ("<100", "100-499", ">=500"):
    ww = {n: v for n, v in whole.items() if n in tips[c]}
    pp = {n: v for n, v in part.items() if n in tips[c]}
    hi = [n for n, v in ww.items() if v[0] <= 5]; lo = [n for n, v in ww.items() if v[0] >= 6]
    print(c, "parts", sum(1 for j in done if cls(sizes[j]) == c), "tips", len(tips[c]), "| whole flags", len(ww), "part flags", len(pp),
          "| ranks2-5: whole", len(hi), "also part", sum(1 for n in hi if n in pp),
          "| ranks6-7: whole", len(lo), "also part", sum(1 for n in lo if n in pp))
