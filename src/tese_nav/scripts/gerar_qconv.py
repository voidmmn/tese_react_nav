#!/usr/bin/env python3
"""Residuo COMPLETO |alpha*td + eta*Phi| ao longo da missao, SOBREPONDO os quatro
valores de eta (E0/E2/E3/E4).

Resubmissao (R2#1/R2#2/R2#4): a versao anterior plotava so o E3, de modo que a
unica figura dedicada a atualizacao de valor nao permitia ao leitor ver se eta
importa. Os dados dos quatro eta ja existiam. A figura agora mostra que o
instrumento detecta o termo que deve detectar -- e que o comportamento nao o
acompanha, o que e o argumento do Apendice (a tabela de valor nao seleciona acoes).

Saida: qconv.pdf/.png
"""
import csv, glob, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RES = os.path.expanduser('~/tese_ws/results')
METRIC = 'update_residual'
GRID = np.linspace(0, 1, 60)
CFGS = [('E0', 0.0, 'tab:gray'), ('E2', 0.3, 'tab:green'),
        ('E3', 0.5, 'tab:blue'), ('E4', 0.8, 'tab:red')]


def series_de(cfg):
    out = []
    for f in sorted(glob.glob(os.path.join(RES, f'metrics_{cfg}_*.csv'))):
        t, v, dist = [], [], 0.0
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
        if dist <= 1.0 or len(t) < 5:          # exclui spawn-fail
            continue
        t = np.array(t); v = np.array(v)
        t = (t - t[0]) / (t[-1] - t[0])
        out.append(np.interp(GRID, t, v))
    return np.array(out)


fig, ax = plt.subplots(figsize=(5.2, 3.3))
for cfg, eta, cor in CFGS:
    M = series_de(cfg)
    if M.size == 0:
        continue
    mean = M.mean(axis=0)
    lo = np.percentile(M, 2.5, axis=0)
    hi = np.percentile(M, 97.5, axis=0)
    ax.fill_between(GRID, lo, hi, color=cor, alpha=0.12)
    ax.plot(GRID, mean, color=cor, lw=1.7,
            label=rf'$\eta={eta}$  (n={M.shape[0]})')
ax.set_xlabel('normalized mission time')
ax.set_ylabel(r'complete residual $|\alpha\delta+\eta\Phi|$')
ax.grid(True, ls=':', alpha=0.4)
ax.legend(fontsize=7, title='value-update weight', title_fontsize=7)
fig.tight_layout()
out = os.path.expanduser('~/tese_ws/docs/artigo/figs/qconv')
fig.savefig(out + '.pdf'); fig.savefig(out + '.png', dpi=200)
print('gravado:', out + '.pdf')
