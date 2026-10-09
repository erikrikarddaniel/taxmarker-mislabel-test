import re, sys, statistics
sys.setrecursionlimit(20000)
tax = {l.split('\t')[0]: l.rstrip().split('\t')[1] for l in open('k0_seed42.results/profilecover/user-alignment.covfiltered.tax')}
import csv
name = sys.argv[1] if len(sys.argv) > 1 else 'k0'
real = set(open('real.txt').read().split())
if name != 'k0': real |= {r['id'].replace('~','_').replace('#','_') for r in csv.DictReader(open(f'{name}.truth.tsv'), delimiter='\t')}
t = open(f'{name}_seed42.results/raxmlng/user-alignment.raxml.bestTree').read()
tok = re.findall(r'\(|\)|,|;|[^(),;:]+|:[0-9.eE+-]+', t)
class N:
    def __init__(s): s.kids=[]; s.name=None; s.bl=0.0; s.par=None; s.leaves=None
i = 0
def parse():
    global i
    n = N()
    if tok[i] == '(':
        i += 1
        while True:
            c = parse(); c.par = n; n.kids.append(c)
            if tok[i] == ',': i += 1; continue
            break
        i += 1
        if i < len(tok) and tok[i] not in ',();:' and not tok[i].startswith(':'): n.name = tok[i]; i += 1
    else:
        n.name = tok[i]; i += 1
    if i < len(tok) and tok[i].startswith(':'): n.bl = float(tok[i][1:]); i += 1
    return n
root = parse()
def lv(n):
    if n.leaves is None: n.leaves = [n.name] if not n.kids else [x for k in n.kids for x in lv(k)]
    return n.leaves
nodes = []
def walk(n):
    nodes.append(n)
    for k in n.kids: walk(k)
walk(root); lv(root)
sp = lambda x: tax[x].split(';')[-1]
def mrca(names):
    s = set(names); n = next(x for x in nodes if not x.kids and x.name in s)
    while not s <= set(lv(n)): n = n.par
    return n
ec = [x for x in tax if sp(x) == 's__Escherichia coli']
true_ec = [x for x in ec if x not in real]
m_ec = mrca(ec); m_real = mrca(real)
print(f'E. coli labelled: {len(ec)} leaves; MRCA subtree has {len(lv(m_ec))} leaves (is the labelled clade monophyletic: {len(lv(m_ec))==len(ec)})')
print(f'real contaminants: MRCA subtree {len(lv(m_real))} leaves, a clade of their own: {set(lv(m_real))==real}; stem length above it {m_real.bl:.4f}')
tb = {x.name: x.bl for x in nodes if not x.kids}
print('terminal branches: contaminants', [round(tb[r],4) for r in real], '| true E. coli median %.4f range %.4f-%.4f' % (statistics.median(tb[x] for x in true_ec), min(tb[x] for x in true_ec), max(tb[x] for x in true_ec)), '| all leaves median %.4f' % statistics.median(tb.values()))
inner = [x.bl for x in nodes if x.kids and x is not root and len(lv(x)) >= 2]
below = sum(v < m_real.bl for v in inner)
print(f'stem above the contaminant clade: longer than {100*below/len(inner):.1f}% of {len(inner)} internal branches (p99 = {sorted(inner)[int(.99*len(inner))]:.4f})')
# internal branches inside each labelled-species clade at least 6 leaves, longest first
within = []
for n in nodes:
    if n.kids and len(lv(n)) >= 2:
        sps = {sp(x) for x in lv(n)}
        if len(sps) == 1: within.append((n.bl, len(lv(n)), next(iter(sps))))
within.sort(reverse=True)
print('longest internal branches that subtend a single-species group:', [(round(b,3), n, s[3:20]) for b, n, s in within[:5]])
sa = [x for x in tax if sp(x) == 's__Staphylococcus aureus']
m_sa = mrca(sa); print(f'S. aureus: {len(sa)} leaves, monophyletic subtree {len(lv(m_sa))}, median terminal %.4f' % statistics.median(tb[x] for x in sa))
print('contaminant clade sister:', sorted({sp(x) for x in lv(m_real.par)})[:5], 'parent subtree', len(lv(m_real.par)), 'leaves')
