#!/usr/bin/env python3
"""For each representative that stands for an injected sequence in a full-pipeline run, write a TSV row with
the top raxtax genus, the top summed SATIVA lwr species, and which method flagged it ('-' if none).
Usage: trace_full.py NAME   (reads NAME_full.results and NAME.truth.tsv)
"""
import csv, collections, glob, json, re, sys
name = sys.argv[1]
R = f'{name}_full.results/'
norm = lambda s: s.replace('~', '_').replace('#', '_')
truth = {norm(r['id']): r for r in csv.DictReader(open(f'{name}.truth.tsv'), delimiter='\t')}
inj_taxon = next(iter(truth.values()))['injected_lineage']
sel = list(csv.DictReader(open(R + 'clusterselect/user-alignment.selection.tsv'), delimiter='\t'))
byc = collections.defaultdict(list)
for r in sel: byc[r['cluster_id']].append(r)
reps = {}
for c in byc.values():
    for m in c:
        if m['is_representative'] == 'True' and m['taxon'] == inj_taxon:
            n = sum(x['seq_name'] in truth for x in c if x['taxon'] == inj_taxon)
            if n: reps[m['seq_name']] = (n, len(c), len({x['taxon'] for x in c}))
flag = {}
for r in csv.DictReader(open(R + 'mislabels/user-alignment.mislabels.tsv'), delimiter='\t'):
    flag.setdefault(r['seq_name'], []).append((r['method'], r['lwr']))
tax = {l.split('\t')[0]: l.rstrip().split('\t')[1] for l in open(R + 'clusterselect/user-alignment.representatives.tax')}
rax = collections.defaultdict(dict)
for l in open(R + 'raxtax/user-alignment/raxtax.out'):
    f = l.rstrip('\n').split('\t')
    q = f[0].split(';tax=')[0]; g = f[1].split(',')[5]
    rax[q][g] = float(f[2].split(',')[5])
def parse(tree):
    tok = re.findall(r'\(|\)|,|;|[^(),;:{}]*(?::[0-9.eE+-]+)?(?:\{\d+\})?', tree)
    tok = [t for t in tok if t != '']
    edges = {}
    def node(i):
        if tok[i] == '(':
            i += 1; leaves = []
            while True:
                l, i = node(i); leaves += l
                if tok[i] == ',': i += 1; continue
                break
            i += 1
            lab = ''
            if i < len(tok) and tok[i] not in ',();': lab = tok[i]; i += 1
        else:
            lab = tok[i]; i += 1; leaves = None
        m = re.match(r'([^:{]*)(?::[0-9.eE+-]+)?(?:\{(\d+)\})?$', lab)
        if leaves is None:
            nm = m.group(1); nm = nm[2:] if nm.startswith('r_') else nm; leaves = [nm]
        if m.group(2): edges[int(m.group(2))] = leaves
        return leaves, i
    node(0)
    return edges
place = {}
for f in glob.glob(R + 'sativaepang/looplace/user-alignment.l1o_tasks/fold_*/epa_result.jplace'):
    j = json.load(open(f)); edges = None
    for p in j['placements']:
        for n in p.get('n', p.get('nm', [])):
            n = n if isinstance(n, str) else n[0]
            q = n[2:] if n[:2] in ('q_', 'r_') else n
            if q in reps:
                edges = edges or parse(j['tree'])
                tot = collections.Counter()
                for x in p['p']:
                    lv = edges[x[0]]
                    for l in lv: tot[tax.get(l, '?').split(';')[-1]] += x[2] / len(lv)
                place[q] = tot
print('set', 'representative', 'stands_for_injected', 'cluster_size', 'cluster_taxa', 'raxtax_top_genus', 'raxtax_top_conf', 'sativa_top_species', 'sativa_top_lwr', 'flagged_by', sep='\t')
for q, (n, size, ntax) in reps.items():
    r = rax.get(q, {})
    top = sorted(((v, g) for g, v in r.items()), reverse=True)[:1]
    pl = place.get(q, collections.Counter()).most_common(1)
    print(name, q, n, size, ntax,
          top[0][1].split('g__')[-1] if top else 'NA', top[0][0] if top else 'NA',
          pl[0][0][3:] if pl else 'NA', round(pl[0][1], 2) if pl else 'NA',
          ','.join(sorted({m for m, _ in flag.get(q, [])})) or '-', sep='\t')
