import os, json
base = "/data/users/dl/projects/sbdi-gtdb/taxmarker/"
O = os.path.expanduser("~/projects/taxmarker/dnc50/")
os.makedirs(O + "jobs", exist_ok=True)
plan = {j["id"]: j for j in json.load(open(O + "plan.json"))["jobs"]}
tax = {}
for l in open(base + "bac-ssu-r232-1/profilecover/user-alignment.covfiltered.tax"):
    n, _, t = l.rstrip("\n").partition("\t"); tax[n] = t
old = os.path.expanduser("~/projects/taxmarker/dnc/")
bad = 0
for l in open(old + "sample.tsv"):
    j = l.split("\t")[0]
    names = [x[1:].split()[0] for x in open(O + "parts/" + j + ".fasta") if x[0] == ">"]
    with open(O + "jobs/" + j + ".tax", "w") as ft:
        for n in names: ft.write(n + "\t" + tax[n] + "\n")
    own = set(names) - set(plan[j]["outgroups"]) - set(plan[j]["reps"])
    with open(O + "jobs/" + j + ".own", "w") as fo:
        for n in sorted(own): fo.write(n + "\n")
    oldown = {x.strip() for x in open(old + "jobs/" + j + ".own")}
    bad += own != oldown
    print(j, len(names), len(plan[j]["outgroups"]), len(own), file=open(O + "sample.tsv", "a"))
print("jobs with different own tips vs 4-outgroup run:", bad)
