#!/usr/bin/env python3
"""Alternative raxtax flagging rules at one rank, from raxtax.out.
Usage: raxrule.py RUNDIR [TRUTH]   (RUNDIR has raxtax/user-alignment/raxtax.out)
 now : best != declared and conf(best) >= 0.9        (current filter)
 A   : conf(best) > conf(declared)                    (strictly higher than the declared label's support)
 B   : best != declared                               (any different assignment, ties included)
"""
import collections, csv, sys
rundir = sys.argv[1]
RANK = 5  # index into the 7 ranks d,p,c,o,f,g,s; 5 = genus, 6 = species
if len(sys.argv) > 3: RANK = int(sys.argv[3])
cand = collections.defaultdict(dict)  # query -> taxon at rank -> conf
declared = {}
for l in open(rundir + '/raxtax/user-alignment/raxtax.out'):
    f = l.rstrip('\n').split('\t')
    q, tax = f[0].split(';tax=')
    declared[q] = tax.rstrip(';').split(',')[RANK]
    t = f[1].split(',')[RANK]; c = float(f[2].split(',')[RANK])
    cand[q][t] = max(c, cand[q].get(t, 0))
def best(q): return max(cand[q].items(), key=lambda kv: kv[1])
count = collections.Counter(declared.values())
flags = {'now': set(), 'A': set(), 'B': set()}
checkable = 0
for q, d in declared.items():
    if count[d] < 2: continue
    checkable += 1
    t, c = best(q); cd = cand[q].get(d, 0)
    if t != d and c >= 0.9: flags['now'].add(q)
    if c > cd: flags['A'].add(q)
    if t != d: flags['B'].add(q)
sat = set()
try:
    sat = {r['seq_name'] for r in csv.DictReader(open(rundir + '/sativaepang/user-alignment.mislabels.tsv'), delimiter='\t')}
except FileNotFoundError: pass
print(f'{rundir}: {len(declared)} queries, {checkable} checkable (declared taxon has another member), rank index {RANK}')
for k, v in flags.items():
    print(f'  {k:3s} flags {len(v):4d}  also flagged by SATIVA {len(v & sat):3d}')
if len(sys.argv) > 2 and sys.argv[2] != '-':
    t = {r['id'].replace('~', '_').replace('#', '_') for r in csv.DictReader(open(sys.argv[2]), delimiter='\t')}
    sel = list(csv.DictReader(open(rundir + '/clusterselect/user-alignment.selection.tsv'), delimiter='\t'))
    reps = {m['seq_name'] for m in sel if m['is_representative'] == 'True' and any(x['cluster_id'] == m['cluster_id'] and x['taxon'] == m['taxon'] and x['seq_name'] in t for x in sel)}
    print(f'  injected representatives: {len(reps)}; caught: ' + ', '.join(f'{k} {len(v & reps)}' for k, v in flags.items()))
