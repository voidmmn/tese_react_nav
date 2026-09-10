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
    # §10/§13: desfechos separados (auditoria de sucesso vs falha/adiamento)
    'investigation_timeouts', 'investigation_deferred',
    'nav_aborted', 'nav_canceled', 'nav_rejected',
]
CONFIGS = ['E1', 'E0', 'E2', 'E3', 'E4', 'E5', 'APF', 'RHM', 'RHB',
           'N1', 'N2', 'CONF', 'KOa', 'KOb', 'DHa', 'DHb']

# Nº de anomalias elegíveis POR CENÁRIO (denominador da "inspeção completa"),
# definido a priori pela configuração do cenário --- NÃO derivado do máximo
# observado nos resultados (que subestimaria em grupos degenerados como KOb).
TARGET_ANOM = {
    'E1': 3, 'E0': 3, 'E2': 3, 'E3': 3, 'E4': 3, 'APF': 3, 'N1': 3, 'N2': 3,
    'CONF': 3,                       # 3 elegíveis; a 4ª (co-localizada) é suprimida
    'E5': 5,                         # cenário denso
    'RHM': 3, 'RHB': 3, 'KOa': 3, 'KOb': 3,   # perigo-na-rota: 3 anomalias
    'DHa': 1, 'DHb': 1,                        # ensaio dirigido: 1 anomalia
}

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
    # ensaio dirigido: benefício transiente do recuo (perigo durante investigação)
    ('DHb vs DHa', 'DHb', 'DHa', 'min_hazard_distance_m', 'Min. hazard dist. [m]'),
    ('DHb vs DHa', 'DHb', 'DHa', 'min_ttc_s', 'Min. time-to-collision [s]'),
    ('DHb vs DHa', 'DHb', 'DHa', 'time_below_clearance_s', 'Time below clearance [s]'),
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
        if a.mean() == b.mean():
            return 1.0
        # arms constantes disjuntos: p EXATO de permutação (2 caudas)
        return 2.0 / math.comb(len(a) + len(b), len(a))
    try:
        # permutação exata quando não há empates entre grupos; senão assintótico
        ties = len(set(a).intersection(set(b))) > 0 or \
            len(set(np.concatenate([a, b]))) < len(a) + len(b)
        method = 'asymptotic' if (ties or len(a) + len(b) > 20) else 'exact'
        _, p = stats.mannwhitneyu(a, b, alternative='two-sided', method=method)
        return p
    except Exception:
        return float('nan')


def holm(ps):
    order = np.argsort(ps); m = len(ps); out = [None] * m; run = 0.0
    for rank, idx in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[idx])); out[idx] = run
    return out


def wilson_ci(k, n, z=1.96):
    """§12.3: IC de Wilson (95%) para proporção binária (sucesso por missão)."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((center - half) / denom, (center + half) / denom)


def tost(a, b, margin):
    """§12.2: dois testes unilaterais (Welch) para EQUIVALÊNCIA dentro de
    +/-margin. Retorna (p_tost, diff): equivalência declarada se p_tost < 0.05.
    O TOST exige VARIÂNCIA POSITIVA: para braços constantes (variância zero,
    ex.: contagens todas iguais no teto da escala) NÃO há evidência inferencial
    de equivalência --- a ausência de dispersão em duas amostras pequenas não
    demonstra ausência de variabilidade populacional. Nesse caso retorna None
    (reportar como 'desempenho observado idêntico', não como equivalência)."""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return None
    ma, mb = a.mean(), b.mean()
    va, vb = a.var(ddof=1), b.var(ddof=1)
    se = math.sqrt(va / na + vb / nb)
    diff = mb - ma
    if se == 0.0:                      # braço(s) constante(s): TOST não se aplica
        return None
    df = (va / na + vb / nb) ** 2 / (
        (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    t_low = (diff + margin) / se
    t_up = (diff - margin) / se
    p_tost = max(stats.t.sf(t_low, df), stats.t.cdf(t_up, df))
    return (p_tost, diff)


def stat_row(runs, a, b, metric):
    A, B = vals(runs, a, metric), vals(runs, b, metric)
    if len(A) < 1 or len(B) < 1:
        return None
    lo, hi = boot_ci(A, B)
    return dict(delta=B.mean() - A.mean(), cliff=cliffs_delta(A, B),
                ci=(lo, hi), p=mwu(A, B), nA=len(A), nB=len(B))


def fmt_p(p):
    # §12.1: valor NUMÉRICO (notação científica p/ pequenos), nunca só "<0.001"
    if p != p:            # nan
        return 'nan'
    return f'{p:.2e}' if p < 1e-3 else f'{p:.3f}'


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
    print('\n=== FAMÍLIA CONFIRMATÓRIA (Mann-Whitney; Holm dentro da família) ===')
    print(f'{"pair":<12}{"metric":<26}{"n":>7}{"Δ":>9}{"δ":>7}{"95% CI":>20}{"p":>11}{"p_H":>11}')
    for (lab, pr, r), h in zip(rows, hp):
        ci = f'[{r["ci"][0]:+.2f},{r["ci"][1]:+.2f}]'
        n = f'{r["nA"]}/{r["nB"]}'
        print(f'{lab:<12}{pr:<26}{n:>7}{r["delta"]:>+9.2f}{r["cliff"]:>+7.2f}'
              f'{ci:>20}{fmt_p(r["p"]):>11}{fmt_p(h):>11}')

    # 2) família secundária (equivalência / robustez / custo) — efeito + IC (+TOST)
    print('\n=== FAMÍLIA SECUNDÁRIA (equivalência/robustez/custo — efeito+IC) ===')
    print(f'{"pair":<12}{"metric":<26}{"n":>7}{"Δ":>9}{"δ":>7}{"95% CI":>20}{"p":>11}')
    for lab, a, b, mk, pretty in SECONDARY:
        r = stat_row(runs, a, b, mk)
        if not r:
            continue
        ci = f'[{r["ci"][0]:+.2f},{r["ci"][1]:+.2f}]'
        n = f'{r["nA"]}/{r["nB"]}'
        print(f'{lab:<12}{pretty:<26}{n:>7}{r["delta"]:>+9.2f}{r["cliff"]:>+7.2f}'
              f'{ci:>20}{fmt_p(r["p"]):>11}')

    # 3) EQUIVALÊNCIA por TOST (§12.2): ausência de diferença != equivalência.
    # Margens declaradas A PRIORI: tempo de missão +/-5 s; anomalias +/-0.5.
    print('\n=== EQUIVALÊNCIA (TOST; margem declarada a priori) ===')
    print(f'{"pair":<12}{"metric":<26}{"margem":>8}{"Δ":>9}{"p_TOST":>10}{"equiv?":>8}')
    TOST_PAIRS = [
        ('E0 vs E3', 'E0', 'E3', 'mission_duration_s', 'Mission time [s]', 5.0),
        ('E0 vs E2', 'E0', 'E2', 'mission_duration_s', 'Mission time [s]', 5.0),
        ('E0 vs E4', 'E0', 'E4', 'mission_duration_s', 'Mission time [s]', 5.0),
        ('E3 vs N1', 'E3', 'N1', 'anomalies_unique', 'Anomalies inspected', 0.5),
        ('E3 vs N2', 'E3', 'N2', 'anomalies_unique', 'Anomalies inspected', 0.5),
    ]
    for lab, a, b, mk, pretty, margin in TOST_PAIRS:
        A, B = vals(runs, a, mk), vals(runs, b, mk)
        res = tost(A, B, margin)
        if res is None:   # braço(s) constante(s): TOST não se aplica
            diff = (B.mean() - A.mean()) if len(A) and len(B) else float('nan')
            note = 'idênticos' if abs(diff) < 1e-9 else 'obs. difere'
            print(f'{lab:<12}{pretty:<26}{("+-"+str(margin)):>8}{diff:>+9.2f}'
                  f'{"n/a":>10}{note:>12}')
            continue
        p_tost, diff = res
        eq = 'sim' if p_tost < 0.05 else 'não'
        print(f'{lab:<12}{pretty:<26}{("+-"+str(margin)):>8}{diff:>+9.2f}'
              f'{fmt_p(p_tost):>10}{eq:>8}')

    # 4) SUCESSO POR MISSÃO (§12.3): binário por run + IC de Wilson (NÃO tratar as
    # 3 anomalias de uma missão como 3 repetições independentes).
    print('\n=== SUCESSO POR MISSÃO (IC de Wilson 95%) ===')
    print(f'{"config":<7}{"métrica":<26}{"k/n":>8}{"taxa":>7}{"IC 95% Wilson":>20}')
    for c in CONFIGS:
        v = valid(runs, c)
        if not v:
            continue
        insp = [r.get('anomalies_unique', 0.0) for r in v]
        target = TARGET_ANOM.get(c, 0)   # §8.3: alvo do CENÁRIO, não o máx. observado
        if target > 0 and c != 'E1' and c != 'RHB':   # configs que inspecionam
            k = sum(1 for x in insp if x >= target)
            lo, hi = wilson_ci(k, len(v))
            print(f'{c:<7}{f"inspeção completa (/{target})":<26}{f"{k}/{len(v)}":>8}'
                  f'{k/len(v):>7.2f}{f"[{lo:.2f},{hi:.2f}]":>20}')
        coll = [r.get('collisions', 0.0) for r in v]
        kc = sum(1 for x in coll if x == 0)
        lo, hi = wilson_ci(kc, len(v))
        print(f'{c:<7}{"sem colisão":<26}{f"{kc}/{len(v)}":>8}'
              f'{kc/len(v):>7.2f}{f"[{lo:.2f},{hi:.2f}]":>20}')


if __name__ == '__main__':
    main()
