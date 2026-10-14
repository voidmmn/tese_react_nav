#!/usr/bin/env python3
"""
Métrica de PRIORIDADE — tempo até inspecionar o evento prioritário (D1).
=========================================================================

Responde R2#3 / crítica v3 §5: para afirmar que a seleção por saliência traz
benefício, é preciso um critério operacional INDEPENDENTE da própria regra de
saliência. "Escolheu o mais saliente" é reproduzir a regra, não evidência.

DEFINIÇÃO OPERACIONAL (fechada antes das execuções — D1 do plano):

  1. evento prioritário = MAIOR INTENSIDADE VERDADEIRA do cenário, comparada
     DENTRO DA MESMA MODALIDADE. Entre modalidades o peso de tipo (thermal 1.0,
     acoustic 1.2) É a regra sob teste e não pode julgá-la.
  2. desempate: MENOR id.
  3. relógio: a partir do INÍCIO DA MISSÃO (não do início do episódio).
  4. horizonte H = 400 s (acima dos ~372 s do método em route_hazard e dos
     ~365 s da missão nominal; abaixo do timeout de 600 s).
  5. não inspecionado até H => recebe H no escore, e esse caso é relatado
     SEPARADAMENTE junto da proporção inspecionada até H. O H imputado NÃO é
     tempo observado de inspeção.

  6. (refinamento sobre D1, ver AVISO) anomalias CO-LOCALIZADAS com um perigo
     são EXCLUÍDAS do conjunto prioritário.

AVISO — por que o item 6 existe:
  No cenário `conflict` a anomalia de maior intensidade acústica (id=5, 0.95)
  está DELIBERADAMENTE co-localizada com o perigo, e o comportamento CORRETO é
  recuar e NÃO inspecioná-la (precedência categórica de segurança). Sem o item
  6, a métrica puniria o comportamento correto. Com ele, a prioridade acústica
  em `conflict` passa a ser id=2 (0.72). A exclusão é por distância
  (`--colocated`, default 1.0 m) e fica registrada na saída.

Uso:
    python3 metrica_prioridade.py [results_dir] [--H 400] [--colocated 1.0]
"""
import argparse
import csv
import glob
import math
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tese_nav', 'utils'))
from scenarios import scenario_events          # noqa: E402  (sem rclpy)

# Mapa config -> cenário. Fonte única; atualizar ao criar bloco novo.
CONFIG_SCENARIO = {
    'E0': 'default', 'E1': 'default', 'E2': 'default', 'E3': 'default',
    'E4': 'default', 'E3reg': 'default', 'APF': 'default',
    'N1': 'default', 'N2': 'default',
    'E5': 'adverse',
    'CONF': 'conflict',
    'RHM': 'route_hazard', 'RHB': 'route_hazard', 'KOa': 'route_hazard',
    'KOb': 'route_hazard', 'KOF': 'route_hazard',
    'DHa': 'dyn_hazard', 'DHb': 'dyn_hazard',
    # resubmissão
    'HEUd': 'default', 'HEUc': 'conflict', 'HEUa': 'adverse',
    'HEUseld': 'default', 'HEUselc': 'conflict', 'HEUsela': 'adverse',
    'HAZ20': 'conflict', 'HAZ30': 'conflict', 'HAZ40': 'conflict',
    'CM': 'conflict_marginal',
    'HYSnar': 'default', 'HYSoff': 'default',
}


def priority_targets(scenario, colocated_m):
    """{modalidade: (id, intensidade)} do evento prioritário, por modalidade."""
    anomalies, hazards = scenario_events(scenario)
    elegiveis, excluidas = [], []
    for a in anomalies:
        perto = any(math.hypot(a['x'] - h['x'], a['y'] - h['y']) <= colocated_m
                    for h in hazards)
        (excluidas if perto else elegiveis).append(a)
    out = {}
    for a in elegiveis:
        m = a['type']
        # maior intensidade; desempate por MENOR id
        if m not in out or (a['intensity'], -a['id']) > (out[m][1], -out[m][0]):
            out[m] = (a['id'], a['intensity'])
    return out, [a['id'] for a in excluidas]


def mission_clock(results, config):
    """
    {rep: (t_wp0_epoch, fator_wall_para_sim)} por run válido.

    PROBLEMA DE RELÓGIO (achado ao validar): o `timestamp` dos CSVs de métricas
    é tempo de SIMULAÇÃO (use_sim_time=true), enquanto o `time_log_s` da trilha
    de auditoria é EPOCH (wall) do cabeçalho do log ROS. Os dois não se somam.

    SOLUÇÃO: mapa linear wall->sim por run, ancorado em dois pontos recuperáveis
    de QUALQUER log (antigo ou novo), o que preserva o reúso de E3/CONF/E5:
      - início da missão  = 1º `-> WP[0]` do mission_node (epoch)
      - fim da missão     = `Missão COMPLETA` do metrics_node (epoch)
        <-> max(mission_duration_s) do CSV (sim)
    O fator corrige a deriva de RTF, que é de 0.967-1.000 e **varia por run** —
    sem a correção, uma config que replaneja mais (mais CPU, RTF menor) teria
    tempos inflados por artefato de host, não por comportamento.
    """
    out = {}
    for lg in glob.glob(os.path.join(results, f'launch_{config}_r*.log')):
        m = re.search(r'launch_' + re.escape(config) + r'_r(\d+)\.log$', lg)
        if not m:
            continue
        rep = int(m.group(1))
        txt = open(lg, errors='ignore').read()
        m0 = re.search(r'\[(\d+\.\d+)\] \[mission_node\]: -> WP\[0\]', txt)
        m1 = re.search(r'\[(\d+\.\d+)\] \[metrics_node\]: Miss.o COMPLETA', txt)
        mc = re.search(r'gravando em (\S+metrics_\S+\.csv)', txt)
        if not (m0 and m1 and mc):
            continue                      # run sem missão completa -> fora
        t_wp0, t_end = float(m0.group(1)), float(m1.group(1))
        sim_total, dist = 0.0, 0.0
        csv_path = mc.group(1)
        if not os.path.exists(csv_path):
            csv_path = os.path.join(results, os.path.basename(csv_path))
        if not os.path.exists(csv_path):
            continue
        for r in csv.DictReader(open(csv_path)):
            try:
                v = float(r['value'])
            except (ValueError, TypeError, KeyError):
                continue
            if r['metric'] == 'mission_duration_s':
                sim_total = max(sim_total, v)
            elif r['metric'] == 'distance_traveled_m':
                dist = max(dist, v)
        wall_total = t_end - t_wp0
        if dist <= 1.0 or wall_total <= 1.0 or sim_total <= 1.0:
            continue                      # spawn-fail / run degenerado
        out[rep] = (t_wp0, sim_total / wall_total)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('results', nargs='?',
                    default=os.path.expanduser('~/tese_ws/results'))
    ap.add_argument('--H', type=float, default=400.0)
    ap.add_argument('--colocated', type=float, default=1.0)
    ap.add_argument('--configs', default='')
    a = ap.parse_args()

    audit = os.path.join(a.results, 'audit_trail.csv')
    if not os.path.exists(audit):
        sys.exit(f'audit_trail.csv ausente em {a.results} '
                 '(rode gerar_auditoria.py primeiro)')
    rows = list(csv.DictReader(open(audit)))

    want = [c for c in a.configs.split(',') if c] or \
        sorted({r['config'] for r in rows})

    print(f'# Métrica de prioridade — H={a.H:.0f}s, '
          f'co-localização={a.colocated:.1f}m')
    print(f"{'cfg':8s} {'cenário':13s} {'modal':9s} {'alvo':>5s} {'int':>5s} "
          f"{'n':>3s} {'insp<=H':>8s} {'mediana_s':>10s} {'media_s':>9s}")
    for cfg in want:
        scen = CONFIG_SCENARIO.get(cfg)
        if scen is None:
            print(f'{cfg:8s} (cenário desconhecido — adicione a CONFIG_SCENARIO)')
            continue
        prio, excl = priority_targets(scen, a.colocated)
        clock = mission_clock(a.results, cfg)
        if not clock:
            print(f'{cfg:8s} {scen:13s} (sem métricas válidas)')
            continue
        ins = {}   # (rep, target_id) -> time_log_s
        for r in rows:
            if r['config'] == cfg and r['event'] == 'inspected':
                try:
                    ins[(int(r['rep']), int(r['target_id']))] = float(r['time_log_s'])
                except (ValueError, TypeError):
                    continue
        for modal, (tid, inten) in sorted(prio.items()):
            escores, n_insp = [], 0
            for rep, (t_wp0, k) in sorted(clock.items()):
                t = ins.get((rep, tid))
                # wall -> sim: corrige a deriva de RTF por run
                t_sim = (t - t_wp0) * k if t is not None else None
                if t_sim is not None and t_sim <= a.H:
                    escores.append(t_sim); n_insp += 1
                else:
                    escores.append(a.H)       # censurado em H
            n = len(escores)
            print(f'{cfg:8s} {scen:13s} {modal:9s} {tid:5d} {inten:5.2f} '
                  f'{n:3d} {n_insp:4d}/{n:<3d} {st.median(escores):10.1f} '
                  f'{st.mean(escores):9.1f}')
        if excl:
            print(f'{"":8s} -> excluidas por co-localizacao com perigo: {excl}')


if __name__ == '__main__':
    main()
