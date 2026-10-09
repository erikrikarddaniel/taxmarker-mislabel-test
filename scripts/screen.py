#!/usr/bin/env python3
"""List sequences of the given species whose median identity to another species beats that to their own.
Usage: screen.py 's__Staphylococcus aureus' ['s__Escherichia coli' ...]
Identity = matches over columns where both sequences have a base, from the aligned covfiltered fasta.
"""
import sys
tax = {l.split('\t')[0]: l.rstrip().split('\t')[1] for l in open('k0_seed42.results/profilecover/user-alignment.covfiltered.tax')}
seqs = {}
for l in open('k0_seed42.results/profilecover/user-alignment.covfiltered.fasta'):
    if l[0] == '>': name = l[1:].split()[0]; seqs[name] = []
    else: seqs[name].append(l.strip().upper())
seqs = {k: ''.join(v) for k, v in seqs.items()}
sp = lambda n: tax[n].split(';')[-1]
def ident(a, b):
    m = t = 0
    for x, y in zip(a, b):
        if x != '-' and y != '-' and x != '.' and y != '.':
            t += 1; m += x == y
    return m / t if t else 0
import collections, statistics
for species in sys.argv[1:]:
    own = [n for n in seqs if sp(n) == species]
    print(f'{species}: {len(own)} sequences')
    for n in own:
        vals = collections.defaultdict(list)
        for m in seqs:
            if m == n: continue
            vals[sp(m)].append(ident(seqs[n], seqs[m]))
        mean = {k: statistics.median(v) for k, v in vals.items()}
        other = max((k for k in mean if k != species), key=mean.get)
        if mean[other] > mean[species]:
            print(f'  SUSPECT {n}: median identity to own species {mean[species]:.4f}, to {other} {mean[other]:.4f}')
