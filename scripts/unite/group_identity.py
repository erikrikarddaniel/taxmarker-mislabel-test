"""Identity of a labelled group to the rest of its declared parent taxon, and to a contrast taxon.

usage: group_identity.py viridiplantae.fasta GROUP TARGETS PARENT PARENT_N CONTRAST CONTRAST_N EXCLUDE.tsv
  TARGETS    comma-separated accessions of the group
  PARENT     taxon the group is declared in, such as p__Coniferophyta (all members if fewer than PARENT_N)
  CONTRAST   taxon the group may belong to, such as f__Apocynaceae
  EXCLUDE.tsv  accessions (first column) kept out of both samples, normally the pipeline taxonomy of the cluster
Aligns targets and samples with MAFFT (needs `mafft`) and prints, per sequence, the best identity to the
other targets, to the parent sample and to the contrast sample, over aligned columns where both have a residue
(at least 100 such columns). Eight sequences of the parent sample are also printed as a scale (role=reference).
"""
import random
import subprocess
import sys
import tempfile

fasta, group, targets, parent, parent_n, contrast, contrast_n, exclude = sys.argv[1:9]
targets = targets.split(',')
parent_n, contrast_n = int(parent_n), int(contrast_n)
excluded = {line.split('\t')[0] for line in open(exclude)} | set(targets)

recs, name = {}, None
for line in open(fasta):
    line = line.rstrip('\n')
    if line[0] == '>':
        f = line[1:].split('|')
        name = f[1]
        recs[name] = [set(f[4].split(';')), []]
    else:
        recs[name][1].append(line)

random.seed(1)
parent_ids = [a for a, v in recs.items() if parent in v[0] and a not in excluded]
contrast_ids = [a for a, v in recs.items() if contrast in v[0] and a not in excluded]
parent_s = random.sample(parent_ids, min(parent_n, len(parent_ids)))
contrast_s = random.sample(contrast_ids, min(contrast_n, len(contrast_ids)))

with tempfile.TemporaryDirectory() as tmp:
    with open(f'{tmp}/in.fasta', 'w') as out:
        for role, ids in (('T', targets), ('P', parent_s), ('C', contrast_s)):
            for a in ids:
                out.write(f'>{role}_{a}\n{"".join(recs[a][1])}\n')
    aligned = subprocess.run(['mafft', '--auto', '--preservecase', '--thread', '4', f'{tmp}/in.fasta'],
                             capture_output=True, text=True, check=True).stdout

seqs, name = {}, None
for line in aligned.splitlines():
    if line[0] == '>':
        name = line[1:]
        seqs[name] = []
    else:
        seqs[name].append(line.upper())
seqs = {k: ''.join(v) for k, v in seqs.items()}


def identity(a, b):
    match = total = 0
    for x, y in zip(seqs[a], seqs[b]):
        if x != '-' and y != '-':
            total += 1
            match += x == y
    return match / total if total >= 100 else None


def best(a, role):
    v = [identity(a, b) for b in seqs if b[0] == role and b != a]
    v = [x for x in v if x is not None]
    return f'{max(v):.3f}' if v else 'NA'


print('group', 'role', 'seq', 'best_targets', 'best_parent', 'best_contrast', sep='\t')
for a in seqs:
    if a[0] == 'T':
        print(group, 'target', a[2:], best(a, 'T'), best(a, 'P'), best(a, 'C'), sep='\t')
for a in [k for k in seqs if k[0] == 'P'][:8]:
    print(group, 'reference', a[2:], 'NA', best(a, 'P'), best(a, 'C'), sep='\t')
