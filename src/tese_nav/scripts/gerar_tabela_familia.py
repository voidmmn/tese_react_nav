#!/usr/bin/env python3
"""
Gera a TABELA COMPLETA da familia de comparacao primaria (15 testes) em LaTeX.

Motivacao (13/11/2026): o texto declarava tres contrastes x cinco desfechos = quinze
testes e afirmava que o conjunto completo era tabulado, mas o PDF trazia apenas um
recorte. Esta tabela e o conjunto completo, sem omissao de teste, de modo que o
denominador da correcao de Holm possa ser conferido em vez de aceito por confianca.

Entrada : results/familia_confirmatoria.csv  (produzido por analise_estatistica.py)
Saida   : docs/tese/tabelas/familia_primaria.tex  (um tabular, para \\input)

Convencao de sinal: Delta e delta sao do BRACO COMPARADO MENOS O METODO, isto e,
positivos quando o braco comparado apresenta o valor maior. A mesma convencao vale
para as demais tabelas de contraste da tese.

Uso: python3 src/tese_nav/scripts/gerar_tabela_familia.py [raiz_do_repo]
"""
import csv
import os
import sys

DESFECHO = {
    'anomalies_unique': 'Anomalias inspecionadas',
    'min_hazard_distance_m': 'Dist.\\ mín.\\ ao risco [m]',
    'mission_duration_s': 'Duração da missão [s]',
    'hazard_avoidances': 'Recuos',
    'investigation_time_s': 'Tempo de investigação [s]',
}
TESTE = {
    'identical': 'idênt.',
    'exact U': '$U$ exato',
    'exact permutation': 'permut.',
    'asymptotic (tie-corrected)': 'normal',
}
CONTRASTE = {
    'E3 vs HEU': 'Prop.\\,/\\,HEU',
    'E3 vs HEU-sel': 'Prop.\\,/\\,HEU-sel',
    'KOa vs KOF': 'KOa\\,/\\,KOF',
}


def fmt_p(p):
    p = float(p)
    if p >= 0.001:
        return f'{p:.4f}'.replace('.', '{,}')
    expo = f'{p:.1e}'.split('e')
    return f'${float(expo[0]):.1f}'.replace('.', '{,}') + \
        f'\\times10^{{{int(expo[1])}}}$'


def num(x, dec=2):
    return f'{float(x):+.{dec}f}'.replace('.', '{,}') if float(x) or True else x


def main(raiz):
    src = os.path.join(raiz, 'results', 'familia_confirmatoria.csv')
    dst = os.path.join(raiz, 'docs', 'tese', 'tabelas', 'familia_primaria.tex')
    rows = list(csv.DictReader(open(src, encoding='utf-8')))
    assert len(rows) == 15, f'esperados 15 testes, lidos {len(rows)}'
    out = []
    out.append('%% GERADO por src/tese_nav/scripts/gerar_tabela_familia.py -- nao editar a mao.')
    out.append('%% Fonte: results/familia_confirmatoria.csv')
    out.append('\\begin{tabular}{llcccrll}')
    out.append('\\hline')
    out.append('\\textbf{Contraste} & \\textbf{Desfecho} & $\\bm{n}$ & '
               '$\\bm{\\Delta}$ & $\\bm{\\delta}$ & \\textbf{IC\\,95\\%} & '
               '\\textbf{Teste} & $\\bm{p}$ \\textbf{bruto / Holm}\\\\')
    out.append('\\hline')
    atual = None
    for r in rows:
        if r['contrast'] != atual:
            if atual is not None:
                out.append('\\hline')
            atual = r['contrast']
            nome = CONTRASTE[atual]
        else:
            nome = ''
        ic = f"[{num(r['ci_lo'])};\\,{num(r['ci_hi'])}]"
        out.append(
            f"{nome} & {DESFECHO[r['metric']]} & ${r['n_A']}/{r['n_B']}$ & "
            f"${num(r['delta'])}$ & ${num(r['cliff'])}$ & ${ic}$ & "
            f"{TESTE[r['procedure']]} & {fmt_p(r['p_raw'])} / {fmt_p(r['p_holm'])}\\\\")
    out.append('\\hline')
    out.append('\\end{tabular}')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(f'{dst}: {len(rows)} testes')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else
         os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
