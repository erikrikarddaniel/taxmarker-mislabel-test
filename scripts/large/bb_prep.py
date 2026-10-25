import os, random, re, collections, sys
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/"
O = os.path.expanduser("~/projects/taxmarker/bb/")
os.makedirs(O + "jobs", exist_ok=True)
lin = {}
for l in open(base + "profilecover/user-alignment.covfiltered.tax"):
    n, _, t = l.rstrip("\n").partition("\t"); lin[n] = t
wt = {}
with open(base + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[2] in lin: wt[f[2]] = float(f[4])
flag = {}
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa": flag[f[0]] = int(f[4])
genus = collections.defaultdict(list)
for n, t in lin.items():
    p = t.split(";")
    if len(p) >= 6: genus[";".join(p[:6])].append(n)
backbone = set()
for g, ns in genus.items():
    ok = [n for n in ns if n not in flag]
    if ok: backbone.add(max(ok, key=lambda n: (wt[n], n)))
cand = {n for n, r in flag.items() if 2 <= r <= 6}
random.seed(1)
pool = sorted(n for n in lin if n not in flag and n not in backbone)
controls = set(random.sample(pool, 14000))
keep = backbone | cand | controls
print("backbone", len(backbone), "candidates", len(cand), "controls", len(controls), "tips", len(keep), "genera", len(genus))
with open(O + "backbone.tsv", "w") as fo:
    for n in sorted(keep): fo.write("%s\t%s\n" % (n, "backbone" if n in backbone else "candidate" if n in cand else "control"))
# newick prune (iterative)
s = open(base + "raxmlng/user-alignment.raxml.bestTree").read().strip().rstrip(";")
kids, parent, name, bl = [], [], [], []
def new(p):
    kids.append([]); parent.append(p); name.append(None); bl.append(0.0)
    if p is not None: kids[p].append(len(kids) - 1)
    return len(kids) - 1
root = new(None); cur = root; i = 0; n = len(s)
tok = re.compile(r"[^(),:;]+")
while i < n:
    c = s[i]
    if c == "(":
        cur = new(cur); i += 1
    elif c == ",":
        cur = new(parent[cur]); i += 1
    elif c == ")":
        cur = parent[cur]; i += 1
    elif c == ":":
        m = re.match(r":([^(),;]+)", s[i:i+40]); bl[cur] = float(m.group(1)); i += m.end()
    else:
        m = tok.match(s, i); name[cur] = m.group(0); i = m.end()
# the first "(" created a child of root; treat the outermost as root itself
if len(kids[root]) == 1 and name[root] is None:
    root = kids[root][0]; parent[root] = None
order = []; st = [root]
while st:
    v = st.pop(); order.append(v); st.extend(kids[v])
alive = {}
for v in reversed(order):
    if not kids[v]: alive[v] = name[v] in keep
    else:
        k = [c for c in kids[v] if alive.get(c)]
        alive[v] = bool(k)
def collapse(v):
    # returns (node, blen) after skipping unary kept nodes
    extra = 0.0
    while kids[v] and sum(1 for c in kids[v] if alive[c]) == 1:
        c = [c for c in kids[v] if alive[c]][0]
        extra += bl[c]; v = c
    return v, extra
out = {}
def write(v):
    parts = {}
    stack = [(v, False)]; res = {}
    while stack:
        u, done = stack.pop()
        k = [c for c in kids[u] if alive[c]]
        if not done:
            if not k: res[u] = name[u]; continue
            stack.append((u, True))
            for c in k:
                w, ex = collapse(c); parts[c] = (w, bl[c] + ex); stack.append((w, False))
        else:
            res[u] = "(" + ",".join("%s:%.6f" % (res[parts[c][0]], parts[c][1]) for c in k) + ")"
    return res[v]
r, _ = collapse(root)
rk = [c for c in kids[r] if alive[c]]
if len(rk) == 2:
    # suppress the root: join the two root edges
    a, b = rk
    if not kids[a]: a, b = b, a
    ba, bb = bl[a], bl[b]
    kids[a].append(b); bl[b] = ba + bb; alive[b] = True; r = a
    # b is now a child of a; set parent unused
tree = write(r) + ";\n"
open(O + "jobs/bb.nwk", "w").write(tree)
tips = [x for x in re.findall(r"[(,]([^(),:;]+):", tree)]
print("tips in pruned tree", len(tips), "expected", len(keep), "missing", len(keep - set(tips)))
names = set(tips)
with open(O + "jobs/bb.tax", "w") as ft:
    for t in sorted(names): ft.write("%s\t%s\n" % (t, lin[t]))
with open(O + "jobs/bb.fasta", "w") as fo:
    w = False
    for l in open(base + "profilecover/user-alignment.covfiltered.fasta"):
        if l[0] == ">":
            w = l[1:].split()[0] in names
        if w: fo.write(l)
os.system("cp %sraxmlng/user-alignment.raxml.bestModel %sjobs/bb.raxml.bestModel" % (base, O))
