#!/usr/bin/env python3
"""Painel 2x2 de boxplots das métricas-chave p/ o paper (bateria uniforme).
Lê ~/tese_ws/results/metrics_*.csv, EXCLUI spawn-fails (distância~0).
Configs: E1 (baseline), E0 (ablação η=0), E3 (método), E5 (adverso),
APF (baseline reativo). Saída: box_panel.pdf/.png."""
import csv, glob, os, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RES = os.path.expanduser('~/tese_ws/results')
LABEL_RE = re.compile(r'metrics_([A-Za-z0-9]+)_\d{8}_\d{6}\.csv$')
EXPS = ['E1', 'E0', 'E3', 'E5', 'APF']
PANELS = [
    ('anomalies_unique', 'Anomalies inspected'),
    ('min_hazard_distance_m', 'Min. hazard distance [m]'),
    ('mission_duration_s', 'Mission duration [s]'),
    ('hazard_avoidances', 'Hazard avoidances'),
]


def final_values(path):
    best = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            try:
                ts, v = float(row['timestamp']), float(row['value'])
            except (ValueError, TypeError, KeyError):
                continue
            m = row['metric']
            if m not in best or ts >= best[m][0]:
                best[m] = (ts, v)
    return {k: v for k, (t, v) in best.items()}


runs = []
for p in sorted(glob.glob(os.path.join(RES, 'metrics_*.csv'))):
    m = LABEL_RE.search(os.path.basename(p))
    if not m:
        continue
    rec = final_values(p)
    if rec.get('distance_traveled_m', 0) <= 1.0:   # exclui spawn-fail
        continue
    rec['experiment'] = m.group(1)
    runs.append(rec)


def vals(exp, metric):
    return [r[metric] for r in runs if r.get('experiment') == exp
            and metric in r and np.isfinite(r[metric])]


fig, axes = plt.subplots(2, 2, figsize=(6.8, 5.2))
for ax, (metric, label) in zip(axes.ravel(), PANELS):
    data = [vals(e, metric) or [np.nan] for e in EXPS]
    ax.boxplot(data, labels=EXPS, showmeans=True)
    ax.set_ylabel(label, fontsize=8)
    ax.tick_params(labelsize=8)
    ax.grid(True, axis='y', ls=':', alpha=0.4)
fig.tight_layout()
fig.savefig('box_panel.pdf')
fig.savefig('box_panel.png', dpi=150)
n = {e: len(vals(e, 'anomalies_unique')) for e in EXPS}
print('salvo box_panel.pdf/.png | n válidos por config:', n)
