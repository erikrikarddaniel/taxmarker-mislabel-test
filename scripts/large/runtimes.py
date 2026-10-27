import csv, glob, re, sys, collections

def secs(s):
    s = s.strip()
    if s in ('', '-'):
        return 0.0
    t = 0.0
    for v, u in re.findall(r'([\d.]+)\s*(ms|d|h|m|s)', s):
        v = float(v)
        t += v * {'ms': 0.001, 's': 1, 'm': 60, 'h': 3600, 'd': 86400}[u]
    return t

def pct(s):
    s = s.strip()
    return float(s.rstrip('%')) / 100 if s not in ('', '-') else 0.0

def proc(name):
    return re.sub(r'\s*\(.*\)$', '', name).split(':')[-1]

def load(f):
    with open(f) as fh:
        return list(csv.DictReader(fh, delimiter='\t'))

runs = sys.argv[1:]
for d in runs:
    files = sorted(glob.glob(f'{d}/pipeline_info/execution_trace_*.txt'))
    rows = [(f, load(f)) for f in files]
    last = rows[-1][1]
    ok = [r for r in last if r['status'] in ('COMPLETED', 'CACHED')]
    wall = sum(secs(r['realtime']) for r in ok)
    cpu = sum(secs(r['realtime']) * pct(r['%cpu']) for r in ok)
    bad = [r for _, rs in rows for r in rs if r['status'] in ('FAILED', 'ABORTED')]
    bwall = sum(secs(r['realtime']) or secs(r['duration']) for r in bad)
    print(f'== {d}  launches={len(files)} final={files[-1].split("_",2)[-1]}')
    print(f'   tasks={len(ok)} walltime_sum={wall/3600:.1f} h cpu_time={cpu/3600:.1f} h  '
          f'failed/aborted={len(bad)} wasted_wall={bwall/3600:.1f} h')
    by = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for r in ok:
        p = proc(r['name'])
        by[p][0] += 1
        by[p][1] += secs(r['realtime'])
        by[p][2] += secs(r['realtime']) * pct(r['%cpu'])
    for p, (n, w, c) in sorted(by.items(), key=lambda x: -x[1][1])[:12]:
        print(f'   {p:34s} n={n:4d} wall={w/3600:7.2f} h cpu={c/3600:8.2f} h')
    badby = collections.defaultdict(lambda: [0, 0.0])
    for r in bad:
        p = proc(r['name'])
        badby[p][0] += 1
        badby[p][1] += secs(r['realtime']) or secs(r['duration'])
    for p, (n, w) in sorted(badby.items(), key=lambda x: -x[1][1])[:6]:
        print(f'   [failed] {p:28s} n={n:3d} wall={w/3600:7.2f} h')
