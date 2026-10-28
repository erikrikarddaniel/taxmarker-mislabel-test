"""One row per (cluster, run): sequence counts through the pipeline and the flags, by rank and method.

usage: unite_pipeline.py INPUTS LABEL=RUNDIR [LABEL=RUNDIR ...]
INPUTS/<cluster>/sequences.fasta is the pipeline input, RUNDIR/run_<cluster>/out the published results.
"""
import collections
import csv
import os
import re
import sys

PLACEHOLDER = re.compile(r'(?i)[ _]sp[.]?$|Incertae[ _]sedis|^unidentified')
RANKS = 'kpcofgs'
CLUSTERS = ['carex', 'orchidaceae', 'hoya_leichhardtia', 'bryophyta_fabaceae']

inputs = sys.argv[1]


def count_fasta(path):
    return sum(1 for line in open(path) if line[0] == '>')


def rows(path):
    return list(csv.DictReader(open(path), delimiter='\t'))


def last_rank_placeholder(label):
    name = label.split(';')[-1].split('__', 1)[-1]
    return bool(PLACEHOLDER.search(name))


cols = ['cluster', 'run', 'input', 'representatives', 'after_raxtax', 'excluded_gapfilter', 'scored',
        'flags', 'raxtax_flags', 'sativa_flags', 'flags_placeholder'] + [f'rank_{r}' for r in RANKS]
print(*cols, sep='\t')
for cluster in CLUSTERS:
    for spec in sys.argv[2:]:
        label, rundir = spec.split('=', 1)
        out = f'{rundir}/run_{cluster}/out'
        if not os.path.isdir(out):
            continue
        selection = rows(f'{out}/clusterselect/user-alignment.selection.tsv')
        flags = rows(f'{out}/mislabels/user-alignment.mislabels.tsv')
        summary = dict(line.strip().split(': ') for line in open(f'{out}/sativaepang/user-alignment.summary.txt'))
        method = collections.Counter(f['method'] for f in flags)
        rank = collections.Counter(int(f['mismatch_rank']) for f in flags)
        placeholder = sum(1 for f in flags if last_rank_placeholder(f['original_label']) or last_rank_placeholder(f['predicted_label']))
        print(cluster, label, count_fasta(f'{inputs}/{cluster}/sequences.fasta'),
              sum(1 for s in selection if s['is_representative'] == 'True'),
              count_fasta(f'{out}/raxtaxfilter/user-alignment.filtered.fasta'),
              len(rows(f'{out}/gapfilter/user-alignment.excluded.tsv')),
              summary['sequences scored'], len(flags), method['raxtax'], method['sativa'], placeholder,
              *[rank[i + 1] for i in range(len(RANKS))], sep='\t')
