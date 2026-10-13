#!/usr/bin/env python3
"""Relabel k donor-species sequences with the recipient species' lineage.

With --drop n, n further donor sequences are removed from the output, so the donor
species ends up the same size for every k with the same k + n. The k + n donors are drawn
together and the first k are injected, which makes sets nested and matches the plain
-k (k + n) draw of the same seed.

Headers must be GTDB style: >ID LINEAGE [...]. Writes the modified FASTA to
--out and a truth table (id, original and injected lineage, substitutions) to --truth.
"""
import argparse, random

p = argparse.ArgumentParser()
p.add_argument('fasta')
p.add_argument('--donor', default='s__Staphylococcus aureus')
p.add_argument('--recipient', default='s__Escherichia coli')
p.add_argument('-k', type=int, required=True)
p.add_argument('--drop', type=int, default=0, help='donor sequences to delete in addition to the k injected')
p.add_argument('--dropped', help='file to list the deleted ids in (required with --drop)')
p.add_argument('--mutation-rate', type=float, default=0.0, help='per-site substitution probability, drawn independently per sequence')
p.add_argument('--seed', type=int, default=1)
p.add_argument('--exclude', help='file of sequence ids that must not be drawn as donors (~ and # read as _)')
p.add_argument('--out', required=True)
p.add_argument('--truth', required=True)
a = p.parse_args()

recs = []
for line in open(a.fasta):
    if line[0] == '>':
        recs.append([line.rstrip('\n'), []])
    else:
        recs[-1][1].append(line.strip())
recs = [(h, ''.join(s)) for h, s in recs]

lineage = lambda h: h.split(' ', 1)[1].split(' [')[0]
species = lambda h: lineage(h).split(';')[-1]
recipient = next((lineage(h) for h, _ in recs if species(h) == a.recipient), None)
norm = lambda h: h.split()[0][1:].replace('~', '_').replace('#', '_')
excluded = set(open(a.exclude).read().split()) if a.exclude else set()
donors = [i for i, (h, _) in enumerate(recs) if species(h) == a.donor and norm(h) not in excluded]
if recipient is None or len(donors) < a.k + a.drop or (a.drop and not a.dropped):
    raise SystemExit(f'recipient found: {recipient is not None}; donors: {len(donors)} < k+drop={a.k + a.drop}; --dropped given: {bool(a.dropped)}')

rng = random.Random(a.seed)
drawn = rng.sample(donors, a.k + a.drop)
chosen, dropped = set(drawn[:a.k]), set(drawn[a.k:])
bases = 'ACGT'
with open(a.out, 'w') as out, open(a.truth, 'w') as truth:
    print('id\toriginal_lineage\tinjected_lineage\tsubstitutions', file=truth)
    for i, (h, s) in enumerate(recs):
        if i in dropped:
            continue
        nsub = 0
        if i in chosen:
            s = list(s)
            for j, b in enumerate(s):
                if b in bases and rng.random() < a.mutation_rate:
                    s[j] = rng.choice([x for x in bases if x != b])
                    nsub += 1
            s = ''.join(s)
            print(h.split()[0][1:], lineage(h), recipient, nsub, sep='\t', file=truth)
            h = h.replace(lineage(h), recipient, 1)
        out.write(h + '\n' + s + '\n')
if a.dropped:
    open(a.dropped, 'w').write(''.join(norm(recs[i][0]) + '\n' for i in sorted(dropped)))
