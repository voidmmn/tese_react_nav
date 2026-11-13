#!/usr/bin/env python3
"""
Comparacao EXPLORATORIA: metodo proposto x baseline Q-DRIVEN (RL comportamental).
=================================================================================

O qdriven_node usa uma Q-table pre-treinada com recompensa aumentada por Phi
(train_qdriven.py) que SELECIONA a acao executada em modo greedy, comandando
/cmd_vel durante o episodio reativo. O metodo proposto mantem a tabela de valor
passiva e dispara por limiar, emitindo METAS a pilha Nav2/MPPI. Mesma patrulha
por baixo, mesmo protocolo de eventos, mesmos parametros de inspecao
(standoff 2,0 m; recuo em R+Delta = 6,5 m), mesmos cenarios.

ESCOPO ESTATISTICO -- IMPORTANTE: a familia confirmatoria do estudo esta
fechada e corrigida por Holm desde a bateria de outubro. Estes contrastes sao
EXPLORATORIOS e devem ser rotulados como tais onde forem reportados. Para
transparencia a saida traz o p bruto e, em coluna separada, o p corrigido por
Holm DENTRO desta familia exploratoria.

Reusa os instrumentos de analise_estatistica.py (validade por deslocamento,
Mann-Whitney com permutacao exata para bracos degenerados, Cliff's delta, IC 95%
bootstrap da diferenca de medias) para que a comparacao seja feita com a mesma
regua dos demais blocos.

NAO compara route_deviations: a metrica conta metas enviadas ao Nav2 e o
qdriven nao envia metas, de modo que o zero dele e artefato de definicao, nao
desempenho.

Uso: python3 analise_qdriven.py [~/tese_ws/results]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analise_estatistica import (load, valid, vals, cliffs_delta, boot_ci,
                                 mwu, procedure, holm, fmt_p)

PARES = [
    ('default',  'E3',   'QDRVd'),
    ('conflict', 'CONF', 'QDRVc'),
    ('adverse',  'E5',   'QDRVa'),
]

METRICAS = [
    ('anomalies_unique',       'anomalias inspecionadas'),
    ('mission_duration_s',     'duracao da missao (s)'),
    ('investigation_time_s',   'tempo em investigacao (s)'),
    ('min_hazard_distance_m',  'afastamento minimo do perigo (m)'),
    ('time_below_clearance_s', 'tempo sob a faixa de 2 m (s)'),
    ('collisions',             'entradas em regiao de contato'),
    ('safety_zone_violations', 'violacoes de zona de seguranca'),
    ('distance_traveled_m',    'distancia percorrida (m)'),
]


def med(x):
    return float(np.median(x)) if len(x) else float('nan')


def main():
    res = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/tese_ws/results')
    runs = load(res)

    linhas, ps = [], []
    for cenario, cfg_met, cfg_qdr in PARES:
        a, b = valid(runs, cfg_met), valid(runs, cfg_qdr)
        print(f'\n=== {cenario}: {cfg_met} (metodo, n={len(a)}) x '
              f'{cfg_qdr} (qdriven, n={len(b)}) ===')
        for metric, rotulo in METRICAS:
            x, y = vals(runs, cfg_met, metric), vals(runs, cfg_qdr, metric)
            if len(x) == 0 or len(y) == 0:
                print(f'  {rotulo:38s} SEM DADOS')
                continue
            d = cliffs_delta(x, y)
            lo, hi = boot_ci(x, y)
            p = mwu(x, y)
            ps.append(p)
            linhas.append((cenario, rotulo, med(x), med(y), d, lo, hi, p,
                           procedure(x, y)))
            print(f'  {rotulo:38s} metodo={med(x):8.2f}  qdriven={med(y):8.2f}  '
                  f'delta={d:+.2f}  IC95%=[{lo:+.2f},{hi:+.2f}]  p={fmt_p(p)}')

    adj = holm(ps)
    print('\n\n=== TABELA EXPLORATORIA (p corrigido por Holm DENTRO desta familia) ===')
    print(f'{"cenario":9s} {"metrica":38s} {"metodo":>9s} {"qdriven":>9s} '
          f'{"delta":>7s} {"IC95%":>20s} {"p":>10s} {"p_Holm":>10s}  procedimento')
    for (cen, rot, mx, my, d, lo, hi, p, proc), pa in zip(linhas, adj):
        ic = f'[{lo:+.2f},{hi:+.2f}]'
        print(f'{cen:9s} {rot:38s} {mx:9.2f} {my:9.2f} {d:+7.2f} {ic:>20s} '
              f'{fmt_p(p):>10s} {fmt_p(pa):>10s}  {proc}')

    out = os.path.join(res, 'qdriven_exploratorio.csv')
    with open(out, 'w') as f:
        f.write('cenario,metrica,mediana_metodo,mediana_qdriven,cliffs_delta,'
                'ic95_lo,ic95_hi,p,p_holm,procedimento\n')
        for (cen, rot, mx, my, d, lo, hi, p, proc), pa in zip(linhas, adj):
            f.write(f'{cen},"{rot}",{mx:.4f},{my:.4f},{d:.4f},{lo:.4f},{hi:.4f},'
                    f'{p:.6g},{pa:.6g},{proc}\n')
    print(f'\nescrito: {out}')


if __name__ == '__main__':
    main()
