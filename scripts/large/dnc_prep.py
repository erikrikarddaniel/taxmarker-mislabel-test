import os, glob, json, csv
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
out = os.path.expanduser("~/projects/taxmarker/dnc/")
os.makedirs(out + "jobs", exist_ok=True)
plan = json.load(open(base + "work/fb/4cc04dd1704ffb44dc7bd1d7c6610c/user-alignment.plan.json"))["jobs"]
plan = {j["id"]: j for j in plan}
trace = base + "bac-ssu-r232-1/pipeline_info/execution_trace_2026-10-23_09-18-42.txt"
where = {}
for l in open(trace):
    f = l.rstrip("\n").split("\t")
    if "DIVIDED_TREE_SEARCH:RAXMLNG_SEARCH" in f[3]:
        job = f[3].split("(")[1].rstrip(")")
        where[job] = glob.glob(base + "work/" + f[1] + "*")[0]
tax = {}
for l in open(base + "bac-ssu-r232-1/profilecover/user-alignment.covfiltered.tax"):
    n, _, t = l.rstrip("\n").partition("\t"); tax[n] = t
# stratified sample by size, root excluded
ids = sorted((j for j in plan if not plan[j]["root"] and j in where), key=lambda j: plan[j]["n"])
sample = ids[::12]
with open(out + "sample.tsv", "w") as fh:
    for j in sample:
        d = where[j]
        names = [l[1:].split()[0] for l in open(d + "/" + j + ".fasta") if l[0] == ">"]
        with open(out + "jobs/" + j + ".tax", "w") as ft:
            for n in names: ft.write(n + "\t" + tax[n] + "\n")
        own = set(names) - set(plan[j]["outgroups"]) - set(plan[j]["reps"])
        with open(out + "jobs/" + j + ".own", "w") as fo:
            for n in sorted(own): fo.write(n + "\n")
        fh.write("\t".join([j, d, str(plan[j]["n"]), str(len(names)), str(len(own))]) + "\n")
print(len(sample), "jobs; own tips total", sum(int(l.split("\t")[4]) for l in open(out + "sample.tsv")))
