#!/usr/bin/env python3
"""Auguste's four metrics as TSV: baseline = k0 flags, after = NAME flags, per seed.
Usage: auguste_metrics.py THR NAME...   (run in the directory with the NAME_seed<S>.results; seeds 42 43 44)
Rows with set 'k0 vs k0' give the noise floor: collateral = gained and lost_baseline = lost between two k0 seeds.
Sets without a seed are skipped.
"""
import csv, os, sys
thr = float(sys.argv[1])
real = set(open('real.txt').read().split())
def flags(name, seed):
    p = f'{name}_seed{seed}.results/mislabels/user-alignment.mislabels.tsv'
    return {r['seq_name'] for r in csv.DictReader(open(p), delimiter='\t')
            if r['method'] == 'sativa' and float(r['lwr']) > thr}
def truth(name):
    return {r['id'].replace('~', '_').replace('#', '_') for r in csv.DictReader(open(f'{name}.truth.tsv'), delimiter='\t')}
seeds = ['42', '43', '44']
b = {s: flags('k0', s) for s in seeds}
print('set', 'seed', 'injected', 'recalled', 'collateral', 'lost_baseline', 'after_flags', 'baseline_flags', sep='\t')
for a in seeds:
    for c in seeds:
        if a < c:
            print('k0 vs k0', f'{a}->{c}', 0, 0, len(b[c] - b[a]), len(b[a] - b[c]), len(b[c]), len(b[a]), sep='\t')
for name in sys.argv[2:]:
    t = truth(name)
    for s in seeds:
        if not os.path.exists(f'{name}_seed{s}.results'):
            continue
        a = flags(name, s)
        print(name, s, len(t), len(a & t), len(a - t - b[s] - real), len(b[s] - a), len(a), len(b[s]), sep='\t')
