"""Replace the lineage of named genera by the one UNITE uses for the family of the backbone's accepted genus.

usage: lineage_correct.py unite.fasta taxonomy.tsv survey.tsv GENUS[,GENUS...] > corrected.tsv
taxonomy.tsv: accession, tab, lineage (k__...;s__...). survey.tsv: output of gbif_genus_survey.py. For each genus
the family is the single accepted family of the backbone; the ranks from kingdom to family are taken from the most
common UNITE lineage of that family, the genus and species are kept. The changes are listed on stderr.
"""
import collections
import csv
import sys

fasta, taxonomy, survey, genera = sys.argv[1:5]
genera = genera.split(',')

above = collections.defaultdict(collections.Counter)
for line in open(fasta):
    if line[0] == '>':
        ranks = line.rstrip('\n').split('|')[4].split(';')
        for i, r in enumerate(ranks):
            if r.startswith('f__'):
                above[r[3:]][';'.join(ranks[:i + 1])] += 1

family = {}
for row in csv.DictReader(open(survey), delimiter='\t'):
    if row['genus'] in genera and ';' not in row['gbif_accepted_families'] and row['gbif_accepted_families'] != 'NA':
        family[row['genus']] = row['gbif_accepted_families']
missing = set(genera) - set(family)
if missing:
    sys.exit(f'no single accepted family in the survey for: {", ".join(sorted(missing))}')
prefix = {g: above[f].most_common(1)[0][0] for g, f in family.items()}

changed = collections.Counter()
for line in open(taxonomy):
    acc, lineage = line.rstrip('\n').split('\t')
    ranks = lineage.split(';')
    genus = next((r[3:] for r in ranks if r.startswith('g__')), None)
    if genus in prefix:
        new = ';'.join([prefix[genus]] + [r for r in ranks if r[:3] in ('g__', 's__')])
        changed[(lineage.rsplit(';g__', 1)[0], prefix[genus])] += 1
        lineage = new
    print(acc, lineage, sep='\t')
for (old, new), n in changed.items():
    print(f'{n} sequences: {old}  ->  {new}', file=sys.stderr)
