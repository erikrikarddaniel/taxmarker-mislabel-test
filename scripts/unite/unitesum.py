"""Summarise an mmseqs cluster table over UNITE sequences: cluster counts, sizes, taxon composition.

usage: unitesum.py viridiplantae.fasta mmc0.90_cluster.tsv [identity-label]
"""
import collections
import sys

RANKS = 'kpcofgs'
NAMES = {'k': 'kingdom', 'p': 'phylum', 'c': 'class', 'o': 'order', 'f': 'family', 'g': 'genus', 's': 'species'}

fasta, tsv = sys.argv[1], sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else tsv

tax = {}
for line in open(fasta):
    if line[0] != '>':
        continue
    h = line[1:].strip()
    f = h.split('|')
    ranks = dict(x.split('__', 1) for x in f[4].split(';'))
    tax[h] = ranks

clusters = collections.defaultdict(list)
for line in open(tsv):
    rep, mem = line.rstrip('\n').split('\t')
    clusters[rep].append(mem)

sizes = sorted((len(m) for m in clusters.values()))
n = sum(sizes)
print(f'== {label}: {len(clusters)} clusters, {n} sequences')
bins = [(1, 1), (2, 2), (3, 5), (6, 10), (11, 25), (26, 50), (51, 100), (101, 10**9)]
print('size      clusters   % of clusters   sequences   % of sequences')
for lo, hi in bins:
    c = [s for s in sizes if lo <= s <= hi]
    lab = f'{lo}' if lo == hi else (f'{lo}-{hi}' if hi < 10**9 else f'>{lo-1}')
    print(f'{lab:8s} {len(c):8d}   {100*len(c)/len(sizes):9.1f}      {sum(c):8d}   {100*sum(c)/n:9.1f}')
print('largest 10 clusters:', sizes[-10:][::-1], ' median', sizes[len(sizes) // 2])


def is_labelled(rank, name):
    if rank == 's':
        return not (name.endswith('_sp') or '_sp_' in name or 'Incertae' in name or 'unidentified' in name.lower())
    return 'Incertae' not in name and 'unidentified' not in name.lower() and not name.endswith('_sp')


def distinct(members, rank):
    return {tax[m][rank] for m in members if is_labelled(rank, tax[m][rank])}


print('\nclusters with more than one distinct label at a rank (clusters of size >= 2):')
multi = [m for m in clusters.values() if len(m) >= 2]
print(f'  clusters of size >= 2: {len(multi)}')
for r in 'pcofgs':
    k = sum(1 for m in multi if len(distinct(m, r)) > 1)
    print(f'  >1 {NAMES[r]:8s}: {k:6d}  ({100*k/len(multi):.1f}% of them)')

print('\nper rank, share of sequences with a labelled taxon that has a same-label partner in its cluster (testable):')
for r in 'pcofgs':
    tot = ok = 0
    for m in clusters.values():
        cnt = collections.Counter(tax[x][r] for x in m if is_labelled(r, tax[x][r]))
        for c in cnt.values():
            tot += c
            if c >= 2:
                ok += c
    print(f'  {NAMES[r]:8s}: {ok}/{tot} = {100*ok/tot:.1f}%')

print('\nper rank, taxa spread over clusters (taxa with >=2 sequences):')
for r in 'pcofg':
    where = collections.defaultdict(collections.Counter)
    for rep, m in clusters.items():
        for x in m:
            if is_labelled(r, tax[x][r]):
                where[tax[x][r]][rep] += 1
    multi_t = {t: c for t, c in where.items() if sum(c.values()) >= 2}
    in_one = sum(1 for c in multi_t.values() if len(c) == 1)
    big = sum(max(c.values()) for c in multi_t.values()) / max(1, sum(sum(c.values()) for c in multi_t.values()))
    print(f'  {NAMES[r]:8s}: {len(multi_t)} taxa, {in_one} entirely in one cluster, '
          f'{100*big:.1f}% of their sequences in the taxon\'s largest cluster')

print('\n20 largest clusters (size; phyla/families/genera/species counts; top families and genera):')
for rep, m in sorted(clusters.items(), key=lambda kv: -len(kv[1]))[:20]:
    fam = collections.Counter(tax[x]['f'] for x in m)
    gen = collections.Counter(tax[x]['g'] for x in m)
    print(f'  {len(m):5d}  p={len(distinct(m, "p"))} f={len(distinct(m, "f"))} g={len(distinct(m, "g"))} s={len(distinct(m, "s"))}  '
          f'fam: {", ".join(f"{k}({v})" for k, v in fam.most_common(3))}  gen: {", ".join(f"{k}({v})" for k, v in gen.most_common(3))}')

print('\nclusters mixing phyla or orders (size >= 2), with composition:')
mixed = [(rep, m) for rep, m in clusters.items() if len(m) >= 2 and len(distinct(m, 'p')) > 1]
print(f'  {len(mixed)} clusters with >1 phylum')
for rep, m in sorted(mixed, key=lambda kv: -len(kv[1]))[:15]:
    ph = collections.Counter(tax[x]['p'] for x in m)
    print(f'  {len(m):4d}  {", ".join(f"{k}({v})" for k, v in ph.most_common())}  e.g. {tax[rep]["s"]}')
