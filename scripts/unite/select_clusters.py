"""Write the members of four mmseqs clusters as pipeline input (sequences.fasta, taxonomy.tsv).

usage: select_clusters.py viridiplantae.fasta mmc0.85_cluster.tsv OUTDIR
"""
import collections
import os
import sys

fasta, tsv, out = sys.argv[1:4]

seqs, tax, name = {}, {}, None
for line in open(fasta):
    line = line.rstrip('\n')
    if line[0] == '>':
        name = line[1:]
        f = name.split('|')
        tax[name] = (f[1], f[4])
        seqs[name] = []
    else:
        seqs[name].append(line)

clusters = collections.defaultdict(list)
for line in open(tsv):
    rep, mem = line.rstrip('\n').split('\t')
    clusters[rep].append(mem)


def containing(acc):
    return next(m for m in clusters.values() if any(tax[x][0] == acc for x in m))


def represented_by(acc):
    return next(m for r, m in clusters.items() if tax[r][0] == acc)


selected = {
    'hoya_leichhardtia': containing('MW226603'),
    'bryophyta_fabaceae': containing('FJ037826'),
    'orchidaceae': represented_by('AF262817'),
    'carex': represented_by('HG992852'),
}
for tag, members in selected.items():
    os.makedirs(f'{out}/{tag}', exist_ok=True)
    with open(f'{out}/{tag}/sequences.fasta', 'w') as fa, open(f'{out}/{tag}/taxonomy.tsv', 'w') as tt:
        for x in members:
            acc, lineage = tax[x]
            fa.write(f'>{acc}\n{"".join(seqs[x])}\n')
            tt.write(f'{acc}\t{lineage}\n')
    print(tag, len(members))
