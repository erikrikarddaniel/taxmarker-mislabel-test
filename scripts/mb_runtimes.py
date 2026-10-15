#!/usr/bin/env python3
"""Runtime of the taxmarker setups on MislabelBench cells, from Nextflow execution traces.
Usage: mb_runtimes.py   (run in the directory holding traces/<setup>__<cell>.trace.txt)
Seconds. wall = first submit to last task end; the other columns sum task durations by stage.
Runs without a completed MULTIQC task (unfinished) are skipped.
"""
import csv, glob, os, re, sys
from datetime import datetime

def secs(s):
    t = 0.0
    for v, u in re.findall(r'([\d.]+)(ms|h|m|s|d)', s):
        t += float(v) * {'ms': 0.001, 's': 1, 'm': 60, 'h': 3600, 'd': 86400}[u]
    return t

def stage(name):
    if 'RAXMLNG_SEARCH' in name: return 'raxml'
    if 'SATIVAEPANG_' in name: return 'placement'
    if 'WEIGHTED_CLUSTERING' in name or 'RAXTAX_PREFILTER' in name: return 'prefilter'
    return 'other'

print('setup', 'k', 'seed', 'wall', 'raxml', 'placement', 'prefilter', 'other', sep='\t')
for p in sorted(glob.glob('traces/*.trace.txt')):
    setup, cell = os.path.basename(p).replace('.trace.txt', '').split('__')
    rows = list(csv.DictReader(open(p), delimiter='\t'))
    if not any('MULTIQC' in r['name'] and r['status'] == 'COMPLETED' for r in rows):
        continue
    m = re.match(r'inj_family_r0.05_k(\d+)_s(\d+)', cell)
    k, seed = (m.group(1), m.group(2)) if m else ('0', '0')
    sub = [datetime.strptime(r['submit'], '%Y-%m-%d %H:%M:%S.%f') for r in rows]
    end = [s.timestamp() + secs(r['duration']) for s, r in zip(sub, rows)]
    tot = dict.fromkeys(('raxml', 'placement', 'prefilter', 'other'), 0.0)
    for r in rows:
        tot[stage(r['name'])] += secs(r['duration'])
    print(setup, k, seed, round(max(end) - min(s.timestamp() for s in sub)), *(round(tot[x]) for x in ('raxml', 'placement', 'prefilter', 'other')), sep='\t')
