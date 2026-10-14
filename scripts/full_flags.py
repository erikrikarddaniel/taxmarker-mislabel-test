#!/usr/bin/env python3
"""Flags of full-pipeline runs split into injected, known real and background, one TSV row per run.
Collateral and lost_baseline are relative to the flags of k0_full.results, same definitions as auguste_metrics.py.
Usage: full_flags.py THR NAME...   (reads NAME_full.results, NAME.truth.tsv if present, k0_full.results and real.txt)
"""
import csv, os, sys
thr = float(sys.argv[1])
norm = lambda s: s.replace('~', '_').replace('#', '_')
real = set(open('real.txt').read().split())
def flags(name):
    p = f'{name}_full.results/mislabels/user-alignment.mislabels.tsv'
    return {r['seq_name'] for r in csv.DictReader(open(p), delimiter='\t') if float(r['lwr']) > thr}
base = flags('k0')
print('set', 'injected', 'injected_flagged', 'real_flagged', 'background', 'collateral', 'lost_baseline', sep='\t')
for name in sys.argv[2:]:
    p = f'{name}.truth.tsv'
    truth = {norm(r['id']) for r in csv.DictReader(open(p), delimiter='\t')} if os.path.exists(p) else set()
    a = flags(name)
    print(name, len(truth), len(a & truth), len(a & real), len(a - truth - real), len(a - truth - real - base), len(base - a), sep='\t')
