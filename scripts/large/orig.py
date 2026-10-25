import os, random
b = os.path.expanduser("~/projects/taxmarker/blast/")
os.makedirs(b + "queries_orig/", exist_ok=True)
names = {}
for f in sorted(os.listdir(b + "queries")):
    names[f[:-4]] = [l[1:].strip() for l in open(b + "queries/" + f) if l[0] == ">"]
allnames = {n: k for k, v in names.items() for n in v}
out = {k: open(b + "queries_orig/" + k + ".fna", "w") for k in names}
w = None
for l in open("/data/users/dl/projects/sbdi-gtdb/taxmarker/bac-ssu-r232-1/weightfilter/user-alignment.weightfiltered.ungapped.fasta"):
    if l[0] == ">":
        n = l[1:].split()[0]
        w = out[allnames[n]] if n in allnames else None
        if w: w.write(">" + n + "\n")
    elif w: w.write(l)
for f in out.values(): f.close()
print({k: sum(1 for l in open(b + "queries_orig/" + k + ".fna") if l[0] == ">") for k in names})
