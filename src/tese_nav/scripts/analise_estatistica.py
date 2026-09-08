#!/usr/bin/env python3
"""
Análise estatística da bateria uniforme (resubmissão IEEE Access).
==================================================================

Substitui a análise Welch de ``analise_resultados.py`` pela análise
*distribution-free* efetivamente reportada no artigo, porque várias métricas
são contagens limitadas com variância (quase) nula, para as quais as premissas
do teste t de Welch não valem.

Lê os CSVs longos (``timestamp,metric,value``) gerados pelo metrics_node,
extrai o valor FINAL de cada métrica por execução e produz:

  1. Resumo por configuração  -> results/resumo_experimentos.csv
     (n válidas, n falhas de init, média ± desvio das métricas-chave).
  2. Família CONFIRMATÓRIA (Tabela de estatísticas do §V): Mann-Whitney U
     (permutação exata p/ arms degenerados), Cliff's delta, IC 95% bootstrap
     da diferença de médias, correção de Holm dentro da família.
  3. Família SECUNDÁRIA (Apêndice B): equivalência da ablação (eta), robustez
     a ruído e custo do cenário adverso, reportadas com Cliff's delta + IC 95%
     (equivalência se prova por tamanho de efeito + IC estreito ao redor de
     zero, NÃO por p-valor de significância).

Uma execução é "válida" se o robô de fato se moveu (distance_traveled_m > 1 m);
execuções que não inicializaram (distance ~ 0) são contadas à parte como
desfecho de confiabilidade de partida e excluídas das estatísticas
comportamentais.

Sem dependência de pandas (csv + numpy + scipy).

Uso:
    python3 analise_estatistica.py [~/tese_ws/results]
"""
import csv
import glob
import os
import re
import sys
import math

import numpy as np
from scipy import stats

LABEL_RE = re.compile(r'metrics_([A-Za-z0-9]+)_\d{8}_\d{6}\.csv$')
VALID_MIN_DIST = 1.0  # m; abaixo disso a execução não iniciou

SUMMARY_METRICS = [
    'anomalies_unique', 'route_deviations', 'hazard_avoidances',
    'min_hazard_distance_m', 'min_ttc_s', 'collisions',
    'mission_duration_s', 'distance_traveled_m', 'update_residual',
]
CONFIGS = ['E1', 'E0', 'E2', 'E3', 'E4', 'E5', 'APF', 'RHM', 'RHB',
           'N1', 'N2', 'CONF']

# Família confirmatória (Holm dentro dela).
CONFIRMATORY = [
    ('E1 vs E3', 'E1', 'E3', 'anomalies_unique', 'Anomalies inspected'),
    ('E1 vs E3', 'E1', 'E3', 'min_hazard_distance_m', 'Min. hazard dist. [m]'),
    ('E1 vs E3', 'E1', 'E3', 'mission_duration_s', 'Mission time [s]'),
    ('E3 vs APF', 'E3', 'APF', 'mission_duration_s', 'Mission time [s]'),
    ('RHB vs RHM', 'RHB', 'RHM', 'anomalies_unique', 'Anomalies inspected'),
    ('RHB vs RHM', 'RHB', 'RHM', 'min_hazard_distance_m', 'Min. hazard dist. [m]'),
    ('RHB vs RHM', 'RHB', 'RHM', 'min_ttc_s', 'Min. time-to-collision [s]'),
]
# Família secundária (equivalência / robustez / custo) — reportada por efeito+IC.
SECONDARY = [
    ('E0 vs E3', 'E0', 'E3', 'anomalies_unique', 'Anomalies inspected'),
    ('E0 vs E3', 'E0', 'E3', 'mission_duration_s', 'Mission time [s]'),
    ('E0 vs E2', 'E0', 'E2', 'mission_duration_s', 'Mission time [s]'),
    ('E0 vs E4', 'E0', 'E4', 'mission_duration_s', 'Mission time [s]'),
    ('E3 vs N1', 'E3', 'N1', 'anomalies_unique', 'Anomalies inspected'),
    ('E3 vs N2', 'E3', 'N2', 'anomalies_unique', 'Anomalies inspected'),
    ('E3 vs N1', 'E3', 'N1', 'min_hazard_distance_m', 'Min. hazard dist. [m]'),
    ('E3 vs N2', 'E3', 'N2', 'min_hazard_distance_m', 'Min. hazard dist. [m]'),
    ('E3 vs E5', 'E3', 'E5', 'anomalies_unique', 'Anomalies inspected'),
    ('E3 vs E5', 'E3', 'E5', 'mission_duration_s', 'Mission time [s]'),
]


def final_values(path):
    d = {}
    for r in csv.DictReader(open(path, newline='')):
        try:
            ts = float(r['timestamp']); v = float(r['value'])
        except (TypeError, ValueError, KeyError):
            continue
        m = r['metric']
        if m not in d or ts >= d[m][0]:
            d[m] = (ts, v)
    return {m: v for m, (ts, v) in d.items()}


def load(results_dir):
    runs = {}
    for p in sorted(glob.glob(os.path.join(results_dir, 'metrics_*.csv'))):
        m = LABEL_RE.search(os.path.basename(p))
        if not m:
            continue
        runs.setdefault(m.group(1), []).append(final_values(p))
    return runs


def valid(runs, cfg):
    return [r for r in runs.get(cfg, [])
            if r.get('distance_traveled_m', 0.0) > VALID_MIN_DIST]


def vals(runs, cfg, metric):
    xs = [r[metric] for r in valid(runs, cfg)
          if metric in r and np.isfinite(r[metric])]
    return np.array(xs, dtype=float)


def cliffs_delta(a, b):
    gt = sum(1 for x in b for y in a if x > y)
    lt = sum(1 for x in b for y in a if x < y)
    return (gt - lt) / (len(a) * len(b))


def boot_ci(a, b, n=10000, seed=0):
    rng = np.random.default_rng(seed)
    diffs = np.array([rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean()
                      for _ in range(n)])
    return np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)


def mwu(a, b):
    if a.std() == 0 and b.std() == 0:
        return 1.0 if a.mean() == b.mean() else 0.0
    try:
        _, p = stats.mannwhitneyu(a, b, alternative='two-sided', method='auto')
        return p
    except Exception:
        return float('nan')


def holm(ps):
    order = np.argsort(ps); m = len(ps); out = [None] * m; run = 0.0
    for rank, idx in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[idx])); out[idx] = run
    return out


def stat_row(runs, a, b, metric):
    A, B = vals(runs, a, metric), vals(runs, b, metric)
    if len(A) < 1 or len(B) < 1:
        return None
    lo, hi = boot_ci(A, B)
    return dict(delta=B.mean() - A.mean(), cliff=cliffs_delta(A, B),
                ci=(lo, hi), p=mwu(A, B), nA=len(A), nB=len(B))


def fmt_p(p):
    return '<0.001' if p < 0.001 else f'{p:.3g}'


def write_summary(runs, results_dir):
    out = os.path.join(results_dir, 'resumo_experimentos.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        header = ['config', 'n_valid', 'n_failed_init']
        for m in SUMMARY_METRICS:
            header += [f'{m}_mean', f'{m}_std']
        w.writerow(header)
        for c in CONFIGS:
            allr = runs.get(c, []); v = valid(runs, c)
            row = [c, len(v), len(allr) - len(v)]
            for m in SUMMARY_METRICS:
                xs = vals(runs, c, m)
                if len(xs):
                    row += [f'{xs.mean():.4f}',
                            f'{xs.std(ddof=1) if len(xs) > 1 else 0.0:.4f}']
                else:
                    row += ['', '']
            w.writerow(row)
    print(f'Resumo -> {out}')


def main():
    rd = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/tese_ws/results')
    runs = load(rd)
    if not runs:
        print(f'Nenhum CSV em {rd}'); return

    total = sum(len(v) for v in runs.values())
    nvalid = sum(len(valid(runs, c)) for c in runs)
    print(f'Execuções: {total} totais, {nvalid} válidas, '
          f'{total - nvalid} falhas de inicialização\n')
    for c in CONFIGS:
        v = valid(runs, c); allr = runs.get(c, [])
        print(f'  {c:5s} n={len(v):2d} válidas'
              + (f' (+{len(allr) - len(v)} falha init)' if len(allr) != len(v) else ''))

    write_summary(runs, rd)

    # 1) família confirmatória com Holm
    rows = [(lab, pretty, stat_row(runs, a, b, mk))
            for lab, a, b, mk, pretty in CONFIRMATORY]
    rows = [(lab, pr, r) for lab, pr, r in rows if r]
    hp = holm([r['p'] for _, _, r in rows])
    print('\n=== FAMÍLIA CONFIRMATÓRIA (Holm dentro da família) ===')
    print(f'{"pair":<12}{"metric":<26}{"Δ":>9}{"δ":>7}{"95% CI":>20}{"p":>9}{"p_H":>9}')
    for (lab, pr, r), h in zip(rows, hp):
        ci = f'[{r["ci"][0]:+.2f},{r["ci"][1]:+.2f}]'
        print(f'{lab:<12}{pr:<26}{r["delta"]:>+9.2f}{r["cliff"]:>+7.2f}'
              f'{ci:>20}{fmt_p(r["p"]):>9}{fmt_p(h):>9}')

    # 2) família secundária (equivalência / robustez / custo) — efeito + IC
    print('\n=== FAMÍLIA SECUNDÁRIA (equivalência/robustez/custo — efeito+IC) ===')
    print(f'{"pair":<12}{"metric":<26}{"Δ":>9}{"δ":>7}{"95% CI":>20}{"p":>9}')
    for lab, a, b, mk, pretty in SECONDARY:
        r = stat_row(runs, a, b, mk)
        if not r:
            continue
        ci = f'[{r["ci"][0]:+.2f},{r["ci"][1]:+.2f}]'
        print(f'{lab:<12}{pretty:<26}{r["delta"]:>+9.2f}{r["cliff"]:>+7.2f}'
              f'{ci:>20}{fmt_p(r["p"]):>9}')


if __name__ == '__main__':
    main()
