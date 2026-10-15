#!/usr/bin/env python3
"""Per injected sequence: how many of its S. aureus relatives carry the wrong label.
Usage: relatives.py THR NAME...   (run in the seedtest directory, seed 42; alignment from k0)
Relatives = the S. aureus-origin sequences present in NAME.fna: injected + the 3 real ones (wrong label)
and the donors left (true label). Leave-one-out: the sequence itself is excluded.
Distance = p-distance over alignment columns where both sequences have a base.
"""
import csv, sys
thr, names = float(sys.argv[1]), sys.argv[2:]
san = lambda s: s.replace('~', '_').replace('#', '_')

def fasta(p):
    seqs, name = {}, None
    for l in open(p):
        l = l.strip()
        if l.startswith('>'):
            name = san(l[1:].split()[0]); seqs[name] = []
        elif name:
            seqs[name].append(l)
    return {k: ''.join(v) for k, v in seqs.items()}

aln = fasta('k0_seed42.results/gunzip/user-alignment.afa')
tax = {san(l.split('\t')[0]): l.split('\t')[1].strip() for l in open('k0_seed42.results/checknameconsistency/user-alignment.checked.tax')}
donors = {k for k, v in tax.items() if v.endswith('s__Staphylococcus aureus')}
real = {san(x) for x in open('real.txt').read().split()}
origin = donors | real

def dist(a, b):
    n = d = 0
    for x, y in zip(aln[a], aln[b]):
        if x != '-' and y != '-':
            n += 1; d += x != y
    return d / n if n else 1.0

print('set', 'id', 'flagged', 'wrong_others', 'true_left', 'wrong_share', 'nn1_wrong', 'nn3_wrong', 'd_wrong', 'd_true', 'ident_wrong', 'ident_true', sep='\t')
for name in names:
    present = set(fasta(f'{name}.fna'))
    inj = {san(r['id']) for r in csv.DictReader(open(f'{name}.truth.tsv'), delimiter='\t')}
    flagged = {r['seq_name'] for r in csv.DictReader(open(f'{name}_seed42.results/mislabels/user-alignment.mislabels.tsv'), delimiter='\t')
               if r['method'] == 'sativa' and float(r['lwr']) > thr}
    wrong, true = (inj | real) & present, (origin - inj - real) & present
    for i in sorted(inj):
        others = sorted([(dist(i, j), 'w' if j in wrong else 't') for j in (wrong | true) - {i}])
        dw = min((d for d, c in others if c == 'w'), default='')
        dt = min((d for d, c in others if c == 't'), default='')
        nw = len(wrong) - 1
        print(name, i, int(i in flagged), nw, len(true), f'{nw / (nw + len(true)):.2f}',
              int(others[0][1] == 'w'), sum(c == 'w' for _, c in others[:3]),
              dw if dw == '' else f'{dw:.4f}', dt if dt == '' else f'{dt:.4f}',
              sum(d == 0 and c == 'w' for d, c in others), sum(d == 0 and c == 't' for d, c in others), sep='\t')
