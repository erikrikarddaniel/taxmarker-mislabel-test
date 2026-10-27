import json, sys, glob
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
print("fields", a["fields"] == b["fields"], "tree same", a["tree"] == b["tree"])
def load(j):
    o = {}
    for p in j["placements"]:
        for nm in (p.get("n") or [x[0] for x in p["nm"]]):
            o[nm] = p["p"]
    return o
A, B = load(a), load(b)
print("queries", len(A), len(B), "same names", set(A) == set(B))
f = a["fields"]; ie, il = f.index("edge_num"), f.index("like_weight_ratio")
same_top = same_set = 0; maxd = 0; diffs = 0
for n in A:
    pa, pb = sorted(A[n], key=lambda x: -x[il]), sorted(B[n], key=lambda x: -x[il])
    if pa[0][ie] == pb[0][ie]: same_top += 1
    if {x[ie] for x in pa} == {x[ie] for x in pb}: same_set += 1
    d = abs(pa[0][il] - pb[0][il]); maxd = max(maxd, d)
    if d > 1e-6: diffs += 1
print("same top edge", same_top, "same edge set", same_set, "top LWR differs >1e-6:", diffs, "max diff", maxd)
tie = lambda P: sum(1 for x in P if abs(x[il] - max(y[il] for y in P)) < 1e-9) > 1
diff_top = [n for n in A if sorted(A[n], key=lambda x: -x[il])[0][ie] != sorted(B[n], key=lambda x: -x[il])[0][ie]]
print("queries with tied top LWR (any 2+ edges): A", sum(1 for n in A if tie(A[n])), "B", sum(1 for n in B if tie(B[n])))
print("of the", len(diff_top), "with a different top edge: tied in A", sum(1 for n in diff_top if tie(A[n])), "tied in B", sum(1 for n in diff_top if tie(B[n])))
dset = [n for n in A if {x[ie] for x in A[n]} != {x[ie] for x in B[n]}]
print("different edge set:", len(dset), "LWR of top in A:", [round(max(x[il] for x in A[n]), 3) for n in dset])
