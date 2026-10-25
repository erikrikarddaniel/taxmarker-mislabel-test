cd ~/projects/taxmarker
W=/data/users/dl/projects/sbdi-gtdb/taxmarker/work/fb/4cc04dd1704ffb44dc7bd1d7c6610c
mkdir -p dnc50
time python3 -I treedivide.py split --alignment $W/user-alignment.covfiltered.fasta --constraint $W/user-alignment.guide.nwk \
  --outdir dnc50/parts --plan dnc50/plan.json --max 2000 --min 10 --reps 3 --outgroups 50 2>&1 | tail -3
python3 -I - <<PY
import json
o = {j["id"]: j for j in json.load(open("$W/user-alignment.plan.json"))["jobs"]}
n = {j["id"]: j for j in json.load(open("dnc50/plan.json"))["jobs"]}
print(len(o), len(n), "same ids:", set(o) == set(n))
print("same n/reps/root:", sum(1 for k in o if k in n and o[k]["n"] == n[k]["n"] and o[k]["reps"] == n[k]["reps"] and o[k]["root"] == n[k]["root"]))
print("resolved old/new:", sum(j["resolved"] for j in o.values()), sum(j["resolved"] for j in n.values()))
import statistics as st
print("outgroups new median", st.median(len(j["outgroups"]) for j in n.values()), "old", st.median(len(j["outgroups"]) for j in o.values()))
PY
