#!/usr/bin/env python3
"""
F2.6 — GATE DE REÚSO dos dados do método (Access-2026-46291).
==============================================================

A resubmissão acrescenta parâmetros (`selection_mode`, `trigger_mode`,
limiares de modalidade, par entrada/saída, `inspect_confirm_dist`) cujos
DEFAULTS devem reproduzir exatamente o método publicado. Só assim os blocos
E3 / CONF / E5 podem ser REUSADOS como "o método" nas novas comparações, em
vez de serem refeitos (~225 min).

Este script compara um bloco de regressão (default: E3reg) contra o bloco
publicado (default: E3) e emite APROVADO/REPROVADO.

Critério:
  - métricas de contagem discreta (comportamento): o conjunto de valores do
    bloco novo tem de estar CONTIDO no do bloco publicado;
  - métricas contínuas: cada valor novo dentro do [min, max] publicado.
  Só runs com missão COMPLETA e deslocamento > 1 m entram na comparação.

Uso: python3 gate_reuso.py [results_dir] [--novo E3reg] [--ref E3]
"""
import argparse
import csv
import glob
import os
import re
import sys

DISCRETAS = ('anomalies_unique', 'route_deviations', 'hazard_avoidances',
             'investigation_timeouts', 'collisions', 'safety_zone_violations',
             'investigation_deferred')
CONTINUAS = ('mission_duration_s', 'distance_traveled_m',
             'min_hazard_distance_m', 'investigation_time_s')


def runs_completos(results, cfg):
    """[(rep, {metrica: valor_final})] só de runs com missão completa."""
    out = []
    for lg in sorted(glob.glob(os.path.join(results, f'launch_{cfg}_r*.log'))):
        txt = open(lg, errors='ignore').read()
        if 'COMPLETA' not in txt:
            continue                       # run sem missão completa -> fora
        mc = re.search(r'gravando em (\S+metrics_\S+\.csv)', txt)
        if not mc:
            continue
        p = mc.group(1)
        if not os.path.exists(p):
            p = os.path.join(results, os.path.basename(p))
        if not os.path.exists(p):
            continue
        last = {}
        for r in csv.DictReader(open(p)):
            try:
                last[r['metric']] = float(r['value'])
            except (ValueError, TypeError, KeyError):
                pass
        if last.get('distance_traveled_m', 0.0) <= 1.0:
            continue
        rep = int(re.search(r'_r(\d+)\.log$', lg).group(1))
        out.append((rep, last))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('results', nargs='?',
                    default=os.path.expanduser('~/tese_ws/results'))
    ap.add_argument('--novo', default='E3reg')
    ap.add_argument('--ref', default='E3')
    a = ap.parse_args()

    ref = runs_completos(a.results, a.ref)
    novo = runs_completos(a.results, a.novo)
    if not ref or not novo:
        sys.exit(f'dados insuficientes: {a.ref} n={len(ref)}, '
                 f'{a.novo} n={len(novo)}')

    print(f'# Gate de reúso: {a.novo} (n={len(novo)}) vs '
          f'{a.ref} publicado (n={len(ref)})')
    print(f"{'metrica':26s} {'referencia':>20s} {'novo':>18s} {'':>9s}")
    ok = True
    for k in DISCRETAS + CONTINUAS:
        vr = [d.get(k) for _, d in ref if d.get(k) is not None]
        vn = [d.get(k) for _, d in novo if d.get(k) is not None]
        if not vr or not vn:
            continue
        if k in DISCRETAS:
            passou = set(vn) <= set(vr)
            sref = '{' + ','.join(f'{v:g}' for v in sorted(set(vr))) + '}'
            snov = '{' + ','.join(f'{v:g}' for v in sorted(set(vn))) + '}'
        else:
            lo, hi = min(vr), max(vr)
            passou = all(lo - 1e-9 <= x <= hi + 1e-9 for x in vn)
            sref = f'{lo:.2f}-{hi:.2f}'
            snov = f'{min(vn):.2f}-{max(vn):.2f}'
        ok &= passou
        print(f'{k:26s} {sref:>20s} {snov:>18s} {"OK" if passou else "FORA":>9s}')

    print()
    if ok:
        print('GATE APROVADO — os parâmetros novos são no-op no caminho default.')
        print('=> E3 / CONF / E5 podem ser REUSADOS como "o método" (poupa ~225 min).')
    else:
        print('GATE REPROVADO — há divergência de comportamento no caminho default.')
        print('=> NÃO reusar; a bateria do método precisa ser refeita (+225 min).')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
