"""One row per mmseqs identity: cluster counts, size classes, label mixing and the testable share per rank.

usage: unite_sweep.py CLUSTERDIR   (reads CLUSTERDIR/summary_<identity>.txt written by unitesum.py)
"""
import re
import sys

IDENTITIES = ['0.99', '0.97', '0.95', '0.90', '0.85', '0.80', '0.75']
RANKS = ['phylum', 'class', 'order', 'family', 'genus', 'species']
SIZES = ['1', '2', '3-5', '6-10', '11-25', '26-50', '51-100', '>100']

cols = (['identity', 'clusters', 'sequences'] + [f'seqs_size_{s}' for s in SIZES] + ['clusters_size_1']
        + [f'multi_{r}' for r in RANKS] + [f'testable_{r}' for r in RANKS])
print(*cols, sep='\t')
for ident in IDENTITIES:
    text = open(f'{sys.argv[1]}/summary_{ident}.txt').read()
    clusters, sequences = map(int, re.search(r'(\d+) clusters, (\d+) sequences', text).groups())
    size_rows = {m[0]: m[1:] for m in re.findall(r'^(\S+)\s+(\d+)\s+[\d.]+\s+(\d+)\s+[\d.]+$', text, re.M)}
    multi = {m[0]: m[1] for m in re.findall(r'^\s+>1 (\w+)\s*:\s+(\d+)', text, re.M)}
    testable = {m[0]: m[1] for m in re.findall(r'^\s+(\w+)\s*: \d+/\d+ = ([\d.]+)%', text, re.M)}
    print(ident, clusters, sequences, *[size_rows[s][1] for s in SIZES], size_rows['1'][0],
          *[multi[r] for r in RANKS], *[testable[r] for r in RANKS], sep='\t')
