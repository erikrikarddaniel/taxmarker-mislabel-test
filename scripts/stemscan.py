#!/usr/bin/env python3
"""Longest internal stem that subtends a strict subset of one labelled taxon.
Usage: stemscan.py TREE TAX RANK_INDEX [TOP]
TAX: id<TAB>lineage; RANK_INDEX counts ';'-separated lineage fields from 0 (6 = species for GTDB).
For every taxon with at least 3 leaves: n leaves, whether it is monophyletic in the tree, the longest
stem above a clade made only of that taxon's leaves (2 <= size < n), its size, and the stem's rank
among all internal branches of the tree.
"""
import re, sys, statistics
sys.setrecursionlimit(100000)
tree, taxf, rk = sys.argv[1], sys.argv[2], int(sys.argv[3])
top = int(sys.argv[4]) if len(sys.argv) > 4 else 15
out = sys.argv[5] if len(sys.argv) > 5 else None
tax = {l.split('\t')[0]: l.rstrip('\n').split('\t')[1].split(';')[rk] for l in open(taxf)}
tok = re.findall(r'\(|\)|,|;|[^(),;:]+|:[0-9.eE+-]+', open(tree).read())
class N:
    __slots__ = ('kids', 'name', 'bl', 'par', 'leaves')
    def __init__(s): s.kids = []; s.name = None; s.bl = 0.0; s.par = None; s.leaves = None
i = 0
def parse():
    global i
    n = N()
    if tok[i] == '(':
        i += 1
        while True:
            c = parse(); c.par = n; n.kids.append(c)
            if tok[i] == ',': i += 1; continue
            break
        i += 1
        if i < len(tok) and not tok[i].startswith(':') and tok[i] not in ',();': n.name = tok[i]; i += 1
    else:
        n.name = tok[i]; i += 1
    if i < len(tok) and tok[i].startswith(':'): n.bl = float(tok[i][1:]); i += 1
    return n
root = parse()
nodes = []
def walk(n):
    nodes.append(n)
    for k in n.kids: walk(k)
    n.leaves = frozenset([n.name]) if not n.kids else frozenset().union(*(k.leaves for k in n.kids))
walk(root)
internal = sorted(n.bl for n in nodes if n.kids and n is not root)
def pct(v): 
    import bisect; return 100 * bisect.bisect_left(internal, v) / len(internal)
by = {}
for l in (x for x in root.leaves):
    by.setdefault(tax.get(l, '?'), set()).add(l)
rows = []
for t, L in by.items():
    if len(L) < 3 or t == '?': continue
    best = (0.0, 0, None)
    for n in nodes:
        if n.kids and n is not root and 2 <= len(n.leaves) < len(L) and n.leaves <= L and n.bl > best[0]:
            best = (n.bl, len(n.leaves), n.leaves)
    if best[1]:
        m = next(n for n in nodes if not n.kids and n.name in L)
        while not L <= m.leaves: m = m.par
        rows.append((best[0], best[1], len(L), len(m.leaves) == len(L), t, sorted(best[2])))
rows.sort(reverse=True)
print(f'{len(tax)} labelled leaves, {len(by)} taxa at rank {rk}, {len(rows)} taxa with >=3 leaves and a proper sub-clade; internal branch p50 {statistics.median(internal):.4f} p99 {internal[int(.99*len(internal))]:.4f}')
print('stem   subset/n  monophyletic  pctile  taxon')
for b, k, n, mono, t, _ in rows[:top]:
    print(f'{b:.3f}  {k:>3}/{n:<4} {str(mono):12s}  {pct(b):5.1f}  {t[:60]}')
if out:
    with open(out, 'w') as fh:
        print('taxon\tstem\tsubset\tn_taxon\tmonophyletic\tpctile\tleaves', file=fh)
        for b, k, n, mono, t, lv in rows:
            print(f'{t}\t{b:.4f}\t{k}\t{n}\t{mono}\t{pct(b):.1f}\t{",".join(lv)}', file=fh)
