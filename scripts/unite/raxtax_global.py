"""raxtax of the sequences of a cluster against the cluster plus every other UNITE sequence of two taxa.

usage: raxtax_global.py viridiplantae.fasta CLUSTER_TAXONOMY.tsv TAXON1 TAXON2 > table.tsv
  TAXON1, TAXON2  such as p__Bryophyta and f__Fabaceae
Runs the raxtax of the pipeline (version 1.6.0, `--skip-exact-matches`) in docker and prints, per query, the
probability raxtax gives to each phylum. Needs docker.
"""
import collections
import os
import subprocess
import sys
import tempfile

fasta, cluster, *taxa = sys.argv[1:5]
inc = {line.split('\t')[0] for line in open(cluster)}
recs, name = {}, None
for line in open(fasta):
    line = line.rstrip('\n')
    if line[0] == '>':
        f = line[1:].split('|')
        name = f[1]
        recs[name] = [f[4], []]
    else:
        recs[name][1].append(line)

with tempfile.TemporaryDirectory() as tmp:
    with open(f'{tmp}/query.fasta', 'w') as q, open(f'{tmp}/db.fasta', 'w') as d:
        for a, (lineage, seq) in recs.items():
            entry = f'>{a};tax={lineage.replace(";", ",")};\n{"".join(seq)}\n'
            if a in inc:
                q.write(entry)
                d.write(entry)
            elif any(t in lineage.split(';') for t in taxa):
                d.write(entry)
    subprocess.run(['docker', 'run', '--rm', '--user', f'{os.getuid()}:{os.getgid()}', '-v', f'{tmp}:/w', '-w', '/w', 'quay.io/biocontainers/raxtax:1.6.0--h4349ce8_0',
                    'raxtax', '-d', 'db.fasta', '-i', 'query.fasta', '-o', 'out', '-t', '4', '--skip-exact-matches'],
                   check=True, capture_output=True)
    rows = [line.rstrip('\n').split('\t') for line in open(f'{tmp}/out/raxtax.out')]

phylum = collections.defaultdict(dict)
for query, lineage, prob in [(r[0], r[1], r[2]) for r in rows]:
    p = lineage.split(',')[1]
    phylum[query.split(';')[0]][p] = max(phylum[query.split(';')[0]].get(p, 0), float(prob.split(',')[1]))
declared = {a: recs[a][0].split(';')[1] for a in inc}
print('seq', 'declared_phylum', 'prob_declared', 'prob_other', 'other_phylum', sep='\t')
for a in sorted(phylum):
    p = phylum[a]
    other = max((k for k in p if k != declared[a]), key=lambda k: p[k], default='NA')
    print(a, declared[a], f'{p.get(declared[a], 0):.2f}', f'{p.get(other, 0):.2f}', other, sep='\t')
