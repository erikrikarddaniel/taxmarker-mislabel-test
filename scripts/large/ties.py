import json, sys
for p in sys.argv[1:]:
    j = json.load(open(p)); f = j["fields"]; il = f.index("like_weight_ratio")
    n = t = 0
    for q in j["placements"]:
        w = [x[il] for x in q["p"]]; m = max(w)
        k = len(q.get("n") or q["nm"])
        n += k
        if sum(1 for x in w if abs(x - m) < 1e-9) > 1: t += k
    print(p.split("/work/")[-1][:12], "queries", n, "with tied top edge", t, "%.1f%%" % (100 * t / n))
