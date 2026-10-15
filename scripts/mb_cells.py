#!/usr/bin/env python3
"""Flags of the taxmarker setups on MislabelBench cells (distance, rate, k and cell seed from the cell name).
Usage: mb_cells.py THR   (run in the directory holding truth/<cell>.truth.json and <setup>/<cell>_seed42.results)
testable = injected sequences that reach sativa-epang (gapfilter/*.tax, clusterselect/*.tax or checknameconsistency/*.tax, whichever is last).
Every method counts, as in setup_flags.py. flagged_expanded = injected sequences that are flagged or share a cluster with a flagged representative. added/lost are against the same setup's base run.
"""
import csv, glob, json, os, re, sys
thr = float(sys.argv[1])
SETUPS = ['alone', 'cluster', 'cluster_raxtax']
CELLS = [('base', 'none', 0, 0, 0)]
for p in sorted(glob.glob('truth/inj_*.truth.json')):
    cell = os.path.basename(p)[:-len('.truth.json')]
    d, r, k, s = re.match(r'inj_(\w+?)_r([\d.]+)_k(\d+)_s(\d+)$', cell).groups()
    CELLS.append((cell, d, float(r), int(k), int(s)))

def flags(setup, cell, sativa_only=False):
    p = f'{setup}/{cell}_seed42.results/mislabels/user-alignment.mislabels.tsv'
    return {r['seq_name'] for r in csv.DictReader(open(p), delimiter='\t')
            if float(r['lwr']) > thr and (not sativa_only or r['method'] == 'sativa')}

def present(setup, cell):
    for d, f in (('gapfilter', 'user-alignment.gapfiltered.tax'), ('clusterselect', 'user-alignment.representatives.tax'),
                 ('checknameconsistency', 'user-alignment.checked.tax')):
        p = f'{setup}/{cell}_seed42.results/{d}/{f}'
        if os.path.exists(p):
            return {l.split('\t')[0] for l in open(p)}
    return set()

def expand(setup, cell, names):
    p = f'{setup}/{cell}_seed42.results/clusterselect/user-alignment.selection.tsv'
    if not os.path.exists(p):
        return names
    rows = [l.rstrip('\n').split('\t') for l in open(p)][1:]
    hit = {r[0] for r in rows if r[2] in names}
    return names | {r[2] for r in rows if r[0] in hit}

print('setup', 'distance', 'rate', 'cell_k', 'cell_seed', 'injected', 'testable', 'flagged', 'flagged_sativa', 'flagged_expanded', 'other_flags', 'other_expanded', 'added', 'added_expanded', 'lost', sep='\t')
for setup in SETUPS:
    base = flags(setup, 'base')
    for cell, dist, rate, k, cs in CELLS:
        if not os.path.isdir(f'{setup}/{cell}_seed42.results'):
            continue
        inj = set(json.load(open(f'truth/{cell}.truth.json'))['injected']) if k else set()
        a = flags(setup, cell)
        ex, bex = expand(setup, cell, a), expand(setup, 'base', base)
        print(setup, dist, rate, k, cs, len(inj), len(inj & present(setup, cell)), len(a & inj), len(flags(setup, cell, True) & inj), len(ex & inj),
              len(a - inj), len(ex - inj), len(a - inj - base), len(ex - inj - bex), len(base - a - inj), sep='\t')
