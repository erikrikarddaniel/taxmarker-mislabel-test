import os, re
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/"
out = os.path.expanduser("~/projects/taxmarker/blast/queries/")
os.makedirs(out, exist_ok=True)
species = {"ecoli": "s__Escherichia coli", "saureus": "s__Staphylococcus aureus", "kpneumoniae": "s__Klebsiella pneumoniae",
           "senterica": "s__Salmonella enterica", "paeruginosa": "s__Pseudomonas aeruginosa"}
label = {}
for l in open(base + "profilecover/user-alignment.covfiltered.tax"):
    n, _, t = l.rstrip("\n").partition("\t")
    label[n] = t
flag = {}
with open(base + "mislabels/user-alignment.mislabels.tsv") as fh:
    next(fh)
    for l in fh:
        f = l.rstrip("\n").split("\t")
        if f[5] == "sativa":
            flag[f[0]] = f[2]
fh = {(k, s): open(out + k + "." + s + ".fna", "w") for k in species for s in ("pass", "flag")}
n = {k: [0, 0] for k in species}
name = None
for l in open(base + "profilecover/user-alignment.covfiltered.fasta"):
    if l[0] == ">":
        name = l[1:].split()[0]
        seq = []
        cur = None
        t = label.get(name, "")
        for k, sp in species.items():
            if t.endswith(";" + sp):
                cur = k
        if cur:
            kind = "flag" if name in flag else "pass"
            fh[(cur, kind)].write(">" + name + "\n")
            n[cur][kind == "flag"] += 1
            w = fh[(cur, kind)]
        else:
            w = None
    elif w:
        w.write(l.replace("-", "").replace(".", ""))
for f in fh.values():
    f.close()
for k, (p, fl) in n.items():
    print(k, "pass", p, "flag", fl)
