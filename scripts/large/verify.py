import os, random
b = os.path.expanduser("~/projects/taxmarker/blast/")
def read(path, want=None):
    d, n = {}, None
    for l in open(path):
        if l[0] == ">":
            n = l[1:].split()[0]
            if want is None or n in want: d[n] = []
            else: n = None
        elif n: d[n].append(l.strip())
    return {k: "".join(v) for k, v in d.items()}
q = read(b + "queries/senterica.pass.fna")
random.seed(1)
pick = set(random.sample(sorted(q), 200))
orig = read("/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.ungapped.fasta", pick)
same = sum(1 for k in pick if orig[k].upper().replace("U", "T") == q[k].upper().replace("U", "T"))
low = sum(1 for k in pick if q[k] != q[k].upper())
print("sampled", len(pick), "identical to original (case-insensitive):", same, "| queries with lowercase:", low)
k = sorted(pick)[0]
print(k, len(orig[k]), len(q[k]))
