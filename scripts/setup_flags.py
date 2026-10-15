#!/usr/bin/env python3
"""Flags of one pipeline setup (clustering with or without raxtax) split into injected, known real and background.
Usage: setup_flags.py SETUP THR NAME...   (run in the seedtest directory; reads SETUP/NAME_seed42.results, NAME.truth.tsv, NAME.dropped, real.txt)
injected_testable = injected sequences that are cluster representatives (cluster/NAME.reps, from clusterselect), the only ones sativa-epang places; NA without that file.
Every method counts, as in full_flags.py. Collateral and lost_baseline are relative to the flags of SETUP/k0; baseline flags deleted from the input do not count as lost.
"""
import csv, os, sys
setup, thr = sys.argv[1], float(sys.argv[2])
norm = lambda s: s.replace('~', '_').replace('#', '_')
real = set(open('real.txt').read().split())
def flags(name):
    p = f'{setup}/{name}_seed42.results/mislabels/user-alignment.mislabels.tsv'
    return {r['seq_name'] for r in csv.DictReader(open(p), delimiter='\t') if float(r['lwr']) > thr}
def ids(path):
    if not os.path.exists(path):
        return set()
    return {norm(l.strip().split('\t')[0]) for l in open(path) if l.strip() and not l.startswith('id\t')}
base = flags('k0')
print('setup', 'set', 'injected', 'injected_testable', 'injected_flagged', 'real_flagged', 'background', 'collateral', 'lost_baseline', sep='\t')
for name in sys.argv[3:]:
    t, d = ids(f'{name}.truth.tsv'), ids(f'{name}.dropped')
    a = flags(name)
    testable = len(t & ids(f'cluster/{name}.reps')) if os.path.exists(f'cluster/{name}.reps') else 'NA'
    print(setup, name, len(t), testable, len(a & t), len(a & real), len(a - t - real), len(a - t - real - base), len(base - a - d), sep='\t')
