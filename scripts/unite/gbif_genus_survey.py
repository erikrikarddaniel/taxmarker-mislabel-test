"""Compare the genus-to-lineage assignments of UNITE with the GBIF backbone.

usage: gbif_genus_survey.py unite.fasta simple.txt.gz GBIF_KINGDOM > table.tsv   (GBIF_KINGDOM: Plantae, Fungi ...)
One row per (UNITE genus, UNITE family) with its number of sequences, the phylum, class, order and families of
the accepted genera of that name in the backbone's kingdom, those of its synonym and doubtful records, and:
  class  agrees              an accepted genus of that name is in the same family
         agrees_nonaccepted  no accepted genus; a synonym or doubtful record is in the same family
         synonym_match_only  accepted genera exist, none in UNITE's family, but a synonym or doubtful record is
         differs             accepted genera exist and none (nor any other record) is in UNITE's family
         no_match            only synonym or doubtful records, none in UNITE's family
         not_found           no genus of that name
  phylum_ok, class_ok, order_ok  yes if UNITE's name is that of an accepted genus's taxon, or the two occur
         together in at least MIN_PAIR rows of class agrees (UNITE and GBIF name taxa differently, so the pairs are
         learned from the data); no if not; NA when there is no accepted genus or UNITE's name is a placeholder
  first_mismatch  the highest of phylum, class, order and family at which the lineages differ, none, or NA
Placeholder genera (Incertae sedis, _sp, unidentified) are skipped. Columns of simple.txt.gz by position:
0 id, 4 status, 5 rank, 10 kingdom_key, 11 phylum_key, 12 class_key, 13 order_key, 14 family_key, 20 canonical_name.
"""
import collections
import gzip
import re
import sys

MIN_PAIR = 5
PLACEHOLDER = re.compile(r'(?i)Incertae|_sp$|unidentified')
RANKS = ('phylum', 'class', 'order')
fasta, backbone, gbif_kingdom = sys.argv[1:4]

count = collections.Counter()
for line in open(fasta):
    if line[0] == '>':
        lin = dict(x.split('__', 1) for x in line.rstrip('\n').split('|')[4].split(';'))
        genus = lin.get('g', '')
        if genus and not PLACEHOLDER.search(genus):
            count[(genus, lin.get('f', ''), lin.get('p', ''), lin.get('c', ''), lin.get('o', ''))] += 1
wanted = {k[0] for k in count}

names = {}
genera = collections.defaultdict(list)
with gzip.open(backbone, 'rt') as handle:
    for line in handle:
        f = line.split('\t')
        if f[5] in ('KINGDOM', 'PHYLUM', 'CLASS', 'ORDER', 'FAMILY') and f[4] == 'ACCEPTED':
            names[f[0]] = f[20]
        elif f[5] == 'GENUS' and f[20] in wanted:
            genera[f[20]].append((f[4], f[10], f[11], f[12], f[13], f[14]))

rows = []
for (genus, family, phylum, klass, order), n in sorted(count.items()):
    accepted, other = set(), set()
    gb = {r: set() for r in RANKS}
    for status, kingdom, pk, ck, ok_, fk in genera.get(genus, []):
        if names.get(kingdom) != gbif_kingdom:
            continue
        fam = names.get(fk, f'key{fk}')
        if status == 'ACCEPTED':
            accepted.add(fam)
            for rank, key in zip(RANKS, (pk, ck, ok_)):
                gb[rank].add(names.get(key, f'key{key}'))
        else:
            other.add((fam, status.lower()))
    other_fams = {fam for fam, _ in other}
    if family in accepted:
        cls = 'agrees'
    elif accepted:
        cls = 'synonym_match_only' if family in other_fams else 'differs'
    elif other:
        cls = 'agrees_nonaccepted' if family in other_fams else 'no_match'
    else:
        cls = 'not_found'
    rows.append(dict(genus=genus, unite_phylum=phylum, unite_class=klass, unite_order=order, unite_family=family,
                     sequences=n, gbif_phylum=';'.join(sorted(gb['phylum'])) or 'NA',
                     gbif_class=';'.join(sorted(gb['class'])) or 'NA', gbif_order=';'.join(sorted(gb['order'])) or 'NA',
                     gbif_accepted_families=';'.join(sorted(accepted)) or 'NA',
                     gbif_other_families=';'.join(sorted(f'{a} ({b})' for a, b in other)) or 'NA', **{'class': cls}))

pairs = {r: collections.Counter() for r in RANKS}
for row in rows:
    if row['class'] == 'agrees':
        for rank in RANKS:
            for g in row[f'gbif_{rank}'].split(';'):
                pairs[rank][(row[f'unite_{rank}'], g)] += 1


def judge(unite, gbif, counter):
    if gbif == 'NA' or PLACEHOLDER.search(unite):
        return 'NA'
    return 'yes' if any(unite == g or counter[(unite, g)] >= MIN_PAIR for g in gbif.split(';')) else 'no'


cols = ['genus', 'unite_phylum', 'unite_class', 'unite_order', 'unite_family', 'sequences', 'gbif_phylum', 'gbif_class',
        'gbif_order', 'gbif_accepted_families', 'gbif_other_families', 'class', 'phylum_ok', 'class_ok', 'order_ok',
        'first_mismatch']
print(*cols, sep='\t')
for row in rows:
    for rank in RANKS:
        row[f'{rank}_ok'] = judge(row[f'unite_{rank}'], row[f'gbif_{rank}'], pairs[rank])
    fam = 'NA' if row['gbif_accepted_families'] == 'NA' or PLACEHOLDER.search(row['unite_family']) else \
        ('yes' if row['class'] == 'agrees' else 'no')
    levels = [row['phylum_ok'], row['class_ok'], row['order_ok'], fam]
    row['first_mismatch'] = next((r for r, v in zip(('phylum', 'class', 'order', 'family'), levels) if v == 'no'),
                                 'NA' if all(v == 'NA' for v in levels) else 'none')
    print(*[row[c] for c in cols], sep='\t')
