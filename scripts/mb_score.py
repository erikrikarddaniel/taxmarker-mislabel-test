#!/usr/bin/env python3
"""Score our local runs with MislabelBench's score_injection.py.
Usage: mb_score.py SCORER.py NAME...   (run in the seedtest directory; seed 42, needs sativaepang/*.mis)
Writes a truth.json per set from NAME.truth.tsv, scores against k0 as baseline, prints one row per set
at confidence >= 0.9: injected found (his recall), flags on non-injected, added vs k0 baseline.
"""
import csv, json, subprocess, sys, tempfile
from pathlib import Path

scorer, names = sys.argv[1], sys.argv[2:]
real = set(open('real.txt').read().split())
mis = lambda n: f'{n}_seed42.results/sativaepang/user-alignment.mis'
print('set', 'injected', 'conf_found', 'conf_other', 'conf_added', 'excl_found', 'excl_added', 'at_rank', 'label_correct', sep='\t')
for n in names:
    rows = list(csv.DictReader(open(f'{n}.truth.tsv'), delimiter='\t'))
    inj = {r['id'].replace('~', '_').replace('#', '_'): {'true': r['original_lineage'], 'wrong': r['injected_lineage']} for r in rows}
    truth = {'distance': 'phylum', 'seed': 42, 'k': len(rows), 'n_total': 0, 'injected': inj}
    with tempfile.TemporaryDirectory() as d:
        t, o = Path(d, 't.json'), Path(d, 'o.json')
        t.write_text(json.dumps(truth))
        subprocess.run([sys.executable, scorer, '--truth', str(t), '--mis', mis(n), '--baseline-mis', mis('k0'),
                        '--thresholds', '0.9', '--out', str(o)], check=True, capture_output=True)
        s = json.loads(o.read_text())
    c, e = s['by_confidence'][0], (s['by_exclusion'] or [{}])[0]
    f = lambda x: '' if x is None else round(x * len(inj))
    print(n, len(inj), f(c['recall']), c['flags_on_non_injected'], c['added_vs_baseline'],
          f(e.get('recall')), e.get('added_vs_baseline', ''), f(c['recall_at_injected_rank']), f(c['recall_label_correct']), sep='\t')
