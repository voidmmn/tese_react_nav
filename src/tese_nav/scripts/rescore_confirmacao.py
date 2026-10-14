#!/usr/bin/env python3
"""
F6.1 — RE-SCORING da distância de confirmação (R2#5). ANÁLISE RETROSPECTIVA.
=============================================================================

O R2#5 pergunta: com confirmação em 3.3 m, a degradação sob ruído é propriedade
DO MÉTODO ou DO CRITÉRIO DE CONFIRMAÇÃO?

Auditoria (plano §5-4a) mostrou que `inspect_confirm_dist` é uma FUNÇÃO DE
PONTUAÇÃO PURA: não realimenta o comportamento. Rastreio em `anomaly_simulator`:
  - a supressão de re-atração depende só de `committed`, marcado em
    `investigate_start`;
  - a confirmação ocorre em `investigate_end` e escreve apenas em
    `completed`/`failed`;
  - `failed` NÃO remove de `committed` (só `deferred_hazard` remove).
Logo mudar o critério não muda trajetória nenhuma => **0 runs novos**: basta
re-pontuar a trilha de auditoria existente.

CADA tentativa que chegou ao estágio `reason=inspected` aparece na trilha como
`inspected` (creditada) ou `rejected` (distância > limiar). A união é o conjunto
de tentativas re-pontuáveis; o novo escore é `robot_dist_m <= T`.

LIMITE A DECLARAR (crítica v2, cuidado 3 / v3 §3): `robot_dist_m` é a distância
ao alvo verdadeiro NO ENCERRAMENTO da investigação, não o mínimo da aproximação
(que não está instrumentado por run). É medida física do PONTO DE ENCERRAMENTO
— e, para qualidade de inspeção, mais pertinente que um mínimo atingido de
passagem, já que a inspeção é o dwell no ponto de parada.

Esta é uma análise RETROSPECTIVA sobre dados existentes, e deve ser rotulada
como tal (não é parte do plano de análise prévio).

Uso:
    python3 rescore_confirmacao.py [results] [--T 2.8,3.3,4.0] [--configs E3,N1,N2]
"""
import argparse
import csv
import os
import statistics as st
import sys


def carregar(results):
    p = os.path.join(results, 'audit_trail.csv')
    if not os.path.exists(p):
        sys.exit(f'audit_trail.csv ausente em {results}')
    return list(csv.DictReader(open(p)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('results', nargs='?',
                    default=os.path.expanduser('~/tese_ws/results'))
    ap.add_argument('--T', default='2.8,3.3,4.0',
                    help='limiares de confirmação a testar (m)')
    ap.add_argument('--configs', default='E3,N1,N2')
    a = ap.parse_args()

    rows = carregar(a.results)
    thresholds = [float(x) for x in a.T.split(',')]
    configs = [c for c in a.configs.split(',') if c]

    print('# Re-scoring da confirmação — ANÁLISE RETROSPECTIVA (0 runs novos)')
    print('# robot_dist_m = distância ao alvo verdadeiro NO ENCERRAMENTO da '
          'investigação\n')

    for cfg in configs:
        # tentativas re-pontuáveis = inspected (creditada) + rejected (recusada)
        tent = {}
        for r in rows:
            if r['config'] != cfg or r['event'] not in ('inspected', 'rejected'):
                continue
            try:
                rep, tid = int(r['rep']), int(r['target_id'])
                d = float(r['robot_dist_m'])
            except (ValueError, TypeError):
                continue
            tent.setdefault(rep, {})[tid] = d
        if not tent:
            print(f'{cfg}: sem tentativas na trilha\n')
            continue

        dists = [d for m in tent.values() for d in m.values()]
        n_rep = len(tent)
        print(f'## {cfg} — {n_rep} runs, {len(dists)} tentativas de confirmação')
        print(f'   distância de encerramento: mediana {st.median(dists):.2f} m, '
              f'min {min(dists):.2f}, max {max(dists):.2f}')
        print(f'   {"T (m)":>7s} {"creditadas":>11s} {"por run":>9s} '
              f'{"runs completos":>15s}')
        # nº de anomalias do cenário p/ definir "run completo"
        for T in thresholds:
            por_run = [sum(1 for d in m.values() if d <= T)
                       for m in tent.values()]
            total_alvos = max(len(m) for m in tent.values())
            completos = sum(1 for c in por_run if c >= total_alvos)
            print(f'   {T:7.2f} {sum(por_run):11d} '
                  f'{st.mean(por_run):9.2f} {f"{completos}/{n_rep}":>15s}')
        print()


if __name__ == '__main__':
    main()
