#!/usr/bin/env python3
"""
Análise estatística dos resultados (S6.4).
==========================================

Lê os CSVs gerados pelo metrics_node (formato longo:
timestamp,metric,value), extrai o valor FINAL de cada métrica por execução,
agrega por experimento (rótulo no nome do arquivo: metrics_<LABEL>_*.csv),
salva um resumo (média ± desvio, n) e roda o comparativo Baseline (E1) vs cada
configuração Stay Alert (E2/E3/E4 = eta 0.3/0.5/0.8; E5 = cenário adverso),
com teste t de Welch e boxplots por métrica.

Sem dependência de pandas (usa csv + numpy) — roda em qualquer máquina com o
stack ROS (numpy/scipy/matplotlib já vêm com a simulação).

Uso:
    python3 analise_resultados.py [~/tese_ws/results]
"""
import csv
import glob
import os
import re
import sys

import numpy as np
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

LABEL_RE = re.compile(r'metrics_([A-Za-z0-9]+)_\d{8}_\d{6}\.csv$')

# métricas de interesse (ordem de exibição) e se "maior é melhor"
METRICS = [
    'anomalies_unique',
    'anomalies_detected',
    'investigation_time_s',
    'route_deviations',
    'hazard_avoidances',
    'min_hazard_distance_m',
    'mission_duration_s',
    'distance_traveled_m',
    'q_convergence',
]
EXPERIMENTS = ['E1', 'E2', 'E3', 'E4', 'E5']


def final_values(csv_path):
    """Último valor (maior timestamp) de cada métrica numa execução."""
    best = {}   # metric -> (timestamp, value)
    with open(csv_path, newline='') as f:
        for row in csv.DictReader(f):
            try:
                ts = float(row['timestamp']); val = float(row['value'])
            except (TypeError, ValueError, KeyError):
                continue
            m = row['metric']
            if m not in best or ts >= best[m][0]:
                best[m] = (ts, val)
    return {m: v for m, (ts, v) in best.items()}


def load_runs(results_dir):
    """Lista de execuções: cada item = {'experiment':..., 'file':..., métricas}."""
    runs = []
    for path in sorted(glob.glob(os.path.join(results_dir, 'metrics_*.csv'))):
        m = LABEL_RE.search(os.path.basename(path))
        if not m:
            continue
        rec = final_values(path)
        rec['experiment'] = m.group(1)
        rec['file'] = os.path.basename(path)
        runs.append(rec)
    return runs


def values(runs, experiment, metric):
    """Array dos valores (finitos) de uma métrica para um experimento."""
    xs = [r[metric] for r in runs
          if r.get('experiment') == experiment and metric in r
          and np.isfinite(r[metric])]
    return np.array(xs, dtype=float)


def write_summary(runs, results_dir):
    exps = [e for e in EXPERIMENTS
            if any(r['experiment'] == e for r in runs)]
    out = os.path.join(results_dir, 'resumo_experimentos.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        header = ['experiment', 'n']
        for m in METRICS:
            header += [f'{m}_mean', f'{m}_std']
        w.writerow(header)
        for e in exps:
            n = sum(1 for r in runs if r['experiment'] == e)
            row = [e, n]
            for m in METRICS:
                v = values(runs, e, m)
                if len(v):
                    row += [f'{v.mean():.4f}', f'{v.std(ddof=1) if len(v) > 1 else 0.0:.4f}']
                else:
                    row += ['', '']
            w.writerow(row)
    print(f"Resumo salvo em {out}")
    return exps


def print_table(runs, exps):
    print('\n=== média ± desvio por experimento ===')
    print(f"{'métrica':<22}" + ''.join(f'{e:>16}' for e in exps))
    for m in METRICS:
        cells = []
        for e in exps:
            v = values(runs, e, m)
            cells.append(f'{v.mean():.2f}±{v.std(ddof=1) if len(v) > 1 else 0:.2f}'
                         if len(v) else '—')
        print(f'{m:<22}' + ''.join(f'{c:>16}' for c in cells))


def compare(runs, a, b, metric):
    ga, gb = values(runs, a, metric), values(runs, b, metric)
    if len(ga) < 2 or len(gb) < 2:
        return
    t, p = stats.ttest_ind(ga, gb, equal_var=False)
    sig = 'significativo' if p < 0.05 else 'n.s.'
    print(f'  {metric:<22} {a}={ga.mean():.2f}±{ga.std(ddof=1):.2f}  '
          f'{b}={gb.mean():.2f}±{gb.std(ddof=1):.2f}  '
          f'Welch t={t:+.2f} p={p:.4f} ({sig})')


def boxplot_metric(runs, exps, metric, results_dir):
    data = [values(runs, e, metric) for e in exps]
    data = [(d if len(d) else np.array([np.nan])) for d in data]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=exps)
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} por experimento')
    out = os.path.join(results_dir, f'box_{metric}.pdf')
    fig.savefig(out); plt.close(fig)


def main():
    results_dir = sys.argv[1] if len(sys.argv) > 1 \
        else os.path.expanduser('~/tese_ws/results')
    runs = load_runs(results_dir)
    if not runs:
        print(f'Nenhum CSV encontrado em {results_dir}')
        return

    counts = {e: sum(1 for r in runs if r['experiment'] == e)
              for e in sorted({r['experiment'] for r in runs})}
    print('Execuções carregadas por experimento:')
    for e, n in counts.items():
        print(f'  {e}: {n}')

    exps = write_summary(runs, results_dir)
    print_table(runs, exps)

    # comparativos vs baseline E1 (Welch) para as métricas-chave
    key = ['anomalies_unique', 'investigation_time_s', 'min_hazard_distance_m',
           'hazard_avoidances', 'mission_duration_s', 'route_deviations']
    for b in [e for e in ('E2', 'E3', 'E4', 'E5') if e in exps]:
        print(f'\n=== E1 (baseline) vs {b} ===')
        for m in key:
            compare(runs, 'E1', b, m)

    for m in key:
        boxplot_metric(runs, exps, m, results_dir)
    print(f'\nBoxplots (box_*.pdf) salvos em {results_dir}')


if __name__ == '__main__':
    main()
