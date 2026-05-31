#!/usr/bin/env python3
"""
Análise estatística dos resultados (S6.4).
==========================================

Lê os CSVs gerados pelo metrics_node (formato longo:
timestamp,metric,value), extrai o valor final de cada métrica por execução,
agrega por experimento (rótulo no nome do arquivo: metrics_<LABEL>_*.csv) e
roda o comparativo Baseline (E1) vs Stay Alert (E3).

Uso:
    python3 analise_resultados.py ~/tese_ws/results
"""
import glob
import os
import re
import sys

import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

LABEL_RE = re.compile(r'metrics_([A-Za-z0-9]+)_\d{8}_\d{6}\.csv$')


def final_values(csv_path):
    """Último valor de cada métrica em uma execução."""
    df = pd.read_csv(csv_path)
    last = df.sort_values('timestamp').groupby('metric')['value'].last()
    return last.to_dict()


def load_runs(results_dir):
    """DataFrame: uma linha por execução, colunas = métricas + 'experiment'."""
    rows = []
    for path in sorted(glob.glob(os.path.join(results_dir, 'metrics_*.csv'))):
        m = LABEL_RE.search(os.path.basename(path))
        if not m:
            continue
        rec = final_values(path)
        rec['experiment'] = m.group(1)
        rec['file'] = os.path.basename(path)
        rows.append(rec)
    return pd.DataFrame(rows)


def compare(df, a='E1', b='E3', metric='anomalies_detected'):
    ga = df[df['experiment'] == a][metric].dropna()
    gb = df[df['experiment'] == b][metric].dropna()
    if len(ga) < 2 or len(gb) < 2:
        print(f'[!] amostras insuficientes para {a} vs {b} ({metric})')
        return
    t, p = stats.ttest_ind(ga, gb, equal_var=False)
    print(f'\n=== {metric}: {a} (n={len(ga)}) vs {b} (n={len(gb)}) ===')
    print(f'  média {a} = {ga.mean():.3f} ± {ga.std():.3f}')
    print(f'  média {b} = {gb.mean():.3f} ± {gb.std():.3f}')
    print(f'  Welch t = {t:.3f}, p = {p:.4f}'
          f'  ({"significativo" if p < 0.05 else "n.s."} a 5%)')

    fig, ax = plt.subplots()
    ax.boxplot([ga, gb], labels=[f'{a} (baseline)', f'{b} (Stay Alert)'])
    ax.set_ylabel(metric)
    ax.set_title(f'Comparativo: {a} vs {b}')
    out = f'comparativo_{metric}_{a}_vs_{b}.pdf'
    fig.savefig(out)
    print(f'  -> gráfico salvo em {out}')


def main():
    results_dir = sys.argv[1] if len(sys.argv) > 1 \
        else os.path.expanduser('~/tese_ws/results')
    df = load_runs(results_dir)
    if df.empty:
        print(f'Nenhum CSV encontrado em {results_dir}')
        return

    print('Execuções carregadas por experimento:')
    print(df['experiment'].value_counts().to_string())

    summary = df.groupby('experiment').agg(['mean', 'std'])
    summary.to_csv(os.path.join(results_dir, 'resumo_experimentos.csv'))
    print(f"\nResumo salvo em {os.path.join(results_dir, 'resumo_experimentos.csv')}")

    for metric in ('anomalies_unique', 'investigation_time_s',
                   'min_hazard_distance_m', 'hazard_avoidances',
                   'mission_duration_s', 'distance_traveled_m',
                   'route_deviations'):
        compare(df, 'E1', 'E3', metric)


if __name__ == '__main__':
    main()
