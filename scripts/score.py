#!/usr/bin/env python3
"""Score per-seed SATIVA flags against injected truth.

Usage: score.py NAME [SEED ...]   (default seeds 42 43 44), NAME e.g. k10 or asaia10
Reads <NAME>_seed<S>.results/mislabels/user-alignment.mislabels.tsv and <NAME>.truth.tsv
(k0 has no truth). real.txt lists the 3 S. aureus sequences already labelled E. coli in the
source data; they are scored as 'real', not as background. Only SATIVA flags are used.
Consensus rules: any (union), majority, all.
"""
import csv, sys
from itertools import combinations

k = sys.argv[1]
seeds = sys.argv[2:] or ['42', '43', '44']
try:
    truth = {r['id'].replace('~', '_').replace('#', '_') for r in csv.DictReader(open(f'{k}.truth.tsv'), delimiter='\t')}
except FileNotFoundError:
    truth = set()
real = set(open('real.txt').read().split())

def flags(seed, thr):
    p = f'{k}_seed{seed}.results/mislabels/user-alignment.mislabels.tsv'
    return {r['seq_name'] for r in csv.DictReader(open(p), delimiter='\t')
            if r['method'] == 'sativa' and float(r['lwr']) > thr}

print('set', 'lwr', 'rule', 'flagged', 'injected', 'injected_found', 'real_found', 'background', 'jaccard', sep='\t')
for thr in (0.0, 0.9, 0.95, 0.97, 0.98, 0.99):
    F = {s: flags(s, thr) for s in seeds}
    n = len(seeds)
    pair = [len(F[a] & F[b]) / max(1, len(F[a] | F[b])) for a, b in combinations(seeds, 2)]
    jac = f'{sum(pair) / len(pair):.2f}' if pair else 'NA'
    def row(name, S):
        print(k, thr, name, len(S), len(truth), len(S & truth), len(S & real), len(S - truth - real), jac, sep='\t')
    for s in seeds:
        row('seed ' + s, F[s])
    counts = {}
    for S in F.values():
        for x in S:
            counts[x] = counts.get(x, 0) + 1
    row('any', set(counts))
    row('majority', {x for x, c in counts.items() if c > n / 2})
    row('all', {x for x, c in counts.items() if c == n})
