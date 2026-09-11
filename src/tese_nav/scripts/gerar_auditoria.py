#!/usr/bin/env python3
"""
Gerador da TRILHA DE AUDITORIA por episódio (parecer 3ª rodada, P1-logs).
========================================================================

O avaliador independente (`anomaly_simulator`) registra, em cada episódio, os
eventos que decidem o crédito de inspeção: início (com id e POSIÇÃO VERDADEIRA
do alvo), inspeção confirmada (distância robô->alvo verdadeiro), rejeição de
confirmação (distância > limiar), falha (timeout/navegação), adiamento por
perigo e — nas runs do ensaio dirigido — ativação do perigo dinâmico e primeira
projeção/publicação em cada canal. Essas linhas ficam no stdout capturado de
cada run (`results/launch_<CFG>_r<N>.log`).

Este script consolida essas linhas numa tabela auditável
(`results/audit_trail.csv`, uma linha por evento) para que a atribuição das
rejeições de N2, das falhas de E5/DHa e a ordem de ativação do perigo dinâmico
sejam verificáveis SEM reexecutar a bateria. Não cria métricas novas: só expõe,
de forma estruturada, o que os logs já contêm.

Uso:
    python3 gerar_auditoria.py [~/tese_ws/results]
"""
import csv
import glob
import os
import re
import sys
from collections import Counter

# padrões das mensagens do anomaly_simulator (ver anomaly_simulator.py)
TS = r'\[(\d+\.\d+)\]'                       # timestamp ROS na linha de log
PATTERNS = [
    ('start',   re.compile(TS + r'.*investigate_start alvo=(-?\d+) '
                                r'\(pos_verdadeira=\(([-\d.]+), ([-\d.]+)\)\)')),
    ('inspected', re.compile(TS + r'.*anomalia (\d+) INSPECIONADA '
                                  r'\(robô a ([\d.]+) m; (\d+)/(\d+)\)')),
    ('rejected', re.compile(TS + r'.*inspeção de (\d+) NÃO confirmada '
                                 r'\(robô a ([\d.]+) m > ([\d.]+) m\)')),
    ('failed',  re.compile(TS + r'.*investigação de (\d+) FALHOU \((\w+)\)')),
    ('deferred', re.compile(TS + r'.*investigação de (\d+) ADIADA')),
    ('hazard_activated', re.compile(TS + r'.*HAZARD_ACTIVATED id=(\d+) '
                                    r't=([\d.]+) robot=\(([-\d.]+),([-\d.]+)\)')),
    ('keepout_first', re.compile(TS + r'.*KEEPOUT_FIRST id=(\d+) '
                                 r't=([\d.]+) robot=\(([-\d.]+),([-\d.]+)\)')),
    ('reactive_first', re.compile(TS + r'.*REACTIVE_FIRST id=(\d+) '
                                  r't=([\d.]+) robot=\(([-\d.]+),([-\d.]+)\)')),
]
LOG_RE = re.compile(r'launch_([A-Za-z0-9]+)_r(\d+)\.log$')

COLS = ['config', 'rep', 'event', 't', 'target_id',
        'true_x', 'true_y', 'robot_dist_m', 'threshold_m', 'detail']


def parse_line(line):
    for name, rx in PATTERNS:
        m = rx.search(line)
        if not m:
            continue
        g = m.groups()
        rec = {'event': name, 't': g[0], 'target_id': '', 'true_x': '',
               'true_y': '', 'robot_dist_m': '', 'threshold_m': '', 'detail': ''}
        if name == 'start':
            rec.update(target_id=g[1], true_x=g[2], true_y=g[3])
        elif name == 'inspected':
            rec.update(target_id=g[1], robot_dist_m=g[2],
                       detail=f'credited {g[3]}/{g[4]}')
        elif name == 'rejected':
            rec.update(target_id=g[1], robot_dist_m=g[2], threshold_m=g[3])
        elif name == 'failed':
            rec.update(target_id=g[1], detail=g[2])   # timeout | navegação
        elif name == 'deferred':
            rec.update(target_id=g[1])
        else:  # hazard_activated / keepout_first / reactive_first
            rec.update(target_id=g[1], true_x=g[3], true_y=g[4])
        return rec
    return None


def main(results_dir):
    logs = sorted(glob.glob(os.path.join(results_dir, 'launch_*_r*.log')))
    rows, per_cfg = [], {}
    for lg in logs:
        m = LOG_RE.search(os.path.basename(lg))
        if not m:
            continue
        cfg, rep = m.group(1), int(m.group(2))
        with open(lg, errors='replace') as fh:
            for line in fh:
                rec = parse_line(line)
                if rec is None:
                    continue
                rec['config'] = cfg
                rec['rep'] = rep
                rows.append(rec)
                per_cfg.setdefault(cfg, Counter())[rec['event']] += 1

    out = os.path.join(results_dir, 'audit_trail.csv')
    with open(out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in COLS})

    print(f'trilha de auditoria: {len(rows)} eventos de {len(logs)} logs -> {out}\n')
    print(f'{"cfg":<6}{"start":>6}{"inspec":>7}{"reject":>7}'
          f'{"failed":>7}{"deferr":>7}{"activ":>6}')
    for cfg in sorted(per_cfg):
        c = per_cfg[cfg]
        print(f'{cfg:<6}{c["start"]:>6}{c["inspected"]:>7}{c["rejected"]:>7}'
              f'{c["failed"]:>7}{c["deferred"]:>7}{c["hazard_activated"]:>6}')


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/tese_ws/results')
    main(os.path.expanduser(d))
