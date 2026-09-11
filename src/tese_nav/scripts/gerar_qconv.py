#!/usr/bin/env python3
"""Estabilidade do value update: resíduo COMPLETO |alpha*td + eta*Phi| agregado
across TODOS os runs válidos de E3 (mean + banda 95%), ao longo da missão.
Responde R1.4/R2.4 (o proxy antigo excluía o termo afetivo e usava 1 run só).
Saída: qconv.pdf/.png."""
import csv, glob, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RES = os.path.expanduser('~/tese_ws/results')
METRIC = 'update_residual'          # resíduo completo (com o termo afetivo)
GRID = np.linspace(0, 1, 60)        # tempo normalizado [0,1] (missões ~mesma dur.)

series = []
for f in sorted(glob.glob(os.path.join(RES, 'metrics_E3_*.csv'))):
    t, v = [], []
    dist = 0.0
    with open(f) as fh:
        for row in csv.DictReader(fh):
            try:
                ts, val = float(row['timestamp']), float(row['value'])
            except (ValueError, TypeError, KeyError):
                continue
            if row['metric'] == 'distance_traveled_m':
                dist = max(dist, val)
            elif row['metric'] == METRIC:
                t.append(ts); v.append(val)
    if dist <= 1.0 or len(t) < 5:            # exclui spawn-fail / vazio
        continue
    t = np.array(t); v = np.array(v)
    t = (t - t[0]) / (t[-1] - t[0])          # normaliza tempo a [0,1]
    series.append(np.interp(GRID, t, v))     # reamostra na grade comum

M = np.array(series)                          # (n_runs, len(GRID))
mean = M.mean(axis=0)
lo = np.percentile(M, 2.5, axis=0)
hi = np.percentile(M, 97.5, axis=0)

fig, ax = plt.subplots(figsize=(5.0, 3.2))
ax.fill_between(GRID, lo, hi, color='tab:blue', alpha=0.18,
                label='95% band across runs')
ax.plot(GRID, mean, color='tab:blue', lw=1.8,
        label=f'mean over n={len(series)} runs')
ax.set_xlabel('normalized mission time')
ax.set_ylabel(r'complete residual $|\alpha\delta+\eta\Phi|$')
ax.grid(True, ls=':', alpha=0.4)
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig('qconv.pdf'); fig.savefig('qconv.png', dpi=150)
print(f'salvo qconv.pdf/.png | n={len(series)} runs, resíduo final~{mean[-1]:.4f}')
