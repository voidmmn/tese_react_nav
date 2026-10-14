#!/usr/bin/env python3
"""
R2#8 — efeito da DESCONTINUIDADE em d = R nas transições da FSM.
=================================================================

O revisor observa que o perfil da Eq.(3) produz intensidade I_e/2 na fronteira
e zero imediatamente além, e pede "a brief statement of whether this
discontinuity has any measurable effect on the FSM transitions".

A crítica v2 §7 alertou que uma CONTAGEM GLOBAL de transições não identifica o
efeito da fronteira; e a v3 §6 alertou que uma trajetória TANGENTE pode só
tocar a fronteira sem exercitá-la. Este script evita os dois problemas sem
cenário novo: usa os logs EXISTENTES, onde a ronda real cruza d = R nos dois
sentidos várias vezes por run.

COMO: o `bellman_node` loga `Phi=` a 1 Hz **somente quando |Φ| > 1e-3**. Logo
  - lacuna na série  => nenhum evento no alcance (Φ ≈ 0);
  - 1ª amostra após lacuna => CRUZAMENTO DE FORA PARA DENTRO de d = R;
  - última amostra antes de lacuna => cruzamento de DENTRO PARA FORA.
O salto de Φ no cruzamento de entrada é a descontinuidade, e seu valor esperado
é |w·I_e/2| (metade da contribuição de pico da modalidade).

MEDIDAS REPORTADAS, por configuração:
  - nº de cruzamentos em cada sentido (os dois existem, não é tangência);
  - magnitude do salto de Φ na entrada (a descontinuidade, medida);
  - quantos cruzamentos de entrada são seguidos de transição da FSM em <= 2 s;
  - menor intervalo entre transições consecutivas da FSM (detector de chattering).

ANÁLISE RETROSPECTIVA sobre dados existentes — rotular como tal.

Uso: python3 analise_fronteira_dR.py [results] [--configs E3,E5,CONF,N1,N2]
"""
import argparse
import glob
import os
import re
import statistics as st

RE_PHI = re.compile(r'\[(\d+\.\d+)\] \[bellman_node\]: Phi=([-+0-9.]+)')
RE_FSM = re.compile(r'\[(\d+\.\d+)\] \[stay_alert_node\]: (>>|<<) (\w+)')


def analisar_log(path, gap_s=2.0, janela_s=2.0):
    txt = open(path, errors='ignore').read()
    phi = [(float(t), float(v)) for t, v in RE_PHI.findall(txt)]
    fsm = [(float(t), s, m) for t, s, m in RE_FSM.findall(txt)]
    if len(phi) < 5:
        return None
    entradas, saidas = [], []
    for i in range(1, len(phi)):
        dt = phi[i][0] - phi[i - 1][0]
        if dt > gap_s:                      # lacuna => saiu e voltou a entrar
            saidas.append((phi[i - 1][0], phi[i - 1][1]))
            entradas.append((phi[i][0], phi[i][1]))
    # a primeira amostra do log é também uma entrada (vinha de Φ≈0)
    entradas.insert(0, phi[0])
    saidas.append(phi[-1])
    # transição da FSM dentro da janela após cada entrada
    t_fsm = [t for t, _, _ in fsm]
    com_transicao = sum(
        1 for te, _ in entradas
        if any(te <= t <= te + janela_s for t in t_fsm))
    gaps_fsm = [t_fsm[i] - t_fsm[i - 1] for i in range(1, len(t_fsm))]
    return {
        'entradas': entradas, 'saidas': saidas,
        'com_transicao': com_transicao,
        'n_fsm': len(fsm),
        'min_gap_fsm': min(gaps_fsm) if gaps_fsm else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('results', nargs='?',
                    default=os.path.expanduser('~/tese_ws/results'))
    ap.add_argument('--configs', default='E3,E5,CONF,N1,N2')
    ap.add_argument('--janela', type=float, default=2.0)
    a = ap.parse_args()

    print('# Descontinuidade em d = R vs transições da FSM — RETROSPECTIVO')
    print(f'# cruzamento de entrada = 1ª amostra de Phi após lacuna > 2 s '
          f'(Phi só é logado se |Phi| > 1e-3)')
    print(f'# janela para atribuir transição a um cruzamento: {a.janela:.0f} s\n')
    print(f"{'cfg':6s} {'runs':>5s} {'entra':>6s} {'sai':>5s} "
          f"{'|salto| entrada (mediana/max)':>30s} {'c/transicao':>12s} "
          f"{'min gap FSM':>12s}")
    for cfg in [c for c in a.configs.split(',') if c]:
        tot_e = tot_s = tot_ct = 0
        saltos, min_gaps, runs = [], [], 0
        for lg in sorted(glob.glob(os.path.join(a.results,
                                                f'launch_{cfg}_r*.log'))):
            r = analisar_log(lg, janela_s=a.janela)
            if not r:
                continue
            runs += 1
            tot_e += len(r['entradas']); tot_s += len(r['saidas'])
            tot_ct += r['com_transicao']
            saltos += [abs(v) for _, v in r['entradas']]
            if r['min_gap_fsm'] is not None:
                min_gaps.append(r['min_gap_fsm'])
        if not runs:
            print(f'{cfg:6s} (sem logs)')
            continue
        sm = f'{st.median(saltos):.3f} / {max(saltos):.3f}'
        mg = f'{min(min_gaps):.1f} s' if min_gaps else 'n/a'
        print(f'{cfg:6s} {runs:5d} {tot_e:6d} {tot_s:5d} {sm:>30s} '
              f'{f"{tot_ct}/{tot_e}":>12s} {mg:>12s}')


if __name__ == '__main__':
    main()
