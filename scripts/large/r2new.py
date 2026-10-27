import os
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
B = os.path.expanduser("~/projects/taxmarker/blast/")
A = base + "bac-ssu-r232-1-fixedmodel/"
C = base + "bac-ssu-r232-1-0.97-fixedmodel/"

def names(d):
    return {l[1:].split()[0] for l in open(d + "profilecover/user-alignment.covfiltered.fasta") if l[0] == ">"}

def flags(d, method):
    o = {}
    with open(d + "mislabels/user-alignment.mislabels.tsv") as fh:
        next(fh)
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if f[5] == method:
                o[f[0]] = (int(f[4]), f[3], f[1], f[2])
    return o

scored, fs, rax = names(C), flags(C, "sativa"), flags(C, "raxtax")
seq2key, rep = {}, {}
with open(C + "clusterselect/user-alignment.selection.tsv") as fh:
    next(fh)
    for l in fh:
        c, t, n, _, _, _, isrep = l.rstrip("\n").split("\t")
        seq2key[n] = (c, t)
        if isrep == "True":
            rep[(c, t)] = n

out = open(B + "rank2all_new.tsv", "w")
for s, (r, lwr, o, p) in flags(A, "sativa").items():
    if r != 2:
        continue
    if s in scored:
        cat = "scored+flagged at 0.97" if s in fs else "scored, not flagged at 0.97"
    else:
        rp = rep[seq2key[s]]
        if rp in scored:
            cat = "rep flagged" if rp in fs else "rep not flagged"
        elif rp in rax:
            cat = "rep flagged by raxtax"
        else:
            cat = "rep removed"
    out.write("\t".join((s, cat, o, p, lwr)) + "\n")
out.close()

done = {l.split("\t")[0] for l in open(B + "results_orig/rank2all.tsv")}
old = {l.split("\t")[0] for l in open(B + "rank2all.tsv")}
new = [l.split("\t")[0] for l in open(B + "rank2all_new.tsv")]
print("phylum flags in rerun", len(new), "in first set", sum(1 for n in new if n in old), "with BLAST result", sum(1 for n in new if n in done))
missing = [n for n in new if n not in done and n not in old]
print("not in first set", len(missing))
want = set(n for n in new if n not in old)
os.makedirs(B + "queries_new", exist_ok=True)
w = None
cnt = 0
with open(B + "queries_new/rank2new.fna", "w") as o:
    for l in open(base + "bac-ssu-r232-1-fixedmodel/weightfilter/user-alignment.weightfiltered.ungapped.fasta"):
        if l[0] == ">":
            n = l[1:].split()[0]
            w = n in want
            if w:
                o.write(">" + n + "\n"); cnt += 1
        elif w:
            o.write(l)
print("queries written", cnt)
