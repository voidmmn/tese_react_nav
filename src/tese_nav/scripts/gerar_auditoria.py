#!/usr/bin/env python3
"""
Gerador da TRILHA DE AUDITORIA por episódio (parecer, P1-logs).
==============================================================

Consolida, a partir do stdout capturado de cada execução
(`results/launch_<CFG>_r<N>.log`), os eventos que decidem o crédito de inspeção
e a resposta ao perigo, numa tabela auditável (`results/audit_trail.csv`, uma
linha por evento). Combina duas fontes no mesmo log:

  anomaly_simulator (avaliador independente):
    investigate_start (id + POSIÇÃO VERDADEIRA do alvo), inspected (distância
    robô->alvo verdadeiro), rejected (distância > limiar de confirmação),
    failed (timeout/navegação), deferred (perigo); e, no ensaio dinâmico,
    hazard_activated / keepout_first / reactive_first (com tempo ROS `t=` e a
    pose do robô no instante).

  stay_alert_node (supervisor reativo):
    avoid_start; avoid_end com o motivo (safe / retreated / timeout);
    nav_result com o desfecho da meta reativa (aborted / canceled / rejected).
    O modo corrente (INVESTIGATE/AVOID) é rastreado para atribuir cada saída
    `<< PATROL` ao estado que terminou; as saídas de INVESTIGATE já vêm do
    avaliador (inspected/failed/deferred), então aqui só emitimos avoid_end.

ESQUEMA (colunas com significado ÚNICO, ao contrário da versão anterior):
  config, rep, episode, event,
  time_ros_s  (tempo de simulação, das mensagens que o trazem; vazio se ausente),
  time_log_s  (timestamp do cabeçalho do log, escala de época — só ordem),
  target_id,
  target_true_x, target_true_y  (posição VERDADEIRA do alvo; só em start),
  robot_x, robot_y              (pose do robô; em ativação/keepout/reactive),
  robot_dist_m, threshold_m, detail

`rep` é o run_seed (registrado em cada CSV de métricas) -> chave para casar a
trilha com `metrics_<CFG>_*.csv`. Não cria métricas novas: só expõe, de forma
estruturada e com esquema consistente, o que os logs já contêm.

Uso:
    python3 gerar_auditoria.py [~/tese_ws/results]
"""
import csv
import glob
import os
import re
import sys
from collections import Counter

HDR = r'\[(\d+\.\d+)\]'          # timestamp de época no cabeçalho da linha de log
LOG_RE = re.compile(r'launch_([A-Za-z0-9]+)_r(\d+)\.log$')

# --- padrões do anomaly_simulator ---
RE_START = re.compile(HDR + r'.*investigate_start alvo=(-?\d+) '
                            r'\(pos_verdadeira=\(([-\d.]+), ([-\d.]+)\)\)')
RE_INSP  = re.compile(HDR + r'.*anomalia (\d+) INSPECIONADA '
                            r'\(robô a ([\d.]+) m; (\d+)/(\d+)\)')
RE_REJ   = re.compile(HDR + r'.*inspeção de (\d+) NÃO confirmada '
                            r'\(robô a ([\d.]+) m > ([\d.]+) m\)')
RE_FAIL  = re.compile(HDR + r'.*investigação de (\d+) FALHOU \((\w+)\)')
RE_DEFER = re.compile(HDR + r'.*investigação de (\d+) ADIADA')
RE_ACT   = re.compile(HDR + r'.*HAZARD_ACTIVATED id=(\d+) t=([\d.]+) '
                            r'robot=\(([-\d.]+),([-\d.]+)\)')
RE_KEEP  = re.compile(HDR + r'.*KEEPOUT_FIRST id=(\d+) t=([\d.]+) '
                            r'robot=\(([-\d.]+),([-\d.]+)\)')
RE_REAC  = re.compile(HDR + r'.*REACTIVE_FIRST id=(\d+) t=([\d.]+) '
                            r'robot=\(([-\d.]+),([-\d.]+)\)')
# --- padrões do stay_alert_node ---
RE_ENTER = re.compile(HDR + r'.*(>>|!!) (INVESTIGATE|AVOID) \(Phi=([-\d.]+)\)')
RE_EXIT  = re.compile(HDR + r'.*<< PATROL \(motivo=(\w+), ([\d.]+)s\)')
RE_NAVKO = re.compile(HDR + r'.*navegação reativa não concluída: (\w+)')
RE_REJGL = re.compile(HDR + r'.*Nav2 REJEITOU')

COLS = ['config', 'rep', 'episode', 'event', 'time_ros_s', 'time_log_s',
        'target_id', 'target_true_x', 'target_true_y', 'robot_x', 'robot_y',
        'robot_dist_m', 'threshold_m', 'detail']


def _row(**kw):
    r = {c: '' for c in COLS}
    r.update(kw)
    return r


def parse_log(path, cfg, rep):
    rows = []
    mode = 'PATROL'      # modo corrente do supervisor (rastreia entradas/saídas)
    episode = 0          # id do episódio reativo dentro da execução
    with open(path, errors='replace') as fh:
        for line in fh:
            m = RE_START.search(line)
            if m:
                episode += 1
                rows.append(_row(event='investigate_start', episode=episode,
                                 time_log_s=m.group(1), target_id=m.group(2),
                                 target_true_x=m.group(3), target_true_y=m.group(4)))
                continue
            m = RE_INSP.search(line)
            if m:
                rows.append(_row(event='inspected', episode=episode,
                                 time_log_s=m.group(1), target_id=m.group(2),
                                 robot_dist_m=m.group(3),
                                 detail=f'credited {m.group(4)}/{m.group(5)}'))
                continue
            m = RE_REJ.search(line)
            if m:
                rows.append(_row(event='rejected', episode=episode,
                                 time_log_s=m.group(1), target_id=m.group(2),
                                 robot_dist_m=m.group(3), threshold_m=m.group(4)))
                continue
            m = RE_FAIL.search(line)
            if m:
                rows.append(_row(event='inspection_failed', episode=episode,
                                 time_log_s=m.group(1), target_id=m.group(2),
                                 detail=m.group(3)))   # timeout | navegação
                continue
            m = RE_DEFER.search(line)
            if m:
                rows.append(_row(event='deferred', episode=episode,
                                 time_log_s=m.group(1), target_id=m.group(2)))
                continue
            for ev, rx in (('hazard_activated', RE_ACT),
                           ('keepout_first', RE_KEEP),
                           ('reactive_first', RE_REAC)):
                m = rx.search(line)
                if m:
                    rows.append(_row(event=ev, episode=episode,
                                     time_log_s=m.group(1), time_ros_s=m.group(3),
                                     target_id=m.group(2),
                                     robot_x=m.group(4), robot_y=m.group(5)))
                    break
            else:
                m = RE_ENTER.search(line)
                if m:
                    mode = m.group(3)
                    if mode == 'AVOID':
                        episode += 1
                        rows.append(_row(event='avoid_start', episode=episode,
                                         time_log_s=m.group(1),
                                         detail=f'phi={m.group(4)}'))
                    continue
                m = RE_EXIT.search(line)
                if m:
                    reason, dur = m.group(2), m.group(3)
                    if mode == 'AVOID':   # saídas de INVESTIGATE já vêm do avaliador
                        rows.append(_row(event='avoid_end', episode=episode,
                                         time_log_s=m.group(1),
                                         detail=f'reason={reason} dur={dur}s'))
                    mode = 'PATROL'
                    continue
                m = RE_NAVKO.search(line)
                if m:
                    rows.append(_row(event='nav_result', episode=episode,
                                     time_log_s=m.group(1),
                                     detail=f'outcome={m.group(2)}'))
                    continue
                m = RE_REJGL.search(line)
                if m:
                    rows.append(_row(event='nav_result', episode=episode,
                                     time_log_s=m.group(1), detail='outcome=rejected'))
                    continue
    for r in rows:
        r['config'], r['rep'] = cfg, rep
    return rows


def main(results_dir):
    logs = sorted(glob.glob(os.path.join(results_dir, 'launch_*_r*.log')))
    rows, per_cfg = [], {}
    for lg in logs:
        m = LOG_RE.search(os.path.basename(lg))
        if not m:
            continue
        cfg, rep = m.group(1), int(m.group(2))
        rs = parse_log(lg, cfg, rep)
        rows.extend(rs)
        for r in rs:
            per_cfg.setdefault(cfg, Counter())[r['event']] += 1

    out = os.path.join(results_dir, 'audit_trail.csv')
    with open(out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    print(f'trilha de auditoria: {len(rows)} eventos de {len(logs)} logs -> {out}\n')
    hdr = ('cfg', 'start', 'inspec', 'reject', 'insp_fail',
           'deferr', 'avoid', 'nav_res', 'activ')
    print(''.join(f'{h:>10}' for h in hdr))
    for cfg in sorted(per_cfg):
        c = per_cfg[cfg]
        vals = (cfg, c['investigate_start'], c['inspected'], c['rejected'],
                c['inspection_failed'], c['deferred'], c['avoid_start'],
                c['nav_result'], c['hazard_activated'])
        print(''.join(f'{v:>10}' for v in vals))


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/tese_ws/results')
    main(os.path.expanduser(d))
