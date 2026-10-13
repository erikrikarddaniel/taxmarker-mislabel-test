#!/usr/bin/env python3
"""Flags of a full-pipeline run split into injected, known real and background, as one TSV row.
Usage: full_flags.py THR NAME...   (reads NAME_full.results, NAME.truth.tsv and real.txt)
"""
import csv, sys
thr = float(sys.argv[1])
norm = lambda s: s.replace('~', '_').replace('#', '_')
real = set(open('real.txt').read().split())
print('set', 'injected', 'injected_flagged', 'real_flagged', 'background', sep='\t')
for name in sys.argv[2:]:
    truth = {norm(r['id']) for r in csv.DictReader(open(f'{name}.truth.tsv'), delimiter='\t')}
    flagged = {r['seq_name'] for r in csv.DictReader(open(f'{name}_full.results/mislabels/user-alignment.mislabels.tsv'), delimiter='\t')
               if float(r['lwr']) > thr}
    print(name, len(truth), len(flagged & truth), len(flagged & real), len(flagged - truth - real), sep='\t')
