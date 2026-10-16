#!/usr/bin/env python3
"""Gera o corpo LaTeX da Tabela 4 a partir de results/familia_confirmatoria.csv.

Existe para que a tabela do artigo tenha UMA fonte: o CSV que
analise_estatistica.py escreve. Antes do parecer de 2026-10-16 os p-valores
eram digitados a mao no .tex e dois deles estavam errados (P1).

Uso:  python3 tabela_confirmatoria_tex.py [results_dir] > corpo.tex
"""
import csv
import os
import sys


def fmt_p(x):
    # 4 casas: com 3 o Holm exato 0.005173 virava "0.005" e 0.002679 virava
    # "0.003", divergindo do texto corrido. Tabela e texto citam o MESMO numero.
    v = float(x)
    if v >= 0.001:
        return f'${v:.4f}$'
    e = f'{v:.1e}'.split('e')
    return f'${e[0]}{{\\times}}10^{{{int(e[1])}}}$'


def fmt_num(x, nd=2):
    return f'${float(x):+.{nd}f}$'


def legacy(rd):
    """Corpo LaTeX dos 7 testes da submissao ANTERIOR, sem correcao de Holm.

    Eles sairam da Tabela 4 porque nao pertencem a familia confirmatoria desta
    submissao; ficam no apendice, rotulados como historicos (parecer P1, item 4).
    """
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'ae', os.path.join(here, 'analise_estatistica.py'))
    ae = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ae)
    runs = ae.load(rd)
    print('%% GERADO por tabela_confirmatoria_tex.py --legacy. Nao editar a mao.')
    last = None
    for lab, a, b, mk, pretty in ae.LEGACY_CONFIRMATORY:
        r = ae.stat_row(runs, a, b, mk)
        if not r:
            continue
        pair = lab if lab != last else ''
        last = lab
        nd = 1 if mk == 'mission_duration_s' else 2
        print(f"{pair:<12}& {pretty:<28}& {r['nA']}/{r['nB']} & "
              f"${r['delta']:+.{nd}f}$ & ${r['cliff']:+.2f}$ & "
              f"$[{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]$ & {fmt_p(r['p'])}\\\\")


def main():
    rd = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/tese_ws/results')
    if '--legacy' in sys.argv:
        legacy(rd)
        return
    src = os.path.join(rd, 'familia_confirmatoria.csv')
    rows = list(csv.DictReader(open(src)))
    print(f'%% GERADO por tabela_confirmatoria_tex.py a partir de {os.path.basename(src)}.')
    print('%% NAO editar a mao: reexecutar analise_estatistica.py e regerar.')
    last = None
    for r in rows:
        pair = r['contrast'] if r['contrast'] != last else ''
        last = r['contrast']
        nd = 2 if r['metric'] != 'mission_duration_s' else 1
        print(f"{pair:<14}& {r['label']:<26}& {r['n_A']}/{r['n_B']} & "
              f"{fmt_num(r['delta'], nd)} & {fmt_num(r['cliff'])} & "
              f"$[{float(r['ci_lo']):+.2f},{float(r['ci_hi']):+.2f}]$ & "
              f"{fmt_p(r['p_raw'])} & {fmt_p(r['p_holm'])}\\\\")


if __name__ == '__main__':
    main()
